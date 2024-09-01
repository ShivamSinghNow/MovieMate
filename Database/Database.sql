-- Create Users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL, -- Added email field
);

-- Create Movies table
CREATE TABLE movies (
    movie_id SERIAL PRIMARY KEY, -- Added movie_id as a primary key
    title VARCHAR(255) NOT NULL,
    summary TEXT,
    image_url VARCHAR(255),
    likes INTEGER DEFAULT 0, -- Added likes field with a default value of 0
    dislikes INTEGER DEFAULT 0, -- Added dislikes field with a default value of 0
    genres VARCHAR(255)[] -- Changed genres to an array type
);

-- Sample Query 1: Add a new user with email
INSERT INTO users (password, email)
VALUES ('password', 'nashwaan@veldt.co');

-- Sample Query 2: Add a new movie with likes, dislikes, and genres
INSERT INTO movies (title, summary, image_url, likes, dislikes, genres)
VALUES ('titanic', 'boring', 'http://example.com/image.jpg', 10, 2, ARRAY['Romance', 'Adventure']);

-- Sample Query 3: Retrieve users and their emails
SELECT user_id, email FROM users;

-- Sample Query 4: Retrieve movies with high likes
SELECT title, likes FROM movies WHERE likes > 5;

-- Sample Query 5: Update user email
UPDATE users SET email = 'nkhan040@ucr.edu' WHERE user_id = 1;

-- Sample Query 6: Update movie likes
UPDATE movies SET likes = likes + 1 WHERE title = 'titanic';

-- Sample Query 7: Delete a movie by title
DELETE FROM movies WHERE title = 'titanic';

-- Sample Query 8: Count the number of users
SELECT COUNT(*) FROM users;

-- Sample Query 9: Count the number of movies
SELECT COUNT(*) FROM movies;
