class Registry:
    def __init__(self):
        self._classes = {}
    
    def register(self, name, cls):
        self._classes[name] = cls
    
    def get(self, name):
        return self._classes.get(name)

GLOBAL_REGISTRY = Registry()

class RegisteredClass(type):
    def __new__(cls, name, bases, namespace):
        new_class = super().__new__(cls, name, bases, namespace)
        
        registry_name = namespace.get('_registry_name', name)
        GLOBAL_REGISTRY.register(registry_name, new_class)
        
        return new_class

class PluginA(metaclass=RegisteredClass):
    def run(self):
        return "Plugin A is running."

class PluginB(metaclass=RegisteredClass):
    _registry_name = 'my_plugin_b'
    
    def run(self):
        return "Plugin B is running."

if __name__ == "__main__":
    plugin_a_class = GLOBAL_REGISTRY.get("PluginA")
    if plugin_a_class:
        instance_a = plugin_a_class()
        print(instance_a.run())

    plugin_b_class = GLOBAL_REGISTRY.get("my_plugin_b")
    if plugin_b_class:
        instance_b = plugin_b_class()
        print(instance_b.run())

    unknown_plugin = GLOBAL_REGISTRY.get("PluginB")
    print(unknown_plugin)