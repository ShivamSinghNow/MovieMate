import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.orm import declarative_base, sessionmaker

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

# use a local sqlite db (doesn't support postgres features)
# engine = create_engine('sqlite:///local_database.db')

# take classes extending from base and create them in db
Base.metadata.create_all(bind=engine)

# create session to interact with the db
Session = sessionmaker(bind=engine)
session = Session()

u = User("hollandpleskac@gmail.com")
session.add(u) # add person to db
session.commit() # apply changes to db

# List of movies
movies_list = [
    "1,Toy Story (1995),Adventure|Animation|Children|Comedy|Fantasy",
    "2,Jumanji (1995),Adventure|Children|Fantasy",
    "3,Grumpier Old Men (1995),Comedy|Romance",
    "4,Waiting to Exhale (1995),Comedy|Drama|Romance",
    "5,Father of the Bride Part II (1995),Comedy",
    "6,Heat (1995),Action|Crime|Thriller",
    "7,Sabrina (1995),Comedy|Romance",
    "8,Tom and Huck (1995),Adventure|Children",
    "9,Sudden Death (1995),Action",
    "10,GoldenEye (1995),Action|Adventure|Thriller",
    "11,American President, The (1995),Comedy|Drama|Romance",
    "12,Dracula: Dead and Loving It (1995),Comedy|Horror",
    "13,Balto (1995),Adventure|Animation|Children",
    "14,Nixon (1995),Drama",
    "15,Cutthroat Island (1995),Action|Adventure|Romance",
    "16,Casino (1995),Crime|Drama",
    "17,Sense and Sensibility (1995),Drama|Romance",
    "18,Four Rooms (1995),Comedy",
    "19,Ace Ventura: When Nature Calls (1995),Comedy",
    "20,Money Train (1995),Action|Comedy|Crime|Drama|Thriller",
    "21,Get Shorty (1995),Comedy|Crime|Thriller"
]

# Loop over the list of movies
for movie_entry in movies_list:
    _, name, genres = movie_entry.split(',', 2)  # Split each string into parts

    # Create a new Movie object
    m = Movie(name, genres, "https://www.twincities.com/wp-content/uploads/2022/05/Summer_Film_Preview_71939.jpg")

    # Add to the session and commit
    session.add(m)

# Commit all changes to the database
session.commit()

# Close the session
session.close()

print("Done")