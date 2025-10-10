import os

class EnvConfigMeta(type):
    def __new__(cls, name, bases, namespace):
        new_class = super().__new__(cls, name, bases, namespace)
        
        if name != 'BaseConfig':
            for attr_name, attr_type in new_class.__annotations__.items():
                env_var = attr_name.upper()
                if env_var not in os.environ:
                    raise EnvironmentError(f"Required environment variable '{env_var}' is not set.")
                
                raw_value = os.environ[env_var]
                
                try:
                    if attr_type is int:
                        setattr(new_class, attr_name, int(raw_value))
                    elif attr_type is float:
                        setattr(new_class, attr_name, float(raw_value))
                    else:
                        setattr(new_class, attr_name, raw_value)
                except ValueError:
                    raise TypeError(f"Environment variable '{env_var}' cannot be converted to type {attr_type.__name__}.")
                    
        return new_class

class BaseConfig:
    pass

class AppConfig(BaseConfig, metaclass=EnvConfigMeta):
    HOST: str
    PORT: int
    TIMEOUT: float

if __name__ == '__main__':
    os.environ['HOST'] = '127.0.0.1'
    os.environ['PORT'] = '8080'
    os.environ['TIMEOUT'] = '5.5'
    
    try:
        config = AppConfig()
        print(f"Host: {config.HOST}, Port: {config.PORT}, Timeout: {config.TIMEOUT}")
    except Exception as e:
        print(e)