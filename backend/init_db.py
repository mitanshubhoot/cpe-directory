import sqlite3

def init_db():
    db = sqlite3.connect("cpe.db")
    with open("schema.sql") as f:
        db.executescript(f.read())
    db.close()
    print("cpe.db initialized from schema.sql")

if __name__ == "__main__":
    init_db()
