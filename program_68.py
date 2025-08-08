_PLUGIN_REGISTRY = {}

class BasePlugin:
    def __init_subclass__(cls, name, required_methods=None, **kwargs):
        super().__init_subclass__(**kwargs)
        
        if name in _PLUGIN_REGISTRY:
            raise ValueError(f"Plugin name '{name}' is already registered.")
        
        _PLUGIN_REGISTRY[name] = cls
        
        if required_methods:
            for method_name in required_methods:
                if not hasattr(cls, method_name) or not callable(getattr(cls, method_name)):
                    raise TypeError(f"Subclass {name} must implement method '{method_name}'.")

class DataProcessor(BasePlugin, name='data_processor', required_methods=['process']):
    def process(self, data):
        return [d * 2 for d in data]

class DataFilter(BasePlugin, name='data_filter', required_methods=['filter']):
    def filter(self, data):
        return [d for d in data if d > 5]

class InvalidPlugin(BasePlugin, name='invalid_plugin', required_methods=['process']):
    pass

if __name__ == "__main__":
    try:
        processor = _PLUGIN_REGISTRY['data_processor']()
        print(processor.process([1, 2, 3]))
        
        filter = _PLUGIN_REGISTRY['data_filter']()
        print(filter.filter([1, 6, 3, 8]))
        
        invalid = _PLUGIN_REGISTRY['invalid_plugin']
        print(invalid)
    except TypeError as e:
        print(f"Caught expected error: {e}")