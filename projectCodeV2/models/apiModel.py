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
            {"title": job[2], "industry": job[3], "description": job[8]}
            for job in jobs
        ]
        job_data = json.dumps(job_list)

        # Create prompt for the AI
        prompt = f"""
        Given the following list of jobs that a user is interested in:
        {job_data}
        
        Generate 3 new job suggestions that are relevant based on the provided jobs. 
        Each suggestion should include:
        - Job title
        - Company name (can be fictional)
        - A job link (fictional URL)
        - A match score (percentage based on how relevant it is)

        Return the response in JSON format like this:
        [
            {{"jobTitle": "Example Title", "company": "Example Corp", "link": "http://example.com", "matchScore": 87}},
            ...
        ]
        """

        print("\nSending request to Groq API...\n")
        
        try:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-70b-8192",
            )

            # Extract response
            # Print the entire chat_completion object to see the full API response
            print("Full API response:", chat_completion)

            #response = chat_completion.choices[0].message.content
            #job_suggestions = json.loads(response)  # Convert string to JSON

            # Save suggestions to database
            #JobModel.saveJobSuggestions(userId, job_suggestions)
            
            #return job_suggestions  # Return the suggestions

        except Exception as e:
            print(f"Error communicating with Groq API: {e}")
            return None


