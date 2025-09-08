def matrix_chain_multiplication(dims):
    n = len(dims) - 1
    dp = [[0] * n for _ in range(n)]

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')
            for k in range(i, j):
                cost = dp[i][k] + dp[k+1][j] + dims[i] * dims[k+1] * dims[j+1]
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    
    return dp[0][n-1]

if __name__ == '__main__':
    dims = [10, 20, 30, 40]
    min_ops = matrix_chain_multiplication(dims)
    print(f"Minimum scalar multiplications: {min_ops}")