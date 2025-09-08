class temporarily_patch:
    def __init__(self, obj, method_name, new_method):
        self.obj = obj
        self.method_name = method_name
        self.new_method = new_method
        self.original_method = None

    def __enter__(self):
        self.original_method = getattr(self.obj, self.method_name)
        setattr(self.obj, self.method_name, self.new_method)
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        setattr(self.obj, self.method_name, self.original_method)

class Service:
    def execute(self, task):
        return f"Executing {task} normally."

def mock_execute(self, task):
    return f"Executing {task} with a mock."

if __name__ == "__main__":
    svc = Service()
    print(svc.execute("Task A"))

    with temporarily_patch(svc, 'execute', mock_execute):
        print(svc.execute("Task B"))

    print(svc.execute("Task C"))