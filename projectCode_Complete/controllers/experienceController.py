# ----------------------------------------------
# Title: expirenceController.py
# Description: Expirence of user (work, education, project...) controller
# Author(s): 
# Date created: Mar 8, 2025
# Date modified: Mar 8, 2025
# ----------------------------------------------
from flask import render_template, jsonify, session, request, redirect, url_for, flash
from models.experienceModel import ExperienceModel


class ExperienceController:
    @staticmethod
    def new_experience():
        """Handles adding a new experience"""
        if 'userId' not in session:
            return redirect(url_for('login'))

        experience_model = ExperienceModel()
        user_id = session['userId']

        if request.method == 'POST':
            category = request.form.get('category')
            title = request.form.get('title')
            organization = request.form.get('organization')
            start_date = request.form.get('start-date')
            end_date = request.form.get('end-date')
            description = request.form.get('description')

            if not description:  # Handle missing description
                description = ""

            experience_model.add_experience(user_id, category, title, organization, start_date, end_date, description)

        return render_template('newExperience.html')

    @staticmethod
    def get_experiences():
        """Returns all user experiences as JSON"""
        if 'userId' not in session:
            return jsonify({})

        experience_model = ExperienceModel()
        user_id = session['userId']
        experiences = experience_model.get_experiences(user_id)
        return jsonify(experiences)

    @staticmethod
    def delete_experience():
        """Handles deleting an experience"""
        if 'userId' not in session:
            return jsonify({'success': False})

        data = request.get_json()
        category = data.get('category')
        title = data.get('title')
        user_id = session['userId']

        experience_model = ExperienceModel()
        experience_model.delete_experience(user_id, category, title)

        return jsonify({'success': True})
    
    @staticmethod
    def editWorkByTitle(title):
        if 'userId' not in session:
            return redirect(url_for('login'))

        user_id = session['userId']
        experience_model = ExperienceModel()

        if request.method == 'POST':
            title = request.form['work-title']
            company = request.form['work-company']
            start_date = request.form['start-date']
            end_date = request.form['end-date']
            location = request.form['work-location']
            responsibilities = request.form['work-responsibilities']

            experience_model.update_work_experience_by_title(user_id, title, company, start_date, end_date, location, responsibilities)
            return redirect(url_for('newExperience'))

        work_data = experience_model.get_work_by_title(user_id, title)
        return render_template('newWork.html', work=work_data)

    @staticmethod
    def editVolunteerByTitle(title):
        if 'userId' not in session:
            return redirect(url_for('login'))
        user_id = session['userId']
        experience_model = ExperienceModel()

        if request.method == 'POST':
            # Get updated data from the form
            new_title = request.form.get('volunteer-title')  # volunteer role/title
            organization = request.form.get('volunteer-organization')
            description = request.form.get('volunteer-description')

            # Update the volunteer experience in the database
            experience_model.update_volunteer_experience_by_title(user_id, title, new_title, organization, description)
            return redirect(url_for('newExperience'))

        # GET: Retrieve the existing volunteer record by title
        volunteer_data = experience_model.get_volunteer_by_title(user_id, title)
        return render_template('newVolunteer.html', volunteer=volunteer_data)

    @staticmethod
    def editProjectByTitle(title):
        if 'userId' not in session:
            return redirect(url_for('login'))

        user_id = session['userId']
        experience_model = ExperienceModel()

        if request.method == 'POST':
            new_title = request.form.get('project-title')
            description = request.form.get('project-description')

            experience_model.update_project_by_title(user_id, title, new_title, description)
            return redirect(url_for('newExperience'))

        project_data = experience_model.get_project_by_title(user_id, title)
        return render_template('newProject.html', project=project_data)
    
    @staticmethod
    def editAwardByTitle(title):
        if 'userId' not in session:
            return redirect(url_for('login'))

        user_id = session['userId']
        experience_model = ExperienceModel()

        if request.method == 'POST':
            new_title = request.form.get('award-title')
            issuer = request.form.get('award-issuer')
            year = request.form.get('award-year')

            experience_model.update_award_by_title(user_id, title, new_title, issuer, year)
            return redirect(url_for('newExperience'))

        award_data = experience_model.get_award_by_title(user_id, title)
        return render_template('newAward.html', award=award_data)
    
    @staticmethod
    def editCertificationByTitle(title):
        if 'userId' not in session:
            return redirect(url_for('login'))

        user_id = session['userId']
        experience_model = ExperienceModel()

        if request.method == 'POST':
            new_title = request.form.get('certificate-title')
            issuer = request.form.get('certificate-issuer')
            year = request.form.get('certificate-year')

            experience_model.update_certification_by_title(user_id, title, new_title, issuer, year)
            return redirect(url_for('newExperience'))

        cert_data = experience_model.get_certification_by_title(user_id, title)
        return render_template('newCertification.html', certification=cert_data)

    @staticmethod
    def editEducationByTitle(title):
        if 'userId' not in session:
            return redirect(url_for('login'))

        user_id = session['userId']
        experience_model = ExperienceModel()

        if request.method == 'POST':
            new_title = request.form.get('education-degree')
            university = request.form.get('education-university')
            year = request.form.get('education-year')

            experience_model.update_education_by_title(user_id, title, new_title, university, year)
            return redirect(url_for('newExperience'))

        education_data = experience_model.get_education_by_title(user_id, title)
        return render_template('newEducation.html', education=education_data)



