# no 


# === FIXED CV ANALYZER ===
import time
import os
import pandas as pd
from file_reader import FileReader
from utils.text_processor import TextProcessor
from algorithms.brute_force import BruteForce
from algorithms.kmp import KMP
from algorithms.rabin_karp import RabinKarp

class FixedCVAnalyzer:
    """
    FIXED CV Analyzer system
    """
    
    def __init__(self):
        self.file_reader = FileReader()
        self.text_processor = TextProcessor()
        self.algorithms = {
            'Brute Force': BruteForce,
            'KMP': KMP,
            'Rabin-Karp': RabinKarp
        }
    
    def load_job_description(self, job_file_path):
        """Load job description with lowercase conversion"""
        try:
            job_text = self.file_reader.read_file(job_file_path)
            keywords = [line.strip().lower() for line in job_text.split('\n') if line.strip()]
            return keywords
        except Exception as e:
            print(f"Error loading job description: {e}")
            return []
    
    def analyze_cv(self, cv_file_path, job_keywords, algorithm_name='KMP', case_sensitive=False):
        """Fixed CV analysis"""
        try:
            # Read CV content
            cv_text = self.file_reader.read_file(cv_file_path)
            if not cv_text.strip():
                return {
                    'error': f"Empty CV: {cv_file_path}",
                    'score': 0,
                    'matched_count': 0,
                    'total_keywords': len(job_keywords)
                }
            
            # Preprocess text
            processed_text = self.text_processor.preprocess_text(cv_text)
            
            # Get algorithm
            algorithm_class = self.algorithms.get(algorithm_name)
            if not algorithm_class:
                return {'error': f"Algorithm {algorithm_name} not found"}
            
            # Search for keywords
            start_time = time.time()
            results, total_comparisons = algorithm_class.search_multiple(
                processed_text, job_keywords, case_sensitive
            )
            end_time = time.time()
            
            execution_time = (end_time - start_time) * 1000
            
            # Count matches - FIXED LOGIC
            matched_count = 0
            matched_keywords_list = []
            
            for keyword, result in results.items():
                if result['found']:
                    matched_count += 1
                    matched_keywords_list.append(keyword)
            
            # Calculate score - FIXED: using counts, not lists
            score = self.text_processor.calculate_similarity(matched_count, len(job_keywords))
            
            return {
                'cv_file': os.path.basename(cv_file_path),
                'algorithm': algorithm_name,
                'score': score,
                'matched_keywords': matched_keywords_list,
                'missing_keywords': [k for k in job_keywords if k not in matched_keywords_list],
                'total_keywords': len(job_keywords),
                'matched_count': matched_count,
                'execution_time_ms': execution_time,
                'total_comparisons': total_comparisons
            }
            
        except Exception as e:
            return {
                'error': f"Error analyzing CV: {str(e)}",
                'score': 0,
                'matched_count': 0,
                'total_keywords': len(job_keywords)
            }
    
    def analyze_multiple_cvs(self, cv_directory, job_file_path, algorithm_name='KMP', case_sensitive=False):
        """Analyze multiple CVs"""
        # Load job description
        job_keywords = self.load_job_description(job_file_path)
        if not job_keywords:
            return {"error": "No keywords found"}
        
        print(f" Analyzing CVs for: {os.path.basename(job_file_path)}")
        print(f" Keywords: {len(job_keywords)} skills")
        print(f" Algorithm: {algorithm_name}")
        print()
        
        # Get CV files
        cv_files = []
        for file in os.listdir(cv_directory):
            if file.lower().endswith(('.pdf', '.docx', '.txt')):
                cv_files.append(os.path.join(cv_directory, file))
        
        if not cv_files:
            return {"error": "No CV files found"}
        
        print(f" Found {len(cv_files)} CV files")
        print("=" * 60)
        
        # Analyze each CV
        results = []
        for cv_file in cv_files[:10]:  # Test with first 10 CVs first
            result = self.analyze_cv(cv_file, job_keywords, algorithm_name, case_sensitive)
            if 'error' not in result:
                results.append(result)
                print(f" {os.path.basename(cv_file)}: {result['score']:.1f}% ({result['matched_count']}/{result['total_keywords']})")
            else:
                print(f" {os.path.basename(cv_file)}: {result['error']}")
        
        # Sort by score
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            'job_description': os.path.basename(job_file_path),
            'keywords': job_keywords,
            'algorithm': algorithm_name,
            'total_cvs_analyzed': len(results),
            'results': results
        }

# Create fixed analyzer
fixed_analyzer = FixedCVAnalyzer()
print("  CV ANALYZER READY!")

#CV Files (.pdf, .docx) → File Reader → Text Processing → Algorithm Search → Scoring → Ranking