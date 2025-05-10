import sqlite3
import os
from flask import g

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            os.path.join(os.getcwd(), "cpe.db"),
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()
