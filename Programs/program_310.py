def levenshtein_distance(s1, s2):
    m = len(s1)
    n = len(s2)
    
    # Initialize DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
        
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if s1[i-1] == s2[j-1] else 1
            
            dp[i][j] = min(
                dp[i-1][j] + 1,       # Deletion
                dp[i][j-1] + 1,       # Insertion
                dp[i-1][j-1] + cost   # Substitution
            )
            
    return dp[m][n]

if __name__ == '__main__':
    word1 = "kitten"
    word2 = "sitting"
    print(f"Distance between '{word1}' and '{word2}': {levenshtein_distance(word1, word2)}")
    
    word3 = "flaw"
    word4 = "lawn"
    print(f"Distance between '{word3}' and '{word4}': {levenshtein_distance(word3, word4)}")