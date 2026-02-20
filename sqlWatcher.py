import sqlite3


def watch():
    with sqlite3.connect("data.db") as conn:
        cur = conn.cursor()
        query = "SELECT * FROM users"
        res = cur.execute(query).fetchall()
    return res

if __name__ == "__main__":
    with sqlite3.connect("data.db") as conn:
        cur = conn.cursor()
        query = "SELECT * FROM users"
        res = cur.execute(query).fetchall()

        for i in res:
            print(i)
