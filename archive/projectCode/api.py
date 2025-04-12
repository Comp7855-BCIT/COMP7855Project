# ----------------------------------------------
# Title: api.py
# Description: AI generator
# Author(s):  
# Date created: Feb 19, 2025
# Date modified: Feb 19, 2025
# ----------------------------------------------
import os
import sys
from groq import Groq
class api:
    def __init__(self):
        pass
        #api_key = os.environ.get("GROQ_API_KEY")
        #ima just put the API key directly.
        #technically we're not supposed to define the key here in the application source codes
        #the key should be stored in the environment. however i couldnt get it to work 
        #so i am just defining the key here - hopefully its acceptable.  
        #in actual application, we must define the key in the environment for security
        api_key = "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" 
    def generateResponse(self, prompt):
        if not api_key:
        print("Cant find the key.")
        sys.exit(1)
        # Initialize Groq client
        client = Groq(api_key=api_key)
        prompt = input("Enter your message to the AI: ")
        # Define the model you want to use
        model = "llama3-70b-8192"  # You can change this to another Groq model if needed
        print(f"\nSending request to Groq ({model})...\n")
        try:
            # Send request to Groq API
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=model,
            )
            
            # Extract and print the response
            response = chat_completion.choices[0].message.content
            print("AI Response:\n")
            print(response)
        except Exception as e:
            print(f"Error communicating with Groq API: {e}")
    return response



    
    
    
