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

    for i in range(5):
        cursor.execute('''
            INSERT INTO jobs (userId, jobTitle, location, industry, deadline, salaryRange, experienceLevel, rate, description, status, link, company)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user1_id, job_titles_user1[i], locations_user1[i], industries_user1[i], '2025-06-30', salary_ranges_user1[i], 'Mid', 4, f'Description for {job_titles_user1[i]}', 'Open', f'https://example.com/job{i+1}', f'Company{i+1}'))

        cursor.execute('''
            INSERT INTO jobs (userId, jobTitle, location, industry, deadline, salaryRange, experienceLevel, rate, description, status, link, company)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user2_id, job_titles_user2[i], locations_user2[i], industries_user2[i], '2025-05-15', salary_ranges_user2[i], 'Junior', 3, f'Description for {job_titles_user2[i]}', 'Open', f'https://example.com/job{i+1}', f'Company{i+1}'))

    # ---------------- SIMULATING WORK EXPERIENCE ----------------
    work_titles_user1 = ['Electrical Design Engineer', 'Power Systems Engineer', 'Project Manager']
    companies_user1 = ['ElectroTech Solutions', 'GridPower Corp', 'RenewEnergy Inc']
    start_dates_user1 = ['2018-05-01', '2015-01-01', '2020-06-01']
    end_dates_user1 = ['2023-05-01', '2018-04-01', '2023-12-31']
    responsibilities_user1 = ['Designed electrical layouts for buildings.', 'Managed power grid design and installation.', 'Led renewable energy projects.']

    work_titles_user2 = ['Optometrist', 'Optometry Clinic Manager', 'Eye Health Educator']
    companies_user2 = ['ClearVision Clinic', 'EyeCare Center', 'OptiVision Health']
    start_dates_user2 = ['2017-03-01', '2014-06-01', '2018-02-01']
    end_dates_user2 = ['2023-01-01', '2017-05-01', '2021-08-01']
    responsibilities_user2 = ['Provided eye exams and prescribed lenses.', 'Managed the clinic’s daily operations.', 'Educated the community on eye health and prevention.']

    for i in range(3):
        cursor.execute('''
            INSERT INTO workExperience (userId, jobTitle, company, location, startDate, endDate, responsibilities)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user1_id, work_titles_user1[i], companies_user1[i], 'Vancouver, BC', start_dates_user1[i], end_dates_user1[i], responsibilities_user1[i]))

        cursor.execute('''
            INSERT INTO workExperience (userId, jobTitle, company, location, startDate, endDate, responsibilities)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user2_id, work_titles_user2[i], companies_user2[i], 'Dallas, TX', start_dates_user2[i], end_dates_user2[i], responsibilities_user2[i]))

    # ---------------- SIMULATING EDUCATION ----------------
    degrees_user1 = ['B.Sc. in Electrical Engineering', 'M.Sc. in Power Systems Engineering', 'Ph.D. in Electrical Engineering']
    universities_user1 = ['University of British Columbia', 'Simon Fraser University', 'University of Vancouver']
    graduation_years_user1 = ['2014', '2016', '2020']

    degrees_user2 = ['Doctor of Optometry (OD)', 'B.Sc. in Biology', 'M.Sc. in Optometry']
    universities_user2 = ['University of Houston', 'Texas A&M University', 'University of Texas']
    graduation_years_user2 = ['2019', '2013', '2021']

    for i in range(3):
        cursor.execute('''
            INSERT INTO education (userId, degree, university, graduationYear)
            VALUES (?, ?, ?, ?)
        ''', (user1_id, degrees_user1[i % len(degrees_user1)], universities_user1[i % len(universities_user1)], graduation_years_user1[i % len(graduation_years_user1)]))

        cursor.execute('''
            INSERT INTO education (userId, degree, university, graduationYear)
            VALUES (?, ?, ?, ?)
        ''', (user2_id, degrees_user2[i], universities_user2[i], graduation_years_user2[i]))

    # ---------------- SIMULATING PROJECTS ----------------
    project_names_user1 = ['Smart Grid Design', 'Solar Panel Installation', 'Wind Power Design', 'Energy Efficiency Optimization', 'Power System Analysis', 'Smart Home Automation', 'Electric Vehicle Infrastructure']
    technologies_used_user1 = ['Electrical Engineering', 'Solar Panels', 'Wind Turbines', 'Energy Audits', 'Power Systems', 'IoT', 'EV Chargers']
    impacts_user1 = ['Improved energy efficiency', 'Reduced carbon emissions', 'Enhanced energy production', 'Lowered energy costs', 'Optimized grid operations', 'Automated home energy management', 'Facilitated EV adoption']

    project_names_user2 = ['Community Eye Care', 'Optical Health Awareness', 'Eye Care Camp', 'Vision Therapy', 'Optometric Research', 'Elderly Vision Care', 'Pediatric Eye Exams']
    technologies_used_user2 = ['Optometry', 'Public Health', 'Optical Equipment', 'Vision Therapy Techniques', 'Optometric Tools', 'Pediatric Optometry', 'Community Outreach']
    impacts_user2 = ['Increased access to eye exams', 'Raised awareness about eye health', 'Provided free eye exams', 'Improved vision in children', 'Advanced eye care research', 'Improved elderly vision care', 'Improved pediatric eye health']

    for i in range(7):
        cursor.execute('''
            INSERT INTO projects (userId, projectName, description, technologies, impact)
            VALUES (?, ?, ?, ?, ?)
        ''', (user1_id, project_names_user1[i], f'Description for {project_names_user1[i]}', technologies_used_user1[i], impacts_user1[i]))

        cursor.execute('''
            INSERT INTO projects (userId, projectName, description, technologies, impact)
            VALUES (?, ?, ?, ?, ?)
        ''', (user2_id, project_names_user2[i], f'Description for {project_names_user2[i]}', technologies_used_user2[i], impacts_user2[i]))

    # ---------------- SIMULATING CERTIFICATIONS ----------------
    certifications_user1 = ['Certified Electrical Engineer', 'Certified Power Systems Engineer', 'Licensed Electrical Professional', 'Certified Renewable Energy Professional']
    issuers_user1 = ['Canadian Engineering Association', 'Power Engineers Association', 'Electrical Professionals Group', 'Renewable Energy Council']
    years_user1 = ['2018', '2019', '2020', '2021']

    certifications_user2 = ['Licensed Optometrist', 'Certified Vision Therapist', 'OD Fellowship', 'Advanced Optometric Training']
    issuers_user2 = ['Texas Board of Optometry', 'American Optometry Association', 'Optometry Fellowship Institute', 'American Academy of Optometry']
    years_user2 = ['2015', '2018', '2020', '2022']

    for i in range(4):
        cursor.execute('''
            INSERT INTO certifications (userId, certificateName, issuer, year)
            VALUES (?, ?, ?, ?)
        ''', (user1_id, certifications_user1[i], issuers_user1[i], years_user1[i]))

        cursor.execute('''
            INSERT INTO certifications (userId, certificateName, issuer, year)
            VALUES (?, ?, ?, ?)
        ''', (user2_id, certifications_user2[i], issuers_user2[i], years_user2[i]))

    # ---------------- SIMULATING AWARDS ----------------
    awards_user1 = ['Innovative Engineering Award', 'Best Green Energy Project']
    issuers_user1 = ['BC Engineering Society', 'Renewable Energy Council']
    years_user1 = ['2022', '2023']

    awards_user2 = ['Best Optometrist of the Year', 'Outstanding Vision Care Professional']
    issuers_user2 = ['Optometry Association of Texas', 'American Optometric Society']
    years_user2 = ['2023', '2024']

    for i in range(2):
        cursor.execute('''
            INSERT INTO awards (userId, awardName, issuer, year)
            VALUES (?, ?, ?, ?)
        ''', (user1_id, awards_user1[i], issuers_user1[i], years_user1[i]))

        cursor.execute('''
            INSERT INTO awards (userId, awardName, issuer, year)
            VALUES (?, ?, ?, ?)
        ''', (user2_id, awards_user2[i], issuers_user2[i], years_user2[i]))
    # ---------------- SIMULATING VOLUNTEER EXPERIENCE ----------------
    # Volunteer experience for User 1 (Electrical Engineer, Vancouver)
    volunteer_roles_user1 = ['Volunteer Mentor', 'Community Outreach Coordinator', 'Green Energy Advocate']
    organizations_user1 = ['Tech for Good', 'Vancouver Sustainability Initiative', 'Green Vancouver']
    descriptions_user1 = [
        'Mentored aspiring engineers in local schools to promote STEM education.',
        'Coordinated events to raise awareness about sustainability practices.',
        'Advocated for renewable energy adoption in the local community.'
    ]

    # Volunteer experience for User 2 (Optometrist, Texas)
    volunteer_roles_user2 = ['Eye Health Educator', 'Volunteer Optometrist', 'Vision Care Specialist']
    organizations_user2 = ['Vision Foundation of Texas', 'Optometry for All', 'EyeCare Outreach']
    descriptions_user2 = [
        'Provided free eye health education in underprivileged areas.',
        'Offered pro bono eye exams for low-income communities.',
        'Organized community outreach events to educate people on vision care.'
    ]

    # Add volunteer experience for User 1
    for i in range(3):
        cursor.execute('''
            INSERT INTO volunteerExperience (userId, role, organization, description)
            VALUES (?, ?, ?, ?)
        ''', (user1_id, volunteer_roles_user1[i], organizations_user1[i], descriptions_user1[i]))

    # Add volunteer experience for User 2
    for i in range(3):
        cursor.execute('''
            INSERT INTO volunteerExperience (userId, role, organization, description)
            VALUES (?, ?, ?, ?)
        ''', (user2_id, volunteer_roles_user2[i], organizations_user2[i], descriptions_user2[i]))


    # ---------------- COMMIT & CLOSE ----------------
    conn.commit()
    conn.close()


if __name__ == '__main__':
        initDb()
        simulateUserData()
