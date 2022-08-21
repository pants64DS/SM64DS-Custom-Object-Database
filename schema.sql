CREATE TABLE objects (
	id SERIAL PRIMARY KEY,
	name TEXT,
	creator TEXT,
	rom_hack TEXT,
	category TEXT  DEFAULT 'Misc.',
	object_id INT,
	actor_id INT,
	description TEXT DEFAULT ''
);
