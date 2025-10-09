'''
# Database Management with SQLAlchemy ORM

This program uses SQLAlchemy, a powerful Object-Relational Mapper (ORM), to interact with a SQLite database. Instead of writing raw SQL, you define Python classes (models) that map to database tables, allowing you to manage records as Python objects.

Concepts: Object-Relational Mapping (ORM), database sessions, data persistence.

**How to Run**

**1. Save the code and execute it:**

```
python Program_8.py
```
'''

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Define the base class for our models
Base = declarative_base()

# Define the User model, which maps to a 'users' table
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"

# --- Database Setup ---
# Create an in-memory SQLite database for this example.
# For a persistent file, use: 'sqlite:///mydatabase.db'
engine = create_engine('sqlite:///:memory:')

# Create the table(s) in the database based on the models
Base.metadata.create_all(engine)

# Create a session factory to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# --- Main Logic ---
def manage_database():
    # 1. Add new users (Create)
    print("--- Adding new users ---")
    user1 = User(name='Alice', email='alice@example.com')
    user2 = User(name='Bob', email='bob@example.com')
    session.add(user1)
    session.add(user2)
    session.commit()
    print("Users added successfully.")

    # 2. Query users (Read)
    print("\n--- Querying all users ---")
    all_users = session.query(User).all()
    for user in all_users:
        print(user)

    # 3. Update a user
    print("\n--- Updating a user ---")
    user_to_update = session.query(User).filter_by(name='Alice').first()
    if user_to_update:
        user_to_update.email = 'alice.smith@example.com'
        session.commit()
        print(f"Updated user: {user_to_update}")

    # 4. Delete a user
    print("\n--- Deleting a user ---")
    user_to_delete = session.query(User).filter_by(name='Bob').first()
    if user_to_delete:
        session.delete(user_to_delete)
        session.commit()
        print(f"Deleted user with name: Bob")
    
    # Verify deletion
    print("\n--- Final list of users ---")
    final_users = session.query(User).all()
    for user in final_users:
        print(user)

    # Close the session
    session.close()

if __name__ == "__main__":
    manage_database()