def longest_palindromic_substring(s):
    n = len(s)
    dp = [[False] * n for _ in range(n)]
    longest = ""

    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if i == j:
                dp[i][j] = True
            elif s[i] == s[j]:
                if j - i == 1:
                    dp[i][j] = True
                else:
                    dp[i][j] = dp[i + 1][j - 1]
            
            if dp[i][j] and j - i + 1 > len(longest):
                longest = s[i:j+1]

    return longest

if __name__ == '__main__':
    s1 = "babad"
    print(f"Longest palindromic substring of '{s1}' is '{longest_palindromic_substring(s1)}'")
    
    s2 = "cbbd"
    print(f"Longest palindromic substring of '{s2}' is '{longest_palindromic_substring(s2)}'")