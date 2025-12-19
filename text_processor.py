# no


# src/utils/text_processor.py - Text preprocessing utilities

import re
import string

class TextProcessor:
    """
    Handles text preprocessing for CV analysis
    """
    
    @staticmethod
    def preprocess_text(text):
        """
        Basic text preprocessing: lowercase and remove extra whitespace
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    @staticmethod
    def clean_text(text):
        """
        More aggressive text cleaning
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace and newlines
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    @staticmethod
    def extract_sentences(text):
        """
        Basic sentence extraction
        """
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    @staticmethod
    def calculate_similarity(matched_keywords_count, total_keywords_count):
        """
        Calculate match percentage - FIXED VERSION
        """
        if total_keywords_count == 0:
            return 0.0
        return (matched_keywords_count / total_keywords_count) * 100

print(" FIXED Text processor created!")