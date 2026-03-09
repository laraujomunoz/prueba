import sqlite3

def get_connection():

    conn = sqlite3.connect(
        "turnos.db",
        check_same_thread=False
    )

    conn.execute("PRAGMA journal_mode=WAL")

    return conn


def crear_tablas(conn):

    conn.execute("""

    CREATE TABLE IF NOT EXISTS turnos(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT,
        nombre TEXT,
        carrera TEXT,
        grupo TEXT,
        necesidad TEXT,
        hora TEXT,
        asesora TEXT,
        fecha TEXT

    )

    """)

    conn.commit()