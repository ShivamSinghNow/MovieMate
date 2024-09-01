import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from sqlalchemy import create_engine, update, insert, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm import joinedload
from reccomendation_algorithim import reccomend_movies

from typing import List

from sqlalchemy import create_engine

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

# connect to postgres    
database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(database_url)

class UserModel(BaseModel):
    email: str

class MovieReviewModel(BaseModel):
    user_email: str
    movie_id: int
    rating: float

Session = sessionmaker(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def read_root():
    session = Session()
    results = session.query(Rating).all() # select everything from people table
    print(results)
    session.close()
    return {"Hello": "World"}

class CreateUserRequest(BaseModel):
    email: str

@app.post("/create-user")
def read_item(user_request: CreateUserRequest):
    session = Session()
    email = user_request.email
    query_results = session.query(User).filter(User.email == email).all()
    if (len(query_results) == 0):
        u = User(email)
        session.add(u)
        session.commit()
        session.close()
        return {"status": f"create user {email}"}
    session.close()
    return {"status": f"user {email} already exists"}

@app.get("/rated-movies")
def read_item(email: str):
    session = Session()
    query_results = session.query( Movie.id, Movie.name, Movie.description , Rating.rating,).join(User, email== Rating.userEmail).join(Movie, Movie.id == Rating.movieId).distinct().all()
    result_formatted = [{"id": id, "name": name, "description": description, "rating": rating} for id, name, description, rating in query_results]
    session.close()
    return {"data": result_formatted}

class UpdateRatingRequest(BaseModel):
    email: str
    movieId: int
    newRating: int

@app.post("/rate-movie")
def update_rating(update_rating_request: UpdateRatingRequest):
    session = Session()
    email = update_rating_request.email
    movieId = update_rating_request.movieId
    newRating = update_rating_request.newRating

    # Check if the rating already exists
    existing_rating = session.query(Rating)\
                             .filter(Rating.userEmail == email, Rating.movieId == movieId)\
                             .first()

    if existing_rating:
        # Update the existing rating
        update_stmt = update(Rating)\
            .where(Rating.userEmail == email, Rating.movieId == movieId)\
            .values(rating=newRating)
        session.execute(update_stmt)
    else:
        # Insert a new rating
        insert_stmt = insert(Rating).values(userEmail=email, movieId=movieId, rating=newRating)
        session.execute(insert_stmt)

    session.commit()
    session.close()

    return {"result": "success"}

@app.get("/all-movies")
def get_movies(user_email: str):
    session = Session()

    # Subquery to find movie IDs rated by the user
    rated_movie_ids = session.query(Rating.movieId).filter(Rating.userEmail == user_email).subquery()
    print("rated movie ids all", session.query(rated_movie_ids).all())

    for movie_id in session.query(rated_movie_ids).all():
        print("MOVIE ID",movie_id)

    # Query to find movies not rated by the user
    query_results = session.query(Movie.id, Movie.name, Movie.description,Rating.rating).\
                outerjoin(Rating, Movie.id == Rating.movieId).\
                filter(~Movie.id.in_(rated_movie_ids)).\
                all()
    
    result_formatted = [{"id": movie.id, "name": movie.name, "description": movie.description, "rating": movie.rating} 
                        for movie in query_results]
    print("results formatted", result_formatted[0])

    v = reccomend_movies(1,7)
    recommended_ids = v[1]
    recommended_ids_int = [int(id) for id in recommended_ids]
    filtered_movies = [movie for movie in result_formatted if movie['id'] in recommended_ids_int]


    

    session.close()
    return {"data": filtered_movies}