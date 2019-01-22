from .conn import conn


def insert(userId):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO things (user_id) VALUES (%s);", (userId, ))
    cursor.close()
    conn.commit()


def updateHas(userId, state):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE things SET has_things=%s WHERE user_id=%s;", (state, userId))
    cursor.close()
    conn.commit()


def getHas(userId):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT has_things FROM things WHERE user_id=%s;", (userId, ))
    has = cursor.fetchone()[0]
    cursor.close()
    conn.commit()
    return has


def getAllHas():
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM things WHERE has_things=true;")
    allHas = cursor.fetchall()
    cursor.close()
    conn.commit()
    return allHas
