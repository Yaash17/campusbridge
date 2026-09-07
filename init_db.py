import sqlite3

connection = sqlite3.connect("campusbridge.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS properties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    area TEXT,
    university TEXT
    )
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER NOT NULL,
    rating INTEGER,
    review_text TEXT,
    FOREIGN KEY (property_id) REFERENCES properties (id)
)
""")

connection.commit()
connection.close()

print("Database and tables created successfully.")