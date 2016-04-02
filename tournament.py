#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
from contextlib import contextmanager

def connect():
	"""Connect to the PostgreSQL database.  Returns a database connection."""
	try:
		return psycopg2.connect("dbname=tournament")
	except:
		print("Connection failed")

@contextmanager
def get_cursor():
	"""
	Query helper function using conext lib.
	Creates a cursor from a database connection object
	and performs queries using that cursor
	"""

	DB = connect()
	cursor = DB.cursor()
	try:
		yield cursor
	except:
		raise
	else:
		DB.commit()
	finally:
		cursor.close()
		DB.close()


def deleteMatches():
    	"""Remove all the match records from the database."""

	with get_cursor() as cursor:
		#delete data from match table
		cursor.execute("DELETE from match;")

		#update player table with matchs to 0
		cursor.execute("UPDATE player SET matches = 0")


def deletePlayers():
    	"""Remove all the player records from the database."""

	#delete data from player table
	with get_cursor() as cursor:
    		cursor.execute("DELETE FROM player;")


def countPlayers():
    	"""Returns the number of players currently registered."""

	#return the number of rows in the player table
	with get_cursor() as cursor:
    		cursor.execute("SELECT count(*) FROM player;")
		num_player = int(cursor.fetchone()[0])

	return num_player


def registerPlayer(name):
    	"""Adds a player to the tournament database.
  
    	The database assigns a unique serial id number for the player.  (This
    	should be handled by your SQL database schema, not in your Python code.)
  
    	Args:
      		name: the player's full name (need not be unique).
    	"""

	#Add the name of the player and initialize win,loss,points,matches to 0
	with get_cursor() as cursor:
		cursor.execute("INSERT INTO player (name, matches) VALUES (%s,%s)" , (name,0,))
	
    	
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

	#return player_id along with it's name,win,matches
	standing = []
	with get_cursor() as cursor:
		cursor.execute("SELECT a.player_id, a.name, COUNT(b.winner_id) AS won, a.matches FROM player a LEFT JOIN match b ON a.player_id=b.winner_id GROUP BY a.player_id ORDER BY won desc;")
		standing = cursor.fetchall()

	return standing


def reportMatch(winner, loser):
    	"""Records the outcome of a single match between two players.

    	Args:
      		winner:  the id number of the player who won
      		loser:  the id number of the player who lost
    	"""

  	with get_cursor() as cursor:
		cursor.execute("INSERT INTO match (winner_id, loser_id) VALUES (%s, %s)" , (winner,loser,))
		cursor.execute("UPDATE player SET matches = matches + 1 WHERE player_id = (%s)" % (winner,))
		cursor.execute("UPDATE player SET matches = matches + 1 WHERE player_id = (%s)" % (loser,))
 
 
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

	#return a pair of players by order of most wins
	temp = playerStandings()
	swiss_pairs = []
	for i in range(0, len(temp), 2):
		player1 = temp[i]
		player2 = temp[i+1]
		swiss_pairs.append((player1[0], player1[1], player2[0], player2[1]))

	return swiss_pairs


#if __name__ == '__main__':


