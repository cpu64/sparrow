-- Create a schema for our dummy database
CREATE SCHEMA IF NOT EXISTS my_schema;

-- Switch to the new schema
SET search_path TO my_schema;

-- Create a simple table to store user data
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert some dummy data into the users table
INSERT INTO users (username, email) VALUES
('john_doe', 'john@example.com'),
('jane_smith', 'jane@example.com'),
('sam_jones', 'sam@example.com');

-- Create another table for storing posts (e.g., blog posts)
CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    body TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Insert some dummy posts
INSERT INTO posts (user_id, title, body) VALUES
(1, 'First Post', 'This is the body of the first post by John.'),
(2, 'Introduction to SQL', 'This is a simple introduction to SQL, written by Jane.'),
(3, 'My First Blog', 'This is the first blog post!');

-- Create an index for faster searches on the posts table
CREATE INDEX idx_posts_user_id ON posts (user_id);

-- Simple SELECT query to check the inserted data
SELECT * FROM users;
SELECT * FROM posts;

-- Create a view for easy reporting
CREATE VIEW user_post_summary AS
SELECT u.username, p.title, p.created_at
FROM users u
JOIN posts p ON u.id = p.user_id;
