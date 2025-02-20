
import sqlite3

def collect_multiple_entries(category_name):
    """Asks user if they want to add multiple entries for a category like work experience or projects."""
    entries = []
    
    while True:
        add_entry = input(f"Do you want to add {category_name}? (y/n): ").strip().lower()
        if add_entry != "y":
            break  # Stop asking when the user says "no"

        # Collect the details for one entry
        entry = {}
        if category_name == "work experience":
            entry["job_title"] = input("Enter your job title: ")
            entry["company"] = input("Enter the company name: ")
            entry["location"] = input("Enter the company location: ")
            entry["start_date"] = input("Enter your start date (Month, Year): ")
            entry["end_date"] = input("Enter your end date (or 'Present' if still working there): ")
            entry["responsibilities"] = input("List your job responsibilities and achievements: ")
        
        elif category_name == "projects":
            entry["project_name"] = input("Enter project name: ")
            entry["description"] = input("Enter a brief project description: ")
            entry["technologies"] = input("List technologies used in the project: ")
            entry["impact"] = input("Describe the project's impact or outcome: ")

        elif category_name == "education":
            entry["degree"] = input("Enter your degree (e.g., B.Sc. in Computer Science): ")
            entry["university"] = input("Enter your university/college name: ")
            entry["graduation_year"] = input("Enter your graduation year: ")

        elif category_name == "certifications":
            entry["certificate_name"] = input("Enter certification name: ")
            entry["issuer"] = input("Enter the issuing organization: ")
            entry["year"] = input("Enter the year earned: ")

        elif category_name == "awards":
            entry["award_name"] = input("Enter award/honor name: ")
            entry["issuer"] = input("Enter the issuing organization: ")
            entry["year"] = input("Enter the year received: ")

        elif category_name == "volunteer experience":
            entry["role"] = input("Enter your volunteer role: ")
            entry["organization"] = input("Enter the organization name: ")
            entry["description"] = input("Describe your volunteer work: ")

        # Add the entry to the list
        entries.append(entry)

    return entries  # Return the list of entries


user_data = {
    "personal_info": {
        "full_name": input("Enter your full name: "),
        "email": input("Enter your email address: "),
        "phone": input("Enter your phone number: "),
        "linkedin": input("Enter your LinkedIn profile URL (optional): "),
        "location": input("Enter your current city and country: ")
    },
    "job_title": input("What job are you applying for? "),
    "career_objective": input("Write a short career summary (2-3 sentences): "),
    
    # Collect multiple entries
    "work_experience": collect_multiple_entries("work experience"),
    "education": collect_multiple_entries("education"),
    "projects": collect_multiple_entries("projects"),
    "skills": input("List your top skills (comma-separated): "),
    "certifications": collect_multiple_entries("certifications"),
    "awards": collect_multiple_entries("awards"),
    "volunteer_experience": collect_multiple_entries("volunteer experience"),
    "languages": input("List any additional languages you speak and proficiency level: ")
}

# ---------------- Database Functions ----------------

def insert_user_data(user_data):
    """ Inserts user personal details into the database and returns the user_id. """
    conn = sqlite3.connect("resume.db")
    cursor = conn.cursor()

    # Insert user details
    cursor.execute("""
        INSERT INTO Users (full_name, email, phone, linkedin, location, job_title, career_objective)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        user_data["personal_info"]["full_name"],
        user_data["personal_info"]["email"],
        user_data["personal_info"]["phone"],
        user_data["personal_info"]["linkedin"],
        user_data["personal_info"]["location"],
        user_data["job_title"],
        user_data["career_objective"]
    ))

    user_id = cursor.lastrowid  # Get the last inserted user ID
    conn.commit()
    conn.close()

    return user_id


def insert_work_experience(user_id, work_experiences):
    """ Inserts multiple work experiences for a user. """
    conn = sqlite3.connect("resume.db")
    cursor = conn.cursor()

    for exp in work_experiences:
        cursor.execute("""
            INSERT INTO WorkExperience (user_id, job_title, company, location, start_date, end_date, responsibilities)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, exp["job_title"], exp["company"], exp["location"], exp["start_date"], exp["end_date"], exp["responsibilities"]))

    conn.commit()
    conn.close()


def insert_education(user_id, education_entries):
    """ Inserts multiple education entries for a user. """
    conn = sqlite3.connect("resume.db")
    cursor = conn.cursor()

    for edu in education_entries:
        cursor.execute("""
            INSERT INTO Education (user_id, degree, university, graduation_year)
            VALUES (?, ?, ?, ?)
        """, (user_id, edu["degree"], edu["university"], edu["graduation_year"]))

    conn.commit()
    conn.close()


def insert_projects(user_id, projects):
    """ Inserts multiple projects for a user. """
    conn = sqlite3.connect("resume.db")
    cursor = conn.cursor()

    for project in projects:
        cursor.execute("""
            INSERT INTO Projects (user_id, project_name, description, technologies, impact)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, project["project_name"], project["description"], project["technologies"], project["impact"]))

    conn.commit()
    conn.close()


def insert_certifications(user_id, certifications):
    """ Inserts multiple certifications for a user. """
    conn = sqlite3.connect("resume.db")
    cursor = conn.cursor()
    
    for cert in certifications:
        cursor.execute("""
            INSERT INTO Certifications (user_id, certificate_name, issuer, year)
            VALUES (?, ?, ?, ?)
        """, (user_id, cert["certificate_name"], cert["issuer"], cert["year"]))
    
    conn.commit()
    conn.close()


def insert_awards(user_id, awards):
    """ Inserts multiple awards for a user. """
    conn = sqlite3.connect("resume.db")
    cursor = conn.cursor()
    
    for award in awards:
        cursor.execute("""
            INSERT INTO Awards (user_id, award_name, issuer, year)
            VALUES (?, ?, ?, ?)
        """, (user_id, award["award_name"], award["issuer"], award["year"]))
    
    conn.commit()
    conn.close()


def insert_volunteer_experience(user_id, volunteer_experiences):
    """ Inserts multiple volunteer experiences for a user. """
    conn = sqlite3.connect("resume.db")
    cursor = conn.cursor()
    
    for volunteer in volunteer_experiences:
        cursor.execute("""
            INSERT INTO VolunteerExperience (user_id, role, organization, description)
            VALUES (?, ?, ?, ?)
        """, (user_id, volunteer["role"], volunteer["organization"], volunteer["description"]))
    
    conn.commit()
    conn.close()


# ---------------- Store Data in Database ----------------

user_id = insert_user_data(user_data)  
insert_work_experience(user_id, user_data["work_experience"])  
insert_education(user_id, user_data["education"])  
insert_projects(user_id, user_data["projects"])  
insert_certifications(user_id, user_data["certifications"])  
insert_awards(user_id, user_data["awards"])  
insert_volunteer_experience(user_id, user_data["volunteer_experience"])  

print("\nAll user data has been saved to the database successfully!")
