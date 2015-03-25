#!/usr/bin/python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournaments")

def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    cur = db.cursor()
    cur.execute('delete from matches;')
    db.commit()
    cur.close()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    cur = db.cursor()
    cur.execute('delete from players;')
    db.commit()
    cur.close()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    cur = db.cursor()
    cur.execute('select count(*) from players;')
    count = cur.fetchone()[0]
    cur.close()
    db.close()
    return count

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    cur = db.cursor()
    cur.execute('insert into players (name, wins, losses, matches) values (%s, 0, 0, 0);', (name,))
    db.commit()
    cur.close()
    db.close()

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
    db = connect()
    cur = db.cursor()
    cur.execute('select pid, name, wins, matches from players order by wins;')
    rows = cur.fetchall()
    cur.close()
    db.close()
    return [(row[0], row[1], row[2], row[3]) for row in rows]

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    cur = db.cursor()
    # update winer's info
    cur.execute('select wins, matches from players where pid = %s;', (winner,))
    winner_info = cur.fetchone()
    cur.execute('update players set wins=%s, matches=%s where pid = %s', (1+winner_info[0], 1+winner_info[1], winner))
    # update loser's info
    cur.execute('select losses, matches from players where pid = %s;', (loser,))
    loser_info = cur.fetchone()
    cur.execute('update players set losses=%s, matches=%s where pid = %s;', (1+loser_info[0], 1+loser_info[1], loser))
    db.commit()
    cur.close()
    db.close()
 
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
    db = connect()
    cur = db.cursor()
    cur.execute('select pid, name from players order by wins;')
    pairings = []
    while True:
        a = cur.fetchone()
        b = cur.fetchone()
        if b==None: break
        pairings.append((a[0], a[1], b[0], b[1]))
    return pairings
