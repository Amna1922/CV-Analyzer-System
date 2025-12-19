# no 

import time

class KMP:
    """
    Knuth-Morris-Pratt string matching algorithm implementation
    """
    
    @staticmethod
    def compute_lps(pattern):
        """
        Compute Longest Prefix Suffix (LPS) array for the pattern
        
        Args:
            pattern (str): The pattern to compute LPS for
            
        Returns:
            list: LPS array
        """
        m = len(pattern)
        lps = [0] * m
        length = 0  # length of the previous longest prefix suffix
        i = 1
        
        while i < m:
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
        """
        Search for pattern in text using KMP algorithm
        
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
        
        # Preprocess the pattern
        lps = KMP.compute_lps(pattern)
        
        i = 0  # index for text
        j = 0  # index for pattern
        
        while i < n:
            comparisons += 1
            if pattern[j] == text[i]:
                i += 1
                j += 1
            
            if j == m:
                positions.append(i - j)
                j = lps[j - 1]
            elif i < n and pattern[j] != text[i]:
                comparisons += 1
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1
        
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
            found, positions, comparisons = KMP.search(text, pattern, case_sensitive)
            results[pattern] = {
                'found': found,
                'positions': positions,
                'occurrences': len(positions),
                'comparisons': comparisons
            }
            total_comparisons += comparisons
        
        return results, total_comparisons

# Test function
def test_kmp():
    """Test the KMP algorithm"""
    text = "ABABDABACDABABCABAB"
    pattern = "ABABC"
    
    print("🧪 Testing KMP Algorithm:")
    print(f"Text: {text}")
    print(f"Pattern: {pattern}")
    
    found, positions, comparisons = KMP.search(text, pattern)
    
    print(f"Found: {found}")
    print(f"Positions: {positions}")
    print(f"Comparisons: {comparisons}")
    
    # Test LPS computation
    lps = KMP.compute_lps(pattern)
    print(f"LPS array for '{pattern}': {lps}")
    print(" KMP test completed!\n")

if __name__ == "__main__":
    test_kmp()