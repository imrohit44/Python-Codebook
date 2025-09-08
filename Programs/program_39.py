import threading

class Singleton(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]

class DatabaseConnection(metaclass=Singleton):
    def __init__(self, db_name):
        self.db_name = db_name

    def connect(self):
        return f"Connecting to {self.db_name}"

class Logger(metaclass=Singleton):
    def __init__(self, log_file):
        self.log_file = log_file

    def write_log(self, message):
        with open(self.log_file, 'a') as f:
            f.write(message + '\n')

if __name__ == "__main__":
    db1 = DatabaseConnection('prod_db')
    db2 = DatabaseConnection('dev_db')
    print(db1 is db2)
    print(db1.db_name)
    print(db2.db_name)

    log1 = Logger('app.log')
    log2 = Logger('test.log')
    print(log1 is log2)
    log1.write_log("Log from instance 1.")
    log2.write_log("Log from instance 2.")