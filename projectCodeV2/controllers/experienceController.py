# ----------------------------------------------
# Title: expirenceController.py
# Description: Expirence of user (work, education, project...) controller
# Author(s): 
# Date created: Mar 8, 2025
# Date modified: Mar 8, 2025
# ----------------------------------------------
# experienceController.py
from flask import render_template, request, redirect, url_for, session
from models.experienceModel import ExperienceModel

class ExperienceController:

    @staticmethod
    def addWork():
        """
        Called by /newWork route (POST).
        Gathers form data, calls experienceModel.addWork(...), then redirect.
        """
        if 'userId' not in session:
            return redirect(url_for('login'))
        userId = session['userId']

        # parse form fields (matching newWork.html)
        title = request.form.get('work-title')
        company = request.form.get('work-company')
        location = request.form.get('work-location', '')
        startDate = request.form.get('start-date')
        endDate = request.form.get('end-date')
        responsibilities = request.form.get('work-responsibilities')

        ExperienceModel.addWork(userId, title, company, location, startDate, endDate, responsibilities)
        return redirect(url_for('newExperience'))

    @staticmethod
    def addVolunteer():
        if 'userId' not in session:
            return redirect(url_for('login'))
        userId = session['userId']

        role = request.form.get('volunteer-role')
        org = request.form.get('volunteer-organization')
        desc = request.form.get('volunteer-description')

        ExperienceModel.addVolunteer(userId, role, org, desc)
        return redirect(url_for('newExperience'))

    @staticmethod
    def addProject():
        if 'userId' not in session:
            return redirect(url_for('login'))
        userId = session['userId']

        name = request.form.get('project-name')
        tech = request.form.get('project-technologies')
        desc = request.form.get('project-description')
        # note the 'project-impact' is optional
        impact = request.form.get('project-impact', '')

        ExperienceModel.addProject(userId, name, tech, desc, impact)
        return redirect(url_for('newExperience'))

    @staticmethod
    def addAward():
        if 'userId' not in session:
            return redirect(url_for('login'))
        userId = session['userId']

        awardName = request.form.get('award-name')
        issuer = request.form.get('award-issuer')
        year = request.form.get('award-year')

        ExperienceModel.addAward(userId, awardName, issuer, year)
        return redirect(url_for('newExperience'))

    @staticmethod
    def addCertification():
        if 'userId' not in session:
            return redirect(url_for('login'))
        userId = session['userId']

        certName = request.form.get('certification-name')
        issuer = request.form.get('certification-issuer')
        year = request.form.get('certification-year')

        ExperienceModel.addCertification(userId, certName, issuer, year)
        return redirect(url_for('newExperience'))

    @staticmethod
    def addEducation():
        if 'userId' not in session:
            return redirect(url_for('login'))
        userId = session['userId']

        degree = request.form.get('education-degree')
        univ = request.form.get('education-university')
        gradYear = request.form.get('education-year')

        ExperienceModel.addEducation(userId, degree, univ, gradYear)
        return redirect(url_for('newExperience'))
    
    @staticmethod
    def getAllExperiencesForUser(userId):
        """
        Returns a single string summarizing user experience 
        from all tables: work, volunteer, project, award, etc.
        """
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Summaries
        lines = []

        # 1) Work
        cursor.execute("SELECT jobTitle, company, startDate, endDate, responsibilities FROM workExperience WHERE userId = ?", (userId,))
        works = cursor.fetchall()
        if works:
            lines.append("Work Experience:")
            for w in works:
                lines.append(f" - {w[0]} at {w[1]}, {w[2]} to {w[3]}\n   Responsibilities: {w[4]}")

        # 2) Volunteer
        cursor.execute("SELECT role, organization, description FROM volunteerExperience WHERE userId = ?", (userId,))
        vols = cursor.fetchall()
        if vols:
            lines.append("Volunteer Experience:")
            for v in vols:
                lines.append(f" - {v[0]} at {v[1]}\n   {v[2]}")

        # 3) Projects
        cursor.execute("SELECT projectName, description, technologies, impact FROM projects WHERE userId = ?", (userId,))
        projs = cursor.fetchall()
        if projs:
            lines.append("Projects:")
            for p in projs:
                lines.append(f" - {p[0]}: {p[1]}\n   Tech: {p[2]}, Impact: {p[3]}")

        # 4) Awards
        cursor.execute("SELECT awardName, issuer, year FROM awards WHERE userId = ?", (userId,))
        awards = cursor.fetchall()
        if awards:
            lines.append("Awards:")
            for a in awards:
                lines.append(f" - {a[0]} from {a[1]} in {a[2]}")

        # 5) Certifications
        cursor.execute("SELECT certificateName, issuer, year FROM certifications WHERE userId = ?", (userId,))
        certs = cursor.fetchall()
        if certs:
            lines.append("Certifications:")
            for c in certs:
                lines.append(f" - {c[0]} from {c[1]} in {c[2]}")

        # 6) Education
        cursor.execute("SELECT degree, university, graduationYear FROM education WHERE userId = ?", (userId,))
        edus = cursor.fetchall()
        if edus:
            lines.append("Education:")
            for e in edus:
                lines.append(f" - {e[0]} from {e[1]} (graduated {e[2]})")

        conn.close()

        # Join everything into one big text
        # If there's no experience at all, lines might be []
        final_text = "\n".join(lines)
        return final_text

