from abc import abstractmethod

class InterfaceEnforcer(type):
    """
    A metaclass that enforces the implementation of abstract methods.
    If a method in the base class is decorated with @abstractmethod,
    any concrete subclass must implement it.
    """
    def __new__(cls, name, bases, dct):
        # Create the new class normally first
        new_class = super().__new__(cls, name, bases, dct)

        # Check for abstract methods in base classes that were not implemented
        # in the new_class (dct contains methods defined in new_class itself)
        
        # Iterate through all base classes (including the class itself)
        for base in bases + (new_class,):
            for attr_name, attr_value in base.__dict__.items():
                # Check if it's an abstract method from abstractmethod decorator
                if hasattr(attr_value, '__isabstractmethod__') and attr_value.__isabstractmethod__:
                    # Check if the method exists in the newly created class's dictionary
                    # and if it's not still the abstract placeholder.
                    # We check `attr_name in dct` because `dct` contains the methods
                    # directly defined in the current class being created.
                    # If it's not in `dct`, it means the subclass didn't define it.
                    if attr_name not in dct or getattr(new_class, attr_name) is attr_value:
                        raise TypeError(
                            f"Can't instantiate abstract class {name} with abstract method "
                            f"'{attr_name}' not implemented."
                        )
        return new_class

# --- Example Usage ---

# Define an interface using the custom metaclass
class ILogger(metaclass=InterfaceEnforcer):
    @abstractmethod
    def log_info(self, message: str):
        pass

    @abstractmethod
    def log_error(self, message: str, error_code: int):
        pass

    def common_method(self):
        print("This is a common method in the interface.")

# Valid implementation
class FileLogger(ILogger):
    def __init__(self, filename="app.log"):
        self.filename = filename
        print(f"FileLogger initialized for {self.filename}")

    def log_info(self, message: str):
        with open(self.filename, 'a') as f:
            f.write(f"[INFO] {message}\n")
        print(f"Logged INFO: {message}")

    def log_error(self, message: str, error_code: int):
        with open(self.filename, 'a') as f:
            f.write(f"[ERROR] (Code {error_code}) {message}\n")
        print(f"Logged ERROR (Code {error_code}): {message}")

# Invalid implementation (missing log_error)
class ConsoleLogger(ILogger):
    def log_info(self, message: str):
        print(f"Console INFO: {message}")
    # Missing log_error implementation

# Another invalid implementation (missing both)
class IncompleteLogger(ILogger):
    pass # No methods implemented

if __name__ == "__main__":
    print("--- Testing Valid Implementation (FileLogger) ---")
    file_logger = FileLogger("my_logs.txt")
    file_logger.log_info("Application started.")
    file_logger.log_error("Critical error!", 500)
    file_logger.common_method()

    print("\n--- Testing Invalid Implementation (ConsoleLogger) ---")
    try:
        # This should raise a TypeError because log_error is not implemented
        console_logger = ConsoleLogger()
        console_logger.log_info("This should not be reached.")
    except TypeError as e:
        print(f"Caught expected error: {e}")

    print("\n--- Testing Another Invalid Implementation (IncompleteLogger) ---")
    try:
        # This should raise a TypeError because both are not implemented
        incomplete_logger = IncompleteLogger()
    except TypeError as e:
        print(f"Caught expected error: {e}")

    # Clean up the log file created by FileLogger
    import os
    if os.path.exists("my_logs.txt"):
        os.remove("my_logs.txt")