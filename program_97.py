import inspect

class Container:
    def __init__(self):
        self._services = {}
    
    def register(self, service_type, instance):
        self._services[service_type] = instance
    
    def get(self, service_type):
        return self._services.get(service_type)

GLOBAL_CONTAINER = Container()

class Service:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        
        sig = inspect.signature(cls.__init__)
        params = sig.parameters
        
        dependencies = {}
        for name, param in params.items():
            if name != 'self' and param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
                dep_type = param.annotation
                if dep_type is not inspect.Parameter.empty:
                    dependencies[name] = dep_type
        
        cls._dependencies = dependencies

    def __new__(cls, *args, **kwargs):
        deps_to_inject = {}
        for name, dep_type in cls._dependencies.items():
            instance = GLOBAL_CONTAINER.get(dep_type)
            if instance:
                deps_to_inject[name] = instance
        
        return super().__new__(cls)

    def __init__(self, **kwargs):
        for name, instance in self._dependencies.items():
            setattr(self, name, instance)

class Logger:
    def log(self, message):
        print(f"LOG: {message}")

class Database:
    def query(self, sql):
        return f"Executing {sql}"

class UserService(Service):
    def __init__(self, logger: Logger, db: Database):
        self.logger = logger
        self.db = db

    def create_user(self, name):
        self.logger.log(f"Creating user {name}")
        self.db.query(f"INSERT INTO users VALUES ({name})")

if __name__ == '__main__':
    GLOBAL_CONTAINER.register(Logger, Logger())
    GLOBAL_CONTAINER.register(Database, Database())

    user_service = UserService(logger=GLOBAL_CONTAINER.get(Logger), db=GLOBAL_CONTAINER.get(Database))
    user_service.create_user("Alice")