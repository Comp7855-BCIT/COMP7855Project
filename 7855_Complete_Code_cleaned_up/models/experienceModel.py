# ----------------------------------------------
# Title: expirenceModel.py
# Description: Experience of user (work, education, project...) model
# Author(s): Gurp
# Date created: Mar 8, 2025
# Date modified: Mar 8, 2025
# ----------------------------------------------

import sqlite3

class ExperienceModel:
    # Work, Volunteer, Project, Award, Certificate, Education
    # similar to job model
    # below are example functions

    def __init__(self, db_path='database.db'):
        # Store the database path so we can use it later to connect
        self.db_path = db_path

    def connect(self):
        """Connect to the database and return the connection object."""
        return sqlite3.connect(self.db_path)
    
    
    def add_experience(self, user_id, category, title, organization, start_date, end_date, description):
        """
        Insert a new experience record for the user in the appropriate table
        based on the category of the experience.
        
        Parameters:
         - user_id: the ID of the user.
         - category: one of ['Work', 'Volunteer', 'Project', 'Award', 'Certificate', 'Education'].
         - title: Title for work/volunteer/project or the name for Award/Certificate/Education.
         - organization: Company name or institution (for work, volunteer, etc.).
         - start_date, end_date: Dates representing the period of the experience.
         - description: A description of responsibilities or details.
        """
        conn = self.connect()
        cursor = conn.cursor()

        # Mapping from experience category to corresponding SQL INSERT statement.
        query_map = {
            'Work': "INSERT INTO workExperience (userId, jobTitle, company, startDate, endDate, responsibilities) VALUES (?, ?, ?, ?, ?, ?)",
            'Volunteer': "INSERT INTO volunteerExperience (userId, role, organization, description) VALUES (?, ?, ?, ?)",
            'Project': "INSERT INTO projects (userId, projectName, description) VALUES (?, ?, ?)",
            'Award': "INSERT INTO awards (userId, awardName, issuer, year) VALUES (?, ?, ?, ?)",
            'Certificate': "INSERT INTO certifications (userId, certificateName, issuer, year) VALUES (?, ?, ?, ?)",
            'Education': "INSERT INTO education (userId, degree, university, graduationYear) VALUES (?, ?, ?, ?)"
        }

        # Get the appropriate SQL query for the given category.
        query = query_map.get(category)
        if query:
            # Depending on the category, prepare the values tuple.
            if category in ['Work']:
                # For Work, use title, organization as company, start_date, end_date, and description as responsibilities.
                values = (user_id, title, organization, start_date, end_date, description)
            elif category in ['Volunteer']:
                # For Volunteer, use title (as role), organization, and description.
                values = (user_id, title, organization, description)
            elif category in ['Project']:
                # For Project, no organization column is provided.
                values = (user_id, title, description)
            elif category in ['Award', 'Certificate', 'Education']:
                # For Award, Certificate, or Education, use title, organization (issuer/university) and start_date (year or graduationYear)
                values = (user_id, title, organization, start_date)
            else:
                # Fallback if category not explicitly set.
                values = (user_id, title, organization, start_date, end_date, description)

        # Execute the appropriate INSERT query with the given values.
        cursor.execute(query, values)
        conn.commit()
        conn.close()
        
    
    def get_experiences(self, user_id):
        """
        Fetch all experiences for a given user.
        Iterates through each category and retrieves a list of titles (or names) for that category.
        
        Returns a dictionary with keys: 'Work', 'Volunteer', 'Project', 'Award', 'Certificate', 'Education'.
        Each key maps to a list of experience titles (or degrees, etc.) for that user.
        """
        conn = self.connect()
        cursor = conn.cursor()

        # Define the list of experience categories.
        categories = ["Work", "Volunteer", "Project", "Award", "Certificate", "Education"]
        experience_data = {}

        # Map each category to its corresponding table and column name.
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

            # For each category, select the appropriate column from the corresponding table.
            cursor.execute(f"SELECT {column_map[category]} FROM {table_map[category]} WHERE userId = ?", (user_id,))
            # Store the first column of each fetched row in the dictionary.
            experience_data[category] = [row[0] for row in cursor.fetchall()]

        conn.close()
        return experience_data 


    @staticmethod
    def updateExperience():
        """
        Placeholder for updating a user experience.
        Currently not implemented.
        """
        pass

    def delete_experience(self, user_id, category, title):
        """
        Delete an experience entry for a user from the appropriate table.
        
        Parameters:
         - user_id: the ID of the user.
         - category: category of the experience (e.g., "Work", "Volunteer", etc.).
         - title: the title of the experience (column value varies per category).
        
        Maps the category to the corresponding table and column, then deletes the matching record.
        """
        conn = self.connect()
        cursor = conn.cursor()

        # Define mapping from category to table and column name.
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

        # If the category exists in our mapping, execute the DELETE query.
        if category in table_map:
            cursor.execute(f"DELETE FROM {table_map[category]} WHERE userId = ? AND {column_map[category]} = ?", (user_id, title))
            conn.commit()

        conn.close()

    def get_work_by_title(self, user_id, title):
        """
        Retrieve a work experience record for a given user by job title.
        
        Returns the matching row from the workExperience table, or None if not found.
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM workExperience WHERE userId = ? AND jobTitle = ?', (user_id, title))
        data = cursor.fetchone()
        conn.close()
        return data

    def update_work_experience_by_title(self, user_id, title, company, start, end, location, responsibilities):
        """
        Updates an existing work experience based on the job title.
        
        Parameters:
          - user_id: the ID of the user.
          - title: the job title to identify which record to update.
          - company, start, end, location, responsibilities: new values.
        """
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
        """
        Retrieve a volunteer experience record for a given user by role.
        
        Returns the matching row from the volunteerExperience table, or None if not found.
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM volunteerExperience WHERE userId = ? AND role = ?", (user_id, title))
        data = cursor.fetchone()
        conn.close()
        return data

    def update_volunteer_experience_by_title(self, user_id, old_title, new_title, organization, description):
        """
        Updates a volunteer experience for the user based on the role.
        
        Parameters:
          - old_title: the current role stored in the database.
          - new_title: the new role to update.
          - organization and description: updated details.
        """
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
        """
        Retrieve a project record for a given user based on the project name.
        
        Returns the matching project row or None if not found.
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects WHERE userId = ? AND projectName = ?", (user_id, title))
        data = cursor.fetchone()
        conn.close()
        return data

    def update_project_by_title(self, user_id, old_title, new_title, description):
        """
        Updates a project record for a user based on the project name.
        
        Parameters:
          - old_title: the current project name.
          - new_title: the new project name.
          - description: updated project description.
        """
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
        """
        Retrieve an award record for the user based on the award name.
        Returns the matching row or None if no match is found.
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM awards WHERE userId = ? AND awardName = ?", (user_id, title))
        data = cursor.fetchone()
        conn.close()
        return data

    def update_award_by_title(self, user_id, old_title, new_title, issuer, year):
        """
        Updates an award record for the user by matching on the award name.
        
        Parameters:
          - old_title: the current award name.
          - new_title: the updated award name.
          - issuer and year: updated award details.
        """
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
        """
        Retrieve a certification record for a given user based on the certificate name.
        Returns the matching row or None if not found.
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM certifications WHERE userId = ? AND certificateName = ?", (user_id, title))
        data = cursor.fetchone()
        conn.close()
        return data

    def update_certification_by_title(self, user_id, old_title, new_title, issuer, year):
        """
        Updates a certification record by matching the certificate name.
        
        Parameters:
          - old_title: the current certificate name.
          - new_title: the updated certificate name.
          - issuer and year: updated details.
        """
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
        """
        Retrieve an education record for the user based on the degree.
        Returns the matching record as a tuple or None if not found.
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM education WHERE userId = ? AND degree = ?", (user_id, title))
        data = cursor.fetchone()
        conn.close()
        return data

    def update_education_by_title(self, user_id, old_title, new_title, university, year):
        """
        Updates an education record by matching on the degree.
        
        Parameters:
          - old_title: the current degree.
          - new_title: the updated degree.
          - university and year: updated education details.
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE education
            SET degree = ?, university = ?, graduationYear = ?
            WHERE userId = ? AND degree = ?
        ''', (new_title, university, year, user_id, old_title))
        conn.commit()
        conn.close()
