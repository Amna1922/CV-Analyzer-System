#no

# src/file_reader.py - Handles reading different file formats

import PyPDF2
import pdfplumber
from docx import Document
import os

class FileReader:
    """
    Handles reading text from various file formats (PDF, DOCX, TXT)
    """
    
    @staticmethod
    def read_pdf_pypdf2(file_path):
        """
        Read PDF using PyPDF2
        """
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            print(f"Error reading PDF with PyPDF2: {e}")
            return ""
    
    @staticmethod
    def read_pdf_pdfplumber(file_path):
        """
        Read PDF using pdfplumber (more accurate)
        """
        try:
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
            return text
        except Exception as e:
            print(f"Error reading PDF with pdfplumber: {e}")
            return ""
    
    @staticmethod
    def read_docx(file_path):
        """
        Read DOCX file
        """
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            print(f"Error reading DOCX: {e}")
            return ""
    
    @staticmethod
    def read_txt(file_path):
        """
        Read plain text file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading TXT: {e}")
            return ""
    
    @staticmethod
    def read_file(file_path):
        """
        Universal file reader that detects file type and uses appropriate method
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.pdf':
            # Try pdfplumber first, fall back to PyPDF2
            text = FileReader.read_pdf_pdfplumber(file_path)
            if not text.strip():
                text = FileReader.read_pdf_pypdf2(file_path)
            return text
        elif file_ext == '.docx':
            return FileReader.read_docx(file_path)
        elif file_ext == '.txt':
            return FileReader.read_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")

print(" File reader module created!")