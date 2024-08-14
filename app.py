from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('sqli_demo.db')
    conn.row_factory = sqlite3.Row
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
        cursor = conn.cursor()

        # Costruzione della query SQL vulnerabile
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        print(f"Executing SQL Query: {query}")  # Debug: stampa la query eseguita

        cursor.execute(query)
        users = cursor.fetchall()

        if users:
            # Salva i risultati della query
            results['all_users'] = [dict(zip([column[0] for column in cursor.description], row)) for row in users]
        else:
            error = 'Invalid credentials. Please try again.'

        conn.close()

    return render_template('index.html', user=user, error=error, results=results)


if __name__ == '__main__':
    app.run(debug=True)

