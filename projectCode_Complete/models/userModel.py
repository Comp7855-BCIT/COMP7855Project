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
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        for table in tables:
            tableName = table[0]
            print(f"\nTable: {tableName}")
            cursor.execute(f"SELECT * FROM {tableName};")
            rows = cursor.fetchall()
            columnNames = [desc[0] for desc in cursor.description]
            print("Columns:", columnNames)
            for row in rows:
                print(row)
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
        cursor.execute('SELECT fullName FROM users WHERE id = ?', (userId,))
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
        user_id = cursor.lastrowid
        conn.close()
        return user_id

    @staticmethod
    def getUserByUsername(username):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        return user
    
    @staticmethod
    def getUserLocation(userId):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT location FROM users WHERE id = ?', (userId,))
        location = cursor.fetchone()
        conn.close()
        return location[0] if location else None  # Return the location if found

    @staticmethod
    def usernameExists(username):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', (username,))
        count = cursor.fetchone()[0]
        conn.close()
        return (count > 0)

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