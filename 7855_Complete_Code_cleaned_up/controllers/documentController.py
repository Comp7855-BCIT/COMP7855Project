# ----------------------------------------------
# Title: documentController.py
# Description: Resume and cover letter document controller ***This section has not been tested***
# Author(s): Jasmine 
# Date created: Mar 7, 2025
# Date modified: Mar 8, 2025
# ----------------------------------------------

from flask import render_template, request, redirect, url_for
from models.documentModel import DocumentModel

class DocumentController:

    # Returns pdfkit configuration using DocumentModel's configure_pdfkit method.
    @staticmethod
    def configure_pdfkit():
        config = DocumentModel.configure_pdfkit()
        return config

    # Generates a PDF from the resume HTML by calling DocumentModel.
    @staticmethod
    def generate_pdf_from_resume(userId, jobId):
        resumepdf = DocumentModel.generate_pdf_from_resume(userId, jobId)
        return resumepdf

    # Generates a PDF from the cover letter HTML by calling DocumentModel.
    @staticmethod
    def generate_pdf_from_cover(userId, jobId):
        cvpdf = DocumentModel.generate_pdf_from_cover(userId, jobId)
        return cvpdf

    # Retrieves resume HTML content for a user and job.
    @staticmethod
    def get_resume(userId, jobId):
        resume = DocumentModel.get_resume(userId, jobId)
        return resume

    # Retrieves cover letter HTML content for a user and job.
    @staticmethod
    def get_cover_letter(userId, jobId):
        cv = DocumentModel.get_cover_letter(userId, jobId)
        return cv

    # Downloads the resume as a PDF file.
    @staticmethod
    def downloadResumePdf(userId, jobId):
        """
        Downloads the resume as a PDF.
        """
        resumeHtml = DocumentModel.getResume(userId, jobId)
        if not resumeHtml:
            return None

        # Sanitize the resume HTML content.
        sanitizedHtml = DocumentModel.sanitizeHtml(resumeHtml)
        # Construct the output file name.
        outputFile = f"resume_{userId}_{jobId}.pdf"
        # Generate the PDF and return the file path if successful.
        if DocumentModel.generatePdf(sanitizedHtml, outputFile):
            return outputFile
        return None

    # Downloads the cover letter as a PDF file.
    @staticmethod
    def downloadCoverLetterPdf(userId, jobId):
        """
        Downloads the cover letter as a PDF.
        """
        coverLetterHtml = DocumentModel.getCoverLetter(userId, jobId)
        if not coverLetterHtml:
            return None

        # Sanitize the cover letter HTML content.
        sanitizedHtml = DocumentModel.sanitizeHtml(coverLetterHtml)
        # Construct the output file name.
        outputFile = f"cover_letter_{userId}_{jobId}.pdf"
        # Generate the PDF and return the file path if successful.
        if DocumentModel.generatePdf(sanitizedHtml, outputFile):
            return outputFile
        return None

    # Downloads the resume as a Word document.
    @staticmethod
    def downloadResumeWord(userId, jobId, documentModel):
        """
        Downloads the resume as a Word document.
        """
        resumeHtml = DocumentModel.getResume(userId, jobId)
        if not resumeHtml:
            return None

        # Sanitize the resume HTML content.
        sanitizedHtml = DocumentModel.sanitizeHtml(resumeHtml)
        # Construct the output file name.
        outputFile = f"resume_{userId}_{jobId}.docx"
        # Generate the Word document and return the file path if successful.
        if DocumentModel.generateWord(sanitizedHtml, outputFile):
            return outputFile
        return None

    # Downloads the cover letter as a Word document.
    @staticmethod
    def downloadCoverLetterWord(userId, jobId):
        """
        Downloads the cover letter as a Word document.
        """
        coverLetterHtml = DocumentModel.getCoverLetter(userId, jobId)
        if not coverLetterHtml:
            return None

        # Sanitize the cover letter HTML content.
        sanitizedHtml = DocumentModel.sanitizeHtml(coverLetterHtml)
        # Construct the output file name.
        outputFile = f"cover_letter_{userId}_{jobId}.docx"
        # Generate the Word document and return the file path if successful.
        if DocumentModel.generateWord(sanitizedHtml, outputFile):
            return outputFile
        return None