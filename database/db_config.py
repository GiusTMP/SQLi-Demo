import psycopg2
from psycopg2 import sql

    
# Funzione per stabilire la connessione con il db
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="sqli_demo",
        user="gius",   
        password="123"  
    )
    return conn


# Funzione che inizializza il db creando la tabella users solo se non esiste
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

# Funzione utile per popolare il db
def insert_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Controlla se l'utente esiste già, se non esiste lo inserisce nella tabella "users"
    cursor.execute("SELECT 1 FROM users WHERE username=%s;", (username,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s);", (username, password))
        conn.commit()
    
    conn.close()


