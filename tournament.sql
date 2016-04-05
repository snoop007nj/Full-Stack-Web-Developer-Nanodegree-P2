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
	PRIMARY KEY (PLAYER_ID)
);

CREATE TABLE match (
	MATCH_ID	SERIAL,
	WINNER_ID	INT	REFERENCES PLAYER(PLAYER_ID),
	LOSER_ID	INT	REFERENCES PLAYER(PLAYER_ID),
	PRIMARY KEY (MATCH_ID)
);

CREATE VIEW lostview AS 
	SELECT a.player_id, a.name, COUNT(b.loser_id) AS lost 
		FROM player a LEFT JOIN match b ON a.player_id=b.loser_id 
		GROUP BY a.player_id ORDER BY lost asc;

CREATE VIEW wonview AS
	SELECT a.player_id, a.name, COUNT(b.winner_id) AS won 
		FROM player a LEFT JOIN match b ON a.player_id=b.winner_id 
		GROUP BY a.player_id ORDER BY won desc;
	
