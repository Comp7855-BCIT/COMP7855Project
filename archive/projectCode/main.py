# ----------------------------------------------
# Title: main.py
# Description: Main page
# Author(s): Jasmine 
# Date created: Feb 19, 2025
# Date modified: Feb 20, 2025
# ----------------------------------------------

from interfacePages import interfacePages  # Import the interfacePages class
from api import api


def main_menu():
    # Create an instance of the interfacePages class
    pages = interfacePages()
    AIapi = api()

    while True:
        print("Welcome to the Resume and Cover Letter Generator!")
        print("\nMain Menu")
        print("0. Exit")
        print("1. Add Job")
        print("2. Full Resume")
        print("3. Full Cover Letter <-- Under construction")
        print("4. User profile")
        print("5. Archive jobs <-- Under construction")
        print("6. testing purpose-api <-- Under construction")

        """Add function call here to display job status"""
        
        choice = input("Choose an option: ")
        if choice == '0':
            print("Exiting...")
            break
        elif choice == '1':  # Add Job
            pages.addJob()  
        elif choice == '2':  # View Full Resume
            pages.fullResume()  
        elif choice == '3':  # View Full Cover Letter
            pages.fullCoverLetter()  
        elif choice == '4':  # User profile
            pages.userProfile() 
        elif choice == '5':  # Archive jobs
            pages.archiveJobs()
        elif choice == '6':  # Testing purpose- example test API
            prompt = "get me the best chocolate cake recipe"
            response = AIapi.generateResponse(prompt)
            print(f"Response generated: {response}")
        else:
            print(f"Invalid option. Please try again.")

if __name__ == "__main__":
    main_menu()

