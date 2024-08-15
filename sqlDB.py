import sqlite3


def create_connection():
    conn = sqlite3.connect('danzai.db')  # Esto crea el archivo de la base de datos si no existe
    return conn


def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posturas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pose TEXT NOT NULL,
                side TEXT NOT NULL,
                variation TEXT NOT NULL,
                camera_angle TEXT NOT NULL,
                left_armpit REAL NOT NULL,
                right_armpit REAL NOT NULL,
                left_elbow REAL NOT NULL,
                right_elbow REAL NOT NULL,
                left_wrist REAL NOT NULL,
                right_wrist REAL NOT NULL,
                left_hip REAL NOT NULL,
                right_hip REAL NOT NULL,
                left_knee REAL NOT NULL,
                right_knee REAL NOT NULL,
                left_foot REAL NOT NULL,
                right_foot REAL NOT NULL,
                min_left_armpit REAL NOT NULL,
                min_right_armpit REAL NOT NULL,
                min_left_elbow REAL NOT NULL,
                min_right_elbow REAL NOT NULL,
                min_left_wrist REAL NOT NULL,
                min_right_wrist REAL NOT NULL,
                min_left_hip REAL NOT NULL,
                min_right_hip REAL NOT NULL,
                min_left_knee REAL NOT NULL,
                min_right_knee REAL NOT NULL,
                min_left_foot REAL NOT NULL,
                min_right_foot REAL NOT NULL
            );
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(e)


conn = create_connection()
create_table(conn)
