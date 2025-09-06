class Configurable:
    _config_schema = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not isinstance(cls._config_schema, dict):
            raise TypeError("'_config_schema' must be a dictionary.")

    def __init__(self, config):
        for key, expected_type in self._config_schema.items():
            if key not in config:
                raise ValueError(f"Missing required config key: '{key}'")
            if not isinstance(config[key], expected_type):
                raise TypeError(f"Config key '{key}' must be of type {expected_type.__name__}, got {type(config[key]).__name__}")
            setattr(self, key, config[key])

class DatabaseConfig(Configurable):
    _config_schema = {
        'host': str,
        'port': int,
        'database': str
    }

class ServerConfig(Configurable):
    _config_schema = {
        'host': str,
        'port': int
    }

if __name__ == '__main__':
    db_config = DatabaseConfig({'host': 'localhost', 'port': 5432, 'database': 'app_db'})
    print(f"DB host: {db_config.host}, port: {db_config.port}")
    
    try:
        invalid_db_config = DatabaseConfig({'host': 'localhost', 'port': '5432', 'database': 'app_db'})
    except TypeError as e:
        print(e)