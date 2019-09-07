import csv
import time
import ast
import numpy as np
from heapq import nlargest

start = time.time()

max_cost = 0
rev_sum = np.array([])


def read_inputs():
    input_text = list(csv.reader(open('input.txt', 'r'), delimiter=','))
    return input_text


def write_output(output_data):
    output = open('output.txt', 'w')
    output.write(str(output_data).rstrip())
    output.close()


def assign_variables(input_text):
    global city_area, officers, scooters
    city_area = int((input_text[0])[0])
    #city_area = 12
    officers = int((input_text[1])[0])
    #officers = 6
    scooters = int((input_text[2])[0])
    return [city_area, officers, scooters]


def read_scooter_positions(scooters, input_text):
    scooter_positions = []
    for i in range(3, (scooters * 12)+3):
        scooter_positions.append(input_text[i])
    return scooter_positions


def create_heuristic_dict(scooter_positions):
    heuristic_dict = {}
    for position in scooter_positions:
        heuristic_dict[str(position)] = scooter_positions.count(position)
    return heuristic_dict


def create_solution_grid(heuristic_dict):
    grid = [0] * city_area
    for i in range(city_area):
        grid[i] = [0] * city_area

    for key in heuristic_dict.keys():
        i = (ast.literal_eval(key))[0]
        j = (ast.literal_eval(key))[1]
        grid[int(i)][int(j)] = heuristic_dict.get(key)
    return grid


def find_grid_heuristic(grid):
    global rev_sum, max_grid
    max_grid = np.max(grid, axis =0)
    rev_sum = np.cumsum(max_grid[::-1])[::-1]


def create_city(city_area):
    board = [0] * city_area
    for ix in range(city_area):
        board[ix] = [0] * city_area
    return board


def find_np_grid(max_grid):
    global np_grid
    np_grid = [[0 for x in range(city_area + 1)] for y in range(officers + 1)]
    for i in range(city_area+1):
        for j in range(officers+1):
            np_grid[j][i] = sum(nlargest(j, max_grid[i:]))

    return np_grid


def place_officers(board, col, officers_placed, grid, total_cost):
    global max_cost, rev_sum, officers, city_area, np_grid

    if col >= city_area:
        return
    if officers == officers_placed:
        return
    if city_area - col < officers - officers_placed:
        return
    if total_cost + np_grid[officers-officers_placed][col] < max_cost:
        return

    for i in range(city_area):
        if is_safe_position(board, i, col):
            board[i][col] = 1
            officers_placed += 1
            total_cost += grid[i][col]
            if officers_placed == officers:
                if max_cost < total_cost:
                    max_cost = total_cost
            place_officers(board, col + 1,  officers_placed, grid, total_cost)
            board[i][col] = 0
            officers_placed -= 1
            total_cost -= grid[i][col]
    place_officers(board, col + 1,  officers_placed, grid, total_cost)


def is_safe_position(board, row, col):
    for y_coord in range(col):
        if board[row][y_coord] == 1:
            return False

    x_coord = row
    y_coord = col

    while (x_coord >= 0) and (y_coord >= 0):
        if board[x_coord][y_coord] == 1:
            return False
        x_coord = x_coord - 1
        y_coord = y_coord - 1

    x_col = row
    y_col = col

    while x_col < city_area and y_col >= 0:
        if board[x_col][y_col] == 1:
            return False
        x_col = x_col + 1
        y_col = y_col - 1

    return True


#Program starts here
inputs = read_inputs()
input_dict = assign_variables(inputs)
scooters = input_dict[2]
officers = input_dict[1]
city_area = input_dict[0]

scooter_positions = read_scooter_positions(scooters, inputs)

heuristic_dict = create_heuristic_dict(scooter_positions)

board = create_city(city_area)

grid = create_solution_grid(heuristic_dict)
#grid = [[6, 28, 11, 22, 12, 11, 27, 33, 11, 50, 48, 31], [39, 0, 15, 0, 12, 10, 32, 20, 33, 38, 4, 37], [31, 17, 44, 28, 48, 9, 20, 21, 28, 1, 22, 28], [23, 0, 23, 40, 49, 22, 31, 9, 43, 27, 12, 29], [2, 15, 28, 3, 5, 23, 48, 27, 36, 17, 35, 16], [8, 39, 10, 18, 4, 38, 26, 38, 2, 18, 23, 38], [36, 10, 5, 50, 12, 39, 27, 45, 44, 0, 36, 42], [1, 5, 24, 2, 1, 4, 24, 24, 46, 2, 7, 31], [5, 3, 21, 30, 50, 49, 26, 18, 35, 10, 2, 18], [6, 15, 35, 3, 1, 28, 8, 39, 32, 29, 25, 39], [1, 33, 43, 32, 16, 38, 24, 7, 48, 2, 11, 31], [30, 48, 23, 37, 26, 19, 38, 29, 25, 22, 4, 1]]

find_grid_heuristic(grid)

np_grid = find_np_grid(max_grid)

#Call solver
place_officers(board, 0,  0, grid, 0)

output_data = max_cost

write_output(output_data)

print "Max Activity Points:",output_data
end_time = time.time() - start
print "Took", end_time, " to finish"
