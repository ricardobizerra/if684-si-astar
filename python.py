import pandas

real_dist = pandas.read_csv("Distancias_Reais.csv", keep_default_na=False, index_col=0)
direct_dist = pandas.read_csv("Distancias_Diretas.csv", keep_default_na=False, index_col=0)

real = "Real"
direta = "Direta"
train_velocity = 30
change_line_time = 4

station_line_connections = {
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

def pegar_planilha(lista, E1, E2):
    E = [E1 - 1, E2 - 1]
    E.sort()

    if lista == "Direta":
        return float(direct_dist.iloc[E[0], E[1]])
    elif lista == "Real":
        try:
            return float(real_dist.iloc[E[0], E[1]])
        except:
            return -1
        
def get_time_by_distance(distance: int): return distance / train_velocity * 60

def a_star(start: tuple[int, str], dest: tuple[int, str]):

    for station, line in [start, dest]:
        if station not in station_line_connections:
            raise ValueError(f"Station {station} does not exist")
        if line not in ["yellow", "blue", "red", "green"]:
            raise ValueError(f"Line {line} does not exist")
        
    if start == dest:
        return [start]
    
    frontier = []
    costs = {}
    
    # start analysing the start state
    for connection in station_line_connections[start[0]]:
        print(f'analysing {connection}')
        if connection[1] == start[1]:
            frontier.append((connection)) # other stations in the same line
            costs[connection] = get_time_by_distance(pegar_planilha(real, start[0], connection[0]))
        elif (start[0], connection[1]) not in frontier:
            frontier.append((start[0], connection[1])) # other lines in the same station
            costs[(start[0], connection[1])] = change_line_time
    
    print(frontier)
    print(costs)

    # analising the time to go to the start state to any state of the frontier

def cli():
    aaaaaa = int(input("\033[33mskip? (1/0)> \033[0m"))

    if aaaaaa:
        a_star(
            start = (2, 'yellow'), 
            dest = (13, 'red')
        )
    
    else:
        start_number = int(input("Enter start station: "))
        start_line = input("Enter start line (yellow, blue, red OR green): ")
        dest_number = int(input("Enter destination station: "))
        dest_line = input("Enter destination line (yellow, blue, red OR green): ")

        a_star(
            start = (start_number, start_line), 
            dest = (dest_number, dest_line)
        )

    # print(f"Path: {path}")
    # print("Stations passed:")
    # current_color = path[1][1]
    # current_stations = [path[0][0]]
    # previous_station = ''
    # for station, color in path[1:]:
    #     if color != current_color:
    #         print(f"{current_color} line: {'-'.join(map(str, current_stations))}")
    #         print(f"<changed from {current_color} to {color} on station {previous_station}>")
    #         current_color = color
    #         current_stations = [current_stations[-1], station]
    #     else:
    #         current_stations.append(station)
    #     previous_station = station
    # print(f"{current_color} line: {'-'.join(map(str, current_stations))}")
    # print("<finish>")

cli()
