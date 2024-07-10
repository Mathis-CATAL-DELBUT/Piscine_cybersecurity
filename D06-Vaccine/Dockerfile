# Utiliser une image Python officielle comme base
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires dans le répertoire de travail
COPY requirements.txt requirements.txt
COPY app.py app.py
COPY templates/ templates/
COPY init_db.py init_db.py

# Installer les dépendances
RUN pip install -r requirements.txt

# Exécuter le script d'initialisation de la base de données
RUN python init_db.py

# Exposer le port sur lequel l'application va tourner
EXPOSE 5000

# Définir la commande de démarrage
CMD ["python", "app.py"]
