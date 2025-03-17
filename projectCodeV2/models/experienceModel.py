# ----------------------------------------------
# Title: expirenceModel.py
# Description: Expirence of user (work, education, project...) model
# Author(s): 
# Date created: Mar 8, 2025
# Date modified: Mar 8, 2025
# ----------------------------------------------
# experienceModel.py
import sqlite3

class ExperienceModel:

    @staticmethod
    def addWork(userId, title, company, location, startDate, endDate, responsibilities):
        """
        Inserts a record into the workExperience table.
        """
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO workExperience (userId, jobTitle, company, location, startDate, endDate, responsibilities)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (userId, title, company, location, startDate, endDate, responsibilities))
        conn.commit()
        conn.close()

    @staticmethod
    def addVolunteer(userId, role, organization, description):
        """
        Inserts a record into the volunteerExperience table.
        """
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO volunteerExperience (userId, role, organization, description)
            VALUES (?, ?, ?, ?)
        ''', (userId, role, organization, description))
        conn.commit()
        conn.close()

    @staticmethod
    def addProject(userId, projectName, technologies, description, impact):
        """
        Inserts a record into the projects table.
        """
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO projects (userId, projectName, technologies, description, impact)
            VALUES (?, ?, ?, ?, ?)
        ''', (userId, projectName, technologies, description, impact))
        conn.commit()
        conn.close()

    @staticmethod
    def addAward(userId, awardName, issuer, year):
        """
        Inserts a record into the awards table.
        """
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO awards (userId, awardName, issuer, year)
            VALUES (?, ?, ?, ?)
        ''', (userId, awardName, issuer, year))
        conn.commit()
        conn.close()

    @staticmethod
    def addCertification(userId, certName, issuer, year):
        """
        Inserts a record into the certifications table.
        """
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO certifications (userId, certificateName, issuer, year)
            VALUES (?, ?, ?, ?)
        ''', (userId, certName, issuer, year))
        conn.commit()
        conn.close()

    @staticmethod
    def addEducation(userId, degree, university, graduationYear):
        """
        Inserts a record into the education table.
        """
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO education (userId, degree, university, graduationYear)
            VALUES (?, ?, ?, ?)
        ''', (userId, degree, university, graduationYear))
        conn.commit()
        conn.close()

    @staticmethod
    def getAllExperiencesForUser(userId):
        """
        Returns a dictionary containing combined text summaries of the user's
        experiences from each category.
        """
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Work Experience
        cursor.execute("SELECT jobTitle, company, startDate, endDate, responsibilities FROM workExperience WHERE userId = ?", (userId,))
        work_experiences = cursor.fetchall()

        # Volunteer Experience
        cursor.execute("SELECT role, organization, description FROM volunteerExperience WHERE userId = ?", (userId,))
        volunteer_experiences = cursor.fetchall()

        # Projects
        cursor.execute("SELECT projectName, description, technologies, impact FROM projects WHERE userId = ?", (userId,))
        projects = cursor.fetchall()

        # Awards
        cursor.execute("SELECT awardName, issuer, year FROM awards WHERE userId = ?", (userId,))
        awards = cursor.fetchall()

        # Certifications
        cursor.execute("SELECT certificateName, issuer, year FROM certifications WHERE userId = ?", (userId,))
        certifications = cursor.fetchall()

        # Education
        cursor.execute("SELECT degree, university, graduationYear FROM education WHERE userId = ?", (userId,))
        education = cursor.fetchall()

        conn.close()

        return {
            "work": work_experiences,
            "volunteer": volunteer_experiences,
            "project": projects,
            "award": awards,
            "certificate": certifications,
            "education": education,
        }
