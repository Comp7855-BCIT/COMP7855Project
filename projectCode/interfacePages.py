# ----------------------------------------------
# Title: interfacePages.py
# Description: All pages
# Author(s): Jasmine 
# Date created: Feb 19, 2025
# Date modified: Feb 19, 2025
# ----------------------------------------------
from database.jobDatabase import jobDatabase
from database.experienceDatabase import experienceDatabase
from database.resumeDatabase import resumeDatabase
from database.coverLetterDatabase import coverLetterDatabase

class interfacePages:
    def __init__(self):
        # Any initialization logic (if needed)
        pass
    def addJob(self):
        jobDatabase.addJob(self)
        jobDatabase.viewJobs(self)
        jobTitle = input("Enter title for analysis: ")
        jobDatabase.qualificationAnalysis(self, jobTitle)
        print(f"Add job page")
    def addExperience(self):
        while True:
            print("\nNew Experience")
            print("0. Exit")
            print("1. Work")
            print("2. Volunteer")
            print("3. Education")
            print("4. Interest")
            print("5. Project")

            """add function call here to display expirence database"""
        
            choice = input("Choose an option: ")
        
            if choice == '1':  # Add Work
                experienceDatabase.addWork(self)  
            elif choice == '2':  # Add Volunteer
                print(f"Add Volunteer") 
            elif choice == '3':  # Add Education
                print(f"Add Education")  
            elif choice == '4':  # Add Interest
                print(f"Add Interest")
            elif choice == '5':  # Add Project
                print(f"Add Project") 
            elif choice == '0':
                print("Exiting...")
                break
            else:
                print("Invalid option. Please try again.")
            
    def fullResume(self):
        resumeDatabase.viewResume(self)
        print(f"Full resume page")
    def fullCoverLetter(self):
        coverLetter.viewCoverLetter(self)
        print(f"Full cover letter page")
    def userProfile(self):
        print(f"User profile page")
    def archiveJobs(self):
        print(f"Archive jobs page")