import pandas
import time

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

class Node:
    def __init__(self, state: tuple[int, str], parent: 'Node', cost: int, real_cost: int = 0):
        self.state = state
        self.parent = parent
        self.cost = cost
        self.real_cost = real_cost

def pegar_planilha(lista, E1, E2):
    E = [E1 - 1, E2 - 1]
    E.sort()

    if lista == "Direta":
        if direct_dist.iloc[E[0], E[1]] == "-":
            return 0.0
        return float(direct_dist.iloc[E[0], E[1]])
    elif lista == "Real":
        try:
            return float(real_dist.iloc[E[0], E[1]])
        except:
            return -1
        
def get_time_by_distance(distance: int): return distance / train_velocity * 60

def print_frontier_nodes(index: int, frontier: list[Node]):
    message = f'Fronteira {index}: '
    for node in frontier:
        message += f'{node.state}: {node.cost} '
    print(message)

def state_analysis(
    start: tuple[int, str], 
    dest: tuple[int, str], 
    original_frontier: dict[int, list[Node]], 
):
    latest_iteration = max(original_frontier.keys())
    latest_frontier = original_frontier[latest_iteration]

    node_to_analyse = latest_frontier[0]

    new_frontier = []
    for connection in station_line_connections[node_to_analyse.state[0]]:
        print(f'Analysing {connection}')


        if connection[1] == node_to_analyse.state[1]:
            real_distance = get_time_by_distance(pegar_planilha(real, node_to_analyse.state[0], connection[0]))
            print(f'Pegando distancia real entre {node_to_analyse.state[0]} e {connection[0]}: {real_distance}')
            direct_distance = get_time_by_distance(pegar_planilha(direta, connection[0], dest[0]))
            print(f'Pegando distancia direta entre {connection[0]} e {dest[0]}: {direct_distance}')

            real_cost = 0
            node_parent = node_to_analyse
            while node_parent:
                real_cost += node_parent.real_cost
                node_parent = node_parent.parent
            total_cost = real_cost + direct_distance + real_distance
            new_frontier.append(
                Node(
                    state=connection, 
                    parent=node_to_analyse, 
                    cost=total_cost,
                    real_cost=real_cost+direct_distance
                )
            )
            print(f'Added {connection} to frontier, with h = {direct_distance} + {real_distance} + {real_cost} = {total_cost}')
        elif (node_to_analyse.state[0], connection[1]) not in [node.state for node in new_frontier]:
            real_distance = 0
            print(f'Pegando distancia real entre {node_to_analyse.state[0]} e {connection[0]}: {real_distance}')
            direct_distance = get_time_by_distance(pegar_planilha(direta, node_to_analyse.state[0], dest[0]))
            print(f'Pegando distancia direta entre {node_to_analyse.state[0]} e {dest[0]}: {direct_distance}')

            real_cost = 0
            node_parent = node_to_analyse
            while node_parent:
                real_cost += node_parent.real_cost
                node_parent = node_parent.parent
            total_cost = real_cost + direct_distance + real_distance + change_line_time
            new_frontier.append(
                Node(
                    state=(node_to_analyse.state[0], connection[1]), 
                    parent=node_to_analyse, 
                    cost=total_cost,
                    real_cost=real_cost+direct_distance
                )
            )
            print(f'Added {(node_to_analyse.state[0], connection[1])} to frontier, with h = {direct_distance} + {real_distance} + {real_cost} + {change_line_time} = {total_cost}')

    new_frontier = latest_frontier + new_frontier
    new_frontier.sort(key=lambda x: x.cost)

    if new_frontier[0].state == dest:
        print_frontier_nodes(latest_iteration + 1, new_frontier)
        print("Found!")
        return new_frontier
    
    new_frontier = new_frontier[1:]
    new_frontier.sort(key=lambda x: x.cost) 
    print_frontier_nodes(latest_iteration + 1, new_frontier)
    original_frontier[latest_iteration + 1] = new_frontier
    return state_analysis(
        start = start, 
        dest = dest, 
        original_frontier = original_frontier
    )

def a_star(start: tuple[int, str], dest: tuple[int, str]):

    for station, line in [start, dest]:
        if station not in station_line_connections:
            raise ValueError(f"Station {station} does not exist")
        if line not in ["yellow", "blue", "red", "green"]:
            raise ValueError(f"Line {line} does not exist")
    
    print(f'Fronteira 1: {[start]}')
    if start == dest:
        return [start]
    
    state_analysis(
        start = start, 
        dest = dest,
        original_frontier = {
            1: [
                Node(
                    state = start, 
                    parent = None, 
                    cost = get_time_by_distance(pegar_planilha(direta, start[0], dest[0]))
                )
            ],
        },
    )

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

cli()
