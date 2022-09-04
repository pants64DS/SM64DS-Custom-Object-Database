CREATE TABLE objects (
	id SERIAL PRIMARY KEY,
	name TEXT,
	creator TEXT,
	rom_hack TEXT,
	category TEXT  DEFAULT 'Misc.',
	object_id INT,
	actor_id INT,
	description TEXT DEFAULT '',
	image INT REFERENCES images(id)
);

CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	username TEXT UNIQUE NOT NULL,
	password TEXT NOT NULL,
	is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE images (
	id SERIAL PRIMARY KEY,
	name TEXT,
	data BYTEA
);
