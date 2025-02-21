# ----------------------------------------------
# Title: jobDatabase.py
# Description: All pages
# Author(s): Feliex Sarkar  
# Date created: Feb 19, 2025
# Date modified: Feb 20, 2025
# ----------------------------------------------

import sqlite3

class jobDatabase:
    def __init__(self):
        # Initialize and connect to the SQLite database
        self.conn = sqlite3.connect('jobs.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        # Create jobs table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                jobTitle TEXT,
                location TEXT,
                jobType TEXT,
                industry TEXT,
                salaryRange TEXT,
                experienceLevel TEXT
            )
        ''')
        self.conn.commit()

    def addJob(self):
        jobTitle = input("\nEnter job title: ")
        location = input("Enter location: ")
        jobType = input("Enter job type (Full-time, Part-time, Contract, etc.): ")
        industry = input("Enter industry: ")
        salaryRange = input("Enter salary range: ")
        experienceLevel = input("Enter required experience level: ")

        self.cursor.execute('''
            INSERT INTO jobs (jobTitle, location, jobType, industry, salaryRange, experienceLevel)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (jobTitle, location, jobType, industry, salaryRange, experienceLevel))
        self.conn.commit()
        print("Job added successfully.")

    def updateJob(self, jobTitle):
        print(f"Updating job: {jobTitle}")
        field = input("Enter the field to update (location, jobType, industry, salaryRange, experienceLevel): ")
        new_value = input(f"Enter new value for {field}: ")

        self.cursor.execute(f'''
            UPDATE jobs
            SET {field} = ?
            WHERE jobTitle = ?
        ''', (new_value, jobTitle))
        self.conn.commit()
        print("Job updated successfully.")

    def deleteJob(self, jobTitle):
        self.cursor.execute('''
            DELETE FROM jobs WHERE jobTitle = ?
        ''', (jobTitle,))
        self.conn.commit()
        print("Job deleted successfully.")

    def viewJobs(self):
        self.cursor.execute('''
            SELECT * FROM jobs
        ''')
        jobs = self.cursor.fetchall()
        for job in jobs:
            print(job)

    def qualificationAnalysis(self, jobTitle):
        self.cursor.execute('''
            SELECT * FROM jobs WHERE jobTitle = ?
        ''', (jobTitle,))
        job = self.cursor.fetchone()
        if job:
            print(f"Generating qualification analysis for {jobTitle}...")
            # Placeholder for actual qualification analysis logic
            print(f"Job Details: {job}")
        else:
            print("Job not found.")

    def __del__(self):
        self.conn.close()
