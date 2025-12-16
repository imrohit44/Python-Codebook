class Maybe:
    """A simple Monad/Optional type for handling potential missing values."""
    def __init__(self, value):
        self._value = value
    
    @classmethod
    def unit(cls, value):
        return cls(value)
    
    def is_present(self):
        return self._value is not None
        
    def fmap(self, func):
        """Applies a function to the value only if it is present."""
        if self.is_present():
            return Maybe.unit(func(self._value))
        return self
    
    def bind(self, func):
        """Applies a function that returns another Maybe instance."""
        if self.is_present():
            return func(self._value)
        return self

def safe_divide(x, y):
    if y == 0:
        return Maybe.unit(None)
    return Maybe.unit(x / y)

def square(x):
    return x * x

if __name__ == '__main__':
    # Successful computation
    m1 = Maybe.unit(10)
    result1 = m1.fmap(lambda x: x + 5).fmap(square)
    print(f"Result 1: {result1._value}")

    # Handling a potential division by zero using bind
    m2 = Maybe.unit(100)
    result2 = m2.bind(lambda x: safe_divide(x, 10)).fmap(lambda x: x * 2)
    print(f"Result 2: {result2._value}")

    # Failure case
    m3 = Maybe.unit(100)
    result3 = m3.bind(lambda x: safe_divide(x, 0)).fmap(lambda x: x * 2)
    print(f"Result 3: {result3._value}")