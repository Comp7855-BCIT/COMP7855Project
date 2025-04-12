# ----------------------------------------------
# Title: documentModel.py
# Description: Resume and cover letter document model ***This section has not been tested***
# Author(s): Jasmine, Yui
# Date created: Mar 7, 2025
# Date modified: Mar 8, 2025
# ----------------------------------------------
import sqlite3
import pdfkit
from docx import Document
from bs4 import BeautifulSoup
import bleach
import os
import sys

class DocumentModel:
    @staticmethod
    def get_resume(userId, jobId):
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT resume FROM resume 
                WHERE userId = ? AND jobId = ?
            """, (userId, jobId))
            
            result = cursor.fetchone()
            conn.close()
            
            return result[0] if result else None
        except Exception as e:
            print(f"Error getting resume: {e}")
            return None
    @staticmethod
    def get_cover_letter(userId, jobId):
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT coverLetter FROM coverLetter
                WHERE userId = ? AND jobId = ?
            """, (userId, jobId))
            
            result = cursor.fetchone()
            conn.close()
            
            return result[0] if result else None
        except Exception as e:
            print(f"Error getting cover letter: {e}")
            return None

    @staticmethod
    def generate_pdf_from_resume(userId, jobId, output_path=None):
        """
        Generates a PDF from the resume in the database
        Returns the path to the generated PDF or None if failed
        """
        resume_html = DocumentModel.get_resume(userId, jobId)
        if not resume_html:
            return None

        # Create a temporary file if no output path provided
        if not output_path:
            import tempfile
            output_path = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False).name

        config = DocumentModel.configure_pdfkit()
        if not config:
            return None

        try:
            options = {
                'encoding': 'UTF-8',
                'quiet': '',
                'margin-top': '0.5in',
                'margin-right': '0.5in',
                'margin-bottom': '0.5in',
                'margin-left': '0.5in',
            }
            
            pdfkit.from_string(resume_html, output_path, configuration=config, options=options)
            return output_path
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return None
    @staticmethod
    def generate_pdf_from_cover(userId, jobId, output_path=None):
        """
        Generates a PDF from the resume in the database
        Returns the path to the generated PDF or None if failed
        """
        cover_letter_html = DocumentModel.get_cover_letter(userId, jobId)
        if not cover_letter_html:
            return None

        # Create a temporary file if no output path provided
        if not output_path:
            import tempfile
            output_path = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False).name

        config = DocumentModel.configure_pdfkit()
        if not config:
            return None

        try:
            options = {
                'encoding': 'UTF-8',
                'quiet': '',
                'margin-top': '0.5in',
                'margin-right': '0.5in',
                'margin-bottom': '0.5in',
                'margin-left': '0.5in',
            }
            
            pdfkit.from_string(cover_letter_html, output_path, configuration=config, options=options)
            return output_path
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return None
    
    @staticmethod  
    def saveResume(userId, jobId, resumeHtml):
        pass
    #Saves the resume HTML to the database.
    
    @staticmethod
    def saveCoverLetter(userId, jobId, coverLetterHtml):
        pass
    #Saves the cover letter HTML to the database.
    


    @staticmethod
    def getCoverLetter(userId, jobId):
        pass
    #Retrieves the cover letter HTML from the database for a specific user and job.   
    @staticmethod
    def configure_pdfkit():
        #Configure pdfkit with the path to wkhtmltopdf
        # Set the path to wkhtmltopdf based on your OS
        if sys.platform == "win32":
            # Windows path - update this to match your installation
            wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

        
        # Check if the file exists
        if os.path.exists(wkhtmltopdf_path):
            print(f"Using wkhtmltopdf at: {wkhtmltopdf_path}")
            # Configure pdfkit with the path
            config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
            return config
        else:
            print("wkhtmltopdf executable not found at the default location.")
            print("Please install wkhtmltopdf from: https://wkhtmltopdf.org/downloads.html")
            print("After installation, update the path in this script.")
            return None

    @staticmethod
    def generatePdf(htmlContent, outputFile):
        """
        Converts HTML content to a PDF file using pdfkit.
        """
        try:
            pdfkit.from_string(htmlContent, outputFile)
            return True
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return False

    @staticmethod
    def generateWord(htmlContent, outputFile):
        """
        Converts HTML content to a Word document.
        """
        try:
            soup = BeautifulSoup(htmlContent, 'html.parser')
            doc = Document()
            for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'ul', 'li']):
                if element.name == 'p':
                    doc.add_paragraph(element.text)
                elif element.name.startswith('h'):
                    doc.add_heading(element.text, level=int(element.name[1]))
                elif element.name == 'ul':
                    for li in element.find_all('li'):
                        doc.add_paragraph(li.text, style='ListBullet')
            doc.save(outputFile)
            return True
        except Exception as e:
            print(f"Error generating Word document: {e}")
            return False

    @staticmethod
    def sanitizeHtml(htmlContent):
        """
        Sanitizes HTML content to remove potentially harmful elements.
        """
        allowedTags = ['p', 'h1', 'h2', 'h3', 'ul', 'li', 'b', 'i', 'a']
        return bleach.clean(htmlContent, tags=allowedTags)
    
    @staticmethod
    def previewPdf(htmlContent):
        """
        Generates a PDF preview of the HTML content and returns the file path.
        """
        sanitizedHtml = DocumentModel.sanitizeHtml(htmlContent)
        outputFile = "preview.pdf"
        if DocumentModel.generatePdf(sanitizedHtml, outputFile):
            return outputFile
        return None

