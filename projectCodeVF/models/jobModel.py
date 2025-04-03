# ----------------------------------------------
# Title: jobModel.py
# Description: user add, modify and delete job model
# Author(s): Felix
# Date created: Feb 19, 2025
# Date modified: Mar 10, 2025
# ----------------------------------------------
import sqlite3
import json

class JobModel:

    @staticmethod
    def createJob(userId, jobTitle, location, industry, deadline, salaryRange,
                  experienceLevel, rate, description, status, link, company):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO jobs (userId, jobTitle, location, industry, deadline,
                              salaryRange, experienceLevel, rate,
                              description, status, link, company)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (userId, jobTitle, location, industry, deadline, salaryRange,
              experienceLevel, rate, description, status, link, company))
        conn.commit()
        conn.close()
        print("Job added successfully.")

    @staticmethod
    def getJobs(userId):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM jobs WHERE userId = ?', (userId,))
        jobs = cursor.fetchall()
        conn.close()
        return jobs

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

    @staticmethod
    def getJobById(jobId):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM jobs WHERE id = ?', (jobId,))
        job = cursor.fetchone()
        conn.close()
        return job

    @staticmethod
    def updateJob(jobId, jobTitle, location, industry, deadline, salaryRange,
                  experienceLevel, rate, description, status, link, company):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE jobs
            SET jobTitle = ?, location = ?, industry = ?, deadline = ?,
                salaryRange = ?, experienceLevel = ?, rate = ?,
                description = ?, status = ?, link = ?, company = ?
            WHERE id = ?
        ''', (jobTitle, location, industry, deadline, salaryRange,
              experienceLevel, rate, description, status, link, company, jobId))
        conn.commit()
        conn.close()
        print("Job updated successfully.")

    @staticmethod
    def deleteJob(jobId):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM jobs WHERE id = ?', (jobId,))
        conn.commit()
        conn.close()
        print("Job deleted successfully.")

    @staticmethod
    def getJobsByFilters():
        """
        Placeholder method if you need more advanced filtering 
        (e.g., location, salary, etc.)
        """
        pass

    @staticmethod
    def saveJobSuggestions(userId, suggestions):
        """
        Save AI-generated job suggestions to the database.
        Clears old suggestions before inserting new ones.
        """
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Clear old suggestions for the user
        cursor.execute("DELETE FROM jobSuggestions WHERE userId = ?", (userId,))

        # Insert new suggestions
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

    @staticmethod
    def getJobSuggestions(userId):
        """
        Retrieve saved AI job suggestions from the database.
        """
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT jobTitle, company, link, matchScore FROM jobSuggestions WHERE userId = ?', (userId,))
        results = cursor.fetchall()
        conn.close()

        # Format results
        return [{"jobTitle": r[0], "company": r[1], "link": r[2], "matchScore": r[3]} for r in results]