CREATE TABLE Ingredients
(ingredient varchar(225),
quantity integer,
threshold integer);

CREATE TABLE users
(
id SERIAL PRIMARY KEY,
email VARCHAR(255) UNIQUE NOT NULL,
password VARCHAR(255) NOT NULL,
username VARCHAR(100) NOT NULL,
phone_number VARCHAR(15) NOT NULL
);