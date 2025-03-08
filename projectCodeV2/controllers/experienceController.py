# ----------------------------------------------
# Title: expirenceController.py
# Description: Expirence of user (work, education, project...) controller
# Author(s): 
# Date created: Mar 8, 2025
# Date modified: Mar 8, 2025
# ----------------------------------------------
from flask import render_template, request, redirect, url_for, flash
from models.experienceModel import ExperienceModel

class ExperienceController:
    #Work, Volunteer, Project, Award, Certificate, Education
    #similar to job controller
    #below are example functions
    
    @staticmethod
    def viewExperience(userId): #Get all the user expirence to give to AI API and display in table on website
        pass
    
    @staticmethod
    def newExperience():
        pass
    
    @staticmethod
    def deleteExperience():
        pass
