# ----------------------------------------------
# Title: main.py
# Description: Main page
# Author(s): Jasmine 
# Date created: Feb 19, 2025
# Date modified: Feb 19, 2025
# ----------------------------------------------

from interfacePages import interfacePages  # Import the interfacePages class
from api import api

def main_menu():
    # Create an instance of the interfacePages class
    pages = interfacePages()
    AIapi = api()
    
    while True:
        print("\nMain Menu")
        print("0. Exit")
        print("1. Add Job")
        print("2. Add Experience")
        print("3. Full Resume")
        print("4. Full Cover Letter")
        print("5. User profile")
        print("6. Archive jobs")
        print("7. testing purpose-api")

        """add function call here to display job status"""
        
        choice = input("Choose an option: ")
        if choice == '0':
            print("Exiting...")
            break
        elif choice == '1':  # Add Job
            pages.addJob()  
        elif choice == '2':  # Add Experience
            pages.addExperience() 
        elif choice == '3':  # View Full Resume
            pages.fullResume()  
        elif choice == '4':  # View Full Cover Letter
            pages.fullCoverLetter()  
        elif choice == '5':  # User profile
            pages.userProfile() 
        elif choice == '6':  # Archive jobs
            pages.archiveJobs()
#        elif choice == '7': 7 # testing purpose- example test api
            prompt="get me the best chocolate cake recepie"
            response= AIapi.generateResponse(prompt)
            print(f"Response generated: {response}")

        else:
            print(f"Invalid option. Please try again.")

if __name__ == "__main__":
    main_menu()
