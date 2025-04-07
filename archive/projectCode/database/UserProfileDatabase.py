import sqlite3

class UserProfileDatabase:
    def __init__(self, db_name="user_profile.db"):
        """Initialize and connect to the SQLite database."""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Create Users table for storing user profile data."""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            birth_date TEXT NOT NULL,
            address TEXT NOT NULL
        );
        """)
        self.conn.commit()

    def add_user(self, full_name, birth_date, address):
        """Insert new user data into the database."""
        self.cursor.execute("""
        INSERT INTO Users (full_name, birth_date, address)
        VALUES (?, ?, ?)
        """, (full_name, birth_date, address))
        self.conn.commit()
        print("User profile saved successfully!")

    def view_users(self):
        """Retrieve and display all users from the database."""
        print("\nList of Users in the Database:")

        self.cursor.execute("SELECT * FROM Users")
        users = self.cursor.fetchall()

        if users:
            for user in users:
                print(f"\nUser ID: {user[0]}")
                print(f"Full Name: {user[1]}")
                print(f"Birth Date: {user[2]}")
                print(f"Address: {user[3]}")
                print("-" * 40)  # Separator
        else:
            print("No users found in the database.")

    def get_user(self, user_id):
        """Retrieve a specific user's profile from the database."""
        self.cursor.execute("SELECT * FROM Users WHERE user_id = ?", (user_id,))
        return self.cursor.fetchone()

    def update_user(self, user_id, full_name, birth_date, address):
        """Update user profile information."""
        self.cursor.execute("""
        UPDATE Users
        SET full_name = ?, birth_date = ?, address = ?
        WHERE user_id = ?
        """, (full_name, birth_date, address, user_id))
        self.conn.commit()
        print("User profile updated successfully!")

    def delete_user(self, user_id):
        """Delete a user profile from the database."""
        self.cursor.execute("DELETE FROM Users WHERE user_id = ?", (user_id,))
        self.conn.commit()
        print(f"User with ID {user_id} has been deleted.")

    def close_connection(self):
        """Close the database connection."""
        self.conn.close()
