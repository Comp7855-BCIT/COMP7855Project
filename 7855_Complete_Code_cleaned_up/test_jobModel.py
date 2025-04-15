# test_jobDatabase.py
import unittest
import sqlite3
import os
import tempfile
from models.jobModel import JobModel

class TestJobDatabase(unittest.TestCase):
    def setUp(self):
        # Create a temporary file for our test database.
        self.db_fd, self.db_path = tempfile.mkstemp()
        # Open a connection to the temporary database.
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        # Create the 'jobs' table using the same schema as defined in your initDb.py.
        self.cursor.execute('''
            CREATE TABLE jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                userId INTEGER,
                jobTitle TEXT,
                location TEXT,
                industry TEXT,
                deadline DATE,
                salaryRange TEXT,
                experienceLevel TEXT,
                rate INTEGER,
                description TEXT,
                status TEXT,
                link TEXT,
                company TEXT
            )
        ''')
        # Create the jobSuggestions table (if needed for your tests).
        self.cursor.execute('''
            CREATE TABLE jobSuggestions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                userId INTEGER,
                jobTitle TEXT,
                company TEXT,
                link TEXT,
                matchScore REAL,
                FOREIGN KEY (userId) REFERENCES users(id)
            )
        ''')
        self.conn.commit()

        # Monkey-patch sqlite3.connect so that every connection is made to our temporary DB.
        # Use a helper function to avoid recursion.
        self.original_connect = sqlite3.connect
        def fake_connect(_):
            return self.original_connect(self.db_path)
        sqlite3.connect = fake_connect

    def tearDown(self):
        # Close the connection and remove the temporary database file.
        self.conn.close()
        os.close(self.db_fd)
        os.remove(self.db_path)
        # Restore the original sqlite3.connect function.
        sqlite3.connect = self.original_connect

    def test_addJob(self):
        # Test that adding a job works as expected.
        JobModel.createJob(
            1, "Engineer", "City", "Tech", "2025-12-31", "50k-70k", "Mid", 5,
            "Job Description", "Open", "http://job.com", "CompanyA"
        )
        # Retrieve jobs for user 1.
        jobs = JobModel.getJobs(1)
        self.assertEqual(len(jobs), 1)
        # Verify the job title is correct.
        self.assertEqual(jobs[0][2], "Engineer")

    def test_updateJob(self):
        # Insert a job first.
        JobModel.createJob(
            1, "Engineer", "City", "Tech", "2025-12-31", "50k-70k", "Mid", 5,
            "Job Description", "Open", "http://job.com", "CompanyA"
        )
        jobs = JobModel.getJobs(1)
        jobId = jobs[0][0]
        # Update job title and salaryRange.
        JobModel.updateJob(
            jobId, "Senior Engineer", "City", "Tech", "2025-12-31", "60k-80k",
            "Senior", 5, "Updated Description", "Open", "http://job.com", "CompanyA"
        )
        updated_job = JobModel.getJobById(jobId)
        self.assertEqual(updated_job[2], "Senior Engineer")
        # You may add further assertions to check other updated fields.

    def test_deleteJob(self):
        # Insert a job and verify it exists.
        JobModel.createJob(
            1, "Engineer", "City", "Tech", "2025-12-31", "50k-70k", "Mid", 5,
            "Job Description", "Open", "http://job.com", "CompanyA"
        )
        jobs_before = JobModel.getJobs(1)
        self.assertEqual(len(jobs_before), 1)
        jobId = jobs_before[0][0]
        # Delete the job.
        JobModel.deleteJob(jobId)
        jobs_after = JobModel.getJobs(1)
        self.assertEqual(len(jobs_after), 0)

    def test_viewJobs(self):
        # Insert multiple jobs to check view functionality.
        JobModel.createJob(
            1, "Engineer", "City", "Tech", "2025-12-31", "50k-70k", "Mid", 5,
            "Job Description 1", "Open", "http://job.com/1", "CompanyA"
        )
        JobModel.createJob(
            1, "Analyst", "City", "Finance", "2025-11-30", "40k-60k", "Junior", 4,
            "Job Description 2", "Open", "http://job.com/2", "CompanyB"
        )
        jobs = JobModel.getJobs(1)
        self.assertEqual(len(jobs), 2)
        titles = [job[2] for job in jobs]
        self.assertIn("Engineer", titles)
        self.assertIn("Analyst", titles)

    def test_qualificationAnalysis(self):
        # Assuming you have a qualificationAnalysis() method, implement a test.
        pass

if __name__ == '__main__':
    unittest.main()
