import sqlite3

connection = sqlite3.connect('sqli_demo.db')
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')

# Aggiungi utenti di esempio
cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'adminpass')")
cursor.execute("INSERT INTO users (username, password) VALUES ('user1', 'user1pass')")

connection.commit()
connection.close()