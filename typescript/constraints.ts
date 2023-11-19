import * as fs from 'fs';
import * as csvParser from 'csv-parser';

const REAL: string = "Real";
const DIRETA: string = "Direta";

const TRAIN_VELOCITY: number = 30;
const CHANGE_LINE_TIME: number = 4;

const LOWEST_STATION_NUMBER: number = 1;
const HIGHEST_STATION_NUMBER: number = 14;

const STATION_LINES: string[] = ['blue', 'yellow', 'red', 'green'];

const csvRealData = `,E1,E2,E3,E4,E5,E6,E7,E8,E9,E10,E11,E12,E13,E14
E1,-,10,,,,,,,,,,,,
E2,,-,8.5,,,,,,10,3.5,,,,
E3,,,-,6.3,,,,,9.4,,,,18.7,
E4,,,,-,13,,,15.3,,,,,12.8,
E5,,,,,-,3,2.4,30,,,,,,
E6,,,,,,-,,,,,,,,
E7,,,,,,,-,,,,,,,
E8,,,,,,,,-,9.6,,,6.4,,
E9,,,,,,,,,-,,12.2,,,
E10,,,,,,,,,,-,,,,
E11,,,,,,,,,,,-,,,
E12,,,,,,,,,,,,-,,
E13,,,,,,,,,,,,,-,5.1
E14,,,,,,,,,,,,,,-`;

const rowsReal = csvRealData.split('\n');
const headersReal = rowsReal[0].split(',');

const REAL_DISTANCES_CSV: Record<string, Record<string, number>> = {};

for (let i = 1; i < rowsReal.length; i++) {
    const values = rowsReal[i].split(',');
    const row: Record<string, number> = {};

    for (let j = 1; j < values.length; j++) {
        const value = values[j];
        const header = headersReal[j];

        if (value !== '-') {
            row[header] = parseFloat(value);
        }
    }

    REAL_DISTANCES_CSV[values[0]] = row;
}

const csvDirectData = `E1,E2,E3,E4,E5,E6,E7,E8,E9,E10,E11,E12,E13,E14
E1,-,10,18.5,24.8,36.4,38.8,35.8,25.4,17.6,9.1,16.7,27.3,27.6,29.8
E2,,-,8.5,14.8,26.6,29.1,26.1,17.3,10,3.5,15.5,20.9,19.1,21.8
E3,,,-,6.3,18.2,20.6,17.6,13.6,9.4,10.3,19.5,19.1,12.1,16.6
E4,,,,-,12,14.4,11.5,12.4,12.6,16.7,23.6,18.6,10.6,15.4
E5,,,,,-,3,2.4,19.4,23.3,28.2,34.2,24.8,14.5,17.9
E6,,,,,,-,3.3,22.3,25.7,30.3,36.7,27.6,15.2,18.2
E7,,,,,,,-,20,23,27.3,34.2,25.7,12.4,15.6
E8,,,,,,,,-,8.2,20.3,16.1,6.4,22.7,27.6
E9,,,,,,,,,-,13.5,11.2,10.9,21.2,26.6
E10,,,,,,,,,,-,17.6,24.2,18.7,21.2
E11,,,,,,,,,,,-,14.2,31.5,35.5
E12,,,,,,,,,,,,-,28.8,33.6
E13,,,,,,,,,,,,,-,5.1
E14,,,,,,,,,,,,,,-`;

const rowsDirect = csvDirectData.split('\n');
const headersDirect = rowsDirect[0].split(',');

const DIRECT_DISTANCES_CSV: Record<string, Record<string, number | string>> = {};

for (let i = 1; i < rowsDirect.length; i++) {
    const values = rowsDirect[i].split(',');
    const row: Record<string, number> = {};

    for (let j = 1; j < values.length; j++) {
        const value = values[j];
        const header = headersDirect[j];

        if (value !== '-') {
            row[header] = parseFloat(value);
        }
    }

    DIRECT_DISTANCES_CSV[values[0]] = row;
}

const STATION_LINE_CONNECTIONS: { [key: number]: [number, string][] } = {
        1: [[2, 'blue']],
        2: [[1, 'blue'], [10, 'yellow'], [9, 'yellow'], [3, 'blue']],
        3: [[2, 'blue'], [4, 'blue'], [9, 'red'], [13, 'red']],
        4: [[3, 'blue'], [5, 'blue'], [8, 'green'], [13, 'green']],
        5: [[4, 'blue'], [6, 'blue'], [7, 'yellow'], [8, 'yellow']],
        6: [[5, 'blue']],
        7: [[5, 'yellow']],
        8: [[4, 'green'], [5, 'yellow'], [9, 'yellow'], [12, 'green']],
        9: [[2, 'yellow'], [3, 'red'], [8, 'yellow'], [11, 'red']],
        10: [[2, 'yellow']],
        11: [[9, 'red']],
        12: [[8, 'green']],
        13: [[3, 'red'], [4, 'green'], [14, 'green']],
        14: [[13, 'green']]
};

export {
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
}
