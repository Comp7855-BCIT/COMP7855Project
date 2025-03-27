# ----------------------------------------------
# Title: apiModel.py
# Description: Uses AI API to generate responses
# Author(s): Yui 
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

from groq import Groq
from jobspy import scrape_jobs

from models.jobModel import JobModel
from models.experienceModel import ExperienceModel


class apiModel:
    # Replace with your actual Groq API key
    api_key = "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"

    @staticmethod
    def generateJobSuggestions(userId):
        """
        1) Gather the user's experiences from the DB, truncating if needed.
        2) Use JobSpy to scrape new jobs from Indeed.
        3) Build a prompt that includes experiences + job data.
        4) Send prompt to Groq, parse the AI's JSON output.
        5) Save the suggestions into 'jobSuggestions' table.
        6) Return the newly saved suggestions.

        If you see 'invalid_api_key' or 401 errors, ensure api_key is correct.
        If you see token-limit (413) errors, reduce the data in the prompt.
        """

        # 0) Validate the Groq API key
        if not apiModel.api_key:
            print("No Groq API key provided. Exiting.")
            return None

        # 1) Gather user’s experiences, truncated to keep the prompt smaller
        user_experience_text = apiModel._getUserExperienceText(userId)
        if not user_experience_text.strip():
            user_experience_text = "(No experiences)"

        # Fetch users saved jobs from the database
        jobs = JobModel.getJobs(userId)
        if not jobs:
            print("No jobs found in database.")
            return None

        job_titles = list(set(job[2] for job in jobs if job[2]))

        if not job_titles:
            print("No valid job titles found.")
            return None

        # Fetch jobs using jobspy
        try:
            print(f"Searching for jobs with titles: {job_titles}")

            job_df = scrape_jobs(
                site_name="indeed",
                search_term=" OR ".join(job_titles),
                location="Vancouver, BC",  # or from user’s profile
                results_wanted=5,         # a few results
                hours_old=336,
                country_indeed='Canada'
            )
        except Exception as e:
            print("Error scraping Indeed via JobSpy:", e)
            return None

        # If no jobs returned, bail out
        if not isinstance(job_df, pd.DataFrame) or job_df.empty:
            print("No jobs found from JobSpy.")
            return None

        # Debug: Print the raw DataFrame in your console
        print("\nRaw job results from JobSpy:\n", job_df)
        print("Columns returned by JobSpy:", job_df.columns)

        # Shuffle or limit how many to pass to Groq to reduce token usage
        job_df = job_df.sample(frac=1).head(3).reset_index(drop=True)

        # Convert these jobs to a small JSON-like list
        job_list_for_ai = []
        for _, row in job_df.iterrows():
            job_list_for_ai.append({
                "title": row.get("title", "Unknown"),
                "company": row.get("company", "Unknown"),
                "link": row.get("job_url", "#"),
                # omit big fields to avoid token blowout
                "description": "(omitted to save tokens)"
            })

        # 3) Build your prompt
        #    We'll ask for EXACTLY 3 suggestions in a JSON array.
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
          {{
            "jobTitle": "Software Engineer",
            "company": "TechCorp",
            "link": "https://example.com",
            "matchScore": 70
          }},
          ...
        ]
        """)

        # 4) Call Groq with the prompt
        try:
            client = Groq(api_key=apiModel.api_key)
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-70b-8192",  # replace with your available model
            )
        except Exception as e:
            print(f"Error calling Groq: {e}")
            return None

        if not chat_completion or not chat_completion.choices:
            print("No response from Groq.")
            return None

        response_text = chat_completion.choices[0].message.content.strip()
        print("\nAI Response:\n", response_text)

        # 5) Extract bracketed JSON from the AI response
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

        # The AI should produce a list of dicts with "jobTitle", "company", "link", "matchScore"
        if not isinstance(job_suggestions, list):
            print("AI did not return a list of suggestions.")
            return None

        # 6) Save to DB:  jobSuggestions table
        # (jobTitle, company, link, matchScore)
        JobModel.saveJobSuggestions(userId, job_suggestions)

        # 7) Return the newly saved rows from DB
        return JobModel.getJobSuggestions(userId)

    @staticmethod
    def _getUserExperienceText(userId):
        """
        Gather user experiences from your experienceModel. 
        Return a truncated string so you don’t exceed token limits if huge.
        """
        exp_model = ExperienceModel()
        exp_data = exp_model.get_experiences(userId)  # e.g. {"Work": [...], "Volunteer": [...], ...}

        lines = []
        for category, items in exp_data.items():
            if items:
                lines.append(f"{category}: {', '.join(items)}")

        # Combine into a single text block
        combined = "\n".join(lines)
        # Truncate to avoid 413 token limit errors if needed
        return combined[:800]  # up to 800 characters
