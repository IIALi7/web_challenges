import sqlite3, pathlib, os
BASE = pathlib.Path(__file__).parent.resolve()
DB = BASE / "users.db"
if DB.exists():
    print("DB exists:", DB)
else:
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, username TEXT, password TEXT);")
    cur.executemany("INSERT INTO users(id, username, password) VALUES (?, ?, ?);",
                    [(1,'admin','admin123'), (2,'guest','guest')])
    # create flags table for SQLi challenge
    cur.execute("CREATE TABLE flags(id INTEGER PRIMARY KEY, flag TEXT);")
    cur.execute("INSERT INTO flags(flag) VALUES (?)", ("CSC{SQLI_FLAG_2}",))
    conn.commit()
    conn.close()
    print("Created DB at", DB)
