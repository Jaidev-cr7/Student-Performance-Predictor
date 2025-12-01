import sqlite3

def create_table():
    conn = sqlite3.connect("predictions.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            attendance INTEGER,
            internal_marks INTEGER,
            assignments INTEGER,
            previous_gpa REAL,
            prediction TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def insert_prediction(attendance, internal_marks, assignments, previous_gpa, prediction):
    conn = sqlite3.connect("predictions.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions (attendance, internal_marks, assignments, previous_gpa, prediction)
        VALUES (?, ?, ?, ?, ?)
    """, (attendance, internal_marks, assignments, previous_gpa, prediction))

    conn.commit()
    conn.close()

create_table()
