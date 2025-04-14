# ----------------------------------------------
# Title: apiModel.py
# Description: Uses AI API to generate responses
# Author(s): Yui, Feliex
# Date created: Mar 4, 2025
# Date modified: Mar 4, 2025
# ----------------------------------------------
# --------------------------------------------------
# File: apiModel.py
# Description: Combine JobSpy + Groq to provide job suggestions
#              with a matchScore based on user experience.
# --------------------------------------------------

import sys
import json
import pandas as pd
import textwrap
import sqlite3
import pdfkit

from groq import Groq
from jobspy import scrape_jobs

from models.jobModel import JobModel
from models.userModel import UserModel
from models.experienceModel import ExperienceModel
from models.documentModel import DocumentModel

class apiModel:
    # Replace with your actual Groq API key
    api_key = "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"
    
    @staticmethod
    def generateJobSuggestions(userId):
        """
        Combines user experiences and JobSpy data to generate AI job suggestions.
        Steps:
         0. Validate that the API key is set.
         1. Retrieve and truncate the user's experience text.
         2. Fetch the user's saved jobs and location.
         3. Extract unique job titles from the saved jobs.
         4. Ensure a valid location is available; default if necessary.
         5. Use JobSpy to scrape new jobs based on job titles and location.
         6. If no jobs are returned, exit.
         7. Print the raw job DataFrame and its columns for debugging.
         8. Shuffle and limit job results to reduce token usage.
         9. Convert the DataFrame rows to a minimal JSON-like list.
        10. Build a prompt including experience text and job data.
        11. Call the Groq API with the prompt.
        12. Check the API response for choices.
        13. Extract the raw text from the AI response.
        14. Extract the JSON substring (list of suggestions) from the response.
        15. Parse the JSON substring.
        16. Validate that the response is a list.
        17. Save the suggestions to the database and return them.
        """
        # 0) Validate the Groq API key is set
        if not apiModel.api_key:
            print("No Groq API key provided. Exiting.")
            return None

        # 1) Retrieve and truncate the user experience text from ExperienceModel
        user_experience_text = apiModel._getUserExperienceText(userId)
        if not user_experience_text.strip():
            user_experience_text = "(No experiences)"

        # 2) Fetch saved jobs and user location from the database
        jobs = JobModel.getJobs(userId)
        user_location = UserModel.getUserLocation(userId)

        if not jobs:
            print("No jobs found in database.")
            return None

        # 3) Extract unique job titles from the saved jobs
        job_titles = list(set(job[2] for job in jobs if job[2]))
        if not job_titles:
            print("No valid job titles found.")
            return None

        # 4) Ensure a valid location; default to 'Vancouver, BC' if missing
        if not user_location:
            print("No location found for user. Defaulting to 'Vancouver, BC'.")
            user_location = "Vancouver, BC"

        # 5) Use JobSpy to scrape jobs from Indeed using the job titles and location
        try:
            print(f"Searching for jobs with titles: {job_titles} in {user_location}")
            job_df = scrape_jobs(
                site_name="indeed",
                search_term=" OR ".join(job_titles),
                location=user_location,
                results_wanted=5,
                hours_old=336,
                country_indeed='Canada'
            )
        except Exception as e:
            print("Error scraping Indeed via JobSpy:", e)
            return None

        # 6) Check if jobs were returned; exit if not
        if not isinstance(job_df, pd.DataFrame) or job_df.empty:
            print("No jobs found from JobSpy.")
            return None

        # 7) Print raw job results for debugging
        print("\nRaw job results from JobSpy:\n", job_df)
        print("Columns returned by JobSpy:", job_df.columns)

        # 8) Shuffle and limit job results to reduce the size of the prompt
        job_df = job_df.sample(frac=1).head(3).reset_index(drop=True)

        # 9) Convert job DataFrame to a minimal JSON-like list with essential fields only
        job_list_for_ai = []
        for _, row in job_df.iterrows():
            job_list_for_ai.append({
                "title": row.get("title", "Unknown"),
                "company": row.get("company", "Unknown"),
                "link": row.get("job_url", "#"),
                "description": "(omitted to save tokens)"
            })

        # 10) Build the AI prompt with user experience and job data
        job_data_str = json.dumps(job_list_for_ai, indent=2)
        prompt = textwrap.dedent(f"""
        You are an AI job recommendation assistant.

        The user has these experiences:
        {user_experience_text}

        Here are some new job postings from Indeed:
        {job_data_str}

        Please suggest EXACTLY 3 jobs with the keys: 
          "jobTitle", "company", "link", "matchScore" (0-100).

        Even if fewer than 3 are strongly relevant, fill the extra slots with partial matches.
        Respond with ONLY valid JSON, no extra text. Example:

        [
          {{"jobTitle": "Software Engineer", "company": "TechCorp", "link": "https://example.com", "matchScore": 70}},
          ...
        ]
        """)

        # 11) Call Groq API with the prompt
        try:
            client = Groq(api_key=apiModel.api_key)
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-70b-8192",  # Replace with the available model if necessary
            )
        except Exception as e:
            print(f"Error calling Groq: {e}")
            return None

        # 12) Check that the API response contains choices
        if not chat_completion or not chat_completion.choices:
            print("No response from Groq.")
            return None

        # 13) Extract the response text from the first choice
        response_text = chat_completion.choices[0].message.content.strip()
        print("\nAI Response:\n", response_text)

        # 14) Extract the JSON substring from the AI response
        start_idx = response_text.find("[")
        end_idx = response_text.rfind("]")
        if start_idx == -1 or end_idx == -1 or end_idx < start_idx:
            print("Error: Could not find bracketed JSON in AI response.")
            return None

        json_substring = response_text[start_idx:end_idx + 1]
        try:
            job_suggestions = json.loads(json_substring)
        except Exception as e:
            print(f"Error parsing JSON substring: {e}")
            return None

        # 15) Verify the parsed response is a list of suggestions
        if not isinstance(job_suggestions, list):
            print("AI did not return a list of suggestions.")
            return None

        # 16) Save the suggestions to the database
        JobModel.saveJobSuggestions(userId, job_suggestions)

        # 17) Return the saved job suggestions from the database
        return JobModel.getJobSuggestions(userId)
    
    @staticmethod
    def checkApiKey():
        # Check if an API key is set; print a warning if not.
        if not apiModel.api_key:
            print("Warning: API key not found. Some features may not work.")
            return False
        return True
    
    @staticmethod
    def _getUserExperienceText(userId):
        """
        Retrieves the user's experiences from the ExperienceModel and truncates the result.
        Returns a single string with experiences, capped at 800 characters.
        """
        exp_model = ExperienceModel()
        exp_data = exp_model.get_experiences(userId)  # Expects a dict with keys per experience category

        lines = []
        for category, items in exp_data.items():
            if items:
                lines.append(f"{category}: {', '.join(items)}")

        combined = "\n".join(lines)
        return combined[:800]  # Truncate to 800 characters to avoid token-limit issues
    
    def print_divider():
        # Prints a visual divider line to the console.
        print("\n" + "="*50 + "\n")

    @staticmethod
    def generate_documents(user_id, pdfkit_config):
        # Generates resume and cover letter documents for the demo user.
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # Retrieve the first job for the user.
        cursor.execute("SELECT id FROM jobs WHERE userId = ? LIMIT 1", (user_id,))
        job_result = cursor.fetchone()
        # If no job exists, this block could be modified to create a mock job.
        job_id = job_result[0]  # Currently using the first job's ID
        conn.close()
        
        print("\n" + "="*50 + "\n")
        print(f"GENERATING RESUME FOR USER {user_id}, JOB {job_id}")
        print("\n" + "="*50 + "\n")
        
        # Generate the resume via Groq API.
        resume_html = apiModel.generateResume(user_id, job_id)
        
        if not isinstance(resume_html, str) or resume_html.startswith("Error"):
            print(f"Resume generation failed: {resume_html}")
        else:
            print("Resume generated successfully!")
            # Save the resume HTML to a local file.
            with open("generated_resume.html", "w", encoding="utf-8") as f:
                f.write(resume_html)
            print("Resume saved to 'generated_resume.html'")
            
            # Generate a PDF if pdfkit is configured.
            if pdfkit_config:
                try:
                    pdfkit.from_string(resume_html, "generated_resume.pdf", configuration=pdfkit_config)
                    print("Resume PDF saved to 'generated_resume.pdf'")
                except Exception as e:
                    print(f"Error generating PDF: {e}")
        
        print("\n" + "="*50 + "\n")
        print(f"GENERATING COVER LETTER FOR USER {user_id}, JOB {job_id}")
        print("\n" + "="*50 + "\n")
        
        # Generate the cover letter via Groq API.
        cover_letter_html = apiModel.generateCoverLetter(user_id, job_id)
        
        if not isinstance(cover_letter_html, str) or cover_letter_html.startswith("Error"):
            print(f"Cover letter generation failed: {cover_letter_html}")
        else:
            print("Cover letter generated successfully!")
            # Save the cover letter HTML to a local file.
            with open("generated_cover_letter.html", "w", encoding="utf-8") as f:
                f.write(cover_letter_html)
            print("Cover letter saved to 'generated_cover_letter.html'")
            
            # Generate a PDF if pdfkit is configured.
            if pdfkit_config:
                try:
                    pdfkit.from_string(cover_letter_html, "generated_cover_letter.pdf", configuration=pdfkit_config)
                    print("Cover letter PDF saved to 'generated_cover_letter.pdf'")
                except Exception as e:
                    print(f"Error generating PDF: {e}")
    
    @staticmethod
    def getUserProfile(userId):
        # Retrieves complete user profile information including personal details, work experience, education, projects, and certifications.
        user_data = {}
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # Retrieve basic personal information.
        user = UserModel.getUserById(userId)
        if user:
            user_data["personal"] = {
                "fullName": user[3] if user[3] else "",
                "email": user[4] if user[4] else "",
                "phone": user[5] if user[5] else "",
                "linkedin": user[6] if user[6] else "",
                "location": user[7] if user[7] else "",
                "portfolio": user[8] if user[8] else ""
            }
        
        # Retrieve work experience information.
        cursor.execute("SELECT jobTitle, company, location, startDate, endDate, responsibilities FROM workExperience WHERE userId = ?", (userId,))
        work_experience = cursor.fetchall()
        user_data["workExperience"] = []
        for exp in work_experience:
            user_data["workExperience"].append({
                "jobTitle": exp[0] if exp[0] else "",
                "company": exp[1] if exp[1] else "",
                "location": exp[2] if exp[2] else "",
                "startDate": exp[3] if exp[3] else "",
                "endDate": exp[4] if exp[4] else "",
                "responsibilities": exp[5] if exp[5] else ""
            })
            
        # Retrieve education information.
        cursor.execute("SELECT degree, university, graduationYear FROM education WHERE userId = ?", (userId,))
        education = cursor.fetchall()
        user_data["education"] = []
        for edu in education:
            user_data["education"].append({
                "degree": edu[0] if edu[0] else "",
                "university": edu[1] if edu[1] else "",
                "graduationYear": edu[2] if edu[2] else ""
            })
            
        # Retrieve project information.
        cursor.execute("SELECT projectName, description FROM projects WHERE userId = ?", (userId,))
        projects = cursor.fetchall()
        user_data["projects"] = []
        for proj in projects:
            user_data["projects"].append({
                "projectName": proj[0] if proj[0] else "",
                "description": proj[1] if proj[1] else ""
            })
            
        # Retrieve certification information.
        cursor.execute("SELECT certificateName, issuer, year FROM certifications WHERE userId = ?", (userId,))
        certifications = cursor.fetchall()
        user_data["certifications"] = []
        for cert in certifications:
            user_data["certifications"].append({
                "certificateName": cert[0] if cert[0] else "",
                "issuer": cert[1] if cert[1] else "",
                "year": cert[2] if cert[2] else ""
            })
            
        conn.close()
        return user_data
        
    @staticmethod
    def generateResume(userId, jobId):
        """
        Generate a resume using AI based on the user's profile and job details.
        Returns the generated resume HTML, or an error string if generation fails.
        """
        if not apiModel.checkApiKey():
            return "API key not available. Cannot generate resume."
            
        client = Groq(api_key=apiModel.api_key)
        
        # Retrieve user profile data.
        user_data = apiModel.getUserProfile(userId)
        
        # Retrieve job details.
        job = JobModel.getJobById(jobId)
        if not job:
            return "Failed to retrieve job details."
            
        job_data = {
            "jobTitle": job[2] if job[2] else "",
            "company": job[12] if job[12] else "",
            "description": job[9] if job[9] else ""
        }
        
        # Build the AI prompt for resume generation.
        prompt = f"""
        You are an expert resume writer. Create a professional resume for a job application using the following information:

        JOB DETAILS:
        Title: {job_data['jobTitle']}
        Company: {job_data['company']}
        Description/Requirements: {job_data['description']}

        APPLICANT PROFILE:
        Personal Info: {json.dumps(user_data['personal'])}
        Work Experience: {json.dumps(user_data['workExperience'])}
        Education: {json.dumps(user_data['education'])}
        Projects: {json.dumps(user_data['projects'])}
        Certifications: {json.dumps(user_data['certifications'])}

        Create a targeted resume that highlights relevant experience and skills for this specific job.
        Format the resume as clean HTML with appropriate sections and styling.
        Use best practices for resume design and content.
        Do not include a photo.
        
        Your response should be ONLY the HTML content, starting with <html> and ending with </html>.
        """
        
        try:
            print("\nGenerating resume with Groq API...\n")
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-70b-8192",
            )
            
            if not chat_completion or not chat_completion.choices:
                return "Error: API returned an empty response for resume generation."
                
            html_content = chat_completion.choices[0].message.content.strip()
            print(html_content)
            # Save generated resume HTML to the database
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            
            # Check if a resume already exists for this user and job, then update or insert accordingly.
            cursor.execute("SELECT id FROM resume WHERE userId = ? AND jobId = ?", (userId, jobId))
            existing = cursor.fetchone()
            
            if existing:
                cursor.execute("UPDATE resume SET resume = ? WHERE userId = ? AND jobId = ?", 
                               (html_content, userId, jobId))
            else:
                cursor.execute("INSERT INTO resume (userId, jobId, resume) VALUES (?, ?, ?)",
                               (userId, jobId, html_content))
            
            conn.commit()
            conn.close()
            
            return html_content
            
        except Exception as e:
            print(f"Error generating resume: {e}")
            return f"Error generating resume: {e}"
    
    @staticmethod
    def generateCoverLetter(userId, jobId):
        """
        Generate a cover letter using AI based on the user's profile and job details.
        Returns the generated cover letter HTML, or an error string if generation fails.
        """
        if not apiModel.checkApiKey():
            return "API key not available. Cannot generate cover letter."
            
        client = Groq(api_key=apiModel.api_key)
        
        # Retrieve user profile data.
        user_data = apiModel.getUserProfile(userId)
        
        # Retrieve job details.
        job = JobModel.getJobById(jobId)
        if not job:
            return "Failed to retrieve job details."
            
        job_data = {
            "jobTitle": job[2] if job[2] else "",
            "company": job[12] if job[12] else "",
            "description": job[9] if job[9] else ""
        }
        
        # Build the AI prompt for cover letter generation.
        prompt = f"""
        You are an expert cover letter writer. Create a compelling cover letter for a job application using the following information:

        JOB DETAILS:
        Title: {job_data['jobTitle']}
        Company: {job_data['company']}
        Description: {job_data['description']}

        APPLICANT PROFILE:
        Personal Info: {json.dumps(user_data['personal'])}
        Work Experience: {json.dumps(user_data['workExperience'])}
        Education: {json.dumps(user_data['education'])}
        Projects: {json.dumps(user_data['projects'])}
        Certifications: {json.dumps(user_data['certifications'])}

        Create a personalized cover letter that:
        - Opens with a strong introduction
        - Explains why the applicant is interested in this specific role and company
        - Highlights 2-3 most relevant achievements or experiences that make them a good fit
        - Closes with enthusiasm about the opportunity and a call to action
        
        Format the cover letter as clean HTML with appropriate styling.
        Your response should be ONLY the HTML content, starting with <html> and ending with </html>.
        """
        
        try:
            print("\nGenerating cover letter with Groq API...\n")
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-70b-8192",
            )
            
            if not chat_completion or not chat_completion.choices:
                return "Error: API returned an empty response for cover letter generation."
                
            html_content = chat_completion.choices[0].message.content.strip()
            
            # Save generated cover letter HTML to the database
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            
            # Check if a cover letter already exists for this user-job combo, then update or insert accordingly.
            cursor.execute("SELECT id FROM coverLetter WHERE userId = ? AND jobId = ?", (userId, jobId))
            existing = cursor.fetchone()
            
            if existing:
                cursor.execute("UPDATE coverLetter SET coverLetter = ? WHERE userId = ? AND jobId = ?", 
                               (html_content, userId, jobId))
            else:
                cursor.execute("INSERT INTO coverLetter (userId, jobId, coverLetter) VALUES (?, ?, ?)",
                               (userId, jobId, html_content))
            
            conn.commit()
            conn.close()
            
            return html_content
            
        except Exception as e:
            print(f"Error generating cover letter: {e}")
            return f"Error generating cover letter: {e}"
