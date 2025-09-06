class MockDatabase:
    def __init__(self):
        self.data = {}
    
    def execute(self, query):
        print(f"Executing SQL: {query}")
        return []

class QuerySet:
    def __init__(self, model_class, db_connection):
        self.model_class = model_class
        self.db = db_connection
        self._filters = []

    def filter(self, **kwargs):
        for field, value in kwargs.items():
            self._filters.append(f"{field} = '{value}'")
        return self

    def all(self):
        query = f"SELECT * FROM {self.model_class.__name__.lower()}"
        if self._filters:
            query += " WHERE " + " AND ".join(self._filters)
        return self.db.execute(query)

    def first(self):
        query = f"SELECT * FROM {self.model_class.__name__.lower()}"
        if self._filters:
            query += " WHERE " + " AND ".join(self._filters)
        query += " LIMIT 1"
        results = self.db.execute(query)
        return results[0] if results else None

class Model:
    def __init__(self, db_connection):
        self.db = db_connection

    def objects(self):
        return QuerySet(self.__class__, self.db)

class User(Model):
    def __init__(self, db_connection, name, email):
        super().__init__(db_connection)
        self.name = name
        self.email = email

if __name__ == '__main__':
    mock_db = MockDatabase()
    
    user_query = User(mock_db).objects().filter(name='Alice', age=30)
    user_query.all()
    
    user_query.filter(is_active=True).first()