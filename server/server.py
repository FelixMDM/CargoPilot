from flask import Flask, jsonify, request, session, send_file
from flask_cors import CORS
import heapq
import copy

from utils.logger import server_logger
import os
from datetime import datetime

# app instance
# You will need to create a virtual environment named 'venv' to use (venv is the name specified in the gitignore)
# Windows user might be barred from creating venv; run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Windows: python -m venv venv -> venv/Scripts/activate
# LINUX/UNIX: virutalenv venv -> source venv/bin/activate

# # to kill venv process: deactivate

grid = [[1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

unload = {"1": 3}
load = 1
# /api/home
# @app.route("/api/home", methods=['GET'])
# def return_home():
#     return jsonify({
#         'message': "Testing Testing Testing",
#     })

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

    
def canBalance(grid): # first we will check if can be balanced, if so it will just return true, otherwise it will return true, and (0, 0) otherwise, false nad (leftweight, rightweight) wieghts after sift
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
                newgrid = [row[:] for row in curr_grid]
                newgrid[k][j] = newgrid[index][i]
                newgrid[index][i] = 0
                heapq.heappush(heap, (curr_cost + cost + hueristicBalance(newgrid), newgrid, path + [(index, i, k, j)], curr_cost + cost, (k, j)))
    return None

def balanceOutput(grid, steps):
    output = [grid]
    for item in steps:
        newgrid = [row[:] for row in output[-1]]
        newgrid[]

def hueristicLoad(grid, toUnload, toLoad):
    if(not toUnload and not toLoad):
        return 0
    if(not toUnload):
        return 4 * toLoad
    unload = toUnload.copy()
    unloadCosts = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if str(grid[i][j]) in toUnload:
                unloadCosts += [(8 - i + j + 2, i, j)]
    unloadCosts.sort()
    totalCost = 4 * toLoad
    for cost, row, col in unloadCosts:
        if(str(grid[row][col] in unload)):
            totalCost += cost
            unload[str(grid[row][col])] -= 1
            if(unload[str(grid[row][col])] == 0):
                del unload[str(grid[row][col])]
                if(not unload):
                    return totalCost
            if(not toLoad):
                totalCost += 2
            toLoad -= 1
    return totalCost

    

def loadUnload(grid, toUnload, toLoad):
    heap = []
    heapq.heappush(heap, (0, grid, [], 0, toLoad, toUnload, (8, 0), 1))
    count = 0
    visited = set()
    while(heap):
        count += 1
        hCost, curr_grid, path, curr_cost, load, toUnload, pos, craneDocked = heapq.heappop(heap)
        unload = toUnload.copy()
        gridTuple = tuple(tuple(row) for row in curr_grid)
        if gridTuple in visited:
            continue
        visited.add(gridTuple)
        if(count % 100 == 0):
            print(hCost)
        topContainers = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 , -1]
        for i in range(6):
            for j in range(8):
                if curr_grid[j][i]:
                    topContainers[i] = j
                if curr_grid[j][i + 6]:
                    topContainers[i + 6] = j

        if(not load and not unload):
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
                newgrid = [row[:] for row in curr_grid]
                newgrid[k][j] = newgrid[index][i]
                newgrid[index][i] = 0
                if(craneDocked):
                    cost += 2
                heapq.heappush(heap, (curr_cost + cost + hueristicLoad(newgrid, unload, load), newgrid, path + [(index, i, k, j)], curr_cost + cost, load, unload, (k, j), False))
            #unload i as well
            # cost is 2 from ship to truck and whatever the cost inside the ship is(collum + 8 - row)
            if(load):
                if(topContainers[i] < 7):
                    newgrid = [row[:] for row in curr_grid]
                    cost = i + 8 - topContainers[i] + 2
                    newgrid[topContainers[i] + 1][i] = 96 + toLoad - load #give a unique id
                    if(not craneDocked):
                       cost += 2 + 8 - pos[0] + pos[1]
                    heapq.heappush(heap, (curr_cost + cost + hueristicLoad(newgrid, unload, load - 1), newgrid, path + [(topContainers[i] + 1, i, -1)], curr_cost + cost, load - 1, unload, (topContainers[i] + 1, i), False))
            if(str(curr_grid[topContainers[i]][i]) in unload):
                newgrid = [row[:] for row in curr_grid]
                cost = i + 8 - topContainers[i] + 2 + craneCost
                newgrid[topContainers[i]][i] = 0
                if(craneDocked):
                    cost += 2
                # remove from unload
                newUnload = unload.copy()
                newUnload[str((curr_grid[topContainers[i]][i]))] -= 1
                if(newUnload[str((curr_grid[topContainers[i]][i]))] == 0):
                    del newUnload[str((curr_grid[topContainers[i]][i]))]
                
                heapq.heappush(heap, (curr_cost + cost + hueristicLoad(newgrid, newUnload, load), newgrid, path + [(topContainers[i], i, -2)], curr_cost + cost, load, newUnload, (8, 0), True))
    return None

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
        date_str = datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(os.getcwd(), 'logs', f'server-{date_str}.log')
        
        if os.path.exists(log_file):
            return send_file(
                log_file,
                mimetype='text/plain',
                as_attachment=True,
                download_name=f"cargopilot-logs-{date_str}.log"
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


@app.route("/uploadManifest", methods = ["POST"])
def upload_mainfest():
    try:
        manifest = request.files['manifest']
        manifest_path = "./manifests/" + manifest.filename
        manifest.save(manifest_path)
        server_logger.info("Upload manifest endpoint called", 
                          remote_addr=request.remote_addr,
                          filename=manifest.filename)
        return jsonify({'message': "File uploaded. Press 'OK' to proceed"})
    except Exception as e:
        server_logger.error("Upload manifest error", error=str(e))
        return jsonify({'error': "Upload operation failed"}), 500
      

if __name__ == "__main__":
    print("hello world")
    # solution = balance(grid)
    # print(hueristicBalance(grid))
    solution = loadUnload(grid, unload, load)
    print("goodbye world")
    print(solution[0])
    print(solution[2])
    print(solution[1])

    app.run(debug=True, port=8080)

