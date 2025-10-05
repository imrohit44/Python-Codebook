class MockTracker:
    def __init__(self, original_method):
        self.call_count = 0
        self.original_method = original_method

    def __call__(self, *args, **kwargs):
        self.call_count += 1
        return None

class DynamicMock:
    def __init__(self, target_instance, method_name):
        self.target = target_instance
        self.method_name = method_name
        self.original = None
        self.mock_tracker = None

    def __enter__(self):
        self.original = getattr(self.target, self.method_name)
        self.mock_tracker = MockTracker(self.original)
        
        setattr(self.target, self.method_name, self.mock_tracker)
        return self.mock_tracker

    def __exit__(self, exc_type, exc_val, exc_tb):
        setattr(self.target, self.method_name, self.original)

class ProductionService:
    def process_data(self, data):
        return f"Processing {data}"

if __name__ == '__main__':
    svc = ProductionService()
    
    with DynamicMock(svc, 'process_data') as mock:
        svc.process_data(1)
        svc.process_data(2)
        print(f"Mock was called: {mock.call_count} times.")
    
    print(f"Original method call after restore: {svc.process_data(3)}")