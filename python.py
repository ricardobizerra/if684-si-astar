from constraints import REAL, DIRETA, TRAIN_VELOCITY, CHANGE_LINE_TIME, LOWEST_STATION_NUMBER, HIGHEST_STATION_NUMBER, STATION_LINES, REAL_DISTANCES_CSV, DIRECT_DISTANCES_CSV, STATION_LINE_CONNECTIONS

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
        if DIRECT_DISTANCES_CSV.iloc[E[0], E[1]] == "-":
            return 0.0
        return float(DIRECT_DISTANCES_CSV.iloc[E[0], E[1]])
    elif lista == "Real":
        try:
            return float(REAL_DISTANCES_CSV.iloc[E[0], E[1]])
        except:
            return -1
        
def get_time_by_distance(distance: int): return distance / TRAIN_VELOCITY * 60

def print_frontier_nodes(index: int, frontier: list[Node], nodes_that_were_first: list[tuple[int, str]] = []):
    message = f'Fronteira {index}:'
    for node in frontier:
        if node.state not in nodes_that_were_first:
            message += f'\n{node.state}: {node.cost}'
    print('==============================')
    print(message)

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
    for connection in STATION_LINE_CONNECTIONS[node_to_analyse.state[0]]:

        if connection[1] == node_to_analyse.state[1]:
            real_distance = get_time_by_distance(pegar_planilha(REAL, node_to_analyse.state[0], connection[0]))
            direct_distance = get_time_by_distance(pegar_planilha(DIRETA, connection[0], dest[0]))

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
            direct_distance = get_time_by_distance(pegar_planilha(DIRETA, node_to_analyse.state[0], dest[0]))

            real_cost = 0
            node_parent = node_to_analyse
            while node_parent:
                real_cost += node_parent.real_cost
                node_parent = node_parent.parent
            total_cost = real_cost + direct_distance + real_distance + CHANGE_LINE_TIME
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
    print_frontier_nodes(latest_iteration + 1, new_frontier, nodes_that_were_first)

    first_node_not_analysed = None
    for node in new_frontier:
        if node.state not in nodes_that_were_first:
            first_node_not_analysed = node
            nodes_that_were_first.append(first_node_not_analysed.state)
            break

    if first_node_not_analysed is not None and first_node_not_analysed.state == dest:
        print('==============================')
        print("Found!")
        return new_frontier
    
    original_frontier[latest_iteration + 1] = new_frontier
    return state_analysis(
        start = start, 
        dest = dest, 
        original_frontier = original_frontier,
        nodes_that_were_first = nodes_that_were_first
    )

def a_star(start: tuple[int, str], dest: tuple[int, str]):

    for station, line in [start, dest]:
        if station not in STATION_LINE_CONNECTIONS:
            raise ValueError(f"Station {station} does not exist")
        if line not in ["yellow", "blue", "red", "green"]:
            raise ValueError(f"Line {line} does not exist")
    
    print_frontier_nodes(1, [Node(state=start, parent=None, cost=0)])
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
                    cost = get_time_by_distance(pegar_planilha(DIRETA, start[0], dest[0]))
                )
            ],
        },
    )

def number_not_in_bounds(number: int): return number < LOWEST_STATION_NUMBER or number > HIGHEST_STATION_NUMBER

def line_not_in_bounds(line: str): return line not in STATION_LINES

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
