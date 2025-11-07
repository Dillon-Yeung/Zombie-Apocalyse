import random
import time
import sqlite3

# creates stat template for new players
class player:
    def __init__(self, username, password, gang):
        self.username = username
        self.password = password
        self.stats = {
            'Day': 1,
            'Ammo': 0,
            'Food': 0,
            'Gang': gang,
            'Survivors': 0,
            'Dog': 1,
        }

    def retrieve_stats(self):
        return (
            self.username,
            self.stats['Ammo'],
            self.stats['Food'],
            self.stats['Survivors'],
            self.stats['Gang'],
            self.stats['Dog'],
        )

    def new_day(self):
        if self.stats['Day'] < 100:
            self.stats['Day'] += 1
            return False
        return True

_conn = sqlite3.connect('game_data.db')
_c = _conn.cursor()

table_creation_query = '''CREATE TABLE IF NOT EXISTS PLAYER_DATA (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    food INT,
    ammo INT,
    survivors INT,
    core TEXT,
    dog INT);'''

leaderboard_creation_query = '''CREATE TABLE IF NOT EXISTS LEADERBOARD (
    username TEXT PRIMARY KEY,
    score INTEGER NOT NULL );'''

_c.execute(table_creation_query)
_c.execute(leaderboard_creation_query)
_conn.commit()
_conn.close()

def DiceRoll(sides=6):
    return random.randint(1, sides)

def cleardatabase():
    conn = sqlite3.connect('game_data.db')
    c = conn.cursor()
    c.execute("DELETE FROM PLAYER_DATA")
    conn.commit()
    conn.close()
    print("All data from PLAYER_DATA has been cleared.")

# checks what members of the scooby gang alive
def check_gang_members(name):
    conn = sqlite3.connect('game_data.db')
    c = conn.cursor()
    c.execute("SELECT core FROM PLAYER_DATA WHERE username = ?", (name,))
    row = c.fetchone()
    conn.close()
    
    gang = ["Velma"]  # Velma is always present
    if row and row[0]:
        core = row[0]
        if "D" in core:
            gang.append("Daphne")
        if "F" in core:
            gang.append("Fred")
        if "S" in core:
            gang.append("Shaggy")
    return gang 


    