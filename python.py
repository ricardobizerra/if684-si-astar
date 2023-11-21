# Import necessary modules and classes
from constraints import REAL, DIRETA, TRAIN_VELOCITY, CHANGE_LINE_TIME, LOWEST_STATION_NUMBER, HIGHEST_STATION_NUMBER, STATION_LINES, REAL_DISTANCES_CSV, DIRECT_DISTANCES_CSV, STATION_LINE_CONNECTIONS, AVAILABLE_LINES

# Define the Node class
class Node:
    def __init__(
        self, 
        state: tuple[int, str], 
        p: int,
        g: int = 0,
        h: int = 0,
        c: int = 0,
    ):
        self.state = state
        self.p = p
        self.g = g
        self.h = h
        self.f = p + g + h + c

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
def get_time_by_distance(distance: float): return (distance / TRAIN_VELOCITY) * 60

# Function to calculate time between two stations
def time_between(lista: str, E1: int, E2: int): return get_time_by_distance(pegar_planilha(lista, E1, E2))

# Function to print the nodes in the frontier
def print_frontier_nodes(index: int, frontier: list[Node]):
    message = f'Fronteira {index}:'
    for node in frontier:
        message += f'\n{node.state}: {node.f}'
    print('==============================')
    print(message)

def print_solution(visited_states: list[tuple[int, str]], dest: tuple[int, str]):
    message = ''

    past_state = None
    for state in visited_states:
        if past_state is not None:
            if state[1] != past_state[1]: message += f'{(past_state[0], state[1])} -> '
        message += f'{state} -> '
        past_state = state
    
    cost = 0
    if visited_states[-1][1] != dest[1] and dest[1] in AVAILABLE_LINES[visited_states[-1][0]]: 
        message += f'{(dest[0], dest[1])} -> '
        cost += CHANGE_LINE_TIME
    return message[:-4], cost

# Function to analyze the state and generate new frontier nodes
def state_analysis(
    dest: tuple[int, str], 
    frontier: dict[int, list[Node]], 
    visited_states: list[tuple[int, str]] = []
):
    new_frontier: list[Node] = []

    # Get the latest frontier and node to analyze
    latest_iteration = max(frontier.keys())
    latest_frontier = frontier[latest_iteration]
    node_to_be_compared = latest_frontier[0]

    for connection in STATION_LINE_CONNECTIONS[node_to_be_compared.state[0]]:

        # Check if the connection has already been visited
        if connection not in visited_states:
            p = node_to_be_compared.p + node_to_be_compared.g # p represents the cost of the path until the current connection
            g = time_between(REAL, node_to_be_compared.state[0], connection[0]) # g represents the cost of the path from the state being analyzed to the current connection
            h = time_between(DIRETA, connection[0], dest[0]) # h represents the straight-line cost of the path from the current connection to the destination

            # evaluating if there'll be a line change
            c = 0
            if connection[1] != node_to_be_compared.state[1]: c = CHANGE_LINE_TIME

            # Add the new node to the new frontier
            new_frontier.append(
                Node(
                    state = connection,
                    p = p,
                    g = g,
                    h = h,
                    c = c,
                )
            )
    
    # Sort the new frontier by the f value
    new_frontier.sort(key=lambda node: node.f)

    # Add the new frontier to the dictionary
    frontier[latest_iteration + 1] = new_frontier

    # Print the new frontier
    print_frontier_nodes(latest_iteration + 1, new_frontier)

    # Add the new frontier to the visited states
    visited_states.append(new_frontier[0].state)

    # Check if the destination has been reached
    if new_frontier[0].state[0] == dest[0]:
        message_solution, extra_cost = print_solution(visited_states, dest)
        print('==============================')
        print('⭐ Found solution!')
        print(f'🚆 Solution: {message_solution}')
        print(f'🕐 Cost: {new_frontier[0].f + extra_cost} minutes')
        return
    
    # Call the state analysis function again
    state_analysis(
        dest = dest,
        frontier = frontier,
        visited_states = visited_states
    )

# A* search algorithm
def a_star(start: tuple[int, str], dest: tuple[int, str]):
    
    # Print the initial frontier nodes
    print_frontier_nodes(1, [Node(state=start, p=0, g=0, h=time_between(DIRETA, start[0], dest[0]))])

    # If start and destination are the same, return the start node
    if start == dest: return [start]
    
    # Perform state analysis to find the path
    state_analysis(
        dest = dest,
        frontier = {
            1: [
                Node(
                    state = start, 
                    p = 0,
                    g = 0,
                    h = time_between(DIRETA, start[0], dest[0])
                )
            ],
        },
        visited_states = [start]
    )

# Function to check if a number is within the station number bounds
def number_not_in_bounds(number: int): return number < LOWEST_STATION_NUMBER or number > HIGHEST_STATION_NUMBER

# Function to check if a line is within the valid lines
def line_not_in_bounds(line: str): return line not in STATION_LINES

# Function to check if a line is not in a station
def line_not_in_station(line: str, station: int): return line not in AVAILABLE_LINES[station]

# Command-line interface function
def cli():
    # Get input from the user and validate it
    start_number = int(input("🔜 Enter start station: "))
    if number_not_in_bounds(start_number):
        print(f"⛔ Station {start_number} does not exist")
        exit()

    start_line = input("🔜 Enter start line (yellow, blue, red OR green): ")
    if line_not_in_bounds(start_line):
        print(f"⛔ Line {start_line} does not exist")
        exit()
    if line_not_in_station(start_line, start_number):
        print(f"⛔ Line {start_line} does not pass through station {start_number}")
        exit()
    
    dest_number = int(input("🔚 Enter destination station: "))
    if number_not_in_bounds(dest_number):
        print(f"⛔ Station {dest_number} does not exist")
        exit()
    
    dest_line = input("🔚 Enter destination line (yellow, blue, red OR green): ")
    if line_not_in_bounds(dest_line):
        print(f"⛔ Line {dest_line} does not exist")
        exit()
    if line_not_in_station(dest_line, dest_number):
        print(f"⛔ Line {dest_line} does not pass through station {dest_number}")
        exit()

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
