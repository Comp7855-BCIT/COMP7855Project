# ----------------------------------------------
# Title: jobModel.py
# Description: user add, modify and delete job model
# Author(s): Felix
# Date created: Feb 19, 2025
# Date modified: Mar 10, 2025
# ----------------------------------------------

import sqlite3
import json

# Inserts a new job posting into the job table
class JobModel:

    @staticmethod
    def createJob(userId, jobTitle, location, industry, deadline, salaryRange,
                  experienceLevel, rate, description, status, link, company):
        # Open connection to the database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        # Execute an INSERT statement to add the job into the 'jobs' table.
        cursor.execute('''
            INSERT INTO jobs (userId, jobTitle, location, industry, deadline,
                              salaryRange, experienceLevel, rate,
                              description, status, link, company)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (userId, jobTitle, location, industry, deadline, salaryRange,
              experienceLevel, rate, description, status, link, company))
        # Commit the changes and close the connection.
        conn.commit()
        conn.close()
        print("Job added successfully.")

    # Retrieves all job postings from the job table for a specific user
    @staticmethod
    def getJobs(userId):
        # Open database connection
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        # Select all rows from 'jobs' where userId matches the provided value.
        cursor.execute('SELECT * FROM jobs WHERE userId = ?', (userId,))
        jobs = cursor.fetchall()
        conn.close()
        return jobs

    # Returns only the jobs that have the specified status for a given user
    @staticmethod
    def getJobsByStatus(userId, status):
        """
        Returns only jobs for a given user with the matching status.
        """
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM jobs
            WHERE userId = ?
              AND status = ?
        ''', (userId, status))
        jobs = cursor.fetchall()
        conn.close()
        return jobs

    # Retrieves a specific job posting from the job table by jobId
    @staticmethod
    def getJobById(jobId):
        try:
            # Open database connection
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            # Select the job record matching the given jobId.
            cursor.execute("SELECT * FROM jobs WHERE id = ?", (jobId,))
            job = cursor.fetchone()
            conn.close()
            return job
        except Exception as e:
            print(f"Error getting job by ID: {e}")
            return None

    # Updates an existing job posting in the job table identified by jobId
    @staticmethod
    def updateJob(jobId, jobTitle, location, industry, deadline, salaryRange,
                  experienceLevel, rate, description, status, link, company):
        # Open database connection
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        # Execute an UPDATE statement with the new job data.
        cursor.execute('''
            UPDATE jobs
            SET jobTitle = ?, location = ?, industry = ?, deadline = ?,
                salaryRange = ?, experienceLevel = ?, rate = ?,
                description = ?, status = ?, link = ?, company = ?
            WHERE id = ?
        ''', (jobTitle, location, industry, deadline, salaryRange,
              experienceLevel, rate, description, status, link, company, jobId))
        # Commit changes and close connection.
        conn.commit()
        conn.close()
        print("Job updated successfully.")

    # Deletes a job posting from the job table by jobId
    @staticmethod
    def deleteJob(jobId):
        # Open connection to the database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        # Execute a DELETE statement to remove the job record.
        cursor.execute('DELETE FROM jobs WHERE id = ?', (jobId,))
        conn.commit()
        conn.close()
        print("Job deleted successfully.")

    # Placeholder method for advanced filtering (if needed later)
    @staticmethod
    def getJobsByFilters():
        """
        Placeholder method if you need more advanced filtering 
        (e.g., location, salary, etc.)
        """
        pass

    # Saves AI-generated job suggestions into the jobSuggestions table.
    @staticmethod
    def saveJobSuggestions(userId, suggestions):
        """
        Save AI-generated job suggestions to the database.
        Clears old suggestions before inserting new ones.
        Each suggestion should be a dictionary with keys:
          'jobTitle', 'company', 'link', and 'matchScore'.
        """
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Clear old suggestions for the user.
        cursor.execute("DELETE FROM jobSuggestions WHERE userId = ?", (userId,))

        # Insert each new suggestion.
        for suggestion in suggestions:
            cursor.execute(
                """
                INSERT INTO jobSuggestions (userId, jobTitle, company, link, matchScore) 
                VALUES (?, ?, ?, ?, ?)
                """,
                (userId, suggestion["jobTitle"], suggestion["company"], suggestion["link"], suggestion["matchScore"])
            )

        conn.commit()
        conn.close()

    # Retrieves saved job suggestions for a given user from the jobSuggestions table.
    @staticmethod
    def getJobSuggestions(userId):
        """
        Retrieve saved AI job suggestions from the database.
        Returns a list of dictionaries, each with:
          'jobTitle', 'company', 'link', and 'matchScore'.
        """
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT jobTitle, company, link, matchScore FROM jobSuggestions WHERE userId = ?', (userId,))
        results = cursor.fetchall()
        conn.close()

        # Format the results into dictionaries.
        return [{"jobTitle": r[0], "company": r[1], "link": r[2], "matchScore": r[3]} for r in results]
    
    # Retrieves the resume content from the resume table for the given user and job.
    @staticmethod
    def getResume(userId, jobId):
        """
        Retrieves the resume from the 'resume' table for the specific user and job.
        Returns the resume content as a string if found; otherwise, returns None.
        """
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT resume FROM resume WHERE userId = ? AND jobId = ?", (userId, jobId))
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else None
        except Exception as e:
            print(f"Error fetching resume: {str(e)}")
            return None

    # Saves or updates the resume content for a given user and job in the resume table.
    @staticmethod
    def saveResume(userId, jobId, resume_content):
        """
        Saves AI-generated or manually provided resume content for the user and job.
        If a record exists, it updates it; otherwise, it inserts a new record.
        Returns True if the operation is successful; otherwise, False.
        """
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            
            # Check if a resume entry exists for this user and job.
            cursor.execute("SELECT id FROM resume WHERE userId = ? AND jobId = ?", (userId, jobId))
            exists = cursor.fetchone()
            
            if exists:
                # Update the existing resume.
                cursor.execute("""
                    UPDATE resume SET resume = ? 
                    WHERE userId = ? AND jobId = ?
                """, (resume_content, userId, jobId))
            else:
                # Insert a new resume record.
                cursor.execute("""
                    INSERT INTO resume (userId, jobId, resume)
                    VALUES (?, ?, ?)
                """, (userId, jobId, resume_content))
                
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving resume: {str(e)}")
            return False