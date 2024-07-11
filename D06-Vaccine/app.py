from flask import Flask, request, render_template, g
import sqlite3

app = Flask(__name__)
DATABASE = 'test.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])  # Assurez-vous que cette route accepte bien la méthode POST
def login():
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT name FROM users WHERE name = '%s' AND password = '%s'" % (username, password))
    user = cursor.fetchone()
    if user:
        return f'Welcome {user[0]}'
    else:
        return 'Invalid username or password'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
