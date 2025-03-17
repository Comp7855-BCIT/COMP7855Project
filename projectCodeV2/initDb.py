# ----------------------------------------------
# Title: initDb.py
# Description: Creates all databases
# Author(s): Feliex, Marvin, Gurp
# Date created: Feb 19, 2025
# Date modified: Mar 8, 2025
# ----------------------------------------------
import sqlite3

def initDb():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # ---------------- USERS TABLE ----------------
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT,
            fullName TEXT,
            email TEXT,
            phone TEXT,
            linkedin TEXT,
            location TEXT,
            portfolio TEXT
        )
    ''')

    # ---------------- JOBS TABLE ----------------
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            userId INTEGER, 
            jobTitle TEXT,
            location TEXT,
            industry TEXT,
            deadline DATE,
            salaryRange TEXT,
            experienceLevel TEXT,
            rate INTEGER,
            description TEXT,
            status TEXT,
            link TEXT,
            company TEXT,
            FOREIGN KEY (userId) REFERENCES users(id)
        )
    ''')
    # ---------------- JOB SUGGESTIONS TABLE ----------------
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobSuggestions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            userId INTEGER,
            jobTitle TEXT,
            company TEXT,
            link TEXT,
            matchScore REAL,
            FOREIGN KEY (userId) REFERENCES users(id)
        );
    ''')
    
    # ---------------- WORK EXPERIENCE TABLE ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS workExperience (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userId INTEGER,
        jobTitle TEXT,
        company TEXT,
        location TEXT,
        startDate TEXT,
        endDate TEXT,
        responsibilities TEXT,
        FOREIGN KEY (userId) REFERENCES users(id)
    );
    """)

    # ---------------- EDUCATION TABLE ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS education (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userId INTEGER,
        degree TEXT,
        university TEXT,
        graduationYear TEXT,
        FOREIGN KEY (userId) REFERENCES users(id)
    );
    """)

    # ---------------- PROJECTS TABLE ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userId INTEGER,
        projectName TEXT,
        description TEXT,
        technologies TEXT,
        impact TEXT,
        FOREIGN KEY (userId) REFERENCES users(id)
    );
    """)

    # ---------------- CERTIFICATIONS TABLE ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS certifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userId INTEGER,
        certificateName TEXT,
        issuer TEXT,
        year TEXT,
        FOREIGN KEY (userId) REFERENCES users(id)
    );
    """)

    # ---------------- AWARDS TABLE ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS awards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userId INTEGER,
        awardName TEXT,
        issuer TEXT,
        year TEXT,
        FOREIGN KEY (userId) REFERENCES users(id)
    );
    """)

    # ---------------- VOLUNTEER EXPERIENCE TABLE ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS volunteerExperience (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userId INTEGER,
        role TEXT,
        organization TEXT,
        description TEXT,
        FOREIGN KEY (userId) REFERENCES users(id)
    );
    """)
    
    # ---------------- RESUME TABLE ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resume (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userId INTEGER,
        jobId TEXT,
        resume TEXT,
        FOREIGN KEY (userId) REFERENCES users(id),
        FOREIGN KEY (jobId) REFERENCES jobs(id)
    );
    """)
    # ---------------- COVER LETTER TABLE ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS coverLetter (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userId INTEGER,
        jobId TEXT,
        coverLetter TEXT,
        FOREIGN KEY (userId) REFERENCES users(id),
        FOREIGN KEY (jobId) REFERENCES jobs(id)
    );
    """)
    

    conn.commit()
    conn.close()

