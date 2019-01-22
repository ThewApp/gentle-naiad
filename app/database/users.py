from . import things
from .conn import conn


def userUttered(userId):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT EXISTS(SELECT user_id FROM users WHERE user_id=%s);", (userId, ))
    exists = cursor.fetchone()[0]
    if exists:
        lastSeen(userId)
    else:
        insert(userId)
    cursor.close()
    conn.commit()


def lastSeen(userId):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET last_seen=CURRENT_TIMESTAMP WHERE user_id=%s;", (userId, ))
    cursor.close()
    conn.commit()


def insert(userId):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (user_id) VALUES (%s);", (userId, ))
    things.insert(userId)
    cursor.close()
    conn.commit()
