'''
Small, anonymous functions defined with the lambda keyword. Often used with map(), filter(), sorted()
'''

# a) Doubling numbers with map
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
print("Doubled numbers:", doubled)

# b) Filtering numbers with filter
filtered = list(filter(lambda x: x > 5, [1, 7, 3, 9, 2, 8]))
print("Filtered numbers ( > 5):", filtered)

# Using lambda for sorting (e.g., list of tuples by second element)
students = [('Alice', 25), ('Bob', 20), ('Charlie', 30)]
sorted_students = sorted(students, key=lambda student: student[1])
print("Sorted Students by Age:", sorted_students)