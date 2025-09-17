def find_all_subsets(nums, target):
    dp = [[] for _ in range(target + 1)]
    dp[0] = [[]]
    
    for num in nums:
        for t in range(target, num - 1, -1):
            for subset in dp[t - num]:
                dp[t].append(subset + [num])
    
    return dp[target]

if __name__ == '__main__':
    nums = [1, 2, 3, 4]
    target = 5
    subsets = find_all_subsets(nums, target)
    print(f"Subsets of {nums} that sum to {target}: {subsets}")