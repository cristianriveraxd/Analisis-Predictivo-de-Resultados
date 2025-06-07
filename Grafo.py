import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import json

# Leer el archivo JSON
with open("localhost.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# Filtrar partidos finalizados
df = df[df["status"] == "FINISHED"].copy()

# Crear un grafo dirigido
G = nx.DiGraph()

# Agregar aristas desde home_team → away_team por goles_home y viceversa
for _, row in df.iterrows():
    home = row["home_team"]
    away = row["away_team"]
    goles_home = row["score_home"]
    goles_away = row["score_away"]

    # Goles del local al visitante
    if goles_home > 0:
        if G.has_edge(home, away):
            G[home][away]["weight"] += goles_home
        else:
            G.add_edge(home, away, weight=goles_home)

    # Goles del visitante al local
    if goles_away > 0:
        if G.has_edge(away, home):
            G[away][home]["weight"] += goles_away
        else:
            G.add_edge(away, home, weight=goles_away)

# Dibujar el grafo
plt.figure(figsize=(14, 12))
pos = nx.spring_layout(G, k=1.0, seed=42)

# Dibujar nodos
nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1000)

# Dibujar etiquetas de nodos
nx.draw_networkx_labels(G, pos, font_size=10)

# Dibujar aristas con estilo curvado para evitar solapamiento
for u, v, data in G.edges(data=True):
    weight = data["weight"]
    # Estilo curvado para distinguir direcciones opuestas
    rad = 0.3 if G.has_edge(v, u) else 0.1 
    nx.draw_networkx_edges(
        G, pos,
        edgelist=[(u, v)],
        arrowstyle='-|>',       # Flecha más clásica y visible
        arrowsize=30,           # Flechas más grandes
        width=1,              # Grosor de la línea mayor
        connectionstyle=f'arc3,rad={rad}',
        edge_color='black'      # Color más visible
    )
    # Dibujar etiquetas de los pesos
    x = (pos[u][0] + pos[v][0]) / 2
    y = (pos[u][1] + pos[v][1]) / 2
    plt.text(x, y, str(weight), fontsize=10, ha='center', va='center',
             bbox=dict(facecolor='white', edgecolor='none', alpha=0.3))

plt.title("Grafo de goles entre equipos", fontsize=16)
plt.axis("off")
plt.tight_layout()
plt.show()

