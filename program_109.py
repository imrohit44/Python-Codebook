def longest_increasing_subsequence(arr):
    if not arr:
        return 0
    
    n = len(arr)
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if arr[i] > arr[j]:
                dp[i] = max(dp[i], dp[j] + 1)
                
    return max(dp)

if __name__ == '__main__':
    arr1 = [10, 9, 2, 5, 3, 7, 101, 18]
    print(f"LIS length of {arr1} is {longest_increasing_subsequence(arr1)}")
    
    arr2 = [0, 1, 0, 3, 2, 3]
    print(f"LIS length of {arr2} is {longest_increasing_subsequence(arr2)}")