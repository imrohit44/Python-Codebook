def longest_palindromic_subsequence(s):
    n = len(s)
    dp = [[0] * n for _ in range(n)]

    for i in range(n):
        dp[i][i] = 1
    
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j] and length == 2:
                dp[i][j] = 2
            elif s[i] == s[j]:
                dp[i][j] = 2 + dp[i + 1][j - 1]
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
                
    return dp[0][n - 1]

if __name__ == '__main__':
    s1 = "agbcba"
    print(f"Longest palindromic subsequence of '{s1}' is {longest_palindromic_subsequence(s1)}")
    
    s2 = "bbabcbcab"
    print(f"Longest palindromic subsequence of '{s2}' is {longest_palindromic_subsequence(s2)}")