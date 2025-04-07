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

# ... (previous code remains the same until simulateUserData function)

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
        "Design and develop electrical systems for commercial buildings, ensuring compliance with safety standards and energy efficiency requirements. Collaborate with architects and construction teams to implement sustainable electrical solutions.",
        "Analyze and optimize power distribution systems for reliability and efficiency. Conduct load flow studies and fault analysis to improve grid performance and integrate renewable energy sources.",
        "Lead cross-functional engineering teams to deliver complex electrical projects on time and within budget. Manage project timelines, resources, and stakeholder communications for successful project completion.",
        "Create detailed electrical schematics and layouts for industrial facilities using CAD software. Select appropriate components and materials while adhering to electrical codes and client specifications.",
        "Design and implement renewable energy systems including solar PV and wind power installations. Conduct feasibility studies and energy audits to recommend sustainable solutions for clients."
    ]
    
    job_descriptions_user2 = [
        "Provide comprehensive eye examinations, diagnose vision problems, and prescribe corrective lenses or vision therapy. Manage patient care and follow-up treatments for optimal eye health outcomes.",
        "Oversee daily operations of a busy optometry clinic including staff management, inventory control, and patient scheduling. Implement policies to improve patient satisfaction and clinic efficiency.",
        "Evaluate and treat patients with specialized vision needs including pediatric and geriatric cases. Fit contact lenses and provide training on proper use and maintenance.",
        "Develop and deliver educational programs on eye health and vision care to schools, community centers, and workplaces. Create informational materials to promote vision health awareness.",
        "Consult with patients to recommend appropriate eyewear based on prescription needs and lifestyle. Maintain knowledge of current optical products and trends to provide expert recommendations."
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
    work_titles_user1 = ['Electrical Design Engineer', 'Power Systems Engineer', 'Project Manager']
    companies_user1 = ['ElectroTech Solutions', 'GridPower Corp', 'RenewEnergy Inc']
    start_dates_user1 = ['2018-05-01', '2015-01-01', '2020-06-01']
    end_dates_user1 = ['2023-05-01', '2018-04-01', '2023-12-31']
    
    responsibilities_user1 = [
        """• Designed electrical systems for commercial and residential buildings using AutoCAD and Revit
• Conducted load calculations and circuit analysis to ensure code compliance
• Collaborated with architects and contractors to integrate electrical systems with building designs
• Performed site inspections to verify installation quality and safety standards
• Prepared technical documentation and project specifications for clients""",
        
        """• Analyzed power distribution networks using ETAP software to optimize performance
• Designed protection schemes for electrical substations and transmission lines
• Conducted fault studies and recommended system improvements
• Coordinated with utility companies to implement grid upgrades
• Trained junior engineers on power system analysis techniques""",
        
        """• Led a team of 12 engineers on renewable energy projects worth $5M+
• Developed project schedules, budgets, and resource allocation plans
• Managed stakeholder communications and progress reporting
• Implemented quality control procedures that reduced rework by 30%
• Negotiated contracts with suppliers and subcontractors"""
    ]

    work_titles_user2 = ['Optometrist', 'Optometry Clinic Manager', 'Eye Health Educator']
    companies_user2 = ['ClearVision Clinic', 'EyeCare Center', 'OptiVision Health']
    start_dates_user2 = ['2017-03-01', '2014-06-01', '2018-02-01']
    end_dates_user2 = ['2023-01-01', '2017-05-01', '2021-08-01']
    
    responsibilities_user2 = [
        """• Conducted comprehensive eye exams for 30+ patients daily using advanced diagnostic equipment
• Diagnosed and treated ocular diseases including glaucoma and macular degeneration
• Prescribed corrective lenses and specialized contact lenses for complex cases
• Managed pre- and post-operative care for cataract and LASIK patients
• Maintained detailed patient records and treatment plans""",
        
        """• Oversaw daily operations of a busy optometry practice with 10 staff members
• Implemented new patient management system that reduced wait times by 40%
• Managed inventory of optical products and medical supplies
• Developed marketing strategies that increased patient volume by 25%
• Conducted staff training on new equipment and procedures""",
        
        """• Designed and delivered eye health education programs for schools and community groups
• Created educational materials on topics like digital eye strain and UV protection
• Organized free vision screening events serving 500+ participants annually
• Trained teachers on identifying vision problems in students
• Collaborated with public health officials on vision care initiatives"""
    ]

    for i in range(3):
        cursor.execute('''
            INSERT INTO workExperience (userId, jobTitle, company, location, startDate, endDate, responsibilities)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            user1_id,
            work_titles_user1[i],
            companies_user1[i],
            'Vancouver, BC',
            start_dates_user1[i],
            end_dates_user1[i],
            responsibilities_user1[i]
        ))

        cursor.execute('''
            INSERT INTO workExperience (userId, jobTitle, company, location, startDate, endDate, responsibilities)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            user2_id,
            work_titles_user2[i],
            companies_user2[i],
            'Dallas, TX',
            start_dates_user2[i],
            end_dates_user2[i],
            responsibilities_user2[i]
        ))

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
        ''', (
            user1_id,
            degrees_user1[i % len(degrees_user1)],
            universities_user1[i % len(universities_user1)],
            graduation_years_user1[i % len(graduation_years_user1)]
        ))

        cursor.execute('''
            INSERT INTO education (userId, degree, university, graduationYear)
            VALUES (?, ?, ?, ?)
        ''', (
            user2_id,
            degrees_user2[i],
            universities_user2[i],
            graduation_years_user2[i]
        ))

    # ---------------- SIMULATING PROJECTS ----------------
    project_names_user1 = ['Smart Grid Design', 'Solar Panel Installation', 'Wind Power Design', 'Energy Efficiency Optimization', 'Power System Analysis', 'Smart Home Automation', 'Electric Vehicle Infrastructure']
    
    project_descriptions_user1 = [
        "Developed a smart grid solution integrating IoT sensors and AI analytics to optimize power distribution and reduce energy losses by 15% across the city's electrical network.",
        "Led a team to design and install a 500kW solar PV system for a commercial complex, reducing their energy costs by 40% and achieving LEED Gold certification.",
        "Created innovative wind turbine designs that increased energy output by 12% while reducing maintenance costs through improved component durability.",
        "Implemented energy efficiency measures across 25 industrial facilities, achieving average energy savings of 22% through lighting retrofits and motor upgrades.",
        "Conducted comprehensive analysis of regional power systems to identify vulnerabilities and recommend infrastructure upgrades worth $3.2M to improve reliability.",
        "Developed a smart home automation system integrating energy monitoring and control features that reduced household energy consumption by an average of 18%.",
        "Designed and implemented electric vehicle charging infrastructure for a municipal fleet, including 50 charging stations with smart load balancing technology."
    ]
    
    technologies_user1 = [
        "IoT sensors, Python, Machine Learning, SCADA systems, Power BI",
        "PVsyst, AutoCAD Electrical, SolarEdge, NEC Code Compliance",
        "SolidWorks, ANSYS CFD, MATLAB, Wind Energy Calculations",
        "Energy Auditing Tools, Lighting Design Software, VFD Systems",
        "ETAP, SKM PowerTools, PSCAD, Short Circuit Analysis",
        "Home Assistant, Zigbee, ESP32, Energy Monitoring Hardware",
        "OCPP Protocol, Load Management Systems, ABB Chargers, AutoCAD"
    ]
    
    impacts_user1 = [
        "Reduced peak demand by 8% and improved outage response times by 30% through predictive analytics",
        "Generated 650MWh of clean energy annually, offsetting 450 tons of CO2 emissions",
        "Patent pending design led to $1.2M in commercial licensing agreements",
        "Saved clients $1.8M annually in energy costs with 2-year payback periods",
        "Prevented potential blackouts affecting 50,000 customers through identified upgrades",
        "Won 2023 Smart Home Innovation Award and deployed in 1,200+ homes",
        "Supported city's transition to 100% electric fleet by 2025, reducing emissions by 35%"
    ]

    project_names_user2 = ['Community Eye Care', 'Optical Health Awareness', 'Eye Care Camp', 'Vision Therapy', 'Optometric Research', 'Elderly Vision Care', 'Pediatric Eye Exams']
    
    project_descriptions_user2 = [
        "Organized and led a volunteer initiative providing free eye exams and glasses to 500+ low-income individuals in underserved communities across Texas.",
        "Developed and implemented a comprehensive eye health education program reaching 3,000+ students in 15 schools, improving vision health knowledge by 72%.",
        "Coordinated a 3-day vision care camp offering free screenings, consultations, and subsidized treatments to rural communities with limited access to eye care.",
        "Pioneered a specialized vision therapy program for patients with binocular vision disorders, achieving 85% success rate in improving visual function.",
        "Conducted clinical research on myopia progression in children, contributing data to a national study that influenced new treatment protocols.",
        "Created a tailored vision care program for elderly patients addressing age-related eye conditions, improving quality of life for 200+ seniors.",
        "Developed pediatric eye exam protocols that reduced exam time by 30% while improving accuracy in detecting vision problems in children."
    ]
    
    technologies_user2 = [
        "Portable Optometry Equipment, EHR Systems, Visual Acuity Testing",
        "Educational Technology, Survey Tools, Data Analysis Software",
        "Mobile Clinic Setup, Autorefractors, Tonometry, Fundus Cameras",
        "Vision Therapy Tools, Prism Lenses, Computerized Training Systems",
        "Research Electronic Data Capture (REDCap), Statistical Software",
        "Low Vision Aids, Magnification Devices, Contrast Sensitivity Testing",
        "Pediatric Eye Charts, Retinoscopy, Fixation Targets, Pupillometry"
    ]
    
    impacts_user2 = [
        "Provided $150,000 worth of free eye care services, improving vision for 92% of participants",
        "Reduced reported eye strain symptoms by 65% among participating students",
        "Identified 12 cases of diabetic retinopathy enabling early intervention",
        "Published findings in the Journal of Optometric Vision Development",
        "Contributed to new myopia control guidelines adopted statewide",
        "Improved daily living activities for 85% of participating seniors",
        "Increased early detection of amblyopia by 40% in screened children"
    ]

    for i in range(7):
        cursor.execute('''
            INSERT INTO projects (userId, projectName, description, technologies, impact)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            user1_id,
            project_names_user1[i],
            project_descriptions_user1[i],
            technologies_user1[i],
            impacts_user1[i]
        ))

        cursor.execute('''
            INSERT INTO projects (userId, projectName, description, technologies, impact)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            user2_id,
            project_names_user2[i],
            project_descriptions_user2[i],
            technologies_user2[i],
            impacts_user2[i]
        ))

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
    volunteer_roles_user1 = ['Volunteer Mentor', 'Community Outreach Coordinator', 'Green Energy Advocate']
    organizations_user1 = ['Tech for Good', 'Vancouver Sustainability Initiative', 'Green Vancouver']
    
    volunteer_descriptions_user1 = [
        """Mentored 50+ high school and university students through weekly sessions on electrical engineering concepts and career pathways. Developed curriculum materials and hands-on projects that increased participant interest in STEM fields by 65%. Organized industry site visits and networking events connecting students with professionals.""",
        
        """Led a team of 15 volunteers in organizing community workshops on energy conservation and sustainable living. Developed educational materials that reached 3,000+ residents. Coordinated with local businesses to implement energy-saving measures that reduced community carbon footprint by 12%.""",
        
        """Advocated for renewable energy policies at municipal meetings and public forums. Educated community members on solar and wind power options through informational sessions. Helped 120+ homeowners navigate incentive programs for residential renewable installations."""
    ]

    volunteer_roles_user2 = ['Eye Health Educator', 'Volunteer Optometrist', 'Vision Care Specialist']
    organizations_user2 = ['Vision Foundation of Texas', 'Optometry for All', 'EyeCare Outreach']
    
    volunteer_descriptions_user2 = [
        """Developed and delivered eye health education programs to underserved communities, reaching 2,500+ individuals annually. Created age-appropriate materials for schools and senior centers. Trained 45 community health workers to identify vision problems and make appropriate referrals.""",
        
        """Provided pro bono comprehensive eye exams to low-income families at monthly clinics. Diagnosed and treated vision problems for 800+ patients over 5 years. Organized donations of 500+ pairs of prescription glasses through partnerships with optical suppliers.""",
        
        """Led vision screening initiatives at homeless shelters and community centers. Implemented a mobile eye clinic serving rural areas with limited access to care. Developed protocols that improved screening efficiency by 40% while maintaining accuracy."""
    ]

    # Add volunteer experience for User 1
    for i in range(3):
        cursor.execute('''
            INSERT INTO volunteerExperience (userId, role, organization, description)
            VALUES (?, ?, ?, ?)
        ''', (user1_id, volunteer_roles_user1[i], organizations_user1[i], volunteer_descriptions_user1[i]))

    # Add volunteer experience for User 2
    for i in range(3):
        cursor.execute('''
            INSERT INTO volunteerExperience (userId, role, organization, description)
            VALUES (?, ?, ?, ?)
        ''', (user2_id, volunteer_roles_user2[i], organizations_user2[i], volunteer_descriptions_user2[i]))

    # ---------------- COMMIT & CLOSE ----------------
    conn.commit()
    conn.close()

# ... (rest of the code remains the same)


if __name__ == '__main__':
        initDb()
        simulateUserData()
