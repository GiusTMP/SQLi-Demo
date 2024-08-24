from flask import Flask, request, render_template
import psycopg2
import logging
from db_config import setup_db, insert_user

# Inizializzazione dell'app
app = Flask(__name__)

# Funzione per stabilire una connessione con PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="sqli_demo",
        user="gius",
        password="123"
    ) 
    return conn

# Definizione della route per la pagina principale '/'
@app.route('/', methods=['GET', 'POST'])
def login():
    user = None
    error = None
    results = {}
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Connessione al db
        conn = get_db_connection()

        # Autocommit per tutte le query
        conn.autocommit = True 
        
        cursor = conn.cursor()

        # Costruzione della query vulnerabile a SQLi
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}';"
        print(f"Executing SQL Query: {query}")

        try:
            cursor.execute(query)  

            # Se la query restituisce risultati allora fa fetchall
            if cursor.description: 
                users = cursor.fetchall()

                if users:
                    # Converte i risultati della query in un dizionario
                    results['all_users'] = [dict(zip([desc[0] for desc in cursor.description], row)) for row in users]
                else:
                    error = 'Invalid user credentials. Please try again.'
            else:
                # Gestisce il caso in cui la tabella non esista (dopo un DROP TABLE)
                results['no_users'] = "No such table: users "
                print("Query executed, but no results to fetch.")

        except psycopg2.Error as e:
            # Mostra un messaggio di errore generico    
            error = 'Invalid user credentials. Please try again.'
        conn.close()
        
    # Renderizza il template HTML con i risultati e gli eventuali errori
    return render_template('index.html', user=user, error=error, results=results)


if __name__ == '__main__':
    setup_db()
    insert_user('admin', 'adminpass')
    insert_user('user2', 'user2pass')
    insert_user('rossi', 'passRossi')
    insert_user('utente30', 'passUt30')
    insert_user('utprova', '123pass')
    insert_user('utente3', 'user3pass')
    app.run(debug=True)


'''
                TEST

http://127.0.0.1:5000/

1) ' OR '1'='1'--  Tautologia 
2) admin' -- Eol Comment (commento di fine riga) 
3) _'; DROP TABLE users -- Piggyback Query

'''