from flask import Flask, render_template
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo

app = Flask(__name__)

@app.route('/')
def dashboard():
    # Charger les données
    df = pd.read_csv('data/ventes.csv')

    # Ajouter une colonne montant
    df['Montant'] = df['Quantité'] * df['PrixUnitaire']

    # Ventes par produit
    ventes_par_produit = df.groupby('Produit')['Montant'].sum().sort_values(ascending=False)

    produit_fig = go.Figure([go.Bar(
        x=ventes_par_produit.index,
        y=ventes_par_produit.values,
        marker_color='indigo'
    )])
    produit_fig.update_layout(title='Chiffre d\'Affaires par Produit')
    graph_produit = pyo.plot(produit_fig, output_type='div')

    # Ventes par vendeur
    ventes_par_vendeur = df.groupby('Vendeur')['Montant'].sum().sort_values(ascending=False)

    vendeur_fig = go.Figure([go.Pie(
        labels=ventes_par_vendeur.index,
        values=ventes_par_vendeur.values
    )])
    vendeur_fig.update_layout(title='Répartition des Ventes par Vendeur')
    graph_vendeur = pyo.plot(vendeur_fig, output_type='div')

    return render_template("dashboard.html",
                           graph_produit=graph_produit,
                           graph_vendeur=graph_vendeur)

if __name__ == '__main__':
    app.run(debug=True)
