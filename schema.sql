
DROP TABLE IF EXISTS varbinary_bcrypt_table;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS users;

-- The 'users' Table
CREATE TABLE users(
    user_id VARCHAR(255) PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARBINARY(255) NOT NULL
);

-- The 'posts' Table
CREATE TABLE posts(
    post_id VARCHAR(255) PRIMARY KEY,
    post_title VARCHAR(255) NOT NULL,
    post_content LONGTEXT NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- The 'comments' Table
CREATE TABLE comments(
    comment_id VARCHAR(255) PRIMARY KEY,
    comment_content MEDIUMTEXT NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    post_id VARCHAR(255) NOT NULL, 
    reply_to_id VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (post_id) REFERENCES posts(post_id)
);