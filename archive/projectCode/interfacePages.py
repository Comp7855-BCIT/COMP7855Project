# ----------------------------------------------
# Title: interfacePages.py
# Description: All pages
# Author(s): Jasmine
# Date created: Feb 19, 2025
# Date modified: Feb 20, 2025
# ----------------------------------------------
from database.jobDatabase import jobDatabase


from database.coverLetterDatabase import coverLetterDatabase
from database.UserProfileDatabase import UserProfileDatabase

from database.resume_database import create_resume_table
from database.resume_prompt import collect_user_profile, insert_user_data,insert_work_experience, insert_education,insert_projects,insert_certifications,insert_awards,insert_volunteer_experience  
from database.display_table import display_table


class interfacePages:
    def __init__(self):
        # Initialize jobDatabase instance
        self.db = jobDatabase()
        self.profile_db = UserProfileDatabase()

    def addJob(self):
        while True:
            print("\n0. Exit")
            print("1. New Job")
            print("2. Update Job")
            print("3. Delete Job")
            print("4. View Jobs")
            print("5. Qualification Analysis")

            choice = input("Choose an option: ")

            if choice == '1':  # Add Job
                self.db.addJob()
            elif choice == '2':  # Update Job
                jobTitle = input("Enter the job title to update: ")
                self.db.updateJob(jobTitle)
            elif choice == '3':  # Delete Job
                jobTitle = input("Enter the job title to delete: ")
                self.db.deleteJob(jobTitle)
            elif choice == '4':  # View Jobs
                self.db.viewJobs()
            elif choice == '5':  # Qualification Analysis
                jobTitle = input("Enter the job title for analysis: ")
                self.db.qualificationAnalysis(jobTitle)
            elif choice == '0':
                print("Exiting...")
                break
            else:
                print("Invalid option. Please try again.")


    def fullResume(self):
        create_resume_table()
        while True:
            print("\nUser Profile Menu")
            print("0. Exit")
            print("1. Add Full Resume")
            print("2. View Resume")

            choice = input("Choose an option: ")

            if choice == '1':  # Add new user profile
                user_data=collect_user_profile()
                user_id = insert_user_data(user_data)  
                insert_work_experience(user_id, user_data["work_experience"])  
                insert_education(user_id, user_data["education"])  
                insert_projects(user_id, user_data["projects"])  
                insert_certifications(user_id, user_data["certifications"])  
                insert_awards(user_id, user_data["awards"])  
                insert_volunteer_experience(user_id, user_data["volunteer_experience"])  

                print("\nAll user data has been saved to the database successfully!")

            elif choice == '2':  # View all saved user profiles
                display_table()


            elif choice == '0':  # Exit menu
                print("Exiting user profile menu...")
                break

            else:
                print("Invalid option. Please try again.")


    def fullCoverLetter(self):
        coverLetterDatabase.viewCoverLetter(self)
        print("Full cover letter page")

    def userProfile(self):
        """Calls functions directly from UserProfileDatabase"""
        while True:
            print("\nUser Profile Menu")
            print("0. Exit")
            print("1. Add New User Profile")
            print("2. View Saved User Profiles")
            print("3. Edit Existing User Profile")
            print("4. Delete User Profile")

            choice = input("Choose an option: ")

            if choice == '1':  # Add new user profile
                full_name = input("Enter Full Name: ").strip()
                birth_date = input("Enter Date of Birth (YYYY-MM-DD): ").strip()
                address = input("Enter Home Address: ").strip()
                self.profile_db.add_user(full_name, birth_date, address)
                print("User profile saved successfully!")

            elif choice == '2':  # View all saved user profiles
                self.profile_db.view_users()

            elif choice == '3':  # Edit an existing user profile
                user_id = input("Enter User ID to edit: ").strip()
                existing_profile = self.profile_db.get_user(user_id)

                if existing_profile:
                    print("\nEditing Profile:")
                    print(f"Current Name: {existing_profile[1]}")
                    print(f"Current Birth Date: {existing_profile[2]}")
                    print(f"Current Address: {existing_profile[3]}")

                    full_name = input("New Full Name (leave blank to keep current): ").strip() or existing_profile[1]
                    birth_date = input("New Birth Date (YYYY-MM-DD, leave blank to keep current): ").strip() or existing_profile[2]
                    address = input("New Address (leave blank to keep current): ").strip() or existing_profile[3]

                    self.profile_db.update_user(user_id, full_name, birth_date, address)
                    print("User profile updated successfully!")

                else:
                    print("User ID not found.")

            elif choice == '4':  # Delete user profile
                user_id = input("Enter User ID to delete: ").strip()
                existing_profile = self.profile_db.get_user(user_id)

                if existing_profile:
                    confirm = input(f"Are you sure you want to delete {existing_profile[1]}? (yes/no): ").strip().lower()
                    if confirm == 'yes':
                        self.profile_db.delete_user(user_id)
                        print("User profile deleted successfully!")
                    else:
                        print("Deletion cancelled.")
                else:
                    print("User ID not found.")

            elif choice == '0':  # Exit menu
                print("Exiting user profile menu...")
                break

            else:
                print("Invalid option. Please try again.")

    def archiveJobs(self):
        print("Archive jobs page")
