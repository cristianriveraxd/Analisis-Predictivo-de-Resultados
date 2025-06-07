from flask import Flask, render_template, request, send_file
import io
import requests
import pandas as pd
import networkx as nx
from sklearn.linear_model import LinearRegression
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json
import os
import plotly.express as px
import plotly.io as pio
from datetime import datetime
from html2image import Html2Image

app = Flask(__name__)

API_KEY = '8778d28069434fbd8dc0e71d71120869'
HEADERS = {'X-Auth-Token': API_KEY}
MATCHES_URL = "https://api.football-data.org/v4/competitions/CL/matches"

#dashboard
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

def crear_grafico_general(df):
    fig = px.scatter(
        df, x="GolesContra", y="GolesFavor", size="Puntos", color="Equipo",
        hover_name="Equipo", text="Equipo",
        title="Goles a Favor vs Goles en Contra",
        labels={"GolesFavor": "Goles a Favor", "GolesContra": "Goles en Contra"},
        width=800, height=600
    )
    fig.update_traces(textposition='top center')
    return pio.to_html(fig, full_html=False)

def crear_grafico_por_equipo(matches, equipo_filtrado=None):
    data = []
    for match in matches:
        if match['status'] != 'FINISHED':
            continue

        jornada = match['matchday']
        home = match['homeTeam']['name']
        away = match['awayTeam']['name']
        g_home = match['score']['fullTime']['home']
        g_away = match['score']['fullTime']['away']

        if g_home is not None and g_away is not None:
            data.append({'Equipo': home, 'Jornada': jornada, 'Goles': g_home})
            data.append({'Equipo': away, 'Jornada': jornada, 'Goles': g_away})

    df_evolucion = pd.DataFrame(data)
    if equipo_filtrado:
        df_evolucion = df_evolucion[df_evolucion['Equipo'] == equipo_filtrado]

    fig = px.line(df_evolucion, x="Jornada", y="Goles", color="Equipo", markers=True,
                  title="Evolución de Goles por Equipo", width=900, height=500)
   
def crear_grafico_barras(df):
    fig = px.bar(df, x="Equipo", y="GolesFavor", color="Equipo",
                 title="Total de Goles a Favor por Equipo", 
                 labels={"GolesFavor": "Goles a Favor"},
                 hover_data=["Partidos", "Puntos"],
                 width=900, height=500)
    hti = Html2Image()
    hti.screenshot(
    html_str=pio.to_html(fig, full_html=True),
    save_as="barras_grafo.png",
    size=(1500, 1100)
)   
    return pio.to_html(fig, full_html=False)
@app.route("/dashboard")
def dashboard():
    equipo = request.args.get("equipo")
    matches = cargar_datos()
    df_stats = procesar_estadisticas(matches)
    grafico_html = crear_grafico_general(df_stats)
    grafico_equipos = crear_grafico_por_equipo(matches, equipo_filtrado=equipo)
    grafico_barras = crear_grafico_barras(df_stats)
    nombres_equipos = sorted(df_stats['Equipo'].unique())

    return render_template("dashboard.html", 
                           tabla=df_stats.to_dict(orient="records"), 
                           grafico=grafico_html,
                           grafico_equipos=grafico_equipos,
                           grafico_barras=grafico_barras,
                           equipos=nombres_equipos,
                           equipo_seleccionado=equipo)



def generar_grafo(partidos):
    G = nx.DiGraph()

    for match in partidos:
        if match["status"] != "FINISHED":
            continue

        home = match["homeTeam"]["name"]
        away = match["awayTeam"]["name"]
        home_goals = match["score"]["fullTime"]["home"]
        away_goals = match["score"]["fullTime"]["away"]

        if home_goals is None or away_goals is None:
            continue

        if home_goals > 0:
            if G.has_edge(home, away):
                G[home][away]["weight"] += home_goals
            else:
                G.add_edge(home, away, weight=home_goals)

        if away_goals > 0:
            if G.has_edge(away, home):
                G[away][home]["weight"] += away_goals
            else:
                G.add_edge(away, home, weight=away_goals)

    if G.number_of_nodes() == 0:
        return

    plt.figure(figsize=(14, 12))
    pos = nx.spring_layout(G, k=1.0, seed=42)
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1000)
    nx.draw_networkx_labels(G, pos, font_size=10)

    for u, v, data in G.edges(data=True):
        weight = data["weight"]
        rad = 0.3 if G.has_edge(v, u) else 0.1
        nx.draw_networkx_edges(
            G, pos,
            edgelist=[(u, v)],
            arrowstyle='-|>',
            arrowsize=30,
            width=1,
            connectionstyle=f'arc3,rad={rad}',
            edge_color='black'
        )
        x = (pos[u][0] + pos[v][0]) / 2
        y = (pos[u][1] + pos[v][1]) / 2
        plt.text(x, y, str(weight), fontsize=10, ha='center', va='center',
                 bbox=dict(facecolor='white', edgecolor='none', alpha=0.3))

    plt.title("Grafo de goles entre equipos", fontsize=16)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("static/grafo.png")
    plt.close()

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
                           plot_url=plot_path,
                           output_url="static/grafo.png",
                           current_year=datetime.now().year)

@app.route('/')
def index():
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
        home_goals = match['score']['fullTime']['home']
        away_goals = match['score']['fullTime']['away']

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
    ]).sort_values(by='Puntos', ascending=False)

    # Regresión lineal
    X = df[['Partidos']]
    y = df['Puntos']
    modelo = LinearRegression().fit(X, y)
    pendiente = modelo.coef_[0]
    interseccion = modelo.intercept_
    r2 = modelo.score(X, y)

    # Gráfico de regresión
    plt.figure(figsize=(10, 6))
    plt.scatter(df['Partidos'], df['Puntos'], color='blue', label='Datos reales')
    plt.plot(df['Partidos'], modelo.predict(X), color='red', label='Regresión lineal')
    plt.xlabel('Partidos Jugados')
    plt.ylabel('Puntos')
    plt.title('Regresión Lineal: Puntos vs Partidos')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("static/plot.png")
    plt.close()

    generar_grafo(partidos)

    return render_template("index.html",
                           equipos=df.to_dict(orient='records'),
                           pendiente=round(pendiente, 2),
                           interseccion=round(interseccion, 2),
                           r2=round(r2, 3),
                           plot_url="static/plot.png",
                           output_url="static/grafo.png",
                           current_year=datetime.now().year)

@app.route("/descargar/excel")
def descargar_excel():
    matches = cargar_datos()
    df = procesar_estadisticas(matches)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Estadísticas")
    output.seek(0)
    return send_file(output, download_name="Datos Equipos.xlsx", as_attachment=True)

@app.route("/descargar/pdf")
def descargar_pdf():
    from xhtml2pdf import pisa
    from flask import make_response
    matches = cargar_datos()
    df = procesar_estadisticas(matches)
    html = render_template("reporte_pdf.html", tabla=df.to_dict(orient="records"))

    result = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.StringIO(html), dest=result)
    if pisa_status.err:
        return "Error al generar el PDF", 500

    result.seek(0)
    return send_file(result, download_name="Datos Equipo.pdf", as_attachment=True)



if __name__ == '__main__':
    if not os.path.exists("static"):
        os.makedirs("static")
    app.run(debug=True)
