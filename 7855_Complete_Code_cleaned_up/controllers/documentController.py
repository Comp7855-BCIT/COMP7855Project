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

#configure_pdfkit()
#generate_pdf_from_resume(userId, jobId)
#generate_pdf_from_cover(userId, jobId)
#get_resume(userId, jobId)
#get_cover_letter(userId, jobId)
    @staticmethod
    def configure_pdfkit():
        config = DocumentModel.configure_pdfkit()
        return config
    @staticmethod
    def generate_pdf_from_resume(userId, jobId):
        resumepdf = DocumentModel.generate_pdf_from_resume(userId, jobId)
        return resumepdf
    @staticmethod
    def generate_pdf_from_cover(userId, jobId):
        cvpdf = DocumentModel.generate_pdf_from_cover(userId, jobId)
        return cvpdf
    @staticmethod
    def get_resume(userId, jobId):
        resume = DocumentModel.get_resume(userId, jobId)
        return resume
    @staticmethod
    def get_cover_letter(userId, jobId):
        cv = DocumentModel.get_cover_letter(userId, jobId)
        return cv
    @staticmethod
    def downloadResumePdf(userId, jobId):
        """
        Downloads the resume as a PDF.
        """
        resumeHtml = DocumentModel.getResume(userId, jobId)
        if not resumeHtml:
            return None

        sanitizedHtml = DocumentModel.sanitizeHtml(resumeHtml)
        outputFile = f"resume_{userId}_{jobId}.pdf"
        if DocumentModel.generatePdf(sanitizedHtml, outputFile):
            return outputFile
        return None

    @staticmethod
    def downloadCoverLetterPdf(userId, jobId):
        """
        Downloads the cover letter as a PDF.
        """
        coverLetterHtml = DocumentModel.getCoverLetter(userId, jobId)
        if not coverLetterHtml:
            return None

        sanitizedHtml = DocumentModel.sanitizeHtml(coverLetterHtml)
        outputFile = f"cover_letter_{userId}_{jobId}.pdf"
        if DocumentModel.generatePdf(sanitizedHtml, outputFile):
            return outputFile
        return None

    @staticmethod
    def downloadResumeWord(userId, jobId, documentModel):
        """
        Downloads the resume as a Word document.
        """
        resumeHtml = DocumentModel.getResume(userId, jobId)
        if not resumeHtml:
            return None

        sanitizedHtml = DocumentModel.sanitizeHtml(resumeHtml)
        outputFile = f"resume_{userId}_{jobId}.docx"
        if DocumentModel.generateWord(sanitizedHtml, outputFile):
            return outputFile
        return None

    @staticmethod
    def downloadCoverLetterWord(userId, jobId):
        """
        Downloads the cover letter as a Word document.
        """
        coverLetterHtml = DocumentModel.getCoverLetter(userId, jobId)
        if not coverLetterHtml:
            return None

        sanitizedHtml = DocumentModel.sanitizeHtml(coverLetterHtml)
        outputFile = f"cover_letter_{userId}_{jobId}.docx"
        if DocumentModel.generateWord(sanitizedHtml, outputFile):
            return outputFile
        return None

