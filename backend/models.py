from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# This creates a "Base" that all our models will follow.
Base = declarative_base()

class User(Base):
    """
    We create a class named User. This will become a table in your database.
    """
    __tablename__ = 'users'

    # Every user gets a unique ID number so the database doesn't get them confused.
    id = Column(Integer, primary_key=True)

    # This creates a space for the user's name as text.
    name = Column(String)

    # Adding username and password_hash for full functionality
    username = Column(String, unique=True)
    password_hash = Column(String)

    # This stores the email and ensures no two people can use the same one.
    email = Column(String, unique=True)
