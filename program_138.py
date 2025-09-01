def cut_rod(prices, n):
    dp = [0] * (n + 1)
    
    for i in range(1, n + 1):
        max_val = -1
        for j in range(i):
            if j < len(prices):
                max_val = max(max_val, prices[j] + dp[i - j - 1])
        dp[i] = max_val
        
    return dp[n]

if __name__ == '__main__':
    prices = [1, 5, 8, 9, 10, 17, 17, 20]
    n = 8
    print(cut_rod(prices, n))