# ----------------------------------------------
# Title: apiController.py
# Description: Generate resume and cover letter using AI API
# Author(s): Jasmine 
# Date created: Mar 7, 2025
# Date modified: Mar 8, 2025
# ----------------------------------------------

from flask import flash
from models.apiModel import apiModel

class apiController:
    @staticmethod
    def generateJobSuggestions(userId):
        # Call the apiModel to generate AI job suggestions for the given user.
        suggestions = apiModel.generateJobSuggestions(userId)
        return suggestions

    @staticmethod
    def generate_documents(user_id, pdfkit_config):
        # Generate resume and cover letter documents using the apiModel.
        documents = apiModel.generate_documents(user_id, pdfkit_config)
        return documents

    @staticmethod
    def generateResume(userId, jobId):
        # Generate a resume for the specified user and job using the apiModel.
        resume = apiModel.generateResume(userId, jobId)
        return resume

    @staticmethod
    def generateCoverLetter(userId, jobId):
        # Generate a cover letter for the specified user and job using the apiModel.
        coverletter = apiModel.generateCoverLetter(userId, jobId)
        return coverletter
