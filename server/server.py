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

grid = [[2, 2, 9, 1.1, 5, 5, 7, 7, 8, 8, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 9, 3],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 1.2],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 3],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
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
    heapq.heappush(heap, (0, grid, [], 0, (8, 0)))
    count = 0
    visited = set()
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
                if curr_grid[j][i]:
                    topContainers[i] = j
                if curr_grid[j][i + 6]:
                    topContainers[i + 6] = j
                left += curr_grid[j][i]
                right += curr_grid[j][i + 6]
        if(left != 0 and right != 0 and abs(left - right) / left < 0.1):
            # balanced
            return curr_cost, curr_grid, path
        maxToContainer = -1
        for i in range(12):
            if topContainers[i] == -1:
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
                newgrid = copy.deepcopy(curr_grid)
                newgrid[k][j] = newgrid[index][i]
                newgrid[index][i] = 0
                heapq.heappush(heap, (curr_cost + cost + hueristicBalance(newgrid), newgrid, path + [(index, i, k, j), (cost, pos)], curr_cost + cost, (k, j)))
                
    return None

def loadUnload(grid, toUnload, toLoad, craneDocked):
    heap = []
    heapq.heappush(heap, (0, grid, [], 0, toLoad, toUnload (8, 0)))
    count = 0
    while(heap):
        count += 1
        hCost, curr_grid, path, curr_cost, load, unload, pos = heapq.heappop(heap)
        if(count % 100 == 0):
                    print(curr_cost)
        topContainers = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 , -1]
        for i in range(6):
            for j in range(8):
                if curr_grid[j][i]:
                    topContainers[i] = j
                if curr_grid[j][i + 6]:
                    topContainers[i + 6] = j

        if(load == 0 and unload.len() == 0):
            # finished
            return curr_cost, curr_grid, path
        maxToContainer = -1
        for i in range(12):
            if topContainers[i] == -1:
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
            # now we have the baseline cost to get from wherever the container was before to the container we are trying to move
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
                cost = 0
                k = topContainers[j] # this is the row index of the highest container in column j
                k = k + 1 #0 add 1 to k beacause we need to place the container ontop of the container at kj
                if(maxFromContainer < index or maxFromContainer < k):
                    cost = max(index, k) - index + max(index, k) - k + abs(j - i) + craneCost
                else:
                    cost = maxFromContainer - index + maxFromContainer - k + abs(j - i) + craneCost
                if(cost < 0):
                    print("NEGATIVE!!!!!!!")
                    return None
                newgrid = copy.deepcopy(curr_grid)
                newgrid[k][j] = newgrid[index][i]
                newgrid[index][i] = 0
                if(craneDocked):
                    cost += 2
                heapq.heappush(heap, (curr_cost + cost, newgrid, path + [(index, i, k, j)], curr_cost + cost, (k, j)))
            #unload i as well
            # cost is 2 from ship to truck and whatever the cost inside the ship is(collum + 8 - row)
            if(curr_grid[topContainers[i]][i] in unload):
                newgrid = copy.deepcopy(curr_grid)
                cost = i + 8 - topContainers[i] + 2
                newgrid[topContainers[i]][i] = 0
                if(craneDocked):
                    cost += 2
                # remove from unload
                heapq.heappush(heap, (curr_cost + cost, newgrid, path + [(index, i, k, j)], curr_cost + cost))
            if(load):
                if(topContainers[i] < 7):
                    newgrid = copy.deepcopy(curr_grid)
                    cost = i + 8 - topContainers[i] + 2
                    newgrid[topContainers[i] + 1][i] = -1 #give a unique id
                    if(not craneDocked):
                       cost += 2
                    heapq.heappush(heap, (curr_cost + cost, newgrid, path + [(index, i, k, j)], curr_cost + cost))

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
    print("hello world")
    solution = balance(grid)
    print(hueristicBalance(grid))
    print("goodbye world")
    print(solution[0])
    print(solution[2])
    print(solution[1])
    # app.run(debug=True, port=8080)
