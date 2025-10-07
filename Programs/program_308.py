import abc
import inspect

class PluginMeta(abc.ABCMeta):
    _registry = {}

    def __new__(mcls, name, bases, namespace):
        cls = super().__new__(mcls, name, bases, namespace)
        
        if name != 'BasePlugin' and not inspect.isabstract(cls):
            abstract_methods = getattr(cls, '__abstractmethods__', set())
            if abstract_methods:
                raise TypeError(f"Cannot instantiate concrete class '{name}' with unimplemented abstract methods: {abstract_methods}")
            
            cls._registry[name] = cls
            
        return cls

class BasePlugin(metaclass=PluginMeta):
    @abc.abstractmethod
    def configure(self, config):
        pass

    @abc.abstractmethod
    def execute(self, data):
        pass

class FileProcessor(BasePlugin):
    def configure(self, config):
        self.config = config

    def execute(self, data):
        return f"Processed {len(data)} bytes via {self.__class__.__name__}"

class NetworkAdapter(BasePlugin):
    def configure(self, config):
        self.endpoint = config['endpoint']

    def execute(self, data):
        return f"Sent data to {self.endpoint}"

if __name__ == '__main__':
    processor = PluginMeta._registry['FileProcessor']({'path': '/tmp'})
    adapter = PluginMeta._registry['NetworkAdapter']({'endpoint': 'http://api.local'})

    print(processor.execute(b'test_data'))
    print(adapter.execute(b'network_data'))