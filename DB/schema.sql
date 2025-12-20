CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    username VARCHAR(100) NOT NULL,
    phone_number VARCHAR(15) NOT NULL
);

CREATE TABLE ingredients (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    ingredient VARCHAR(225) NOT NULL,
    quantity INTEGER NOT NULL,
    threshold INTEGER NOT NULL,
    CONSTRAINT fk_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

