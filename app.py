from flask import Flask, render_template
import requests
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

API_KEY = '8778d28069434fbd8dc0e71d71120869'
HEADERS = {'X-Auth-Token': API_KEY}
MATCHES_URL = "https://api.football-data.org/v4/competitions/CL/matches"


@app.route('/')
def puntos_vs_partidos():
    response = requests.get(MATCHES_URL, headers=HEADERS)

    if response.status_code != 200:
        return render_template("index.html", error="No se pudieron obtener los partidos.")

    data = response.json()
    partidos = data.get('matches', [])

    puntos_por_equipo = {}

    for match in partidos:
        if match['status'] != "FINISHED":
            continue

        home = match['homeTeam']['name']
        away = match['awayTeam']['name']
        score = match['score']['fullTime']
        home_goals = score['home']
        away_goals = score['away']

        if home_goals is None or away_goals is None:
            continue

        for equipo in [home, away]:
            if equipo not in puntos_por_equipo:
                puntos_por_equipo[equipo] = {'Partidos': 0, 'Puntos': 0}

        puntos_por_equipo[home]['Partidos'] += 1
        puntos_por_equipo[away]['Partidos'] += 1

        if home_goals > away_goals:
            puntos_por_equipo[home]['Puntos'] += 3
        elif home_goals < away_goals:
            puntos_por_equipo[away]['Puntos'] += 3
        else:
            puntos_por_equipo[home]['Puntos'] += 1
            puntos_por_equipo[away]['Puntos'] += 1

    df = pd.DataFrame([
        {'Equipo': equipo, 'Partidos': datos['Partidos'], 'Puntos': datos['Puntos']}
        for equipo, datos in puntos_por_equipo.items()
    ])
    df = df.sort_values(by='Puntos', ascending=False)

    X = df[['Partidos']]
    y = df['Puntos']
    modelo = LinearRegression().fit(X, y)

    pendiente = modelo.coef_[0]
    interseccion = modelo.intercept_
    r2 = modelo.score(X, y)

    plt.figure(figsize=(10, 6))
    plt.scatter(df['Partidos'], df['Puntos'], color='blue', label='Datos reales')
    plt.plot(df['Partidos'], modelo.predict(X), color='red', label='Regresión lineal')
    plt.xlabel('Partidos Jugados')
    plt.ylabel('Puntos')
    plt.title('Regresión Lineal: Puntos vs Partidos')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plot_path = "static/plot.png"
    plt.savefig(plot_path)
    plt.close()

    return render_template("index.html",
                           equipos=df.to_dict(orient='records'),
                           pendiente=round(pendiente, 2),
                           interseccion=round(interseccion, 2),
                           r2=round(r2, 3),
                           plot_url=plot_path)


@app.route('/localVsVisitante')
def goles_local_vs_visitante():
    response = requests.get(MATCHES_URL, headers=HEADERS)

    if response.status_code != 200:
        return render_template("goles.html", error="No se pudieron obtener los partidos.")

    data = response.json()
    partidos = data.get('matches', [])

    goles_por_equipo = {}

    for match in partidos:
        if match['status'] != "FINISHED":
            continue

        home = match['homeTeam']['name']
        away = match['awayTeam']['name']
        score = match['score']['fullTime']
        home_goals = score['home']
        away_goals = score['away']

        if home_goals is None or away_goals is None:
            continue

        if home not in goles_por_equipo:
            goles_por_equipo[home] = {'Local': 0, 'Visitante': 0}
        if away not in goles_por_equipo:
            goles_por_equipo[away] = {'Local': 0, 'Visitante': 0}

        goles_por_equipo[home]['Local'] += home_goals
        goles_por_equipo[away]['Visitante'] += away_goals

    df = pd.DataFrame([
        {'Equipo': equipo, 'GolesLocal': datos['Local'], 'GolesVisitante': datos['Visitante']}
        for equipo, datos in goles_por_equipo.items()
    ])

    X = df[['GolesLocal']]
    y = df['GolesVisitante']
    modelo = LinearRegression().fit(X, y)

    pendiente = modelo.coef_[0]
    interseccion = modelo.intercept_
    r2 = modelo.score(X, y)

    plt.figure(figsize=(10, 6))
    plt.scatter(df['GolesLocal'], df['GolesVisitante'], color='green', label='Datos reales')
    plt.plot(df['GolesLocal'], modelo.predict(X), color='orange', label='Regresión lineal')
    plt.xlabel('Goles de Local')
    plt.ylabel('Goles de Visitante')
    plt.title('Regresión Lineal: Goles Visitante vs Goles Local')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plot_path = "static/goles.png"
    plt.savefig(plot_path)
    plt.close()

    return render_template("goles.html",
                           equipos=df.to_dict(orient='records'),
                           pendiente=round(pendiente, 2),
                           interseccion=round(interseccion, 2),
                           r2=round(r2, 3),
                           plot_url=plot_path)
    
    
    

if __name__ == '__main__':
    app.run(debug=True)
