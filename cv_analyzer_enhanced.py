# cv_analyzer_enhanced.py
import time
import os
import pandas as pd
import matplotlib.pyplot as plt

class FileReader:
    """Simplified file reader for .docx files"""
    def read_file(self, file_path):
        try:
            # For .docx files, we'll use python-docx
            import docx
            doc = docx.Document(file_path)
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)
            return '\n'.join(full_text)
        except ImportError:
            # Fallback: read as text file
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return ""

class BruteForce:
    """Brute Force string search algorithm"""
    @staticmethod
    def search(text, pattern, case_sensitive=False):
        if not case_sensitive:
            text = text.lower()
            pattern = pattern.lower()
        
        n = len(text)
        m = len(pattern)
        comparisons = 0
        positions = []
        
        for i in range(n - m + 1):
            j = 0
            while j < m:
                comparisons += 1
                if text[i + j] != pattern[j]:
                    break
                j += 1
            if j == m:
                positions.append(i)
        
        return len(positions) > 0, positions, comparisons
    
    @staticmethod
    def search_multiple(text, patterns, case_sensitive=False):
        results = {}
        total_comparisons = 0
        
        for pattern in patterns:
            found, positions, comparisons = BruteForce.search(text, pattern, case_sensitive)
            total_comparisons += comparisons
            results[pattern] = {
                'found': found,
                'occurrences': len(positions),
                'positions': positions
            }
        
        return results, total_comparisons

class KMP:
    """Knuth-Morris-Pratt string search algorithm"""
    @staticmethod
    def build_lps(pattern):
        lps = [0] * len(pattern)
        length = 0
        i = 1
        
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps
    
    @staticmethod
    def search(text, pattern, case_sensitive=False):
        if not case_sensitive:
            text = text.lower()
            pattern = pattern.lower()
        
        if not pattern:
            return False, [], 0
        
        lps = KMP.build_lps(pattern)
        i = j = 0
        positions = []
        comparisons = 0
        n, m = len(text), len(pattern)
        
        while i < n:
            comparisons += 1
            if pattern[j] == text[i]:
                i += 1
                j += 1
            
            if j == m:
                positions.append(i - j)
                j = lps[j - 1]
            elif i < n and pattern[j] != text[i]:
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1
        
        return len(positions) > 0, positions, comparisons
    
    @staticmethod
    def search_multiple(text, patterns, case_sensitive=False):
        results = {}
        total_comparisons = 0
        
        for pattern in patterns:
            found, positions, comparisons = KMP.search(text, pattern, case_sensitive)
            total_comparisons += comparisons
            results[pattern] = {
                'found': found,
                'occurrences': len(positions),
                'positions': positions
            }
        
        return results, total_comparisons

class RabinKarp:
    """Rabin-Karp string search algorithm"""
    @staticmethod
    def search(text, pattern, case_sensitive=False):
        if not case_sensitive:
            text = text.lower()
            pattern = pattern.lower()
        
        d = 256  # number of characters in input alphabet
        q = 101  # prime number
        m = len(pattern)
        n = len(text)
        p_hash = 0  # hash value for pattern
        t_hash = 0  # hash value for text
        h = 1
        positions = []
        comparisons = 0
        
        # Calculate h = d^(m-1) % q
        for i in range(m - 1):
            h = (h * d) % q
        
        # Calculate initial hash values
        for i in range(m):
            p_hash = (d * p_hash + ord(pattern[i])) % q
            t_hash = (d * t_hash + ord(text[i])) % q
        
        # Slide the pattern over text
        for i in range(n - m + 1):
            comparisons += 1
            # Check hash values first
            if p_hash == t_hash:
                # Check characters one by one if hash matches
                match = True
                for j in range(m):
                    comparisons += 1
                    if text[i + j] != pattern[j]:
                        match = False
                        break
                
                if match:
                    positions.append(i)
            
            # Calculate hash for next window
            if i < n - m:
                t_hash = (d * (t_hash - ord(text[i]) * h) + ord(text[i + m])) % q
                if t_hash < 0:
                    t_hash += q
        
        return len(positions) > 0, positions, comparisons
    
    @staticmethod
    def search_multiple(text, patterns, case_sensitive=False):
        results = {}
        total_comparisons = 0
        
        for pattern in patterns:
            found, positions, comparisons = RabinKarp.search(text, pattern, case_sensitive)
            total_comparisons += comparisons
            results[pattern] = {
                'found': found,
                'occurrences': len(positions),
                'positions': positions
            }
        
        return results, total_comparisons

class EnhancedCVAnalyzer:
    """
    Enhanced CV Analyzer for .docx files with complete performance analysis
    """
    
    def __init__(self):
        self.file_reader = FileReader()
        self.algorithms = {
            'Brute Force': BruteForce,
            'KMP': KMP,
            'Rabin-Karp': RabinKarp
        }
    
    def load_job_description(self, job_file_path):
        """Load job description with lowercase conversion"""
        try:
            with open(job_file_path, 'r', encoding='utf-8') as file:
                job_text = file.read()
            keywords = [line.strip().lower() for line in job_text.split('\n') if line.strip()]
            return keywords
        except Exception as e:
            print(f"Error loading job description: {e}")
            return []
    
    def preprocess_text(self, text):
        """Basic text preprocessing"""
        if not text:
            return ""
        text = text.lower()
        return ' '.join(text.split())
    
    def calculate_similarity(self, matched_count, total_count):
        """Calculate match percentage"""
        if total_count == 0:
            return 0.0
        return (matched_count / total_count) * 100
    
    def analyze_cv(self, cv_file_path, job_keywords, algorithm_name='KMP', case_sensitive=False):
        """Analyze single CV with detailed metrics"""
        try:
            # Read only .docx files
            if not cv_file_path.lower().endswith('.docx'):
                return {'error': 'Not a .docx file'}
            
            # Read CV content
            cv_text = self.file_reader.read_file(cv_file_path)
            if not cv_text.strip():
                return {'error': 'Empty CV file', 'score': 0}
            
            # Preprocess text
            processed_text = self.preprocess_text(cv_text)
            
            # Get algorithm
            algorithm_class = self.algorithms.get(algorithm_name)
            if not algorithm_class:
                return {'error': f"Algorithm {algorithm_name} not found"}
            
            # Search for keywords with performance metrics
            start_time = time.time()
            results, total_comparisons = algorithm_class.search_multiple(
                processed_text, job_keywords, case_sensitive
            )
            end_time = time.time()
            
            execution_time = (end_time - start_time) * 1000  # Convert to ms
            
            # Calculate matches and score
            matched_count = 0
            matched_keywords = []
            missing_keywords = []
            
            for keyword, result in results.items():
                if result['found']:
                    matched_count += 1
                    matched_keywords.append({
                        'keyword': keyword,
                        'occurrences': result['occurrences'],
                        'positions': result['positions']
                    })
                else:
                    missing_keywords.append(keyword)
            
            score = self.calculate_similarity(matched_count, len(job_keywords))
            
            return {
                'cv_file': os.path.basename(cv_file_path),
                'algorithm': algorithm_name,
                'score': score,
                'matched_keywords': matched_keywords,
                'missing_keywords': missing_keywords,
                'total_keywords': len(job_keywords),
                'matched_count': matched_count,
                'execution_time_ms': execution_time,
                'total_comparisons': total_comparisons,
                'text_length': len(processed_text)
            }
            
        except Exception as e:
            return {'error': f"Error analyzing CV: {str(e)}", 'score': 0}
    
    def analyze_multiple_cvs(self, cv_directory, job_file_path, algorithm_name='KMP'):
        """Analyze multiple .docx CVs"""
        # Load job description
        job_keywords = self.load_job_description(job_file_path)
        if not job_keywords:
            return {"error": "No keywords found in job description"}
        
        print(f" ANALYZING .DOCX CVs FOR: {os.path.basename(job_file_path)}")
        print(f" Job Keywords: {', '.join(job_keywords)}")
        print(f" Algorithm: {algorithm_name}")
        print()
        
        # Get only .docx files
        cv_files = []
        for file in os.listdir(cv_directory):
            if file.lower().endswith('.docx'):
                cv_files.append(os.path.join(cv_directory, file))
        
        if not cv_files:
            return {"error": "No .docx CV files found"}
        
        print(f" Found {len(cv_files)} .docx CV files")
        print("=" * 70)
        
        # Analyze each CV
        results = []
        for cv_file in cv_files:
            print(f"Analyzing: {os.path.basename(cv_file)}")
            result = self.analyze_cv(cv_file, job_keywords, algorithm_name, case_sensitive=False)
            
            if 'error' not in result:
                results.append(result)
                print(f"   Score: {result['score']:.1f}% | "
                      f"Matches: {result['matched_count']}/{result['total_keywords']} | "
                      f"Time: {result['execution_time_ms']:.2f}ms")
            else:
                print(f"   Error: {result['error']}")
        
        # Sort by score
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            'job_description': os.path.basename(job_file_path),
            'keywords': job_keywords,
            'algorithm': algorithm_name,
            'total_cvs_analyzed': len(results),
            'results': results
        }
    
    def compare_algorithms_single_cv(self, cv_file_path, job_file_path):
        """Compare all 3 algorithms on a single CV"""
        job_keywords = self.load_job_description(job_file_path)
        if not job_keywords:
            return {"error": "No keywords found"}
        
        print(f" ALGORITHM COMPARISON ON: {os.path.basename(cv_file_path)}")
        print(f" Job: {os.path.basename(job_file_path)}")
        print("=" * 70)
        
        comparison_results = []
        
        for algo_name in self.algorithms.keys():
            print(f"\n Testing {algo_name}...")
            
            result = self.analyze_cv(cv_file_path, job_keywords, algo_name)
            
            if 'error' not in result:
                comparison_results.append({
                    'Algorithm': algo_name,
                    'Score (%)': result['score'],
                    'Matches': f"{result['matched_count']}/{result['total_keywords']}",
                    'Time (ms)': f"{result['execution_time_ms']:.2f}",
                    'Comparisons': result['total_comparisons'],
                    'Matched Keywords': [m['keyword'] for m in result['matched_keywords']],
                    'Missing Keywords': result['missing_keywords']
                })
                
                print(f"    Score: {result['score']:.1f}%")
                print(f"    Time: {result['execution_time_ms']:.2f} ms")
                print(f"    Comparisons: {result['total_comparisons']}")
                print(f"    Matches: {result['matched_count']}/{result['total_keywords']}")
            
            else:
                print(f"    Error: {result['error']}")
        
        return pd.DataFrame(comparison_results)
    
    def performance_analysis(self, cv_directory, job_file_path):
        """Complete performance analysis across all algorithms"""
        job_keywords = self.load_job_description(job_file_path)
        if not job_keywords:
            return {"error": "No keywords found"}
        
        # Get .docx files and categorize by size
        cv_files = [f for f in os.listdir(cv_directory) if f.lower().endswith('.docx')]
        if not cv_files:
            return {"error": "No .docx files found"}
        
        # Create results directory if it doesn't exist
        os.makedirs('data/results', exist_ok=True)
        
        performance_data = []
        
        # Test on a few files
        test_files = [os.path.join(cv_directory, f) for f in cv_files[:3]]  # Test on first 3 files
        
        print(" PERFORMANCE ANALYSIS")
        print("=" * 50)
        
        for cv_file in test_files:
            file_size = len(self.file_reader.read_file(cv_file))
            print(f"Testing: {os.path.basename(cv_file)} ({file_size} chars)")
            
            for algo_name in self.algorithms.keys():
                result = self.analyze_cv(cv_file, job_keywords, algo_name)
                if 'error' not in result:
                    performance_data.append({
                        'CV_File': os.path.basename(cv_file),
                        'File_Size_Chars': file_size,
                        'Algorithm': algo_name,
                        'Score_Percentage': result['score'],
                        'Execution_Time_ms': result['execution_time_ms'],
                        'Comparisons': result['total_comparisons']
                    })
        
        # Create performance DataFrame
        perf_df = pd.DataFrame(performance_data)
        
        # Save results
        perf_df.to_csv('data/results/performance_analysis.csv', index=False)
        
        return perf_df
    
    def generate_comprehensive_report(self, analysis_results, performance_df):
        """Generate detailed report"""
        if 'error' in analysis_results:
            print(f"Error: {analysis_results['error']}")
            return
        
        print("\n" + "=" * 80)
        print(" COMPREHENSIVE CV ANALYSIS REPORT")
        print("=" * 80)
        
        # Create results directory if it doesn't exist
        os.makedirs('data/results', exist_ok=True)
        
        # Save detailed results
        detailed_results = []
        for result in analysis_results['results']:
            detailed_results.append({
                'CV_File': result['cv_file'],
                'Score_Percentage': result['score'],
                'Matches_Count': result['matched_count'],
                'Total_Keywords': result['total_keywords'],
                'Execution_Time_ms': result['execution_time_ms'],
                'Comparisons': result['total_comparisons']
            })
        
        results_df = pd.DataFrame(detailed_results)
        results_df.to_csv('data/results/detailed_cv_analysis.csv', index=False)
        print(f"\n Detailed results saved to: data/results/detailed_cv_analysis.csv")
    
    def create_visualizations(self, performance_df):
        """Create comprehensive visualizations"""
        if performance_df is None or performance_df.empty:
            print(" No performance data available for visualizations")
            return
        
        # Create results directory if it doesn't exist
        os.makedirs('data/results', exist_ok=True)
        
        # Create figure
        plt.figure(figsize=(12, 8))
        
        # 1. Algorithm Comparison - Execution Time
        algo_times = performance_df.groupby('Algorithm')['Execution_Time_ms'].mean()
        
        plt.subplot(2, 2, 1)
        plt.bar(algo_times.index, algo_times.values, color=['red', 'blue', 'green'])
        plt.title('Average Execution Time by Algorithm')
        plt.ylabel('Time (milliseconds)')
        
        # 2. Algorithm Comparison - Character Comparisons
        plt.subplot(2, 2, 2)
        algo_comparisons = performance_df.groupby('Algorithm')['Comparisons'].mean()
        plt.bar(algo_comparisons.index, algo_comparisons.values, color=['red', 'blue', 'green'])
        plt.title('Average Character Comparisons by Algorithm')
        plt.ylabel('Number of Comparisons')
        
        # 3. File Size vs Execution Time
        plt.subplot(2, 2, 3)
        for algo in performance_df['Algorithm'].unique():
            algo_data = performance_df[performance_df['Algorithm'] == algo]
            plt.scatter(algo_data['File_Size_Chars'], algo_data['Execution_Time_ms'], 
                       label=algo, s=100, alpha=0.7)
        plt.title('File Size vs Execution Time')
        plt.xlabel('File Size (characters)')
        plt.ylabel('Execution Time (ms)')
        plt.legend()
        
        # 4. Scores by Algorithm
        plt.subplot(2, 2, 4)
        algo_scores = performance_df.groupby('Algorithm')['Score_Percentage'].mean()
        plt.bar(algo_scores.index, algo_scores.values, color=['red', 'blue', 'green'])
        plt.title('Average Score by Algorithm')
        plt.ylabel('Score (%)')
        
        plt.tight_layout()
        plt.savefig('data/results/performance_visualizations.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print(" Visualizations saved to: data/results/performance_visualizations.png")