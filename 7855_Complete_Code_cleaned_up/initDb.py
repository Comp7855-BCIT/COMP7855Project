# ----------------------------------------------
# Title: initDb.py
# Description: Creates all databases
# Author(s): Feliex, Marvin, Gurp
# Date created: Feb 19, 2025
# Date modified: Mar 8, 2025
# ----------------------------------------------
import sqlite3
from controllers.userController import UserController

def initDb():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # ---------------- USERS TABLE ----------------
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT,  -- will store bcrypt-hashed password
            fullName TEXT,
            email TEXT,
            phone TEXT,
            linkedin TEXT,
            location TEXT,
            portfolio TEXT
            -- We'll add plainPassword below
        )
    ''')

    # -- ADDED: Add plainPassword column if it doesn't already exist --
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN plainPassword TEXT")
    except:
        pass

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

def simulateUserData():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # ---------------- SIMULATING USERS ----------------
    # Add User 1
    user1_id = UserController.signUpTemp('John Doe', 'john@example.com', '123-456-7890', 'john_doe', 'Qwertyuiop[1')

    # Add User 2
    user2_id = UserController.signUpTemp('Jane Smith', 'jane@example.com', '123-456-7890', 'jane_smith', 'Qwertyuiop[1')

    # ---------------- SIMULATING JOBS ----------------
    job_titles_user1 = ['Electrical Engineer', 'Power Systems Engineer', 'Project Manager', 'Electrical Design Engineer', 'Renewable Energy Engineer']
    job_titles_user2 = ['Optometrist', 'Optometry Clinic Manager', 'Vision Care Specialist', 'Eye Health Educator', 'Optical Sales Specialist']
    locations_user1 = ['Vancouver, BC', 'Surrey, BC', 'Burnaby, BC', 'Victoria, BC', 'Kelowna, BC']
    locations_user2 = ['Dallas, TX', 'Houston, TX', 'Austin, TX', 'San Antonio, TX', 'Fort Worth, TX']
    salary_ranges_user1 = ['70k-90k', '80k-100k', '90k-110k', '100k-120k', '110k-130k']
    salary_ranges_user2 = ['90k-110k', '100k-120k', '110k-130k', '120k-140k', '130k-150k']
    industries_user1 = ['Engineering', 'Energy', 'Technology', 'Construction', 'Renewable Energy']
    industries_user2 = ['Healthcare', 'Optometry', 'Vision Care', 'Medical', 'Retail']
    status=['💼 Interview', '⏳ Applied and waiting', '📂 Archive', '📝 Want to apply', '📝 Want to apply']
    date=['2025-06-30', '2025-05-30', '2025-06-06', '2025-05-22', '2025-06-15']
    
    job_descriptions_user1 = [
        "Design and develop electrical systems for commercial buildings...",
        "Analyze and optimize power distribution systems for reliability...",
        "Lead cross-functional engineering teams to deliver complex...",
        "Create detailed electrical schematics...",
        "Design and implement renewable energy systems including solar PV..."
    ]
    
    job_descriptions_user2 = [
        "Provide comprehensive eye examinations, diagnose vision problems...",
        "Oversee daily operations of a busy optometry clinic...",
        "Evaluate and treat patients with specialized vision needs...",
        "Develop and deliver educational programs on eye health...",
        "Consult with patients to recommend appropriate eyewear..."
    ]

    for i in range(5):
        cursor.execute('''
            INSERT INTO jobs (userId, jobTitle, location, industry, deadline, salaryRange, experienceLevel, rate, description, status, link, company)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user1_id,
            job_titles_user1[i],
            locations_user1[i],
            industries_user1[i],
            date[i],
            salary_ranges_user1[i],
            'Mid',
            4,
            job_descriptions_user1[i],
            status[i],
            f'https://example.com/job{i+1}',
            f'Company{i+1}'
        ))

        cursor.execute('''
            INSERT INTO jobs (userId, jobTitle, location, industry, deadline, salaryRange, experienceLevel, rate, description, status, link, company)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user2_id,
            job_titles_user2[i],
            locations_user2[i],
            industries_user2[i],
            date[i],
            salary_ranges_user2[i],
            'Junior',
            3,
            job_descriptions_user2[i],
            status[i],
            f'https://example.com/job{i+1}',
            f'Company{i+1}'
        ))

    # ---------------- SIMULATING WORK EXPERIENCE ----------------

    conn.commit()
    conn.close()

if __name__ == '__main__':
    initDb()
    simulateUserData()
