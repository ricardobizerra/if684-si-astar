# Import necessary modules and classes
from constraints import REAL, DIRETA, TRAIN_VELOCITY, CHANGE_LINE_TIME, LOWEST_STATION_NUMBER, HIGHEST_STATION_NUMBER, STATION_LINES, REAL_DISTANCES_CSV, DIRECT_DISTANCES_CSV, STATION_LINE_CONNECTIONS

# Define the Node class
class Node:
    def __init__(self, state: tuple[int, str], parent: 'Node', cost: float, real_cost: float = 0):
        self.state = state
        self.parent = parent
        self.cost = cost
        self.real_cost = real_cost

# Function to retrieve distances from a spreadsheet
def pegar_planilha(lista, E1, E2):
    # Convert station numbers to zero-based indexing
    E = [E1 - 1, E2 - 1]
    E.sort()

    # Retrieve distances based on the type of list (Direta or Real)
    if lista == "Direta":
        if DIRECT_DISTANCES_CSV.iloc[E[0], E[1]] == "-":
            return 0.0
        return float(DIRECT_DISTANCES_CSV.iloc[E[0], E[1]])
    elif lista == "Real":
        try:
            return float(REAL_DISTANCES_CSV.iloc[E[0], E[1]])
        except:
            return -1

# Function to calculate time based on distance
def get_time_by_distance(distance: float): return distance / TRAIN_VELOCITY * 60

# Function to print the nodes in the frontier
def print_frontier_nodes(index: int, frontier: list[Node], nodes_that_were_first: list[tuple[tuple[int, str], float]] = []):
    message = f'Fronteira {index}:'
    for node in frontier:
        if (node.state, node.cost) not in nodes_that_were_first:
            message += f'\n{node.state}: {node.cost}'
    print('==============================')
    print(message)

def print_solution(node: Node):
    solution = f'{node.state}'
    node_parent = node.parent
    while node_parent:
        solution = f'{node_parent.state} -> {solution}'
        node_parent = node_parent.parent
    return solution

# Function to analyze the state and generate new frontier nodes
def state_analysis(
    start: tuple[int, str], 
    dest: tuple[int, str], 
    original_frontier: dict[int, list[Node]], 
    nodes_that_were_first: list[tuple[tuple[int, str], float]] = []
):
    # Get the latest frontier and node to analyze
    latest_iteration = max(original_frontier.keys())
    latest_frontier = original_frontier[latest_iteration]
    node_to_analyse = latest_frontier[0]

    # Generate new frontier nodes based on line connections
    new_frontier: list[Node] = []
    for connection in STATION_LINE_CONNECTIONS[node_to_analyse.state[0]]:

        # If the line of the connection is the same as the line of the node to analyze
        if connection[1] == node_to_analyse.state[1]:
            # Calculate real and direct distances
            real_distance = get_time_by_distance(pegar_planilha(REAL, node_to_analyse.state[0], connection[0]))
            direct_distance = get_time_by_distance(pegar_planilha(DIRETA, connection[0], dest[0]))

            # Calculate real cost by summing the real costs of parent nodes
            real_cost = 0
            node_parent = node_to_analyse
            while node_parent:
                real_cost += node_parent.real_cost
                node_parent = node_parent.parent

            # Calculate total cost and create new node
            total_cost = real_cost + direct_distance + real_distance
            new_frontier.append(
                Node(
                    state=connection, 
                    parent=node_to_analyse, 
                    cost=total_cost,
                    real_cost=real_cost+direct_distance
                )
            )
        
        # Else, we insert a node that represent the change of line, but staying in the same station
        elif (node_to_analyse.state[0], connection[1]) not in [node.state for node in new_frontier]:
            # Calculate direct distance and total cost for changing lines
            real_distance = 0
            direct_distance = get_time_by_distance(pegar_planilha(DIRETA, node_to_analyse.state[0], dest[0]))

            # Calculate real cost by summing the real costs of parent nodes
            real_cost = 0
            node_parent = node_to_analyse
            while node_parent:
                real_cost += node_parent.real_cost
                node_parent = node_parent.parent

            # Calculate total cost and create new node
            total_cost = real_cost + direct_distance + real_distance + CHANGE_LINE_TIME
            new_frontier.append(
                Node(
                    state=(node_to_analyse.state[0], connection[1]), 
                    parent=node_to_analyse, 
                    cost=total_cost,
                    real_cost=real_cost+direct_distance
                )
            )

    # Sort the new frontier based on cost and print the nodes
    new_frontier = new_frontier + latest_frontier[1:]
    new_frontier.sort(key=lambda x: x.cost)
    print_frontier_nodes(latest_iteration + 1, new_frontier, nodes_that_were_first)

    # Find the first node in the new frontier that has not been analyzed
    first_node_not_analysed = None
    for node in new_frontier:
        if (node.state, node.cost) not in nodes_that_were_first:
            first_node_not_analysed = node
            nodes_that_were_first.append((first_node_not_analysed.state, first_node_not_analysed.cost))
            break

    # If the first unanalyzed node is the destination, print "Found!"
    if first_node_not_analysed is not None and first_node_not_analysed.state == dest:
        print('==============================')
        print("Found!")
        print(f'Solução: {print_solution(first_node_not_analysed)}')
        print(f'Custo: {first_node_not_analysed.cost} minutes')
        return new_frontier
    
    # Add the new frontier to the original frontier and recursively call state_analysis
    original_frontier[latest_iteration + 1] = new_frontier
    return state_analysis(
        start = start, 
        dest = dest, 
        original_frontier = original_frontier,
        nodes_that_were_first = nodes_that_were_first
    )

# A* search algorithm
def a_star(start: tuple[int, str], dest: tuple[int, str]):
    
    # Print the initial frontier nodes
    print_frontier_nodes(1, [Node(state=start, parent=None, cost=0)])

    # If start and destination are the same, return the start node
    if start == dest: return [start]
    
    # Perform state analysis to find the path
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

# Function to check if a number is within the station number bounds
def number_not_in_bounds(number: int): return number < LOWEST_STATION_NUMBER or number > HIGHEST_STATION_NUMBER

# Function to check if a line is within the valid lines
def line_not_in_bounds(line: str): return line not in STATION_LINES

# Command-line interface function
def cli():
    # Get input from the user and validate it
    start_number = int(input("🔜 Enter start station: "))
    if number_not_in_bounds(start_number):
        raise ValueError(f"Station {start_number} does not exist")

    start_line = input("🔜 Enter start line (yellow, blue, red OR green): ")
    if line_not_in_bounds(start_line):
        raise ValueError(f"Line {start_line} does not exist")
    
    dest_number = int(input("🔚 Enter destination station: "))
    if number_not_in_bounds(dest_number):
        raise ValueError(f"Station {dest_number} does not exist")
    
    dest_line = input("🔚 Enter destination line (yellow, blue, red OR green): ")
    if line_not_in_bounds(dest_line):
        raise ValueError(f"Line {dest_line} does not exist")

    # Convert input to tuples
    start_tuple = (start_number, start_line)
    dest_tuple = (dest_number, dest_line)

    # Call the A* algorithm with the inputs
    a_star(
        start = start_tuple,
        dest = dest_tuple
    )

# Call the command-line interface function
cli()
