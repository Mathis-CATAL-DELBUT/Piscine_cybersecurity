from flask import Flask, render_template

app = Flask(__name__)

# Liste des images dans l'ordre spécifié
images = [
    "carre.png",
    "rond.png",
    "triangle.png",
    "hexagone.png"
]

# Route pour la page d'accueil
@app.route('/')
def index():
    # La première image de la liste est affichée sur la page d'accueil
    return render_template('index.html', image=images[0])

# Route pour la page 2
@app.route('/page2')
def page2():
    # La deuxième image de la liste est affichée sur la page 2
    return render_template('page2.html', image=images[1])

# Route pour la page 3
@app.route('/page3')
def page3():
    # La troisième image de la liste est affichée sur la page 3
    return render_template('page3.html', image=images[2])

# Route pour la page 4
@app.route('/page4')
def page4():
    # La quatrième image de la liste est affichée sur la page 4
    return render_template('page4.html', image=images[3])

if __name__ == '__main__':
    app.run(debug=True, port=7777)
