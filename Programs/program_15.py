import os

def smart_walk(root_dir, include_files=True, include_dirs=False, extensions=None, min_size_kb=0):
    """
    Walks a directory tree and yields file/directory paths based on specified criteria.

    Args:
        root_dir (str): The starting directory to walk.
        include_files (bool): Whether to yield file paths.
        include_dirs (bool): Whether to yield directory paths.
        extensions (list/tuple, optional): A list/tuple of file extensions to include
                                          (e.g., ('.txt', '.log')). Case-insensitive.
                                          If None, all file extensions are allowed.
        min_size_kb (float): Minimum file size in kilobytes (inclusive).

    Yields:
        str: File or directory paths matching the criteria.
    """
    min_size_bytes = min_size_kb * 1024

    # Convert extensions to lowercase for case-insensitive comparison
    if extensions:
        extensions = tuple(ext.lower() for ext in extensions)

    for dirpath, dirnames, filenames in os.walk(root_dir):
        if include_dirs:
            for dirname in dirnames:
                yield os.path.join(dirpath, dirname)

        if include_files:
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)

                # Check extension
                if extensions:
                    _, ext = os.path.splitext(filename)
                    if ext.lower() not in extensions:
                        continue

                # Check file size
                try:
                    if os.path.getsize(full_path) < min_size_bytes:
                        continue
                except OSError:
                    # Handle cases where file might be inaccessible or doesn't exist anymore
                    continue

                yield full_path

# Example Usage:
if __name__ == "__main__":
    # Create a dummy directory structure for testing
    test_dir = "temp_walk_test"
    os.makedirs(test_dir, exist_ok=True)
    os.makedirs(os.path.join(test_dir, "subdir1"), exist_ok=True)
    os.makedirs(os.path.join(test_dir, "subdir2", "nested"), exist_ok=True)

    with open(os.path.join(test_dir, "file1.txt"), "w") as f: f.write("Hello")
    with open(os.path.join(test_dir, "file2.log"), "w") as f: f.write("Log content")
    with open(os.path.join(test_dir, "large_file.bin"), "wb") as f: f.write(os.urandom(2000)) # 2KB
    with open(os.path.join(test_dir, "small.csv"), "w") as f: f.write("1,2,3") # ~5 bytes
    with open(os.path.join(test_dir, "subdir1", "subfile.txt"), "w") as f: f.write("Another text")
    with open(os.path.join(test_dir, "subdir2", "image.JPG"), "w") as f: f.write("fake image")

    print("--- All files and directories ---")
    for path in smart_walk(test_dir, include_files=True, include_dirs=True):
        print(path)

    print("\n--- Only .txt files ---")
    for path in smart_walk(test_dir, extensions=('.txt',)):
        print(path)

    print("\n--- .log and .csv files larger than 0.001KB (~1 byte) ---")
    for path in smart_walk(test_dir, extensions=('.log', '.csv'), min_size_kb=0.001):
        print(path)
        
    print("\n--- Files larger than 1.5KB ---")
    for path in smart_walk(test_dir, min_size_kb=1.5):
        print(path)

    print("\n--- Only directories ---")
    for path in smart_walk(test_dir, include_files=False, include_dirs=True):
        print(path)

    # Clean up dummy directory
    import shutil
    shutil.rmtree(test_dir)