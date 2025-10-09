'''
# Command-Line Interface (CLI) Tool with argparse

Professional command-line tools parse arguments gracefully. This program uses the standard argparse library to create a simple file utility that can count lines, words, or characters in a file, similar to the wc command on Linux.

Concepts: CLI application structure, argument parsing, optional and positional arguments.

**How to Run**

**1. Save the code and execute it:**

```
python Program_11.py
```
'''

import argparse
import sys

def count_file_stats(filepath, mode):
    """Counts lines, words, or characters in a given file."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            if mode == 'lines':
                return len(content.splitlines())
            elif mode == 'words':
                return len(content.split())
            elif mode == 'chars':
                return len(content)
    except FileNotFoundError:
        print(f"Error: File not found at '{filepath}'", file=sys.stderr)
        sys.exit(1)

def main():
    # 1. Initialize the parser
    parser = argparse.ArgumentParser(
        description="A simple file statistics tool, similar to wc.",
        epilog="Enjoy using the tool!"
    )

    # 2. Add a positional argument (the file to analyze)
    parser.add_argument("filepath", help="Path to the file to be analyzed.")

    # 3. Add an optional argument to specify the mode
    parser.add_argument(
        "-m", "--mode",
        choices=['lines', 'words', 'chars'],
        default='lines',
        help="The counting mode (default: lines)."
    )

    # 4. Parse the arguments from the command line
    args = parser.parse_args()

    # 5. Run the main logic
    count = count_file_stats(args.filepath, args.mode)
    print(f"The file '{args.filepath}' has {count} {args.mode}.")

if __name__ == "__main__":
    main()