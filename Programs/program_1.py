'''
A concise way to create lists
'''
# a) Squares of numbers
squares = [x**2 for x in range(1, 11)]
print("Squares:", squares)

# b) Filter even numbers
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = [x for x in numbers if x % 2 == 0]
print("Evens:", evens)