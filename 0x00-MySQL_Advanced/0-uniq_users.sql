-- Write a SQL script that creates a table users following these requirements:
-- id, integer, never null, auto increment and primary key
-- email, string (255 characters), never null and unique
-- name, string (255 characters)
-- If the table already exists, your script should not fail
-- your script can be executed on any database

CREATE TABLE IF NOT EXISTS users (
  id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  email varchar(255) NOT NULL UNIQUE,
  name varchar(255)
);
