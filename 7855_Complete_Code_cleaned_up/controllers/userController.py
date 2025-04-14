# ----------------------------------------------
# Title: userController.py
# Description: User profile controller
# Author(s): Marvin
# Date created: Feb 28, 2025
# Date modified: Mar 8, 2025
# ----------------------------------------------

import re
import bcrypt
from flask import session, redirect, url_for, render_template, request, flash
from models.userModel import UserModel

class UserController:

    @staticmethod
    def userProfile(userId):
        # If the request method is POST, update or create the user profile
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
                # When updating, hash the new password if it has changed
                hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                # Update user profile in the database
                UserModel.updateUser(
                    userId, userName, hashed_pw, password, fullName, email, phone,
                    linkedin, location, portfolio
                )
            else:
                # For a new user, hash the password and create the user record
                hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                UserModel.addUser(
                    userName, hashed_pw, password, fullName, email, phone,
                    linkedin, location, portfolio
                )
        
            # After update/creation, redirect to the main page
            return redirect(url_for('index'))

        # For GET requests, fetch the current user details (if available)
        user = None
        if userId:
            user = UserModel.getUserById(userId)
        return render_template('profile.html', user=user)

    @staticmethod
    def login(userId):
        """
        Legacy login method that assigns the given userId to session.
        """
        session['userId'] = userId
        return redirect(url_for('index'))
    
    @staticmethod
    def signUp(full_name, email, phone, username, password):
        """
        Creates a new user by checking username availability and password complexity,
        then stores the hashed and plain password in the database.
        """
        # Check if the username is already in use
        if UserModel.usernameExists(username):
            flash("Username is already taken, please choose another one.")
            return redirect(url_for('signUp'))

        # Validate password complexity using a regex pattern
        pattern = r'^(?=.*[A-Z])(?=.*[^a-zA-Z0-9]).{12,}$'
        if not re.match(pattern, password):
            flash("Password must be at least 12 characters, include an uppercase letter, and contain at least one special character.")
            return redirect(url_for('signUp'))

        # Hash the password for secure storage
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Create the user record in the database
        new_user_id = UserModel.addUser(
            username, hashed_pw, password, full_name, email, phone, '', '', ''
        )
        session['userId'] = new_user_id

        return redirect(url_for('index'))
    
    @staticmethod
    def getCurrentUser():
        # Returns the current user record from the database if logged in; otherwise, returns None.
        if 'userId' in session:
            userId = session['userId']
            return UserModel.getUserById(userId)
        return None

    @staticmethod
    def getCurrentUsername():
        # Returns the current user's fullName from the database if logged in; otherwise, returns None.
        if 'userId' in session:
            userId = session['userId']
            return UserModel.getUsernameById(userId)
        return None

    @staticmethod
    def signout():
        # Logs out the current user by removing 'userId' from the session.
        session.pop('userId', None)
        return redirect(url_for('login'))
    
    @staticmethod
    def viewProfile():
        """
        Displays the user profile page after printing the full database (for debugging).
        Only works if the user is logged in.
        """
        UserModel.displayFullDatabase()
        if 'userId' not in session:
            return redirect(url_for('login'))
        
        userId = session['userId']
        user = UserModel.getUserById(userId)
        return render_template('profile.html', user=user)

    @staticmethod
    def validateLogin(username, password):
        """
        Validates the user login by comparing the provided password against the stored hashed password.
        Returns the user ID if the login is valid, or None if invalid.
        """
        user = UserModel.getUserByUsername(username)
        if not user:
            return None  # User not found

        stored_password = user[2]  # Assuming hashed password is at index 2
        # Use bcrypt to compare passwords
        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            return user[0]
        else:
            return None

    # For updating the user profile
    @staticmethod
    def updateProfile():
        """
        Updates the user profile based on form input.
        Compares the new plain password with the stored plain password; if changed,
        validates complexity and updates both the hashed and plain passwords.
        """
        if 'userId' not in session:
            return redirect(url_for('login'))
        
        userId = session['userId']
        user = UserModel.getUserById(userId)
        
        if request.method == 'POST':
            # Parse form data
            fullName = request.form['full-name']
            username = request.form['user-name']
            phone = request.form['phone']
            email = request.form['email']
            location = request.form['location']
            linkedin = request.form.get('linkedin', '')
            portfolio = request.form.get('portfolio', '')

            # Get the new plain password from form input
            new_password = request.form['password']

            # If the new password differs from the stored plain password, validate and update
            if new_password != user[9]:  # Assuming plain password is at index 9
                pattern = r'^(?=.*[A-Z])(?=.*[^a-zA-Z0-9]).{12,}$'
                if not re.match(pattern, new_password):
                    flash("Password must be at least 12 characters, include an uppercase letter, and contain at least one special character.")
                    return redirect(url_for('profile'))

                # Hash the new password
                hashed_pw = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            else:
                # If unchanged, keep the existing hashed and plain password
                hashed_pw = user[2]
                new_password = user[9]

            # Update the user record with the new values
            UserModel.updateUser(
                userId, 
                username,
                hashed_pw,        # updated hashed password
                new_password,     # updated plain password
                fullName,
                email,
                phone,
                linkedin,
                location,
                portfolio
            )
            return redirect(url_for('profile'))
        
        return redirect(url_for('profile'))

    @staticmethod
    def signUpTemp(full_name, email, phone, username, password):  # to be used to create data in initDb
        """
        Creates a new user (for simulation purposes) by hashing the password and storing both values.
        """
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_result = bcrypt.hashpw(password_bytes, salt)
        if isinstance(hashed_result, bytes):
            hashed_pw = hashed_result.decode('utf-8')
        else:
            hashed_pw = hashed_result

        new_user_id = UserModel.addUser(
            username, hashed_pw, password, full_name, email, phone, '', '', ''
        )
        return new_user_id

    ######### NEW METHOD: DELETE ACCOUNT #########
    @staticmethod
    def deleteAccount(userId):
        """
        Permanently deletes the user from the database if the logged-in user matches.
        Logs the user out after deletion and flashes a confirmation message.
        """
        if 'userId' not in session or session['userId'] != userId:
            flash("Unauthorized to delete this user.")
            return redirect(url_for('login'))

        # Delete the user from the database using the model method.
        UserModel.deleteUserById(userId)
        # Remove the user from session.
        session.pop('userId', None)
        flash("Your account has been deleted.")
        return redirect(url_for('login'))
