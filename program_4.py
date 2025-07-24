'''
Functions that return an iterator that produces a sequence of results on the fly, instead of building a whole list in memory. Use yield keyword.
'''

def fibonacci_generator(n):
    a, b = 0, 1
    count = 0
    while count < n:
        yield a
        a, b = b, a + b
        count += 1

# Using the generator
fib_sequence = fibonacci_generator(10)
print("Fibonacci sequence (generator):")
for num in fib_sequence:
    print(num, end=" ")
print()

# Another way to consume:
# print(list(fibonacci_generator(7)))