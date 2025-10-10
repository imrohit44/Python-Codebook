def solve_newton(func, derivative, x0, tolerance=1e-7, max_iterations=100):
    x = x0
    for i in range(max_iterations):
        fx = func(x)
        fpx = derivative(x)
        
        if abs(fpx) < 1e-10:
            raise ValueError("Derivative is near zero. Cannot converge.")
            
        x_next = x - fx / fpx
        
        if abs(x_next - x) < tolerance:
            return x_next
            
        x = x_next
        
    return x

if __name__ == '__main__':
    # Function: f(x) = x^2 - 4
    def f(x):
        return x**2 - 4
    
    # Derivative: f'(x) = 2x
    def fp(x):
        return 2 * x

    root = solve_newton(f, fp, x0=1.0)
    print(f"Root of x^2 - 4: {root}")