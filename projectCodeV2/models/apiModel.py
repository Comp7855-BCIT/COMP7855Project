# ----------------------------------------------
# Title: apiModel.py
# Description: Uses AI API to generate responses
# Author(s): Yui 
# Date created: Mar 4, 2025
# Date modified: Mar 4, 2025
# ----------------------------------------------
import os
import sys
import json
from groq import Groq
from models.jobModel import JobModel  # Import JobModel to fetch jobs

class apiModel:
    api_key = "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"  

    @staticmethod
    def generateJobSuggestions(userId):
        if not apiModel.api_key:
            print("Can't find the key.")
            sys.exit(1)

        client = Groq(api_key=apiModel.api_key)

        # Fetch user's job data from database
        jobs = JobModel.getJobs(userId)
        
        if not jobs:
            print("No jobs found in the database.")
            return None

        # Format job data for API
        job_list = [
            {"title": job[2], "industry": job[4], "description": job[9]}  # Ensure correct column indices
            for job in jobs
        ]
        job_data = json.dumps(job_list)

        # Create prompt for the AI
        prompt = f"""
        You are an AI job recommendation assistant. Given the following jobs the user is interested in:
        {job_data}

        Suggest exactly 3 new jobs in JSON format. Each job must have:
        - "jobTitle"
        - "company"
        - "link" (a fictional URL)
        - "matchScore" (a percentage from 0-100)

        Respond with **only** valid JSON, no explanations.

        Example:
        [
            {{"jobTitle": "Software Engineer", "company": "TechCorp", "link": "http://techcorp.com", "matchScore": 95}},
            {{"jobTitle": "Data Scientist", "company": "DataWorks", "link": "http://dataworks.com", "matchScore": 90}},
            {{"jobTitle": "AI Researcher", "company": "OpenAI", "link": "http://openai.com", "matchScore": 88}}
        ]
        """

        print("\nSending request to Groq API...\n")
        
        try:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-70b-8192",
            )

            # Ensure a valid response is received
            if not chat_completion or not chat_completion.choices:
                print("Error: API returned an empty response.")
                return None

            response_text = chat_completion.choices[0].message.content.strip()
            
            # Debugging output
            print("\nReceived API Response:\n", response_text)

            # Ensure JSON format
            if not response_text.startswith("[") or not response_text.endswith("]"):
                print("Error: API response does not start and end with JSON array brackets.")
                return None

            job_suggestions = json.loads(response_text)  # Parse JSON

            # Save AI-generated suggestions to the database
            JobModel.saveJobSuggestions(userId, job_suggestions)

            # Return saved suggestions
            return JobModel.getJobSuggestions(userId)

        except Exception as e:
            print(f"Error communicating with Groq API: {e}")
            return None

