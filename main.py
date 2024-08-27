from flask import Flask, request, render_template, redirect, url_for, session
import psycopg2
from database.db_config import *

# Inizializzazione dell'app
app = Flask(__name__)
app.secret_key = 'very_secure_key'  # Chiave segreta necessario per la gestione della sessione


# Definizione della route per la pagina principale '/' (login)
@app.route('/', methods=['GET', 'POST'])
def login():
    # Se l'utente è già loggato (presente nella sessione), viene reindirizzato alla pagina di benvenuto
    if 'username' in session:
        return redirect(url_for('welcome'))

    error = None
    consoleError = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        #Crea una connessione al database e imposta l'autocommit    
        conn = get_db_connection()
        conn.autocommit = True 
        cursor = conn.cursor()

        # Costruzione della query SQL vulnerabile
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}';"
        print(f"Executing SQL Query: {query}")

        try:
            cursor.execute(query)  
            
            # Se la query ha prodotto risultati
            if cursor.description: 
                users = cursor.fetchall()

                if users:
                    # Se l'utente è stato trovato, salva username e query nella sessione e reindirizza a welcome
                    session['username'] = username
                    session['login_query'] = query  # Salva la query nella sessione
                    return redirect(url_for('welcome'))
                else:
                    # Se le credenziali non sono valide, manda il messaggio di errore
                    error = 'Invalid user credentials. Please try again.'
                    consoleError = 'Invalid user credentials. Please try again.'
            else:
                # Se la query non ha prodotto risultati
                error = "Invalid user credentials. Please try again."
                consoleError = 'Invalid user credentials. Please try again.'
                print("Query executed, but no results to fetch.")

        except psycopg2.Error as e:
            # Gestisce eventuali errori di database, ad esempio tabella mancante
            if "relation \"users\" does not exist" in str(e):
                consoleError = "No such table: users"
                error = 'Invalid user credentials. Please try again.'
            else:
            # Per qualsiasi altro errore
                error = 'Invalid user credentials. Please try again.'
                consoleError = 'Invalid user credentials. Please try again.'
            print(f"Database error: {error}")
        finally:
            conn.close()

    return render_template('index.html', error=error, consoleError = consoleError)

# Modifica della route per la pagina di benvenuto '/welcome'
@app.route('/welcome')
def welcome():
    # Se l'utente non è loggato (username non presente nella sessione), viene reindirizzato al login
    if 'username' not in session:
        return redirect(url_for('login'))

    # Crea una connessione al database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Utilizza la stessa query usata durante il login
    query = session.get('login_query')
    print(f"Executing SQL Query for welcome page: {query}")

    results = []
    try:
        cursor.execute(query)
        users = cursor.fetchall()
        if cursor.description:
            id_idx = [desc[0] for desc in cursor.description].index('id')
            username_idx = [desc[0] for desc in cursor.description].index('username')

            # Crea la lista di dizionari filtrando solo 'id' e 'username'
            results = [
                {"id": row[id_idx], "username": row[username_idx]}
                for row in users
            ]
        else:
            results = []
    except psycopg2.Error as e:
        # Gestione di eventuali errori del database durante l'esecuzione della query
        results = [] 
        return render_template('welcome.html', results=results, error="Si è verificato un errore nel database. Riprovare più tardi.")
    finally:
        conn.close()

    return render_template('welcome.html', results=results)

# Definizione della route per il logout
@app.route('/logout')
def logout():
    # Rimuove l'username e la query dalla sessione (logout)
    session.pop('username', None)
    session.pop('login_query', None)  
    return redirect(url_for('login'))

if __name__ == '__main__':    
    setup_db()
    insert_user('admin', 'adminpass')
    insert_user('user2', 'user2pass')
    insert_user('rossi', 'passRossi')
    insert_user('utente30', 'passUt30')
    insert_user('utprova', '123pass')
    insert_user('utente3', 'user3pass')
    app.run(debug=True)
