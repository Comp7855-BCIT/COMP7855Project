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

    def get_work_by_title(self, user_id, title):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM workExperience WHERE userId = ? AND jobTitle = ?', (user_id, title))
        data = cursor.fetchone()
        conn.close()
        return data

    def update_work_experience_by_title(self, user_id, title, company, start, end, location, responsibilities):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE workExperience
            SET company = ?, startDate = ?, endDate = ?, location = ?, responsibilities = ?
            WHERE userId = ? AND jobTitle = ?
        ''', (company, start, end, location, responsibilities, user_id, title))
        conn.commit()
        conn.close()

    def get_volunteer_by_title(self, user_id, title):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM volunteerExperience WHERE userId = ? AND role = ?", (user_id, title))
        data = cursor.fetchone()
        conn.close()
        return data

    def update_volunteer_experience_by_title(self, user_id, old_title, new_title, organization, description):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE volunteerExperience
            SET role = ?, organization = ?, description = ?
            WHERE userId = ? AND role = ?
        ''', (new_title, organization, description, user_id, old_title))
        conn.commit()
        conn.close()

    def get_project_by_title(self, user_id, title):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects WHERE userId = ? AND projectName = ?", (user_id, title))
        data = cursor.fetchone()
        conn.close()
        return data

    def update_project_by_title(self, user_id, old_title, new_title, description):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE projects
            SET projectName = ?, description = ?
            WHERE userId = ? AND projectName = ?
        ''', (new_title, description, user_id, old_title))
        conn.commit()
        conn.close()

    def get_award_by_title(self, user_id, title):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM awards WHERE userId = ? AND awardName = ?", (user_id, title))
        data = cursor.fetchone()
        conn.close()
        return data

    def update_award_by_title(self, user_id, old_title, new_title, issuer, year):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE awards
            SET awardName = ?, issuer = ?, year = ?
            WHERE userId = ? AND awardName = ?
        ''', (new_title, issuer, year, user_id, old_title))
        conn.commit()
        conn.close()

    def get_certification_by_title(self, user_id, title):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM certifications WHERE userId = ? AND certificateName = ?", (user_id, title))
        data = cursor.fetchone()
        conn.close()
        return data

    def update_certification_by_title(self, user_id, old_title, new_title, issuer, year):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE certifications
            SET certificateName = ?, issuer = ?, year = ?
            WHERE userId = ? AND certificateName = ?
        ''', (new_title, issuer, year, user_id, old_title))
        conn.commit()
        conn.close()


    def get_education_by_title(self, user_id, title):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM education WHERE userId = ? AND degree = ?", (user_id, title))
        data = cursor.fetchone()
        conn.close()
        return data

    def update_education_by_title(self, user_id, old_title, new_title, university, year):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE education
            SET degree = ?, university = ?, graduationYear = ?
            WHERE userId = ? AND degree = ?
        ''', (new_title, university, year, user_id, old_title))
        conn.commit()
        conn.close()





