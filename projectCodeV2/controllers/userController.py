# ----------------------------------------------
# Title: userController.py
# Description: User profile controller
# Author(s): Jasmine 
# Date created: Feb 28, 2025
# Date modified: Mar 8, 2025
# ----------------------------------------------
from flask import session, redirect, url_for, render_template, request
from models.userModel import UserModel

class UserController:

    @staticmethod
    def userProfile(userId):
        if request.method == 'POST':
            # Parse incoming form data
            fullName = request.form['full-name']
            userName = request.form['user-name']
            password = request.form['password']
            phone = request.form['phone']
            email = request.form['email']
            location = request.form['location']
            linkedin = request.form['linkedin']
            portfolio = request.form['portfolio']

            if userId:
                # Update the existing job
                UserModel.updateUser(userId, userName, password, fullName, email, phone, linkedin, location, portfolio)
            else:
                # Create a new user
                UserModel.addUser(userId, userName, password, fullName, email, phone, linkedin, location, portfolio)
        
            # Redirect to the main page (index)
            return redirect(url_for('index'))

        # If userId is provided, fetch the user details for editing
        user = None
        if userId:
            user = UserModel.getUserById(userId)

        return render_template('profile.html', user=user)

    @staticmethod
    def login(userId): #<-- have to update this (currently works with 2 buttons for 2 users)
        session['userId'] = userId
        return redirect(url_for('index'))
    
    @staticmethod
    def signUp(): #<-- can use UserModel.addUser to create new user
        pass

    @staticmethod
    def getCurrentUser():
        if 'userId' in session:
            userId = session['userId']
            return UserModel.getUserById(userId)
        return None

    @staticmethod
    def getCurrentUsername():
        if 'userId' in session:
            userId = session['userId']
            return UserModel.getUsernameById(userId)
        return None

    @staticmethod
    def signout():
        # Clear the user ID from the session
        session.pop('userId', None)
        return redirect(url_for('login'))
    
    @staticmethod
    def viewProfile():
        UserModel.displayFullDatabase()
        if 'userId' not in session:
            return redirect(url_for('login'))
        
        userId = session['userId']
        user = UserModel.getUserById(userId)
        return render_template('profile.html', user=user)

    @staticmethod
    def updateProfile():
        if 'userId' not in session:
            return redirect(url_for('login'))
        
        userId = session['userId']
        
        if request.method == 'POST':
            # Parse form data
            fullName = request.form['full-name']
            username = request.form['user-name']
            password = request.form['password']
            phone = request.form['phone']
            email = request.form['email']
            location = request.form['location']
            linkedin = request.form.get('linkedin', '')
            portfolio = request.form.get('portfolio', '')
            
            # Update the user in the database
            UserModel.updateUser(
                userId, username, password, fullName, email, phone, linkedin, location, portfolio
            )
            return redirect(url_for('profile'))
        
        return redirect(url_for('profile'))