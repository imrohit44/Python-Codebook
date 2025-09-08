import abc

class ComponentMeta(abc.ABCMeta):
    _registry = {}
    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        if name != 'Component' and not inspect.isabstract(cls):
            cls._registry[name.lower()] = cls

class Component(metaclass=ComponentMeta):
    @abc.abstractmethod
    def __init__(self, config):
        pass

    @abc.abstractmethod
    def run(self):
        pass

class DataProcessor(Component):
    def __init__(self, config):
        self.source = config.get('source')
    def run(self):
        return f"Processing data from {self.source}"

class FileLogger(Component):
    def __init__(self, config):
        self.filename = config.get('filename')
    def run(self):
        return f"Logging to file {self.filename}"

class Factory:
    def create_component(self, name, config):
        cls = ComponentMeta._registry.get(name.lower())
        if cls:
            return cls(config)
        raise ValueError(f"Component '{name}' not found.")

if __name__ == '__main__':
    factory = Factory()
    
    processor_config = {'source': 'database'}
    processor = factory.create_component('DataProcessor', processor_config)
    print(processor.run())
    
    logger_config = {'filename': 'app.log'}
    logger = factory.create_component('FileLogger', logger_config)
    print(logger.run())

    try:
        factory.create_component('NetworkService', {})
    except ValueError as e:
        print(e)