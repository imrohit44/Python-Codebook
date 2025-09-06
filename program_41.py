def word_break(s, wordDict):
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    word_set = set(wordDict)

    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    
    return dp[n]

if __name__ == "__main__":
    s1 = "leetcode"
    dict1 = ["leet", "code"]
    print(word_break(s1, dict1))

    s2 = "applepenapple"
    dict2 = ["apple", "pen"]
    print(word_break(s2, dict2))

    s3 = "catsandog"
    dict3 = ["cats", "dog", "sand", "and", "cat"]
    print(word_break(s3, dict3))

    s4 = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab"
    dict4 = ["a", "aa", "aaa", "aaaa", "aaaaa", "aaaaaa", "aaaaaaa", "aaaaaaaa", "aaaaaaaaa", "aaaaaaaaaa"]
    print(word_break(s4, dict4))