# no
import time
import matplotlib.pyplot as plt
import pandas as pd
from algorithms.brute_force import BruteForce
from algorithms.kmp import KMP
from algorithms.rabin_karp import RabinKarp

class PerformanceAnalyzer:
    """
    Analyzes performance of different string matching algorithms
    """
    
    @staticmethod
    def analyze_single_pattern(text, pattern, case_sensitive=False):
        """
        Analyze performance for single pattern search
        """
        algorithms = [
            ("Brute Force", BruteForce),
            ("KMP", KMP), 
            ("Rabin-Karp", RabinKarp)
        ]
        
        results = []
        
        for algo_name, algo_class in algorithms:
            # Measure time
            start_time = time.time()
            found, positions, comparisons = algo_class.search(text, pattern, case_sensitive)
            end_time = time.time()
            
            execution_time = (end_time - start_time) * 1000  # ms
            
            results.append({
                'algorithm': algo_name,
                'found': found,
                'positions': positions,
                'occurrences': len(positions),
                'comparisons': comparisons,
                'time_ms': execution_time
            })
        
        return results
    
    @staticmethod
    def analyze_multiple_patterns(text, patterns, case_sensitive=False):
        """
        Analyze performance for multiple pattern search
        """
        algorithms = [
            ("Brute Force", BruteForce),
            ("KMP", KMP),
            ("Rabin-Karp", RabinKarp)
        ]
        
        results = []
        
        for algo_name, algo_class in algorithms:
            # Measure time
            start_time = time.time()
            results_dict, total_comparisons = algo_class.search_multiple(text, patterns, case_sensitive)
            end_time = time.time()
            
            execution_time = (end_time - start_time) * 1000  # ms
            
            # Count matches
            matched_count = sum(1 for result in results_dict.values() if result['found'])
            match_percentage = (matched_count / len(patterns)) * 100
            
            results.append({
                'algorithm': algo_name,
                'time_ms': execution_time,
                'total_comparisons': total_comparisons,
                'patterns_found': matched_count,
                'total_patterns': len(patterns),
                'match_percentage': match_percentage
            })
        
        return results
    
    @staticmethod
    def create_comparison_chart(results, title="Algorithm Comparison"):
        """
        Create visualization comparing algorithm performance
        """
        df = pd.DataFrame(results)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Time comparison
        ax1.bar(df['algorithm'], df['time_ms'], color=['red', 'blue', 'green'])
        ax1.set_title(f'{title} - Execution Time')
        ax1.set_ylabel('Time (milliseconds)')
        ax1.set_xlabel('Algorithm')
        
        # Comparison count
        ax2.bar(df['algorithm'], df['total_comparisons'], color=['red', 'blue', 'green'])
        ax2.set_title(f'{title} - Character Comparisons')
        ax2.set_ylabel('Number of Comparisons')
        ax2.set_xlabel('Algorithm')
        
        plt.tight_layout()
        plt.show()
        
        return df

# Test the performance analyzer
if __name__ == "__main__":
    # Sample test
    analyzer = PerformanceAnalyzer()
    sample_text = "This is a sample text for testing algorithms. Python, Java, SQL, Machine Learning."
    patterns = ["Python", "Java", "SQL", "Machine Learning", "C++"]
    
    results = analyzer.analyze_multiple_patterns(sample_text, patterns)
    df = analyzer.create_comparison_chart(results)
    print(df)