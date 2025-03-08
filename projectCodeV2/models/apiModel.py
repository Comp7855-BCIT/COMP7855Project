# ----------------------------------------------
# Title: apiModel.py
# Description: Uses AI API to generate responses
# Author(s): Yui 
# Date created: Mar 4, 2025
# Date modified: Mar 4, 2025
# ----------------------------------------------
import os
import sys
from groq import Groq

class apiModel:
    api_key = "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"  

    @staticmethod
    def generateResponse(prompt):
        if not api.api_key:
            print("Can't find the key.")
            sys.exit(1)
        
        # Initialize Groq client
        client = Groq(api_key=api.api_key)
        
        # Use the prompt passed to the function
        print(f"\nSending request to Groq (llama)...\n")
        
        try:
            # Send request to Groq API
            chat_completion = client.chat.completions.create(
                messages=[{
                    "role": "user",
                    "content": prompt,
                }],
                model="llama3-70b-8192",  # Specify the model you're using
            )
            
            # Extract and print the response
            response = chat_completion.choices[0].message.content
            print("AI Response:\n")
            print(response)
            
            return response  # Returning the response after printing it

        except Exception as e:
            print(f"Error communicating with Groq API: {e}")
            return None  # Return None if there's an error
    
