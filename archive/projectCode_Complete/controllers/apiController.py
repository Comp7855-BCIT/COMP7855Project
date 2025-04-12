# ----------------------------------------------
# Title: apiController.py
# Description: Generate resume and cover letter using AI API
# Author(s): Feliex
# Date created: Mar 7, 2025
# Date modified: Mar 8, 2025
# ----------------------------------------------
# apiController.py


from flask import flash
from models.apiModel import apiModel

class apiController:
    @staticmethod
    def generateJobSuggestions(userId):
        return apiModel.generateJobSuggestions(userId)

    @staticmethod
    def generate_documents(user_id, pdfkit_config):
        return apiModel.generate_documents(user_id, pdfkit_config)

    @staticmethod
    def generateResume(userId, jobId):
        return apiModel.generateResume(userId, jobId)

    @staticmethod
    def generateCoverLetter(userId, jobId):
        return apiModel.generateCoverLetter(userId, jobId)

    @staticmethod
    def getUserProfile(userId):
        return apiModel.getUserProfile(userId)

    @staticmethod
    def checkApiKey():
        return apiModel.checkApiKey()
