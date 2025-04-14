# ----------------------------------------------
# Title: userModel.py
# Description: User profile model
# Author(s): Marvin
# Date created: Feb 19, 2025
# Date modified: Mar 8, 2025
# ----------------------------------------------

import sqlite3

class UserModel:
    @staticmethod
    def displayFullDatabase():
        """
        Debugging method to show all tables and their rows in the database.
        Prints column names and each record for every table found.
        """
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        # Fetch the names of all tables in the database.
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # Iterate over each table, print its structure and contents.
        for table in tables:
            tableName = table[0]
            print(f"\nTable: {tableName}")
            cursor.execute(f"SELECT * FROM {tableName};")
            rows = cursor.fetchall()

            # Print the column names for clarity.
            columnNames = [desc[0] for desc in cursor.description]
            print("Columns:", columnNames)

            # Print each row found in the current table.
            for row in rows:
                print(row)

        conn.close()

    @staticmethod
    def getUserById(userId):
        """
        Retrieve the entire user record (row) matching 'userId' from the 'users' table.
        Returns the record as a tuple, or None if not found.
        """
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        # Query for a row in 'users' where the 'id' matches userId.
        cursor.execute('SELECT * FROM users WHERE id = ?', (userId,))
        user = cursor.fetchone()
        conn.close()
        return user

    @staticmethod
    def getUsernameById(userId):
        """
        Retrieve the 'fullName' field for a user with the given 'userId'.
        Returns the full name string if the user exists, else None.
        """
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT fullName FROM users WHERE id = ?', (userId,))
        user = cursor.fetchone()
        conn.close()
        # user is a tuple like ('John Doe',), so return user[0] if it exists.
        return user[0] if user else None

    @staticmethod
    def addUser(username, password, plainPassword, fullName, email, phone, linkedin, location, portfolio):
        """
        Insert a new user record into the 'users' table.
         - username: must be unique (UNIQUE constraint).
         - password: hashed password string (secure).
         - plainPassword: the original, unencrypted password (insecure).
         - fullName, email, phone, etc.: additional personal info.
        Returns the newly inserted user's ID (primary key).
        """
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (username, password, plainPassword, fullName, email, phone, linkedin, location, portfolio)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (username, password, plainPassword, fullName, email, phone, linkedin, location, portfolio))
        conn.commit()
        user_id = cursor.lastrowid  # The ID of the newly inserted row.
        conn.close()
        return user_id

    @staticmethod
    def getUserByUsername(username):
        """
        Return the entire user record (row) for a given username.
        Returns None if no user with that username exists.
        """
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        return user
    
    @staticmethod
    def getUserLocation(userId):
        """
        Return the 'location' field for a user with the given 'userId',
        or None if the user doesn't exist or has no location set.
        """
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT location FROM users WHERE id = ?', (userId,))
        location = cursor.fetchone()
        conn.close()
        # location is a tuple like ('Vancouver, BC',); return the first element if it exists.
        return location[0] if location else None  # Return the location if found

    @staticmethod
    def usernameExists(username):
        """
        Check if a username is already present in the 'users' table.
        Returns True if at least one row has that username, otherwise False.
        """
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        # Count how many rows in 'users' have the matching username.
        cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', (username,))
        count = cursor.fetchone()[0]
        conn.close()
        return (count > 0)

    @staticmethod
    def updateUser(userId, username, password, plainPassword, fullName, email, phone, linkedin, location, portfolio):
        """
        Update an existing user record's fields in the 'users' table.
         - userId: primary key for the user being updated.
         - username: the new or existing username (must be unique overall).
         - password: the hashed password.
         - plainPassword: the unencrypted password (insecure).
         - fullName, email, phone, etc.: additional personal fields to be updated.
        Prints a success message upon completion.
        """
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users
            SET username = ?, password = ?, plainPassword = ?, fullName = ?, email = ?, phone = ?, linkedin = ?, location = ?, portfolio = ?
            WHERE id = ?
        ''', (username, password, plainPassword, fullName, email, phone, linkedin, location, portfolio, userId))
        conn.commit()
        conn.close()
        print("User profile updated successfully.")

    ######### NEW METHOD: DELETE USER #########
    @staticmethod
    def deleteUserById(userId):
        """
        Permanently remove the user record with the given 'userId' from the 'users' table.
        Prints a confirmation message.
        """
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (userId,))
        conn.commit()
        conn.close()
        print(f"User with ID {userId} deleted from the database.")
