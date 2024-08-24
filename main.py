from flask import Flask, request, render_template
import psycopg2
import logging
from db_config import setup_db, insert_user

app = Flask(__name__)


def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="sqli_demo",
        user="gius",
        password="123"
    )
    return conn

@app.route('/', methods=['GET', 'POST'])
def login():
    user = None
    error = None
    results = {}
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        # Setting auto commit to True 
        conn.autocommit = True
        cursor = conn.cursor()

        # Costruzione della query SQL vulnerabile
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}';"
        print(f"Executing SQL Query: {query}")

        try:
            cursor.execute(query)  # Usa execute per la query SELECT

            # Se la query non restituisce risultati, non chiamare fetchall
            if cursor.description:  # Se la query ha una descrizione (ovvero restituisce risultati)
                users = cursor.fetchall()

                if users:
                    results['all_users'] = [dict(zip([desc[0] for desc in cursor.description], row)) for row in users]
                else:
                    error = 'Invalid user credentials. Please try again.'
            else:
                results['no_users'] = "No such table: users "
                print("Query executed, but no results to fetch.")
                # Gestisci eventuali modifiche non risultanti da fetchall

        except psycopg2.Error as e:
            # Registra l'errore e mostra un messaggio generico
            logging.error(f'Error executing query: {str(e)}')
            error = 'Invalid user credentials. Please try again.'
        conn.close()

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