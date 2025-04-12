# ----------------------------------------------
# Title: userController.py
# Description: User profile controller
# Author(s): Jasmine
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
                # We want to hash the new password if the user changed it
                hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                UserModel.updateUser(
                    userId, userName, hashed_pw, password, fullName, email, phone,
                    linkedin, location, portfolio
                )
            else:
                hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                UserModel.addUser(
                    userName, hashed_pw, password, fullName, email, phone,
                    linkedin, location, portfolio
                )
        
            return redirect(url_for('index'))

        # If GET and userId is provided, fetch the user details for editing
        user = None
        if userId:
            user = UserModel.getUserById(userId)
        return render_template('profile.html', user=user)

    @staticmethod
    def login(userId):
        """
        Old method that logs in user 1 or 2 by ID. 
        Possibly unused now, if you have a real login with username/password.
        """
        session['userId'] = userId
        return redirect(url_for('index'))
    
    @staticmethod
    def signUp(full_name, email, phone, username, password):
        """
        Creates a new user after checking:
         - username availability
         - password complexity (≥12 chars, 1 uppercase, 1 special char)
         - hashed password stored in DB
        """
        # 1) Check if username is already in use
        if UserModel.usernameExists(username):
            flash("Username is already taken, please choose another one.")
            return redirect(url_for('signUp'))

        # 2) Validate password complexity
        pattern = r'^(?=.*[A-Z])(?=.*[^a-zA-Z0-9]).{12,}$'
        if not re.match(pattern, password):
            flash("Password must be at least 12 characters, include an uppercase letter, and contain at least one special character.")
            return redirect(url_for('signUp'))

        # 3) Hash the password before storing
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # 4) Create user in the database
        new_user_id = UserModel.addUser(
            username, hashed_pw, password, full_name, email, phone, '', '', ''
        )
        session['userId'] = new_user_id

        return redirect(url_for('index'))
    

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
        # Clear the user ID from session
        session.pop('userId', None)
        return redirect(url_for('login'))
    
    @staticmethod
    def viewProfile():
        """
        Displays entire DB for debugging, then shows user profile page if logged in.
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
        Checks user by username, compares hashed password.
        If valid, returns user ID; otherwise None.
        """
        user = UserModel.getUserByUsername(username)
        if not user:
            return None  # user not found

        stored_password = user[2]  # hashed password in DB
        # Compare using bcrypt
        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            return user[0]
        else:
            return None

    @staticmethod
    def updateProfile():
        """
        Called from the /profile POST if the user is editing profile info.
        Allows updating both hashed & plain password with same complexity rules as signUp.
        """
        if 'userId' not in session:
            return redirect(url_for('login'))
        
        userId = session['userId']
        user = UserModel.getUserById(userId)
        
        if request.method == 'POST':
            fullName = request.form['full-name']
            username = request.form['user-name']
            phone = request.form['phone']
            email = request.form['email']
            location = request.form['location']
            linkedin = request.form.get('linkedin', '')
            portfolio = request.form.get('portfolio', '')

            # The new password typed by user in the form
            new_password = request.form['password']

            # If the user typed something different than the old plain password, we validate it:
            if new_password != user[9]:  # user[9] is the old plainPassword
                # Apply the same complexity checks
                pattern = r'^(?=.*[A-Z])(?=.*[^a-zA-Z0-9]).{12,}$'
                if not re.match(pattern, new_password):
                    flash("Password must be at least 12 characters, include an uppercase letter, and contain at least one special character.")
                    return redirect(url_for('profile'))

                # If valid, hash the new password
                hashed_pw = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            else:
                # If no change, keep the existing hashed password
                hashed_pw = user[2]  # old hashed password
                new_password = user[9]  # keep the same plain

            UserModel.updateUser(
                userId, 
                username,
                hashed_pw,        # hashed password
                new_password,     # plain password
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
    def signUpTemp(full_name, email, phone, username, password): # to be used to create data in initDb
        """
        Creates a new user after checking:
         - hashed password stored in DB
         - also storing plain password for simulation
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
        Permanently delete this user from the DB if authorized,
        then log them out.
        """
        if 'userId' not in session or session['userId'] != userId:
            flash("Unauthorized to delete this user.")
            return redirect(url_for('login'))

        UserModel.deleteUserById(userId)
        session.pop('userId', None)
        flash("Your account has been deleted.")
        return redirect(url_for('login'))
