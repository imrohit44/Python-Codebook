class SingletonFactory(type):
    _instances = {}
    _registry = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        
        def create_instance(name):
            if name not in cls._registry:
                cls._registry[name] = cls()
            return cls._registry[name]
            
        cls.create = create_instance

class Service(metaclass=SingletonFactory):
    def __init__(self):
        self.name = random.choice(['A', 'B', 'C'])

class Logger(Service):
    def __init__(self):
        super().__init__()

class Database(Service):
    def __init__(self):
        super().__init__()

if __name__ == '__main__':
    logger1 = Logger.create('logger1')
    logger2 = Logger.create('logger1')
    print(logger1 is logger2)
    print(logger1.name, logger2.name)
    
    db1 = Database.create('db1')
    db2 = Database.create('db2')
    print(db1 is db2)
    print(db1.name, db2.name)