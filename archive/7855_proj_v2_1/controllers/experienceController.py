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
