# ----------------------------------------------
# Title: jobModel.py
# Description: user add, modify and delete job model
# Author(s): Feliex
# Date created: Feb 19, 2025
# Date modified: Mar 8, 2025
# ----------------------------------------------
import sqlite3

class JobModel:
    
    @staticmethod
    def createJob(userId, jobTitle, location, industry, deadline, salaryRange, experienceLevel, rate, description, status, link, company):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # Insert job into the database
        cursor.execute('''
            INSERT INTO jobs (userId, jobTitle, location, industry, deadline, salaryRange, experienceLevel, rate, description, status, link, company)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
        ''', (userId, jobTitle, location, industry, deadline, salaryRange, experienceLevel, rate, description, status, link, company))

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
    def getJobById(jobId):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM jobs WHERE id = ?', (jobId,))
        job = cursor.fetchone()
        conn.close()
        return job

    @staticmethod
    def updateJob(jobId, jobTitle, location, industry, deadline, salaryRange, experienceLevel, rate, description, status, link, company):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE jobs
            SET jobTitle = ?, location = ?, industry = ?, deadline = ?, salaryRange = ?, experienceLevel = ?, rate = ?, description = ?, status = ?, link=?, company=?
            WHERE id = ?
        ''', (jobTitle, location, industry, deadline, salaryRange, experienceLevel, rate, description, status, link, company, jobId))
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
        pass
    #Retrieves jobs based on filters like archive
    
    @staticmethod
    def saveJobSuggestions(userId, jobTitle, company, link):
        pass
    #Save into database jobs suggestions
    
    @staticmethod
    def getJobSuggestions(userId):
        pass
    #reteive into database jobs suggestions so display them