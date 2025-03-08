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
        # Connect to the SQLite database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Get a list of all tables in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # Loop through each table and display its content
        for table in tables:
            tableName = table[0]
            print(f"\nTable: {tableName}")
        
            # Get all rows from the table
            cursor.execute(f"SELECT * FROM {tableName};")
            rows = cursor.fetchall()
        
            # Get column names
            columnNames = [description[0] for description in cursor.description]
            print("Columns:", columnNames)
        
            # Print all rows
            for row in rows:
                print(row)

        # Close the connection
        conn.close()

    @staticmethod
    def getUserById(userId):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (userId,))
        user = cursor.fetchone()
        conn.close()
        return user

    @staticmethod
    def getUsernameById(userId):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT username FROM users WHERE id = ?', (userId,))
        user = cursor.fetchone()
        conn.close()
        return user[0] if user else None

    @staticmethod
    def addUser(username, password, fullName, email, phone, linkedin, location, portfolio): 
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (username, password, fullName, email, phone, linkedin, location, portfolio)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (username, password, fullName, email, phone, linkedin, location, portfolio))
        conn.commit()
        conn.close()

    @staticmethod
    def updateUser(userId, username, password, fullName, email, phone, linkedin, location, portfolio):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users
            SET username = ?, password = ?, fullName = ?, email = ?, phone = ?, linkedin = ?, location = ?, portfolio = ?
            WHERE id = ?
        ''', (username, password, fullName, email, phone, linkedin, location, portfolio, userId))
        conn.commit()
        conn.close()
        print("User profile updated successfully.")