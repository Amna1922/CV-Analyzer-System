# no 

import time

class BruteForce:
    """
    Brute Force string matching algorithm implementation
    """
    
    @staticmethod
    def search(text, pattern, case_sensitive=False):
        """
        Search for pattern in text using Brute Force algorithm
        
        Args:
            text (str): The text to search in
            pattern (str): The pattern to search for
            case_sensitive (bool): Whether search should be case sensitive
            
        Returns:
            tuple: (found, positions, comparisons)
        """
        if not text or not pattern:
            return False, [], 0
            
        if not case_sensitive:
            text = text.lower()
            pattern = pattern.lower()
        
        n = len(text)
        m = len(pattern)
        positions = []
        comparisons = 0
        
        for i in range(n - m + 1):
            j = 0
            while j < m:
                comparisons += 1
                if text[i + j] != pattern[j]:
                    break
                j += 1
            
            if j == m:  # Pattern found
                positions.append(i)
        
        return len(positions) > 0, positions, comparisons
    
    @staticmethod
    def search_multiple(text, patterns, case_sensitive=False):
        """
        Search for multiple patterns in text
        
        Args:
            text (str): The text to search in
            patterns (list): List of patterns to search for
            case_sensitive (bool): Whether search should be case sensitive
            
        Returns:
            dict: Results for each pattern
        """
        results = {}
        total_comparisons = 0
        
        for pattern in patterns:
            found, positions, comparisons = BruteForce.search(text, pattern, case_sensitive)
            results[pattern] = {
                'found': found,
                'positions': positions,
                'occurrences': len(positions),
                'comparisons': comparisons
            }
            total_comparisons += comparisons
        
        return results, total_comparisons

# Test function
def test_brute_force():
    """Test the Brute Force algorithm"""
    text = "ABABDABACDABABCABAB"
    pattern = "ABABC"
    
    print(" Testing Brute Force Algorithm:")
    print(f"Text: {text}")
    print(f"Pattern: {pattern}")
    
    found, positions, comparisons = BruteForce.search(text, pattern)
    
    print(f"Found: {found}")
    print(f"Positions: {positions}")
    print(f"Comparisons: {comparisons}")
    print(" Brute Force test completed!\n")

if __name__ == "__main__":
    test_brute_force()