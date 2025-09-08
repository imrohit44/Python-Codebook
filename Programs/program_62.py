class MockDatabase:
    def __init__(self):
        self.data = {}
        self.counter = {}

    def get_next_id(self, table):
        self.counter.setdefault(table, 0)
        self.counter[table] += 1
        return self.counter[table]

    def save(self, table, record):
        record['id'] = self.get_next_id(table)
        self.data.setdefault(table, {})
        self.data[table][record['id']] = record
        return record

    def find(self, table, id):
        return self.data.get(table, {}).get(id)

    def delete(self, table, id):
        if table in self.data and id in self.data[table]:
            del self.data[table][id]
            return True
        return False

db = MockDatabase()

class Model(type):
    def __new__(cls, name, bases, namespace):
        new_class = super().__new__(cls, name, bases, namespace)
        
        if name != 'Model':
            new_class._table_name = name.lower()
            
            def save(self):
                record = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
                saved_record = db.save(self._table_name, record)
                self.id = saved_record['id']
                
            def find(cls, id):
                record = db.find(cls._table_name, id)
                if record:
                    obj = cls.__new__(cls)
                    obj.__dict__.update(record)
                    return obj
                return None
            
            def delete(self):
                if hasattr(self, 'id'):
                    db.delete(self._table_name, self.id)
            
            new_class.save = save
            new_class.find = classmethod(find)
            new_class.delete = delete
            
        return new_class

class User(metaclass=Model):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.id = None

class Product(metaclass=Model):
    def __init__(self, title, price):
        self.title = title
        self.price = price
        self.id = None

if __name__ == "__main__":
    user1 = User("Alice", "alice@example.com")
    user1.save()
    print(f"Saved user: {user1.__dict__}")
    
    found_user = User.find(user1.id)
    print(f"Found user: {found_user.__dict__}")

    product1 = Product("Laptop", 1200)
    product1.save()
    print(f"Saved product: {product1.__dict__}")

    product1.delete()
    found_product = Product.find(product1.id)
    print(f"Found product after deletion: {found_product}")