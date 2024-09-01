import pytest
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from fastapi.testclient import TestClient
import requests

# ---- SETUPBASE SQL DB ------

# Load environment variables from .env file
load_dotenv()

# Retrieve variables from environment
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')


Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    email = Column("email", String, primary_key=True)

    def __init__(self, email):
        self.email = email

    # for printing User objects
    def __repr__(self):
        return f"{self.email}"

class Movie(Base):
    __tablename__ = "movies"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name",String, nullable=False)
    description = Column("description", String, nullable=False)
    imageUrl = Column("imageUrl", String, nullable=False)

    # owner = Column(Integer, ForeignKey("people.ssn"))

    def __init__(self, name, description, imageUrl):
        self.name = name
        self.description = description
        self.imageUrl = imageUrl

    def __repr__(self):
        return f"({self.id}) {self.name}"


class Rating(Base):
    __tablename__ = "ratings"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    userEmail = Column(String, ForeignKey("users.email"), nullable=False)  # Reference to User.email
    movieId = Column(Integer, ForeignKey("movies.id"), nullable=False)
    rating = Column("rating", Integer, nullable=True)

    def __init__(self, userEmail, movieId, rating):
        self.userEmail = userEmail
        self.movieId = movieId
        self.rating = rating

    def __repr__(self):
        return f"({self.userEmail}) ({self.movieId}) {self.rating}"

TEST_DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

@pytest.fixture(scope="function")
def db_session():

    # Create an engine to the test database
    engine = create_engine(TEST_DATABASE_URL)

    # Use scoped_session to ensure thread safety
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

    # Create all tables
    Base.metadata.create_all(engine)

    yield db_session  # this is where the testing happens

    db_session.close()
    Base.metadata.drop_all(engine)

def test_create_user(db_session):
    # Use db_session to interact with the database
    new_user = User(email="test55@example.com")
    db_session.add(new_user)
    db_session.commit()

    # Query the user back
    user = db_session.query(User).filter_by(email="test55@example.com").first()
    assert user is not None
    assert user.email == "test55@example.com"