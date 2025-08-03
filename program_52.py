class AutoFactory(type):
    _registry = {}

    def __new__(cls, name, bases, namespace):
        new_class = super().__new__(cls, name, bases, namespace)
        
        for base in bases:
            if isinstance(base, AutoFactory):
                base._registry[new_class.__name__] = new_class
        
        return new_class

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        
        if len(bases) > 0 and isinstance(bases[0], AutoFactory):
            def create(cls_to_create, *args, **kwargs):
                return cls_to_create(*args, **kwargs)

            for registered_name, registered_cls in cls._registry.items():
                factory_method_name = f"create_{registered_name.lower()}"
                def factory_method(self, *args, **kwargs):
                    return create(registered_cls, *args, **kwargs)
                setattr(cls, factory_method_name, factory_method)

class AbstractProductFactory(metaclass=AutoFactory):
    pass

class ConcreteProductA(AbstractProductFactory):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"ProductA({self.value})"

class ConcreteProductB(AbstractProductFactory):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"ProductB({self.name})"

if __name__ == "__main__":
    factory = AbstractProductFactory()
    
    product_a = factory.create_concreteproducta(10)
    print(product_a)

    product_b = factory.create_concreteproductb("test")
    print(product_b)