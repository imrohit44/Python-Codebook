'''
# Memory-Efficient Large File Processing with Generators

When dealing with massive files, loading the entire file into memory can cause your program to crash. This program demonstrates how to use a generator to process a large (simulated) CSV file line-by-line, consuming very little memory.

Concepts: Generators, yield keyword, lazy evaluation, memory efficiency.

**How to Run**

**1. Save the code and execute it:**

```
python Program_9.py
```
'''

import csv
import os

def create_large_csv(filename="large_log.csv", rows=1_000_000):
    """Helper function to create a large dummy CSV file."""
    print(f"Creating a large dummy CSV file with {rows} rows...")
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'level', 'message'])
        for i in range(rows):
            level = "ERROR" if i % 100 == 0 else "INFO"
            writer.writerow([f"2025-10-09T14:{i%60:02d}:{i%60:02d}", level, f"Log message number {i}"])
    print("Dummy file created.")

def process_log_file(filename):
    """
    A generator function that reads a log file line-by-line
    and yields only the rows that represent errors.
    """
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header row
        for row in reader:
            if row[1] == 'ERROR':
                # yield pauses the function and returns a value,
                # resuming from here on the next call.
                yield row

if __name__ == "__main__":
    csv_file = "large_log.csv"
    create_large_csv(csv_file)

    print("\n--- Processing file to find all ERROR entries ---")
    error_count = 0
    # The file is read line-by-line, not all at once.
    # This is extremely memory-efficient.
    for error_log in process_log_file(csv_file):
        if error_count < 5: # Print first 5 errors found
            print(f"Found error: {error_log}")
        error_count += 1
    
    print(f"\nTotal errors found: {error_count}")

    # Clean up the large file
    os.remove(csv_file)
    print(f"Cleaned up {csv_file}.")