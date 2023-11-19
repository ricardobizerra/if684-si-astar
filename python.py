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

def print_frontier_nodes(index: int, frontier: list[Node], nodes_that_were_first: list[tuple[int, str]] = []):
    message = f'Fronteira {index}:'
    for node in frontier:
        if node.state not in nodes_that_were_first:
            message += f'\n{node.state}: {node.cost}'
    print('==============================')
    print(message)
    print('==============================')

def state_analysis(
    start: tuple[int, str], 
    dest: tuple[int, str], 
    original_frontier: dict[int, list[Node]], 
    nodes_that_were_first: list[tuple[int, str]] = []
):
    latest_iteration = max(original_frontier.keys())
    latest_frontier = original_frontier[latest_iteration]

    node_to_analyse = latest_frontier[0]

    new_frontier = []
    for connection in station_line_connections[node_to_analyse.state[0]]:

        if connection[1] == node_to_analyse.state[1]:
            real_distance = get_time_by_distance(pegar_planilha(real, node_to_analyse.state[0], connection[0]))
            direct_distance = get_time_by_distance(pegar_planilha(direta, connection[0], dest[0]))

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

        elif (node_to_analyse.state[0], connection[1]) not in [node.state for node in new_frontier]:
            real_distance = 0
            direct_distance = get_time_by_distance(pegar_planilha(direta, node_to_analyse.state[0], dest[0]))

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

    new_frontier = new_frontier + latest_frontier[1:]
    new_frontier.sort(key=lambda x: x.cost)

    first_node_not_analysed = None
    for node in new_frontier:
        if node.state not in nodes_that_were_first:
            first_node_not_analysed = node
            nodes_that_were_first.append(first_node_not_analysed.state)
            break

    if first_node_not_analysed is not None and first_node_not_analysed.state == dest:
        print_frontier_nodes(latest_iteration + 1, new_frontier, nodes_that_were_first)
        print("Found!")
        return new_frontier
    
    print_frontier_nodes(latest_iteration + 1, new_frontier, nodes_that_were_first)
    original_frontier[latest_iteration + 1] = new_frontier
    return state_analysis(
        start = start, 
        dest = dest, 
        original_frontier = original_frontier,
        nodes_that_were_first = nodes_that_were_first
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

def number_not_in_bounds(number: int):
    lower_bound = 1
    upper_bound = 14

    return number < lower_bound or number > upper_bound

def line_not_in_bounds(line: str):
    return line not in ["yellow", "blue", "red", "green"]

def cli():
    
    start_number = int(input("Enter start station: "))
    if number_not_in_bounds(start_number):
        raise ValueError(f"Station {start_number} does not exist")

    start_line = input("Enter start line (yellow, blue, red OR green): ")
    if line_not_in_bounds(start_line):
        raise ValueError(f"Line {start_line} does not exist")
    
    dest_number = int(input("Enter destination station: "))
    if number_not_in_bounds(dest_number):
        raise ValueError(f"Station {dest_number} does not exist")
    
    dest_line = input("Enter destination line (yellow, blue, red OR green): ")
    if line_not_in_bounds(dest_line):
        raise ValueError(f"Line {dest_line} does not exist")

    start_tuple = (start_number, start_line)
    dest_tuple = (dest_number, dest_line)

    a_star(
        start = start_tuple,
        dest = dest_tuple
    )

cli()
