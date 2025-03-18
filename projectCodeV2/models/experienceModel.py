# ----------------------------------------------
# Title: expirenceModel.py
# Description: Expirence of user (work, education, project...) model
# Author(s): 
# Date created: Mar 8, 2025
# Date modified: Mar 8, 2025
# ----------------------------------------------
import sqlite3

class ExperienceModel:
    #Work, Volunteer, Project, Award, Certificate, Education
    #similar to job model
    #below are examples functions

    def __init__(self, db_path='database.db'):
        self.db_path = db_path

    def connect(self):
        """Connect to the database"""
        return sqlite3.connect(self.db_path)
    
    
    def add_experience(self, user_id, category, title, organization, start_date, end_date, description):
        conn = self.connect()
        cursor = conn.cursor()

        query_map = {
            'Work': "INSERT INTO workExperience (userId, jobTitle, company, startDate, endDate, responsibilities) VALUES (?, ?, ?, ?, ?, ?)",
            'Volunteer': "INSERT INTO volunteerExperience (userId, role, organization, description) VALUES (?, ?, ?, ?)",
            'Project': "INSERT INTO projects (userId, projectName, description) VALUES (?, ?, ?)",
            'Award': "INSERT INTO awards (userId, awardName, issuer, year) VALUES (?, ?, ?, ?)",
            'Certificate': "INSERT INTO certifications (userId, certificateName, issuer, year) VALUES (?, ?, ?, ?)",
            'Education': "INSERT INTO education (userId, degree, university, graduationYear) VALUES (?, ?, ?, ?)"
        }

        query = query_map.get(category)
        if query:
            if category in ['Work']:
                values = (user_id, title, organization, start_date, end_date, description)
            elif category in ['Volunteer']:
                values = (user_id, title, organization, description)
            elif category in ['Project']:
                values = (user_id, title, description)
            elif category in ['Award', 'Certificate', 'Education']:
                values = (user_id, title, organization, start_date)
            else:
                values = (user_id, title, organization, start_date, end_date, description)

        cursor.execute(query, values)
        conn.commit()

        conn.close()
        
    
    def get_experiences(self, user_id):
        """Fetch all experiences of a user"""
        conn = self.connect()
        cursor = conn.cursor()

        categories = ["Work", "Volunteer", "Project", "Award", "Certificate", "Education"]
        experience_data = {}

        for category in categories:
            table_map = {
                "Work": "workExperience",
                "Volunteer": "volunteerExperience",
                "Project": "projects",
                "Award": "awards",
                "Certificate": "certifications",
                "Education": "education"
            }
            column_map = {
                "Work": "jobTitle",
                "Volunteer": "role",
                "Project": "projectName",
                "Award": "awardName",
                "Certificate": "certificateName",
                "Education": "degree"
            }

            cursor.execute(f"SELECT {column_map[category]} FROM {table_map[category]} WHERE userId = ?", (user_id,))
            experience_data[category] = [row[0] for row in cursor.fetchall()]

        conn.close()
        return experience_data 


    @staticmethod
    def updateExperience():
        pass


    def delete_experience(self, user_id, category, title):
        """Delete an experience from the appropriate table"""
        conn = self.connect()
        cursor = conn.cursor()

        table_map = {
            "Work": "workExperience",
            "Volunteer": "volunteerExperience",
            "Project": "projects",
            "Award": "awards",
            "Certificate": "certifications",
            "Education": "education"
        }
        column_map = {
            "Work": "jobTitle",
            "Volunteer": "role",
            "Project": "projectName",
            "Award": "awardName",
            "Certificate": "certificateName",
            "Education": "degree"
        }

        if category in table_map:
            cursor.execute(f"DELETE FROM {table_map[category]} WHERE userId = ? AND {column_map[category]} = ?", (user_id, title))
            conn.commit()

        conn.close()
