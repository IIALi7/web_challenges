import sqlite3, pathlib, os
BASE = pathlib.Path(__file__).parent.resolve()
DB = BASE / "users.db"
if DB.exists():
    print("DB exists:", DB)
else:
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, username TEXT);")
    cur.executemany("INSERT INTO users(id, username) VALUES (?, ?);", [(1,'admin'),(2,'ali'),(3,'mohammed')])
    conn.commit()
    conn.close()
    print("Created DB at", DB)
