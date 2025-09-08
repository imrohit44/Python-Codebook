def longest_common_substring(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    max_length = 0
    end_index = 0
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
                if dp[i][j] > max_length:
                    max_length = dp[i][j]
                    end_index = i
            else:
                dp[i][j] = 0
                
    start_index = end_index - max_length
    return max_length, s1[start_index:end_index]

if __name__ == '__main__':
    s1 = "abacaba"
    s2 = "abacax"
    length, substr = longest_common_substring(s1, s2)
    print(f"Longest common substring of '{s1}' and '{s2}': length={length}, substring='{substr}'")

    s3 = "abcde"
    s4 = "xyzab"
    length, substr = longest_common_substring(s3, s4)
    print(f"Longest common substring of '{s3}' and '{s4}': length={length}, substring='{substr}'")