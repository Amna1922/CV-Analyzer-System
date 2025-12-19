# no

#%%writefile src/algorithms/rabin_karp.py

import time

class RabinKarp:
    """
    Rabin-Karp string matching algorithm implementation
    """
    
    @staticmethod
    def search(text, pattern, case_sensitive=False, prime=101):
        """
        Search for pattern in text using Rabin-Karp algorithm
        
        Args:
            text (str): The text to search in
            pattern (str): The pattern to search for
            case_sensitive (bool): Whether search should be case sensitive
            prime (int): A prime number for hash calculation
            
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
        
        if m > n:
            return False, [], 0
        
        # Calculate hash values
        pattern_hash = 0
        text_hash = 0
        h = 1
        
        # The value of h would be "pow(d, m-1) % prime"
        d = 256  # Number of characters in the input alphabet
        
        for i in range(m - 1):
            h = (h * d) % prime
        
        # Calculate initial hash values
        for i in range(m):
            pattern_hash = (d * pattern_hash + ord(pattern[i])) % prime
            text_hash = (d * text_hash + ord(text[i])) % prime
        
        # Slide the pattern over text one by one
        for i in range(n - m + 1):
            # Check the hash values first
            if pattern_hash == text_hash:
                # Check characters one by one if hash matches
                match = True
                for j in range(m):
                    comparisons += 1
                    if text[i + j] != pattern[j]:
                        match = False
                        break
                
                if match:
                    positions.append(i)
            
            # Calculate hash value for next window of text
            if i < n - m:
                text_hash = (d * (text_hash - ord(text[i]) * h) + ord(text[i + m])) % prime
                
                # We might get negative value of text_hash, converting it to positive
                if text_hash < 0:
                    text_hash = text_hash + prime
        
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
            found, positions, comparisons = RabinKarp.search(text, pattern, case_sensitive)
            results[pattern] = {
                'found': found,
                'positions': positions,
                'occurrences': len(positions),
                'comparisons': comparisons
            }
            total_comparisons += comparisons
        
        return results, total_comparisons

# Test function
def test_rabin_karp():
    """Test the Rabin-Karp algorithm"""
    text = "ABABDABACDABABCABAB"
    pattern = "ABABC"
    
    print("🧪 Testing Rabin-Karp Algorithm:")
    print(f"Text: {text}")
    print(f"Pattern: {pattern}")
    
    found, positions, comparisons = RabinKarp.search(text, pattern)
    
    print(f"Found: {found}")
    print(f"Positions: {positions}")
    print(f"Comparisons: {comparisons}")
    print(" Rabin-Karp test completed!\n")

if __name__ == "__main__":
    test_rabin_karp()