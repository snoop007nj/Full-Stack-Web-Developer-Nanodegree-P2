-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament;

CREATE TABLE player (
	PLAYER_ID	SERIAL,
	NAME		VARCHAR(80),
	WIN		INT,
	LOSS		INT,
	POINTS		INT,
	MATCHES		INT,
	PRIMARY KEY (PLAYER_ID)
);

CREATE TABLE match (
	MATCH_ID	SERIAL,
	WINNER_ID	INT	REFERENCES PLAYER(PLAYER_ID),
	LOSER_ID	INT	REFERENCES PLAYER(PLAYER_ID),
	PRIMARY KEY (MATCH_ID)
);
