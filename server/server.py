import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import heapq
import copy
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
        curr = heapq.heappop(heap)
        topContainers = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 , -1]
        if(count % 100 == 0):
            print(curr[0])
        left = 0
        right = 0
        for i in range(6):
            for j in range(8):
                if curr[1][j][i]:
                    topContainers[i] = curr[1][j][i]
                if curr[1][j][i + 6]:
                    topContainers[i + 6] = curr[1][j][i + 6]
                left += curr[1][j][i]
                right += curr[1][j][i + 6]
        if(left != 0 and right != 0 and abs(left - right) / left < 0.1):
            # balanced
            return curr
        for i in range(12):
            if topContainers[i] == -1:
                continue
            index = topContainers[i]
            # for l in range(8):
            #     if curr[1][l][i]:
            #         continue
            #     index = l
            #     break
            maxValue = 0
            if(index == 0):
                continue
            for j in range(12):
                if j == i:
                    maxValue = 0
                    continue
                if topContainers[j] == -1:
                    continue
                if topContainers[j] > maxValue:
                    maxValue = topContainers[j]
                cost = 0
                k = topContainers[j]
                if(maxValue < index or maxValue < k):
                    cost = max(index, k) - index + max(index, k) - k + abs(j - i)
                else:
                    cost = maxValue + 1 - index + maxValue - k + abs(j - i)
                newgrid = copy.deepcopy(grid)
                newgrid[k][j] = newgrid[index - 1][i]
                newgrid[index - 1][i] = 0
                heapq.heappush(heap, (curr[0] + cost, newgrid))
                # for k in range(8):
                #     if(curr[1][k][j]):
                #         continue
                #     if k > maxValue:
                #         maxValue = k
                #     # calculate cost to move one from i to on in j
      
                    
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

@app.route("/upload", methods = ["POST"])
def upload_manifest():
    file = request.files['file']
   #  manifest = 

if __name__ == "__main__":
    # print("hello world")
    # solution = balance(grid)
    # print("goodbye world")
    # print(solution[0])
    app.run(debug=True, port=8080)
