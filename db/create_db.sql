CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
	age VARCHAR (10),
	income VARCHAR (20),
	sex VARCHAR (1),
	kids_flg INTEGER
);

CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    item_id INTEGER,
	content_type VARCHAR (30),
	title VARCHAR (200),
	title_orig VARCHAR (200),
	release_year INTEGER,
	genres VARCHAR (200),
	countries VARCHAR (200),
	for_kids INTEGER,
	age_rating INTEGER,
	studios VARCHAR (200),
	directors VARCHAR (200),
	actors VARCHAR (200),
	description VARCHAR (1000),
	keywords VARCHAR (1000)
);

CREATE TABLE interactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    item_id INTEGER,
	last_watch_dt DATE,
	total_dur INTEGER,
	watched_pct DECIMAL(3,1)
);
