import sqlite3


def get_connection():

    conn = sqlite3.connect(
        "turnos.db",
        check_same_thread=False
    )

    conn.execute("PRAGMA journal_mode=WAL")

    return conn


def crear_tablas(conn):

    # Crear tabla si no existe
    conn.execute("""

    CREATE TABLE IF NOT EXISTS turnos(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT,
        nombre TEXT,
        usuario TEXT,
        carrera TEXT,
        grupo TEXT,
        necesidad TEXT,
        hora TEXT,
        asesora TEXT,
        fecha TEXT,
        estado TEXT DEFAULT 'pendiente'

    )

    """)

    # --------------------------------
    # Verificar si la columna estado existe
    # (para bases creadas antes)
    # --------------------------------

    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(turnos)")

    columnas = [col[1] for col in cursor.fetchall()]

    if "estado" not in columnas:

        conn.execute(
            "ALTER TABLE turnos ADD COLUMN estado TEXT DEFAULT 'pendiente'"
        )

    conn.commit()

