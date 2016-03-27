#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
	"""Connect to the PostgreSQL database.  Returns a database connection."""
    	return psycopg2.connect("dbname=tournament")


def deleteMatches():
    	"""Remove all the match records from the database."""
  
  	conn = psycopg2.connect("dbname=tournament")
    	cursor = conn.cursor()

	#delete data from match table
	cursor.execute("DELETE from match;")

	#update player table with win,loss,points,matchs to 0
	cursor.execute("UPDATE player SET win = 0")
	cursor.execute("UPDATE player SET loss = 0")
	cursor.execute("UPDATE player SET points = 0")
	cursor.execute("UPDATE player SET matches = 0")
	
	conn.commit()
	conn.close()


def deletePlayers():
    	"""Remove all the player records from the database."""
    
  	conn = psycopg2.connect("dbname=tournament")
    	cursor = conn.cursor()

	#delete data from player table
    	cursor.execute("DELETE FROM player;")
	
	conn.commit()
	conn.close()


def countPlayers():
    	"""Returns the number of players currently registered."""

  	conn = psycopg2.connect("dbname=tournament")
    	cursor = conn.cursor()

	#return the number of rows in the player table
    	cursor.execute("SELECT count(*) FROM player;")
	num_player = int(cursor.fetchone()[0])
	
	conn.close()

	return num_player


def registerPlayer(name):
    	"""Adds a player to the tournament database.
  
    	The database assigns a unique serial id number for the player.  (This
    	should be handled by your SQL database schema, not in your Python code.)
  
    	Args:
      		name: the player's full name (need not be unique).
    	"""

  	conn = psycopg2.connect("dbname=tournament")
    	cursor = conn.cursor()

	#Add the name of the player and initialize win,loss,points,matches to 0
	cursor.execute("INSERT INTO player (name, win, loss, points, matches) VALUES (%s, %s, %s, %s, %s)" , (name,0,0,0,0))
	
	conn.commit()
	conn.close()
    	

def playerStandings():
	"""Returns a list of the players and their win records, sorted by wins.

    	The first entry in the list should be the player in first place, or a player
    	tied for first place if there is currently a tie.

    	Returns:
      	A list of tuples, each of which contains (id, name, wins, matches):
        	id: the player's unique id (assigned by the database)
        	name: the player's full name (as registered)
        	wins: the number of matches the player has won
        	matches: the number of matches the player has played
    	"""
  	
	conn = psycopg2.connect("dbname=tournament")
    	cursor = conn.cursor()

	#return player_id along with it's name,win,matches
	cursor.execute("SELECT player_id, name, win, matches FROM player")
	standings = cursor.fetchall()
	
	conn.close()

	return standings


def reportMatch(winner, loser):
    	"""Records the outcome of a single match between two players.

    	Args:
      		winner:  the id number of the player who won
      		loser:  the id number of the player who lost
    	"""

  	conn = psycopg2.connect("dbname=tournament")
    	cursor = conn.cursor()
	cursor.execute("INSERT INTO match (winner_id, loser_id) VALUES (%s, %s)" , (winner,loser))
	cursor.execute("UPDATE player SET matches = matches + 1 WHERE player_id = %i" % (winner))
	cursor.execute("UPDATE player SET matches = matches + 1 WHERE player_id = %i" % (loser))
	cursor.execute("UPDATE player SET win = win + 1 WHERE player_id = %i" % (winner))
	conn.commit()
	
	conn.close()
 
 
def swissPairings():
    	"""Returns a list of pairs of players for the next round of a match.
  
    	Assuming that there are an even number of players registered, each player
    	appears exactly once in the pairings.  Each player is paired with another
    	player with an equal or nearly-equal win record, that is, a player adjacent
    	to him or her in the standings.
  
    	Returns:
      	A list of tuples, each of which contains (id1, name1, id2, name2)
        	id1: the first player's unique id
        	name1: the first player's name
        	id2: the second player's unique id
        	name2: the second player's name
    	"""
	
	conn = psycopg2.connect("dbname=tournament")
    	cursor = conn.cursor()

	#return a pair of players by order of most wins
	cursor.execute("SELECT player_id, name FROM player ORDER BY win DESC");
	temp = cursor.fetchall()
	swiss_pairs = []
	for i in range(0, len(temp), 2):
		swiss_pairs.append(temp[i] + temp[i+1])
	conn.close()

	return swiss_pairs


'''
if __name__ == '__main__':

	deleteMatches()
	deletePlayers()
	registerPlayer("Twilight Sparkle")
	registerPlayer("Fluttershy")
	registerPlayer("Applejack")
	registerPlayer("Pinkie Pie")
	registerPlayer("Rarity")
	registerPlayer("Rainbow Dash")
	registerPlayer("Princess Celestia")
	registerPlayer("Princess Luna")
    	standings = playerStandings()
        [id1, id2, id3, id4, id5, id6, id7, id8] = [row[0] for row in standings]
	reportMatch(id1, id2)
	reportMatch(id3, id4)
	reportMatch(id5, id6)
	reportMatch(id7, id8)
	pairing = swissPairings()
	print pairing
	print len(pairing)
'''
