import os
from flask import Flask, jsonify, request, session
from flask_cors import CORS
import heapq
import copy

# import read_mainfest

# from read_mainfest import read_manifest

# app instance
# You will need to create a virtual environment named 'venv' to use (venv is the name specified in the gitignore)
# Windows user might be barred from creating venv; run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Windows: python -m venv venv -> venv/Scripts/activate
# LINUX/UNIX: virutalenv venv -> source venv/bin/activate

# # to kill venv process: deactivate

# BELOW ARE 
# 1. Process functions (balance, load/unload)
#   IN: Manifest grid read_manifest.py
#   OUT: Formatted list of ship "states" to be iterated over in process by FE components
# 2. Routes to handle call to balance 
#   IN: NA (Route called on 'some' event (corresponding action))
#   OUT: Returns the value of 'func corresponding event()', whether that is a call to balance, load, etc

# test grid
grid = [[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

# begin funcs
def hueristicBalance(grid):
    leftSum = 0
    rightSum = 0
    right = []
    left = []
    for i in range(6):
        for j in range(8):
            leftSum += grid[j][i]
            rightSum += grid[j][i + 6]
            if grid[j][i] > 0:
                left += (grid[j][i], j, i)
            if grid[j][i + 6] > 0:
                right += (grid[j][i + 6], j, i + 6)
    right.sort(reverse=True)
    left.sort(reverse=True)
    delta = abs(rightSum - leftSum)
    imbalance = delta / max(leftSum, rightSum)
    if imbalance < 0.1:
        return 0
    if(leftSum > rightSum):
        print("test")
        for container in left:
            if imbalance - container[0] > 0 or abs((rightSum + container[0]) - (leftSum - container[0])) / max((leftSum - container[0])):
                pass

    
def canBalance(grid):
    return True
def balance(grid):
    # create a queue
    # add start state to queue
    # While q is not empty, or optimal not found 
        # pop a grid off the queue
        # check if it is goal
        # if goal break
        # for each possible move, add it to the queue.
    heap = []
    heapq.heappush(heap, (0, grid, []))
    count = 0
    while(heap):
        count += 1
        curr_cost, curr_grid, path = heapq.heappop(heap)
        if(count % 100 == 0):
                    print(curr_cost)
        topContainers = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 , -1]
        left = 0
        right = 0
        for i in range(6):
            for j in range(8):
                if curr_grid[j][i]:
                    topContainers[i] = j
                if curr_grid[j][i + 6]:
                    topContainers[i + 6] = j
                left += curr_grid[j][i]
                right += curr_grid[j][i + 6]
        if(left != 0 and right != 0 and abs(left - right) / left < 0.1):
            # balanced
            return curr_cost, curr_grid, path
        for i in range(12):
            if topContainers[i] == -1:
                continue
            index = topContainers[i] # this is the row index of the highest container in column i
            maxValue = -1
            if(index == -1):
                continue
            for j in range(12):
                if j == i:
                    maxValue = -1
                    continue
                if topContainers[j] == 7:
                    continue
                if topContainers[j] >= maxValue:
                    maxValue = topContainers[j] + 1
                cost = 0
                k = topContainers[j] # this is the row index of the highest container in column j
                k = k + 1 #0 add 1 to k beacause we need to place the container ontop of the container at kj
                if(maxValue < index or maxValue < k):
                    cost = max(index, k) - index + max(index, k) - k + abs(j - i)
                else:
                    cost = maxValue - index + maxValue - k + abs(j - i)
                if(cost < 0):
                    print("NEGATIVE!!!!!!!")
                    return None
                newgrid = copy.deepcopy(curr_grid)
                newgrid[k][j] = newgrid[index][i]
                newgrid[index][i] = 0
                heapq.heappush(heap, (curr_cost + cost + 1, newgrid, path + [(index, i, k, j)]))
                
    return None

# begin routes
app = Flask(__name__)
CORS(app)

# api route to parse input
@app.route("/test", methods=['GET'])
def read_input():
    return jsonify({
        'message': "Placeholder Message",
    })

# api route to call balance function
@app.route("/balance", methods=['GET'])
def do_balance():
    return jsonify({
        'message': "Placeholder",
    })
# api route to call load or unload function
@app.route("/loadUnload", methods=['GET'])
def return_home():
    return jsonify({
        'message': "Placeholder",
    })

@app.route("/uploadManifest", methods = ["POST"])
def upload_mainfest():
    manifest = request.files['manifest']
    manifest_path = "./manifests/" + manifest.filename
    manifest.save(manifest_path)

    return jsonify ({
        'message': "uploadManifest endpoint called",
    })

if __name__ == "__main__":
    
    # print("hello world")
    # solution = balance(grid)
    # print("goodbye world")
    # print(solution[0])
    # print(solution[2])
    # print(solution[1])

    app.run(debug=True, port=8080)
