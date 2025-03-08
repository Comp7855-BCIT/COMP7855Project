# ----------------------------------------------
# Title: jobController.py
# Description: user add, modify and delete job controller
# Author(s): Jasmine
# Date created: Feb 28, 2025
# Date modified: Mar 8, 2025
# ----------------------------------------------
from flask import render_template, request, redirect, url_for
from models.jobModel import JobModel

class JobController:

    @staticmethod
    def viewJobs(userId):
        # Get jobs for the user from the database
        jobs = JobModel.getJobs(userId)
        return jobs
    
    @staticmethod
    def newJob(jobId, userId):
        if request.method == 'POST':
            # Parse incoming form data
            title = request.form['job-title']
            description = request.form['job-description']
            rate = request.form['rate']
            deadline = request.form['deadline']
            location = request.form['job-location']
            industry = request.form['job-industry']
            salary = request.form['job-salary']
            level = request.form['job-level']
            status = request.form['job-status']
            link = request.form['job-link']
            company = request.form['job-company']

            if jobId:
                # Update the existing job
                JobModel.updateJob(jobId, title, location, industry, deadline, salary, level, rate, description, status, link,company)
            else:
                # Create a new job
                JobModel.createJob(userId, title, location, industry, deadline, salary, level, rate, description, status, link,company)
        
            # Redirect to the main page (index)
            return redirect(url_for('index'))

        # If jobId is provided, fetch the job details for editing
        job = None
        if jobId:
            job = JobModel.getJobById(jobId)

        return render_template('newJob.html', job=job)
    
    @staticmethod
    def deleteJob(jobId):
        JobModel.deleteJob(jobId)
        return redirect(url_for('index'))
    
    @staticmethod
    def viewJobSuggestions(userId):
        pass
    #view job suggestion on html page
    #will call on jobModel.getJobSuggestions(userId)