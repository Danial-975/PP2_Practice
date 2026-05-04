import psycopg2
from config import DB_CONFIG

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def create_tables():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS game_sessions (
        id SERIAL PRIMARY KEY,
        player_id INTEGER REFERENCES players(id),
        score INTEGER,
        level_reached INTEGER,
        played_at TIMESTAMP DEFAULT NOW()
    );
    """)
    conn.commit()
    cur.close()
    conn.close()

def get_player(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM players WHERE username=%s", (username,))
    res = cur.fetchone()
    if res:
        player_id = res[0]
    else:
        cur.execute("INSERT INTO players(username) VALUES(%s) RETURNING id", (username,))
        player_id = cur.fetchone()[0]
        conn.commit()
    cur.close()
    conn.close()
    return player_id

def save_score(username, score, level):
    conn = get_connection()
    cur = conn.cursor()
    player_id = get_player(username)
    cur.execute("""
        INSERT INTO game_sessions(player_id, score, level_reached)
        VALUES (%s, %s, %s)
    """, (player_id, score, level))
    conn.commit()
    cur.close()
    conn.close()

def get_top10():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.username, g.score, g.level_reached
        FROM game_sessions g
        JOIN players p ON p.id = g.player_id
        ORDER BY g.score DESC
        LIMIT 10
    """)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def get_best(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT MAX(g.score)
        FROM game_sessions g
        JOIN players p ON p.id = g.player_id
        WHERE p.username=%s
    """, (username,))
    res = cur.fetchone()[0]
    cur.close()
    conn.close()
    return res if res else 0