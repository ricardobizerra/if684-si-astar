import pandas as pd

REAL = "Real"
DIRETA = "Direta"

TRAIN_VELOCITY = 30
CHANGE_LINE_TIME = 4

LOWEST_STATION_NUMBER = 1
HIGHEST_STATION_NUMBER = 14

STATION_LINES = ['blue', 'yellow', 'red', 'green']

REAL_DISTANCES_CSV = pd.read_csv("Distancias_Reais.csv", keep_default_na=False, index_col=0)
DIRECT_DISTANCES_CSV = pd.read_csv("Distancias_Diretas.csv", keep_default_na=False, index_col=0)

STATION_LINE_CONNECTIONS: dict[int, list[tuple[int, str]]] = {
    1: [(2, 'blue')],
    2: [(1, 'blue'), (10, 'yellow'), (9, 'yellow'), (3, 'blue')],
    3: [(2, 'blue'), (4, 'blue'), (9, 'red'), (13, 'red')],
    4: [(3, 'blue'), (5, 'blue'), (8, 'green'), (13, 'green')],
    5: [(4, 'blue'), (6, 'blue'), (7, 'yellow'), (8, 'yellow')],
    6: [(5, 'blue')],
    7: [(5, 'yellow')],
    8: [(4, 'green'), (5, 'yellow'), (9, 'yellow'), (12, 'green')],
    9: [(2, 'yellow'), (3, 'red'), (8, 'yellow'), (11, 'red')],
    10: [(2, 'yellow')],
    11: [(9, 'red')],
    12: [(8, 'green')],
    13: [(3, 'red'), (4, 'green'), (14, 'green')],
    14: [(13, 'green')]
}

AVAILABLE_LINES: dict[int, list[str]] = {}
for station, connections in STATION_LINE_CONNECTIONS.items():
    lines = [line for _, line in connections]
    AVAILABLE_LINES[station] = lines
