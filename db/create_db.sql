CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
	age VARCHAR (10),
	income VARCHAR (20),
	sex VARCHAR (1),
	kids_flg INTEGER
);