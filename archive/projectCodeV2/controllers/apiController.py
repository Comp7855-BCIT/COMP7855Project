# ----------------------------------------------
# Title: apiController.py
# Description: Generate resume and cover letter using AI API
# Author(s): Jasmine 
# Date created: Mar 7, 2025
# Date modified: Mar 8, 2025
# ----------------------------------------------
# apiController.py
# apiController.py

import sqlite3
from flask import flash
from models.apiModel import apiModel
from models.jobModel import JobModel
from models.experienceModel import ExperienceModel

# class apiController:
#     @staticmethod
#     def suggestJobs(userId):
#         """
#         Compare user experiences with existing job listings from the 'jobs' table,
#         then store AI suggestions in jobSuggestions table.
#         The final suggestions are returned to be displayed on index.html
#         """

#         # 1) Combine user experiences into a single text
#         userExperienceText = ExperienceModel.getAllExperiencesForUser(userId)

#         # If no experience text, bail out
#         if not userExperienceText.strip():
#             flash("No experiences found for this user. Please add experiences first.")
#             return []

#         # 2) Gather job postings from 'jobs' table
#         conn = sqlite3.connect('database.db')
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM jobs")
#         all_jobs = cursor.fetchall()
#         conn.close()

#         if not all_jobs:
#             flash("No jobs found in the database.")
#             return []

#         # Build a summary of all jobs for the AI
#         # job structure: (id, userId, jobTitle, location, industry, deadline, salaryRange,
#         #                experienceLevel, rate, description, status, link, company)
#         jobs_summary_text = "List of jobs:\n"
#         for job_row in all_jobs:
#             j_id       = job_row[0]
#             j_title    = job_row[2]
#             j_company  = job_row[12] or "Unknown"
#             j_desc     = job_row[9]  or ""
#             jobs_summary_text += f"JobID {j_id}: Title={j_title}, Company={j_company}, Desc={j_desc}\n"

#         # 3) Create AI prompt
#         # Tweak your instructions to ensure AI returns lines with JobID, Title, Score, Reason
#         prompt = f"""
# The user has the following experiences (from Work, Volunteer, Project, Award, Certificate, Education):
# ---
# {userExperienceText}
# ---

# Below is a list of jobs from the database:
# ---
# {jobs_summary_text}
# ---

# Please recommend up to 3 jobs that best match the user's background. 
# For each recommended job, output one line in the exact format:

# JobID: <id> | Title: <title> | Score: <score> | Reason: <brief reason>

# Where:
#  - <id> is the numeric JobID from the list,
#  - <score> is a match percentage from 0 to 100,
#  - <brief reason> is a quick explanation.

# If no match is found, say: "No good matches found." 
# """

#         # 4) Send prompt to Groq
#         ai_response = apiModel.generateResponse(prompt)
#         if not ai_response:
#             flash("No response from Groq AI.")
#             return []

#         # 5) Parse the AI response
#         # We'll look for lines containing 'JobID:' and 'Score:' to parse out the data
#         suggestions = []
#         lines = ai_response.strip().split('\n')
#         for line in lines:
#             if "JobID:" in line and "Score:" in line:
#                 parts = line.split('|')
#                 # Expected format: 
#                 #   "JobID: 3 | Title: Designer | Score: 85 | Reason: Good alignment..."
#                 if len(parts) < 3:
#                     continue

#                 jobIdStr  = parts[0].replace("JobID:", "").strip()
#                 titleStr  = parts[1].replace("Title:", "").strip()
#                 scoreStr  = parts[2].replace("Score:", "").strip()
#                 # reasonStr = parts[3].replace("Reason:", "").strip() if len(parts) >= 4 else ""

#                 # Convert jobIdStr to int
#                 try:
#                     jobIdVal = int(jobIdStr)
#                 except:
#                     jobIdVal = None

#                 # Convert scoreStr to float
#                 try:
#                     matchScoreVal = float(scoreStr)
#                 except:
#                     matchScoreVal = 0.0

#                 # Now see if jobIdVal is in all_jobs
#                 matchingJobRow = next((j for j in all_jobs if j[0] == jobIdVal), None)
#                 if matchingJobRow:
#                     # If found, we can get actual jobTitle, link, company from DB row
#                     actualTitle  = matchingJobRow[2]
#                     actualLink   = matchingJobRow[11] or ""
#                     actualCompany= matchingJobRow[12] or "Unknown"
#                 else:
#                     # fallback if not found
#                     actualTitle   = titleStr
#                     actualLink    = ""
#                     actualCompany = "N/A"

#                 # 6) Save suggestion in DB
#                 #   jobSuggestions table is: (id, userId, jobTitle, company, link, matchScore)
#                 JobModel.saveJobSuggestions(
#                     userId=userId,
#                     jobTitle=actualTitle,
#                     company=actualCompany,
#                     link=actualLink,
#                     matchScore=matchScoreVal
#                 )

#                 # Build suggestion for direct return
#                 suggestions.append({
#                     "jobTitle": actualTitle,
#                     "company": actualCompany,
#                     "link": actualLink,
#                     "matchScore": matchScoreVal
#                 })

#         # If the AI didn't produce lines with "JobID:" or "Score:", suggestions might be empty
#         if not suggestions:
#             flash("AI did not produce any matching lines. Possibly no matches found.")
#         else:
#             flash(f"Generated {len(suggestions)} job suggestions!")

#         return suggestions