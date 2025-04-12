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
        suggestions = apiModel.generateJobSuggestions(userId)
        return suggestions
    @staticmethod
    def generate_documents(user_id, pdfkit_config):
        documents = apiModel.generate_documents(user_id, pdfkit_config)
        return documents
    @staticmethod
    def generateResume(userId, jobId):
        resume = apiModel.generateResume(userId, jobId)
        return resume
    @staticmethod
    def generateCoverLetter(userId, jobId):
        coverletter = apiModel.generateCoverLetter(userId, jobId)
        return coverletter
    