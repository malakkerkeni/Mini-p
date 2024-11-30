from flask import Flask, render_template, request, redirect
import pyodbc

app = Flask(__name__)


import os
import pyodbc
# Connexion à la base de données Azure SQL
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=miniprojet.database.windows.net;'
    'DATABASE=Mini-Projet;'
    'UID=user;'
    'PWD=Pa$$w0rd1234'
)


# Récupérer les variables d'environnement
server = os.getenv('SQL_SERVER')
database = os.getenv('SQL_DATABASE')
username = os.getenv('SQL_USERNAME')
password = os.getenv('SQL_PASSWORD')



# Route : Ajouter un client
@app.route('/ajout_client', methods=['GET', 'POST'])
def ajout_client():
    cursor = conn.cursor()
    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.form['nom']
        prenom = request.form['prenom']
        age = int(request.form['age'])
        id_region = int(request.form['region'])

        # Insérer les données dans la base
        cursor.execute("INSERT INTO client (nom, prenom, age, ID_region) VALUES (?, ?, ?, ?)",
                       (nom, prenom, age, id_region))
        conn.commit()
        return redirect('/liste_client')

    # Récupérer les régions pour le menu déroulant
    cursor.execute("SELECT ID_region, libelle FROM region")
    regions = cursor.fetchall()
    return render_template('ajout_client.html', regions=regions)

# Route : Liste des clients
@app.route('/liste_client')
def liste_client():
    cursor = conn.cursor()
    cursor.execute("SELECT c.ID_client, c.nom, c.prenom, c.age, r.libelle "
                   "FROM client c JOIN region r ON c.ID_region = r.ID_region")
    clients = cursor.fetchall()
    return render_template('liste_client.html', clients=clients)

# Route : Modifier un client
@app.route('/modifier/<int:id_client>', methods=['GET', 'POST'])
def modifier_client(id_client):
    cursor = conn.cursor()
    if request.method == 'POST':
        # Récupérer les nouvelles données
        nom = request.form['nom']
        prenom = request.form['prenom']
        age = int(request.form['age'])
        id_region = int(request.form['region'])

        # Mettre à jour la base
        cursor.execute("UPDATE client SET nom = ?, prenom = ?, age = ?, ID_region = ? WHERE ID_client = ?",
                       (nom, prenom, age, id_region, id_client))
        conn.commit()
        return redirect('/liste_client')

    # Récupérer les infos du client et les régions
    cursor.execute("SELECT * FROM client WHERE ID_client = ?", (id_client,))
    client = cursor.fetchone()
    cursor.execute("SELECT ID_region, libelle FROM region")
    regions = cursor.fetchall()
    return render_template('modifier_client.html', client=client, regions=regions)

@app.route('/supprimer/<int:id_client>', methods=['GET'])
def supprimer_client(id_client):
    cursor = conn.cursor()
    # Supprime le client avec l'ID correspondant
    cursor.execute("DELETE FROM client WHERE ID_client = ?", (id_client,))
    conn.commit()
    return redirect('/liste_client')


@app.route('/home')
def home():
    return 'Page d\'accueil'


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

