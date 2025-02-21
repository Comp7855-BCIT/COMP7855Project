import sqlite3

def create_resume_table():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect("resume.db")
    cursor = conn.cursor()

    # ---------------- USERS TABLE ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        linkedin TEXT,
        location TEXT,
        job_title TEXT,
        career_objective TEXT
    );
    """)

    # ---------------- WORK EXPERIENCE TABLE ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS WorkExperience (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        job_title TEXT,
        company TEXT,
        location TEXT,
        start_date TEXT,
        end_date TEXT,
        responsibilities TEXT,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    );
    """)

    # ---------------- EDUCATION TABLE ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Education (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        degree TEXT,
        university TEXT,
        graduation_year TEXT,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    );
    """)

    # ---------------- PROJECTS TABLE ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        project_name TEXT,
        description TEXT,
        technologies TEXT,
        impact TEXT,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    );
    """)

    # ---------------- CERTIFICATIONS TABLE ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Certifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        certificate_name TEXT,
        issuer TEXT,
        year TEXT,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    );
    """)

    # ---------------- AWARDS TABLE ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Awards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        award_name TEXT,
        issuer TEXT,
        year TEXT,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    );
    """)

    # ---------------- VOLUNTEER EXPERIENCE TABLE ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS VolunteerExperience (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        role TEXT,
        organization TEXT,
        description TEXT,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    );
    """)

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    print("Database and tables created successfully!")
