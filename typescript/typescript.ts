import * as readlineSync from 'readline-sync';

// Import necessary modules and classes
import { 
    REAL,
    DIRETA,
    TRAIN_VELOCITY,
    CHANGE_LINE_TIME,
    LOWEST_STATION_NUMBER,
    HIGHEST_STATION_NUMBER,
    STATION_LINES,
    REAL_DISTANCES_CSV,
    DIRECT_DISTANCES_CSV,
    STATION_LINE_CONNECTIONS
} from './constraints';

// Define the Node class
class Node {
    state: [number, string];
    parent: Node | null;
    cost: number;
    real_cost: number;

    constructor(state: [number, string], parent: Node | null, cost: number, real_cost: number = 0) {
        this.state = state;
        this.parent = parent;
        this.cost = cost;
        this.real_cost = real_cost;
    }
}

// Function to retrieve distances from a spreadsheet
function pegar_planilha(lista: string, E1: number, E2: number): number | undefined {
    // Convert station numbers to zero-based indexing
    const E: [number, number] = [E1, E2];
    E.sort();

    // Retrieve distances based on the type of list (Direta or Real)
    if (lista === "Direta") {
        if (DIRECT_DISTANCES_CSV[`E${E[0].toString()}`][`E${E[1].toString()}`] === "-") {
            return 0.0;
        }
        return DIRECT_DISTANCES_CSV[`E${E[0].toString()}`][`E${E[1].toString()}`] as number;
    } else if (lista === "Real") {
        try {
            return REAL_DISTANCES_CSV[`E${E[0].toString()}`][`E${E[1]}`];
        } catch {
            return -1;
        }
    }
}

// Function to calculate time based on distance
function get_time_by_distance(distance: number | undefined): number {
    const distanceToCalc = distance ? distance : 0;
    return distanceToCalc / TRAIN_VELOCITY * 60;
}

// Function to print the nodes in the frontier
function print_frontier_nodes(index: number, frontier: Node[], nodes_that_were_first: [ [number, string], number ][] = []): void {
    let message = `Fronteira ${index}:`;
    for (const node of frontier) {
        if (!nodes_that_were_first.some(([state, cost]) => state === node.state && cost === node.cost)) {
            message += `\n${node.state}: ${node.cost}`;
        }
    }
    console.log('==============================');
    console.log(message);
}

function print_solution(node: Node): string {
    let solution = `${node.state}`;
    let node_parent = node.parent;
    while (node_parent) {
        solution = `${node_parent.state} -> ${solution}`;
        node_parent = node_parent.parent;
    }
    return solution;
}

// Function to analyze the state and generate new frontier nodes
function state_analysis(
    start: [number, string],
    dest: [number, string],
    original_frontier: { [key: number]: Node[] },
    nodes_that_were_first: [ [number, string], number ][] = []
): Node[] {
    // Get the latest frontier and node to analyze
    const latest_iteration = Math.max(...Object.keys(original_frontier).map(Number));
    const latest_frontier = original_frontier[latest_iteration];
    const node_to_analyse = latest_frontier[0];

    // Generate new frontier nodes based on line connections
    const new_frontier: Node[] = [];
    for (const connection of STATION_LINE_CONNECTIONS[node_to_analyse.state[0]]) {
        // If the line of the connection is the same as the line of the node to analyze
        if (connection[1] === node_to_analyse.state[1]) {
            // Calculate real and direct distances
            const real_distance = get_time_by_distance(pegar_planilha(REAL, node_to_analyse.state[0], connection[0]));
            const direct_distance = get_time_by_distance(pegar_planilha(DIRETA, connection[0], dest[0]));

            // Calculate real cost by summing the real costs of parent nodes
            let real_cost = 0;
            let node_parent: Node | null = node_to_analyse;
            while (node_parent) {
                real_cost += node_parent.real_cost;
                node_parent = node_parent.parent;
            }

            // Calculate total cost and create new node
            const total_cost = real_cost + direct_distance + real_distance;
            new_frontier.push(
                new Node(
                    connection,
                    node_to_analyse,
                    total_cost,
                    real_cost + direct_distance
                )
            );
        }
        // Else, we insert a node that represent the change of line, but staying in the same station
        else if (!new_frontier.some(node => node.state[0] === node_to_analyse.state[0] && node.state[1] === connection[1])) {
            // Calculate direct distance and total cost for changing lines
            const real_distance = 0;
            const direct_distance = get_time_by_distance(pegar_planilha(DIRETA, node_to_analyse.state[0], dest[0]));

            // Calculate real cost by summing the real costs of parent nodes
            let real_cost = 0;
            let node_parent: Node | null = node_to_analyse;
            while (node_parent) {
                real_cost += node_parent.real_cost;
                node_parent = node_parent.parent;
            }

            // Calculate total cost and create new node
            const total_cost = real_cost + direct_distance + real_distance + CHANGE_LINE_TIME;
            new_frontier.push(
                new Node(
                    [node_to_analyse.state[0], connection[1]],
                    node_to_analyse,
                    total_cost,
                    real_cost + direct_distance
                )
            );
        }
    }

    // Sort the new frontier based on cost and print the nodes
    new_frontier.push(...latest_frontier.slice(1));
    new_frontier.sort((a, b) => a.cost - b.cost);
    print_frontier_nodes(latest_iteration + 1, new_frontier, nodes_that_were_first);

    // Find the first node in the new frontier that has not been analyzed
    let first_node_not_analysed: Node | null = null;
    for (const node of new_frontier) {
        if (!nodes_that_were_first.some(([state, cost]) => state === node.state && cost === node.cost)) {
            first_node_not_analysed = node;
            nodes_that_were_first.push([first_node_not_analysed.state, first_node_not_analysed.cost]);
            break;
        }
    }

    // If the first unanalyzed node is the destination, print "Found!"
    if (first_node_not_analysed && first_node_not_analysed.state === dest) {
        console.log('==============================');
        console.log("Found!");
        console.log(`Solução: ${print_solution(first_node_not_analysed)}`);
        console.log(`Custo: ${first_node_not_analysed.cost} minutes`);
        return new_frontier;
    }

    // Add the new frontier to the original frontier and recursively call state_analysis
    original_frontier[latest_iteration + 1] = new_frontier;
    return state_analysis(
        start,
        dest,
        original_frontier,
        nodes_that_were_first
    );
}

// A* search algorithm
function a_star(start: [number, string], dest: [number, string]): void {
    // Print the initial frontier nodes
    print_frontier_nodes(1, [new Node(start, null, get_time_by_distance(pegar_planilha(DIRETA, start[0], dest[0])))]);

    // If start and destination are the same, return the start node
    if (!(start[0] === dest[0]) || !(start[1] === dest[1])) {
        // Perform state analysis to find the path
        state_analysis(
            start,
            dest,
            {
                1: [
                    new Node(
                        start,
                        null,
                        get_time_by_distance(pegar_planilha(DIRETA, start[0], dest[0]))
                    )
                ]
            }
        );
    }

}

// Function to check if a number is within the station number bounds
function number_not_in_bounds(number: number): boolean {
    return number < LOWEST_STATION_NUMBER || number > HIGHEST_STATION_NUMBER;
}

// Function to check if a line is within the valid lines
function line_not_in_bounds(line: string): boolean {
    return !STATION_LINES.includes(line);
}

// Command-line interface function
function cli(): void {
    // Get input from the user and validate it
    const start_number = parseInt(readlineSync.question("🔜 Enter start station: ") || "", 10);
    if (number_not_in_bounds(start_number)) {
        throw new Error(`Station ${start_number} does not exist`);
    }

    const start_line = readlineSync.question("🔜 Enter start line (yellow, blue, red OR green): ") || "";
    if (line_not_in_bounds(start_line)) {
        throw new Error(`Line ${start_line} does not exist`);
    }

    const dest_number = parseInt(readlineSync.question("🔚 Enter destination station: ") || "", 10);
    if (number_not_in_bounds(dest_number)) {
        throw new Error(`Station ${dest_number} does not exist`);
    }

    const dest_line = readlineSync.question("🔚 Enter destination line (yellow, blue, red OR green): ") || "";
    if (line_not_in_bounds(dest_line)) {
        throw new Error(`Line ${dest_line} does not exist`);
    }

    // Convert input to tuples
    const start_tuple: [number, string] = [start_number, start_line];
    const dest_tuple: [number, string] = [dest_number, dest_line];

    // Call the A* algorithm with the inputs
    a_star(start_tuple, dest_tuple);
}

// Call the command-line interface function
cli();
