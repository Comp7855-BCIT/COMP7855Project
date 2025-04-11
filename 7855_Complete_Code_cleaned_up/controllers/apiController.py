# ----------------------------------------------
# Title: apiController.py
# Description: Generate resume and cover letter using AI API
# Author(s): Jasmine 
# Date created: Mar 7, 2025
# Date modified: Mar 8, 2025
# ----------------------------------------------
# apiController.py
# apiController.py

import sqlite3
from flask import flash
from models.apiModel import apiModel
from models.jobModel import JobModel
from models.experienceModel import ExperienceModel

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
    