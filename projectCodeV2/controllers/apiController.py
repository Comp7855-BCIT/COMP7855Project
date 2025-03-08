# ----------------------------------------------
# Title: apiController.py
# Description: Generate resume and cover letter using AI API
# Author(s): Jasmine 
# Date created: Mar 7, 2025
# Date modified: Mar 8, 2025
# ----------------------------------------------
from flask import render_template, request, redirect, url_for, flash
from models.apiModel import apiModel

from controllers.experienceController import ExperienceController
from controllers.jobController import JobController
from controllers.userController import UserController

class apiController:
    #below are example functions
    
    @staticmethod
    def generateResume(userId, jobId):
        pass
    """
    Fetches user profile, expirence and job details from the database.
    
    Create resume prompt.

    Calls apiModel.generateResponse(prompt) to get the resume HTML.

    Calls documentModel.saveResume() to save the HTML to the database.

    Returns the generated resume HTML.
    """

    @staticmethod
    def generateCoverLetter(userId, jobId):
        pass
    """
    Fetches user profile, expirence and job details from the database.

    Create cover letter prompt.

    Calls apiModel.generateResponse(prompt) to get the cover letter HTML.

    Calls documentModel.saveCoverLetter() to save the HTML to the database.

    Returns the generated cover letter HTML.
    """
    @staticmethod
    def suggestJobs(userId, jobModel):
        pass
    """
    Fetches user job history from the database.

    Create a prompt.

    Calls apiModel.generateResponse(prompt) to get the job suggestion.

    Calls jobModel.saveJobSuggestions() to save the HTML to the database.

    """
