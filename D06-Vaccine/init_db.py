import sqlite3

# Chemin vers la base de données
DATABASE = 'test.db'

# Script SQL pour initialiser la base de données
INIT_SCRIPT = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        password TEXT
    );

    INSERT OR IGNORE INTO users (name, password) VALUES ('Alice', 'password1');
    INSERT OR IGNORE INTO users (name, password) VALUES ('Bob', 'password2');
    INSERT OR IGNORE INTO users (name, password) VALUES ('Charlie', 'password3');
"""

def initialize_database():
    # Connexion à la base de données
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Exécution du script SQL d'initialisation
    cursor.executescript(INIT_SCRIPT)

    # Valider et fermer la connexion
    conn.commit()
    conn.close()

if __name__ == '__main__':
    initialize_database()
    print("Database initialized successfully.")
