from flask import Flask, jsonify, request, session, send_file
from flask_cors import CORS
import heapq
import copy
import numpy as np
import re 
import json

from datetime import datetime
from utils.logger import server_logger
import os
from datetime import datetime
import read_manifest
from read_manifest import Container

from functools import lru_cache
import numpy as np

# app instance
# You will need to create a virtual environment named 'venv' to use (venv is the name specified in the gitignore)
# Windows user might be barred from creating venv; run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Windows: python -m venv venv -> venv/Scripts/activate
# LINUX/UNIX: virutalenv venv -> source venv/bin/activate

# # to kill venv process: deactivate

grid = [[7, -1, 12, -1, 31, 1, -1, -1, 10, -1, -1, -1],
        [1, -1, 51, -1, 21, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, 10, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, 15, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, 3, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]

grid2 = [[-2, 1, 2, -2, -1, -1, -1, -1, -1, -1, -1, -2],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]

# unload = {"1": 1, "3": 1} # "1": 1, "3": 1
load = 1
# /api/home
# @app.route("/api/home", methods=['GET'])
# def return_home():
#     return jsonify({
#         'message': "Testing Testing Testing",
#     })

# begin funcs
# Creating a function that will take each container in the grid and give it an ID based on it's name.
# Duplicate names get the same ID
def createIDS(grid: list[list[Container]]):
    count = 0
    dict = {}
    for row in grid:
        for col in row:
            if col.get_name() in dict:
                continue
            else:
                dict[col.get_name()] = count
                print("the count for some reason:", count)
                count += 1
    return dict

# Creating a fucntion that takes in a list of container names that are to be unloaded, and the IDs created above
# it will output a new dictionary that is how many of each container to remove based on it's ID
# We are doing it this way ot hopefully save space that way we can represent the grid as just ints and not strings
def createToUnload(toUnload, iDs):
    unload = np.zeros(len(iDs))
    print("IIIIIIIIIIIII")
    print(iDs)
    print(toUnload)
    for container in toUnload:
        if iDs[container]:
            unload[iDs[container]] += 1
    print("jugg messiah:", (unload[0]), type(unload[0]))
    return unload

def manifestToGrid(gridContainerClass: list[list[Container]]):
    # take the container class from the read manfiest function, generate a names only representation of this
    nameGrid = [[0 for _ in range(12)] for _ in range(8)]

    for i in range(8):
        for j in range(12):
            nameGrid[i][j] = gridContainerClass[i][j].get_name()

    return nameGrid

def manifestToGridLoad(gridContainerClass: list[list[Container]], iDs):
    numGrid = np.zeros((8, 12))
    for i in range(8):
        for j in range(12):
            if gridContainerClass[i][j].get_name() == "NAN":
                numGrid[i][j] = -2
                continue
            elif gridContainerClass[i][j].get_name() == "UNUSED":
                numGrid[i][j] = -1
                continue
            numGrid[i][j] = iDs[gridContainerClass[i][j].get_name()]
    return numGrid
def manifestToNum(gridContainerClass: list[list[Container]]):
    # take the container class from the read manfiest function, generate a numbers only representation of this
    numGrid = [[0 for _ in range(12)] for _ in range(8)]

    for i in range(8):
        for j in range(12):
            if gridContainerClass[i][j].get_name() == "NAN":
                numGrid[i][j] = -2
                continue
            elif gridContainerClass[i][j].get_name() == "UNUSED":
                numGrid[i][j] = -1
                continue
            numGrid[i][j] = gridContainerClass[i][j].get_weight()

    return numGrid

def generateSteps(soln, startGrid):
    steps = []
    steps.append(startGrid)

    for i in range(len(soln)):
        startR, startC = soln[i][0], soln[i][1]
        endR, endC = soln[i][2], soln[i][3]
        nextStep = copy.deepcopy(steps[i])

        tmp = nextStep[endR][endC]
        nextStep[endR][endC] = nextStep[startR][startC]
        nextStep[startR][startC] = tmp

        steps.append(nextStep)
    return steps

def generateLURender(soln, startGrid):
    steps = []
    steps.append(startGrid)
    count = 96
    for i in range(len(soln)):
        action = soln[i][2]
        xPos, yPos = soln[i][0], soln[i][1]

        nextGrid = copy.deepcopy(steps[i])
        if action == -1:
            nextGrid[xPos][yPos] = str(count)
            count += 1
        elif action == -2:
            nextGrid[xPos][yPos] = "UNUSED"
        else:
            nextGrid[action][soln[i][3]] = nextGrid[xPos][yPos]
            nextGrid[xPos][yPos] = "UNUSED"
        steps.append(nextGrid)
    return steps

def generateStepsLoadUnload(solution, startGrid):
    steps = []
    steps.append(startGrid)

    # Extract the solution output format (similar to what `balance` function uses)
    #for move in solution:  # solution should be a list of tuples like [(r1, c1, r2, c2), ...]
        #startR, startC, endR, endC = move
        #nextStep = copy.deepcopy(steps[-1])

        #tmp = nextStep[endR][endC]
        #nextStep[endR][endC] = nextStep[startR][startC]
        #nextStep[startR][startC] = tmp

        #steps.append(nextStep)

    return steps

def hueristicBalance(grid):
    # return 1
    leftSum = 0
    rightSum = 0
    right = []
    left = []
    for i in range(6):
        for j in range(8):
            leftSum += grid[j][i]
            rightSum += grid[j][i + 6]
            if grid[j][i] > 0:
                left += [(grid[j][i], j, i)]
            if grid[j][i + 6] > 0:
                right += [(grid[j][i + 6], j, i + 6)]
    right.sort(reverse=True)
    left.sort(reverse=True)
    delta = abs(rightSum - leftSum)
    imbalance = delta / max(leftSum, rightSum)
    cost = 0
    if imbalance < 0.1:
        return 0
    if(leftSum > rightSum):
        for weight, row, collumn in left:
            if imbalance - weight > 0:
                imbalance -= weight
                cost += abs(collumn - 6) + 1
                rightSum += weight
                leftSum -= weight
            elif abs((rightSum + weight) - (leftSum - weight)) / max((leftSum - weight), (rightSum + weight)): # see if we can move this container to the other side 
                cost += abs(collumn - 6) + 1
                return cost * 2
            else:
                continue
    else:
        for weight, row, collumn in right:
            if imbalance - weight > 0:
                imbalance -= weight
                cost += abs(collumn - 6) + 1
                rightSum -= weight
                leftSum += weight
            elif abs((leftSum + weight) - (rightSum - weight)) / max((rightSum - weight), (leftSum + weight)): # see if we can move this container to the other side 
                cost += abs(collumn - 6) + 1
                return cost * 2
            else:
                continue
    return cost


# Using a simple recusrive 0 1 knapsack algorithm to calculate whether it is possible to balance the grid or not
# This is an algorithm that I wrote many times in CS 119/142 and more complicated versions in CS218.
# It was introduced to us in CS141
def recursiveKnap(n, w, dp, weights, values):
    if w == 0:
        return 0
    if n == 0:
        return 0
    if dp[n - 1][w - 1] > 0:
        return dp[n - 1][w - 1]
    if w < weights[n - 1]:
        return recursiveKnap(n - 1, w, dp, weights, values)

    not_taken = recursiveKnap(n - 1, w, dp, weights, values)
    taken = values[n - 1] + recursiveKnap(n - 1, w - weights[n - 1], dp, weights, values)

    if taken > not_taken:
        dp[n - 1][w - 1] = taken
        return taken

    dp[n - 1][w - 1] = not_taken
    return not_taken

def canBalance(grid): # first we will check if can be balanced, if so it will just return true, otherwise it will return true, and (0, 0) otherwise, false nad (leftweight, rightweight) wieghts after sift
    weights = []
    for i in range(6):
            for j in range(8):
                if grid[j][i] >= 0:
                    weights.append(grid[j][i])
                if grid[j][i + 6] >= 0:
                    weights.append(grid[j][i + 6])
    weights.sort(reverse=True)
    sum = np.sum(weights)
    dp = np.zeros((len(weights), sum // 2))
    total = recursiveKnap(len(weights), sum // 2, dp, weights, weights)
    if(((sum - total) - total) / (sum - total) <= 0.1):
        return True, 0, 0
    left = 0
    right = 0
    for i in range(len(weights)):
        if i % 2 == 0:
            left += weights[i]
        else:
            right += weights[i]
    print(f"Left Goal: {left}, Right Goal: {right}")
    return False, left, right
    
def balance(grid):
    # create a queue
    # add start state to queue
    # While q is not empty, or optimal not found 
        # pop a grid off the queue
        # check if it is goal
        # if goal break
        # for each possible move, add it to the queue.
    server_logger.info("Starting balance algorithm")
    heap = []
    heapq.heappush(heap, (0, grid, [], 0, (8, 0)))
    count = 0
    visited = set()
    canB, leftGoal, rightGoal = canBalance(grid)
    while(heap):
        count += 1
        hCost, curr_grid, path, curr_cost, pos = heapq.heappop(heap)
        gridTuple = tuple(tuple(row) for row in curr_grid)
        if gridTuple in visited:
            continue
        visited.add(gridTuple)
        if(count % 100 == 0):
                    print(curr_cost)
        topContainers = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 , -1]
        left = 0
        right = 0
        for i in range(6):
            for j in range(8):
                if curr_grid[j][i] >= 0:
                    topContainers[i] = j
                    left += curr_grid[j][i]
                elif curr_grid[j][i] == -2:
                    topContainers[i] = j
                if curr_grid[j][i + 6] >= 0:
                    topContainers[i + 6] = j
                    right += curr_grid[j][i + 6]
                elif curr_grid[j][i + 6] == -2:
                    topContainers[i + 6] = j
        if((left != 0 and right != 0 and abs(left - right) / left < 0.1) or (not canB and ((left <= leftGoal and right >= rightGoal)))):
            print(f"Left : {left}, Right : {right} CanBalance: {canB}")
            container_count = sum(1 for row in curr_grid for cell in row if cell >= 0)
            server_logger.info(f"Balance operation completed. Final container count: {container_count}")
            # balanced
            return curr_cost, curr_grid, path
        maxToContainer = -1
        for i in range(12):
            if topContainers[i] == -1:
                continue
            elif curr_grid[topContainers[i]][i] == -2:
                continue
            index = topContainers[i] # this is the row index of the highest container in column i
            # first calculate the cost it will take to get from the cranes current position to this specific container
            craneCost = 0
            if i == pos[1]:
                maxToContainer = -1
                craneCost = pos[0] - index
                if index == pos[0]:
                    craneCost = 0
            elif(maxToContainer < index or maxToContainer < pos[0]):
                craneCost = max(index, pos[0]) - index + max(index, pos[0]) - pos[0] + abs(pos[1] - i)
            else:
                craneCost = maxToContainer - index + maxToContainer - pos[0] + abs(pos[1] - i)
            cost = 0
            if topContainers[i] >= maxToContainer:
                maxToContainer = topContainers[i] + 1
            maxFromContainer = -1
            if(index == -1):
                continue
            for j in range(12):
                if j == i:
                    maxFromContainer = -1
                    continue
                if topContainers[j] == 7:
                    continue
                if topContainers[j] >= maxFromContainer:
                    maxFromContainer = topContainers[j] + 1
                k = topContainers[j] # this is the row index of the highest container in column j
                k = k + 1 #0 add 1 to k beacause we need to place the container ontop of the container at kj
                if(maxFromContainer < index or maxFromContainer < k):
                    cost = max(index, k) - index + max(index, k) - k + abs(j - i) + craneCost
                else:
                    cost = maxFromContainer - index + maxFromContainer - k + abs(j - i) + craneCost
                if(cost < 0):
                    print("NEGATIVE!!!!!!!")
                    return None
                # moving container from top of column i, to top of column j
                newgrid = [row[:] for row in curr_grid]
                newgrid[k][j] = newgrid[index][i]
                newgrid[index][i] = -1
                heapq.heappush(heap, (curr_cost + cost + hueristicBalance(newgrid), newgrid, path + [(index, i, k, j, cost)], curr_cost + cost, (k, j)))
    return None

def balanceOutput(grid: list[list[Container]], steps):
    output = [grid]
    for item in steps:
        newgrid = [row[:] for row in output[-1]]
        newgrid[item[2]][item[3]] = output[-1][item[0]][item[1]]
        newgrid[item[0]][item[1]] = 0
        output += [newgrid]

def customKey(item):
    return item[0]

def hueristicLoad(grid, toUnload, toLoad):
    # return sum(toUnload.values()) * 4 + toLoad * 2 # This is faster but also a larger underestimate of the cost
    count = np.sum(toUnload)
    if(not count and not toLoad):
        return 0
    if(not count):
        return 4 * toLoad
    unload = np.copy(toUnload)
    unloadCosts = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] < 96 and grid[i][j] >= 0 and unload[int(grid[i][j])]:
                unloadCosts += [(8 - i + j + 2, i, j)]
    totalCost = 4 * toLoad

    for cost, row, col in unloadCosts:
        if grid[row][col] < 96 and unload[int(grid[row][col])]:
            totalCost += cost
            unload[int(grid[row][col])] -= 1
            count -= 1
            if(count == 0):
                return totalCost
            if(not toLoad):
                totalCost += 2
            toLoad -= 1
    return totalCost

def loadUnload(grid, toUnload, toLoad):
    server_logger.info("Starting Load/Unload algorithm")
    heap = []
    npGrid = np.array(grid)
    global numOfStates
    numOfStates = 0
    heapq.heappush(heap, (0, numOfStates, npGrid, [], 0, toLoad, toUnload, (8, 0), 1))
    count = 0
    visited = set()
    while(heap):
        count += 1
        hCost, _, curr_grid, path, curr_cost, load, toUnload, pos, craneDocked = heapq.heappop(heap)
        unload = toUnload.copy()
        unloadCopy = tuple(unload)  # For immutability in `visited`
        gridTuple = tuple(map(tuple, curr_grid))  # Immutable grid representation
        if (gridTuple, unloadCopy) in visited:
            continue
        visited.add((gridTuple, unloadCopy))
        gridTuple = tuple(tuple(row) for row in curr_grid)

        if(not load and not np.any(unload)):
            # finished
            container_count = sum(1 for row in curr_grid for cell in row if cell >= 0)
            server_logger.info(f"Load/Unload operation completed. Final container count: {container_count}")
            with open("./globals/weights.txt", 'w') as file:
                for line in curr_grid:
                    for weight in line:
                        file.write(f"{int(weight)}\n")
            return curr_cost, curr_grid, path
        if(count % 100 == 0):
            print(hCost)
        topContainers = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 , -1]
        for col in range(12):
            for row in range(8):
                if curr_grid[row][col] != -1:
                    topContainers[col] = row
                else:
                    break
        maxToContainer = -1
        for col, row in enumerate(topContainers):
            if row == -1:
                continue
            elif curr_grid[row][col] == -2:
                if(load and row < 7):
                    newgrid = np.copy(curr_grid)
                    cost = 8 - row + col + 2
                    newgrid[row + 1][col] = 96 + toLoad - load #give a unique id
                    if(not craneDocked):
                        cost += 2 + 8 - pos[0] + pos[1]
                    numOfStates += 1
                    heapq.heappush(heap, (curr_cost + cost + hueristicLoad(newgrid, unload, load - 1), numOfStates, newgrid, path + [(row + 1, col, -1, 0, cost)], curr_cost + cost, load - 1, unload, (row + 1, col), False))
                continue

            # first calculate the cost it will take to get from the cranes current position to this specific container
            craneCost = 0
            if col == pos[1]:
                maxToContainer = -1
                craneCost = pos[0] - row
                if row == pos[0]:
                    craneCost = 0
            elif(maxToContainer < row or maxToContainer < pos[0]):
                craneCost = max(row, pos[0]) - row + max(row, pos[0]) - pos[0] + abs(pos[1] - col)
            else:
                craneCost = maxToContainer - row + maxToContainer - pos[0] + abs(pos[1] - col)
            # now we have the baseline cost to get from wherever the container was before to the container we are trying to move
            maxFromContainer = -1
            if(row == -1):
                continue
            for j in range(12):
                if j == col:
                    maxFromContainer = -1
                    continue
                if topContainers[j] == 7:
                    continue
                if topContainers[j] >= maxFromContainer:
                    maxFromContainer = topContainers[j] + 1
                cost = 0
                k = topContainers[j] # this is the row index of the highest container in column j
                k = k + 1 #0 add 1 to k beacause we need to place the container ontop of the container at kj
                if(maxFromContainer < row or maxFromContainer < k):
                    cost = max(row, k) - row + max(row, k) - k + abs(j - col) + craneCost
                else:
                    cost = maxFromContainer - row + maxFromContainer - k + abs(j - col) + craneCost
                if(cost < 0):
                    print("NEGATIVE!!!!!!!")
                    return None
                newgrid = np.copy(curr_grid)
                newgrid[k][j] = newgrid[row][col]
                newgrid[row][col] = -1
                if(craneDocked):
                    cost += 2
                numOfStates += 1
                heapq.heappush(heap, (curr_cost + cost + hueristicLoad(newgrid, unload, load), numOfStates, newgrid, path + [(row, col, k, j, cost)], curr_cost + cost + 1, load, unload, (k, j), False))
            #unload i as well
            # cost is 2 from ship to truck and whatever the cost inside the ship is(collum + 8 - row)
            if(load):
                if(row < 7):
                    newgrid = np.copy(curr_grid)
                    cost = col + 8 - row + 2
                    newgrid[row + 1][col] = 96 + toLoad - load #give a unique id
                    if(not craneDocked):
                       cost += 2 + 8 - pos[0] + pos[1]
                    numOfStates += 1
                    heapq.heappush(heap, (curr_cost + cost + hueristicLoad(newgrid, unload, load - 1), numOfStates, newgrid, path + [(row + 1, col, -1, 0, cost)], curr_cost + cost, load - 1, unload, (row + 1, col), False))
            if(curr_grid[row][col] < 96 and unload[int(curr_grid[row][col])]):
                newgrid = np.copy(curr_grid)
                cost = col + 8 - row + 2 + craneCost
                newgrid[row][col] = -1
                if(craneDocked):
                    cost += 2
                # remove from unload
                newUnload = np.copy(unload)
                newUnload[int(curr_grid[row][col])] -= 1
                numOfStates += 1
                heapq.heappush(heap, (curr_cost + cost + hueristicLoad(newgrid, newUnload, load), numOfStates, newgrid, path + [(row, col, -2, 0, cost)], curr_cost + cost, load, newUnload, (8, 0), True))
    return None

def getCellIndex(cell_str):
    # Use regular expression to extract the first number before the comma
    match = re.match(r"(\d+),", cell_str)
    if match:
        return int(match.group(1))  # Return the first number as an integer
    else:
        raise ValueError("Invalid cell format")

def getCellTitle(index):
    col = index % 12  # Assume there are 12 columns in the grid
    row = 7 - (index // 12)  # For a 8-row grid, assuming index starts at 0
    f = open("./globals/path.txt", "r")
    manifest_name = f.read().strip()
    f.close()
    manifest_path = "./manifests/" + manifest_name
    containerClassGrid = read_manifest.read_manifest(manifest_path)  
    gridNames = manifestToGrid(containerClassGrid) 
    
    try:
        return gridNames[row][col]  # Get the title from gridNames
    except IndexError:
        return "Unknown" 
    
def cellsToUnloadFile(selected_cells, loadSize):
    file_path = "cellsToUnload.txt"

    # check if the file exists and delete it to write a new one
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{file_path} exists and was deleted.")

    # write to a new file with cell titles instead of cell indexes
    with open(file_path, "w") as file:
        print("file open")
        file.write(f"{loadSize}\n")
        for cell in selected_cells:
            print("in loop")
            print(cell)
            index = getCellIndex(cell)
            cell_title = getCellTitle(index)  # Get the title for the index
            file.write(f"{cell_title}\n")

    print("Unload clicked and data saved to cellsToUnload.txt")

# begin routes
app = Flask(__name__)
CORS(app)

@app.route("/log", methods=['POST'])
def log_message():
    try:
        data = request.json
        level = data.get('level', 'info')
        message = f"{data.get('component')}: {data.get('message')}"
        
        if level == 'error':
            server_logger.error(message)
        elif level == 'warning':
            server_logger.warning(message)
        else:
            server_logger.info(message)
        return jsonify({'status': 'success'})
    except Exception as e:
        server_logger.error(f"Error processing log message: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route("/download-logs", methods=['GET'])
def download_logs():
    try:
        date_str = datetime.now().strftime("%Y")
        log_file = os.path.join(os.getcwd(), 'logs', f'KeoghsPort{date_str}.txt')
        
        if os.path.exists(log_file):
            return send_file(
                log_file,
                mimetype='text/plain',
                as_attachment=True,
                download_name=f"KeoghsPort{date_str}.txt"
            )
        return jsonify({'error': 'Log file not found'}), 404
    except Exception as e:
        server_logger.error(f"Error downloading logs: {str(e)}")
        return jsonify({'error': str(e)}), 500


# api route to parse input
@app.route("/test", methods=['GET'])
def read_input():
    server_logger.info("Test endpoint called", remote_addr=request.remote_addr)
    return jsonify({'message': "Placeholder Message"})

# api route to call balance function
@app.route("/balance", methods=['GET'])
def do_balance():
    try:
        server_logger.info("Balance endpoint called", remote_addr=request.remote_addr)
        return jsonify({'message': "Placeholder"})
    except Exception as e:
        server_logger.error("Balance error", error=str(e))
        return jsonify({'error': "Balance operation failed"}), 500

# api route to call load or unload function
@app.route("/loadUnload", methods=['GET'])
def return_home():
    try:
        server_logger.info("LoadUnload endpoint called", remote_addr=request.remote_addr)
        return jsonify({'message': "Placeholder"})
    except Exception as e:
        server_logger.error("LoadUnload error", error=str(e))
        return jsonify({'error': "Load/Unload operation failed"}), 500

# Add global variable to track last request
last_balance_request = None

@app.route("/uploadManifest", methods = ["POST","GET"])
def upload_mainfest():
    if request.method == "POST":
        try:
            manifest = request.files['manifest']

            # here we are saving the manifest to a specified folder in our repo so we have our manifests for later access
            manifest_path = "./manifests/" + manifest.filename
            manifest.save(manifest_path)

            try:
                f = open("./globals/path.txt", "w")
                f.write(manifest.filename)
                server_logger.info(f"Manifest uploaded successfully: {manifest.filename}")
            except Exception as e:
                server_logger.error(f"Failed to upload Manifest: {manifest.filename}")
                print(f"Failed to write to file: {e}")

            # log to the user that the manifest was uplpoaded
            return jsonify({'message': "File uploaded. Press 'OK' to proceed"})
        except Exception as e:
            server_logger.error("Upload manifest error", error=str(e))
            return jsonify({'error': "Upload operation failed"}), 500
    else:
        try:
            global last_balance_request
            # Get current timestamp
            current_request = datetime.now()

            # If there was a recent request (within last 2 seconds), skip processing
            if last_balance_request and (current_request - last_balance_request).total_seconds() < 2:
                return jsonify({'message': 'Request too soon after previous request'}), 429

            # Update last request time
            last_balance_request = current_request

            f = open("./globals/path.txt", "r")
            manifest_name = f.read().strip()
            f.close()
            manifest_path = "./manifests/" + manifest_name

            # pass the actual manifest file that's presumable cached into the balance function
            containerClassGrid = read_manifest.read_manifest(manifest_path)
            
            simpleGrid = manifestToGrid(containerClassGrid) # convert to an array of names
            numericalGrid = manifestToNum(containerClassGrid) # convert to an array of weight
            print(simpleGrid)
            soln = balance(numericalGrid)
            with open("./globals/weights.txt", 'w') as file:
                for weights in soln[1]:
                    for weight in weights:
                        file.write(f"{weight}\n")
            steps = generateSteps(soln[2], simpleGrid)
            last_step = steps[-1]
            with open("./globals/names.txt", 'w') as file:
                for line in last_step:
                    for name in line:
                        file.write(str(name) + "\n")
            print(steps) # generated steps by this point for balancing, now we just have to pass it right
            # print(numericalGrid)
            # print(containerClassGrid)
            print(soln[2])
            #with open("./globals/names.txt", 'w') as file:
            #    for row in soln[2]:
            #        for name in row:
            #            file.write(name + "\n")
            returnItems = [{"steps": steps}, {"moves": soln[2]}, {"cost": soln[0]}]
            return jsonify(returnItems)
        except Exception as e:
            server_logger.error("Error fetching manifest", error=str(e))
            return jsonify({'error': "Fetch failed for manifest"}), 500
      
@app.route("/unloadAction", methods=["POST"])
def unload_action():
    data = request.get_json()

    if not data or "selectedCells" not in data:
        return jsonify({"message": "No cells provided"}), 400

    selected_cells = data["selectedCells"]
    cellsToUnloadFile(selected_cells)
    # Send confirmation message first
    confirmation = f"Confirm: Unload {len(selected_cells)} containers"
    print(confirmation)

    # Return confirmation to the client
    return jsonify({"message": confirmation}), 200


#IM WORKING HERE
#
#
#
#
#
#
#
#
#
#
#   

@app.route("/confirmUnload", methods=["POST"])
def confirm_unload():
    sizeOfMyLoad = request.args.get('loadSize')
    print(sizeOfMyLoad)
    data = request.get_json()

    if not data or "selectedCells" not in data:
        return jsonify({"message": "No cells provided"}), 400

    selected_cells = data["selectedCells"]
    print(selected_cells)
    cellsToUnloadFile(selected_cells, sizeOfMyLoad)
    return jsonify({"message": "Unload action completed and data saved"}), 200

@app.route("/getLoadGrid", methods=["GET"])
def getLUGrid():
    try:
        manifestName = ""
        with open("./globals/path.txt", "r") as file:
            manifestName = file.readline().strip()
        manifest_path = "./manifests/" + manifestName

        # printing the manifest that we're currently using
        print("manifest curr:", manifest_path)

        containerClassGrid = read_manifest.read_manifest(manifest_path)

        # generate necessary data
        shipNames = manifestToGrid(containerClassGrid)
        returnItems = [{"steps": [shipNames]}]

        return jsonify(returnItems)
    except Exception as e:
        server_logger.error("Server Error fetching grid names", error=str(e))
        return jsonify({'error': "Failed to fetch grid names"}), 500

@app.route("/getLUSteps", methods=["GET"])
def generateLUSteps():
    try:
        """
            - get our manifest per usual and create out necessary grids, and supporting information necessary to complete a load/unload duoperation
            - pass that into load unload
            - process the return values to extract the steps
            - format to return to the frontend so that navya can read this
            - THAT BEING SAID:
                - WRITE FUNCTION TO PROCESS STEPS INTO RENDER-READY MATERIAL
                - FORMAT RESPONSE
                - TWEAK FRONTEND TO PICK UP WHAT IM PUTTING DOWN
        """
        
        # global last_load_request
        # # Get current timestamp
        # current_request = datetime.now()

        # # If there was a recent request (within last 2 seconds), skip processing
        # if last_load_request and (current_request - last_load_request).total_seconds() < 2:
        #     return jsonify({'message': 'Request too soon after previous request'}), 429
        
        # last_load_request = current_request
        # create access
        manifestName = ""
        with open("./globals/path.txt", "r") as file:
            manifestName = file.readline().strip()
        containersToUnload = []
        with open("cellsToUnload.txt", "r") as file:
            loadSize = int(file.readline())
            containersToUnload = [line.strip() for line in file]

        manifest_path = "./manifests/" + manifestName

        # printing the manifest that we're currently using
        print("manifest curr:", manifest_path)

        containerClassGrid = read_manifest.read_manifest(manifest_path)

        # generate necessary data
        iDs = createIDS(containerClassGrid)
        toUnload = createToUnload(containersToUnload, iDs)
        ship = manifestToGridLoad(containerClassGrid, iDs)
        shipNames = manifestToGrid(containerClassGrid)
        solution = loadUnload(ship, toUnload, loadSize)


        # here im basically using the last item in the load unload return array to maniuplate the cargo array to represent the steps
        # it may need to be tweaked based on what andrew was saying about there being moves within the ship unfortunately but we will see
        moves = solution[2]
        steps = generateLURender(moves, shipNames)

        with open("./globals/names.txt", 'w') as file:
            for line in steps[-1]:
                for name in line:
                    file.write(str(name) + "\n")
        returnItems = [{"steps": steps}, {"moves": moves}, {"cost": solution[0]}]

        return jsonify(returnItems)
    except Exception as e:
        server_logger.error("Server Error fetching grid names", error=str(e))
        return jsonify({'error': "Failed to fetch grid names"}), 500

@app.route("/submitLoad", methods=["POST", "GET"])
def submit_load():  
    print("SubmitLoad Called")
    data = request.get_json()

    if not data or "numLoad" not in data:
        return jsonify({"message": "No number of containers provided"}), 400

    numLoad = data["numLoad"]
    #numLoad = int(numLoad)
    manifestName = ""
    with open("./globals/path.txt", "r") as file:
        manifestName = file.readline().strip()
    containersToUnload = []
    with open("cellsToUnload.txt", "r") as file:
        containersToUnload = [line.strip() for line in file]
    
    manifest_path = "./manifests/" + manifestName
    containerClassGrid = read_manifest.read_manifest(manifest_path)
    iDs = createIDS(containerClassGrid)
    toUnload = createToUnload(containersToUnload, iDs)
    ship = manifestToGridLoad(containerClassGrid, iDs)
    shipNames = manifestToGrid(containerClassGrid)
    solution = loadUnload(ship, toUnload, numLoad)
    
    steps = generateStepsLoadUnload(solution, shipNames)

    print(f"Solution of load/unload: {solution}")
    print(f"Solution steps: {steps}")
    print(f"Number of containers to load: {numLoad}")

    return jsonify({"message": f"Successfully received {numLoad} containers"}), 200

@app.route("/getGridNames", methods=["GET"])
def get_grid_names():
    try:
        f = open("./globals/path.txt", "r")
        manifest_name = f.read().strip()
        f.close()
        manifest_path = "./manifests/" + manifest_name
        containerClassGrid = read_manifest.read_manifest(manifest_path)
        
        gridNames = manifestToGrid(containerClassGrid) 
        return jsonify({'gridNames': gridNames}) #send to front-end

    except Exception as e:
        server_logger.error("Server Error fetching grid names", error=str(e))
        return jsonify({'error': "Failed to fetch grid names"}), 500


@app.route("/downloadManifest", methods=["POST","GET"])
def download_manifest():
    try:
        f = open("./globals/path.txt", "r")
        manifest_name = f.read().strip()
        f.close()
        base_name = os.path.splitext(manifest_name)[0]
        new_path = "./new_manifests/" + base_name + "_OUTBOUND.txt"
        weights = []
        names = []
        with open("./globals/weights.txt", "r") as file:
            for line in file:
                clean_line = line.strip()
                if clean_line:
                    weights.append(clean_line)
        with open("./globals/names.txt", "r") as file:
            for line in file:
                clean_line = line.strip()
                if clean_line:
                    names.append(clean_line)
        with open(new_path, 'w') as file:
            i, j = 1, 1
            for weight, name in zip(weights, names):
                if len(str(j)) == 2:
                    file.write(f"[0{i},{j}], ")
                else:
                    file.write(f"[0{i},0{j}], ")
                if int(weight) == -1 or int(weight) == -2:
                    file.write("{0000")
                else:
                    range = 5 - len(weight)
                    file.write("{")
                    while range > 1:
                        file.write("0")
                        range -= 1
                    file.write(weight)
                file.write("}, " + name + "\n")
                if j == 12:
                    i += 1
                    j = 1
                else:
                    j += 1
                
                # keeps printing an extra at 9, so this stops it
                if i == 9:
                    break
        new_name = base_name + "_OUTBOUND.txt"
        return send_file(
                new_path,
                as_attachment=True,
                download_name=new_name
            )
    except Exception as e:
        server_logger.error("downloadManifest error", error=str(e))
        return jsonify({'error': "downloadManifest failed"}), 500
    
@app.route("/saveStepState", methods=["POST"])
def save_step():
    try:
        data = request.get_json()
        with open("./globals/step_state.json", "w") as file:
            json.dump({
                "currentStep": data.get("currentIndex"),
                "grid": data.get("grid"),
                "moves": data.get("moves")
            }, file)
        return jsonify({"success": True})
    except Exception as e:
        server_logger.error(f"Error saving step state: {str(e)}")
        return jsonify({"error": "Failed to save step state"}), 500

@app.route("/loadStepState", methods=["GET"])
def load_step():
    try:
        try:
            with open("./globals/step_state.json", "r") as file:
                state = json.load(file)
                return jsonify({
                    "exists": True,
                    "currentStep": state["currentStep"],
                    "grid": state["grid"],
                    "moves": state["moves"]
                })
        except FileNotFoundError:
            return jsonify({"exists": False})
    except Exception as e:
        server_logger.error(f"Error loading step state: {str(e)}")
        return jsonify({"error": "Failed to load step state"}), 500

@app.route("/clearStepState", methods=["POST"])
def clear_step():
    try:
        if os.path.exists("./globals/step_state.json"):
            os.remove("./globals/step_state.json")
        return jsonify({"success": True})
    except Exception as e:
        server_logger.error(f"Error clearing step state: {str(e)}")
        return jsonify({"error": "Failed to clear step state"}), 500

@app.route('/saveLoadedCellsInfo', methods=['POST'])
def save_loaded_cells_info():
    try:
        loaded_cells_info = request.json

        adjust_files(loaded_cells_info)
        
        if not loaded_cells_info:
            return jsonify({"error": "No data received"}), 400
        
        print("Received Loaded Cells Info:")
        for cell in loaded_cells_info:
            print(f"Container: {cell['label']}, Position: ({cell['posX']}, {cell['posY']}), Weight: {cell['weight']}")
        
        return jsonify({"message": "Loaded cells info saved successfully"}), 200
    
    except Exception as e:
        print(f"Error saving loaded cells info: {str(e)}")
        return jsonify({"error": "Failed to save loaded cells info"}), 500

def adjust_files(loaded_cells_info):
    names = []
    weights = []

    with open("./globals/names.txt", "r") as file:
        for line in file:
            names.append(line.strip())

    with open("./globals/weights.txt", "r") as file:
        for line in file:
            weights.append(line.strip())

    i = 1
    for cell in loaded_cells_info:
        if i == 1: # skipping first case
            i -= 1
            continue

        posX = cell['posX'] # don't need
        posY = cell['posY'] # don't need
        label = cell['label']
        weight = cell['weight']

        index = posX * 12 + posY

        # if the index is invalid
        if 0 <= index < len(names):
            # update name and weight
            names[index] = label
            weights[index] = str(weight)

    with open("./globals/names.txt", "w") as file:
        for name in names:
            file.write(str(name) + "\n")

    with open("./globals/weights.txt", "w") as file:
        for weight in weights:
            file.write(str(weight) + "\n")

if __name__ == "__main__":
    # print("hello world")
    # unload = np.zeros(4)
    # unload[1] = 1
    # unload[2] = 1
    # solution = loadUnload(grid2, unload, 6)
    # # solution = balance(grid)
    # # print(hueristicBalance(grid))
    # print("goodbye world")
    # print(solution[0])
    # print(solution[2])
    # print(solution[1])

    app.run(debug=True, port=8080)

