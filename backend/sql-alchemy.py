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


# # Add row to table
u = User("hollandpleskac@gmail.com")
session.add(u) # add person to db
session.commit() # apply changes to db


# # Add row to table
m = Movie("Movie2", "desc", "https://www.twincities.com/wp-content/uploads/2022/05/Summer_Film_Preview_71939.jpg")
session.add(m)
session.commit()

# # Add row to table
m = Rating(u.email, m.id, 4)
session.add(m)
session.commit()


# Query from table
results = session.query(User).all() # select everything from people table
results_filtered = session.query(User).filter(User.email == "hples001@gmail.com") # filter
# for r in results_filtered:
#     print(r)

# results = session.query(Rating).all() # select everything from people table
# print(results)

# res = session.query(User).filter(User.email == "hples001@gmail.com").all()
# print(res)

results = session.query(Rating).join(User, "hples001@gmail.com" == Rating.userEmail).join(Movie, Movie.id == Rating.movieId).all()
print(results)

# Query from table (things owned by person)
# results = session.query(Thing, Person).filter(Thing.owner == Person.ssn).filter(Person.firstname == "holland").all()
# print("res",results)