from flask import Flask, render_template
import pandas as pd
import json
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

def cargar_datos():
    with open("Partidos.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["matches"]

def procesar_estadisticas(matches):
    equipos = {}

    for match in matches:
        if match['status'] != 'FINISHED':
            continue

        home = match['homeTeam']['name']
        away = match['awayTeam']['name']
        goals_home = match['score']['fullTime']['home']
        goals_away = match['score']['fullTime']['away']

        for equipo in [home, away]:
            if equipo not in equipos:
                equipos[equipo] = {'Equipo': equipo, 'Partidos': 0, 'GolesFavor': 0, 'GolesContra': 0, 'Puntos': 0}

        equipos[home]['Partidos'] += 1
        equipos[away]['Partidos'] += 1
        equipos[home]['GolesFavor'] += goals_home
        equipos[home]['GolesContra'] += goals_away
        equipos[away]['GolesFavor'] += goals_away
        equipos[away]['GolesContra'] += goals_home

        if goals_home > goals_away:
            equipos[home]['Puntos'] += 3
        elif goals_home < goals_away:
            equipos[away]['Puntos'] += 3
        else:
            equipos[home]['Puntos'] += 1
            equipos[away]['Puntos'] += 1

    df = pd.DataFrame(equipos.values())
    df = df.sort_values(by=["Puntos", "GolesFavor"], ascending=False).reset_index(drop=True)
    return df

def crear_grafico(df):
    fig = px.scatter(
        df, x="GolesContra", y="GolesFavor", size="Puntos", color="Equipo",
        hover_name="Equipo", text="Equipo",
        title="Goles a Favor vs Goles en Contra",
        labels={"GolesFavor": "Goles a Favor", "GolesContra": "Goles en Contra"},
        width=800, height=600
    )
    fig.update_traces(textposition='top center')
    return pio.to_html(fig, full_html=False)

@app.route("/")
def index():
    matches = cargar_datos()
    df_stats = procesar_estadisticas(matches)
    grafico_html = crear_grafico(df_stats)
    return render_template("dashboard.html", tabla=df_stats.to_dict(orient="records"), grafico=grafico_html)

if __name__ == '__main__':
    app.run(debug=True)
