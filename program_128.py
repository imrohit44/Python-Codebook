def count_change(coins, amount):
    dp = [0] * (amount + 1)
    dp[0] = 1
    
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]
            
    return dp[amount]

if __name__ == '__main__':
    coins1 = [1, 2, 5]
    amount1 = 5
    print(count_change(coins1, amount1))
    
    coins2 = [2, 3, 5]
    amount2 = 10
    print(count_change(coins2, amount2))