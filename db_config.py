import psycopg2
from psycopg2 import sql

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="sqli_demo",
        user="gius",   
        password="123"  
    )
    return conn

def setup_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Controlla se la tabella esiste già, altrimenti la crea
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
        );
    """)
    conn.commit()
    conn.close()

def insert_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Controlla se l'utente esiste già, se non esiste lo inserisce nella tabella "users"
    cursor.execute("SELECT 1 FROM users WHERE username=%s;", (username,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s);", (username, password))
        conn.commit()
    
    conn.close()

