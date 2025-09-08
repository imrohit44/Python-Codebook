def coin_change(coins, amount):
    """
    Computes the fewest number of coins needed to make up a given amount.

    Args:
        coins (list): A list of coin denominations.
        amount (int): The target amount.

    Returns:
        int: The minimum number of coins, or -1 if the amount cannot be made.
    """
    # dp[i] will store the minimum number of coins needed to make amount i
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # Base case: 0 coins needed for amount 0

    # Iterate through all amounts from 1 to the target amount
    for i in range(1, amount + 1):
        # For each amount, iterate through all available coin denominations
        for coin in coins:
            # If the current coin can be used to form the current amount
            if i - coin >= 0:
                # Update dp[i] with the minimum of its current value
                # and 1 + dp[i - coin] (representing using one coin and the solution for the remaining amount)
                dp[i] = min(dp[i], 1 + dp[i - coin])

    # If dp[amount] is still infinity, it means the amount cannot be made
    return dp[amount] if dp[amount] != float('inf') else -1

# Example Usage:
print("Coins: [1, 2, 5], Amount: 11 ->", coin_change([1, 2, 5], 11))  # Expected: 3 (5 + 5 + 1)
print("Coins: [2], Amount: 3 ->", coin_change([2], 3))            # Expected: -1
print("Coins: [1], Amount: 0 ->", coin_change([1], 0))            # Expected: 0
print("Coins: [186, 419, 83, 408], Amount: 6249 ->", coin_change([186, 419, 83, 408], 6249)) # Expected: 20
print("Coins: [3, 5], Amount: 7 ->", coin_change([3, 5], 7))        # Expected: -1 (3+3+1 not possible, 5+2 not possible)