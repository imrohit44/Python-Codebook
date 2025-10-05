import time

def infinite_data_generator():
    i = 0
    while True:
        yield i
        i += 1

class TimeWindowedStream:
    def __init__(self, generator, window_seconds):
        self.generator = generator
        self.window_seconds = window_seconds
        
    def __iter__(self):
        return self

    def __next__(self):
        window_start = time.time()
        window_data = []
        
        while time.time() < window_start + self.window_seconds:
            try:
                item = next(self.generator)
                window_data.append(item)
            except StopIteration:
                if not window_data:
                    raise StopIteration
                return window_data
            
        if not window_data:
            raise StopIteration
            
        return window_data

if __name__ == '__main__':
    data_stream = TimeWindowedStream(infinite_data_generator(), window_seconds=1.0)
    
    for i, window in enumerate(data_stream):
        if i >= 3:
            break
        print(f"Window {i}: {len(window)} items (First: {window[0]}, Last: {window[-1]})")