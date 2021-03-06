import operator
import string
from math import sqrt
import random

#start and end variables
start = "A11" #default A15
end = "P1" #default P1

#print verbose
v = False

#option to guess or not
takeGuess = True

#making maze graph tests
def findNeighbour(rowCount, cellCount, size):

    neighbours = []

    if cellCount > 1:
        up = chr(rowCount+64) + str(cellCount - 1)
        neighbours.append({up : 1})
    if cellCount < size:
        down = chr(rowCount+64) + str(cellCount + 1)
        neighbours.append({down : 1})
    if rowCount > 1:
        left = chr(rowCount+63) + str(cellCount)
        neighbours.append({left : 1})
    if rowCount < size:
        right = chr(rowCount+65) + str(cellCount)
        neighbours.append({right : 1})

    return neighbours


def makeBlank(size):
    maze = {}
    rowCount = 1
    for x in range(0,size):
        cellCount = 1
        for y in range(0,size):
            cellRef = chr(rowCount+64) + str(cellCount)
            maze[cellRef] = []
            cellCount += 1
        rowCount +=1

    maze = makeMaze(maze)

    if v:
        printMaze(maze)
    printMaze(maze)

    return maze

def makeMaze(maze):

    visited = {}

    size = int(len(maze)**(1/2))

    #fill visited dict with all coords and a False value
    for x in maze:
        visited[x] = False

    stack = []

    def makePath(currentCell, size):
        #mark the current cell as visited
        visited[currentCell] = True

        #get the neighbouring cells
        col = int(currentCell[1:])
        row = string.ascii_lowercase.index(currentCell[0].lower()) + 1
        neighbours = findNeighbour(row, col, size)

        #create a list of all unvisited neighbours
        unvisited = []
        for x in neighbours:
            [(key, value)] = x.items()
            if visited[key] == False:
                unvisited.append(key)

        current = ""

        #if there are unvisited neighbours:
        # 1. append the current cell to the stack
        # 2. pick a random neighbouring cell from the unvisited list
        # 3. mark the randomly selected cell as visited
        # 4. mark the randomly selected cell the current cell
        if unvisited != []:
            stack.append(currentCell)
            randomNeighbour = random.choice(list(unvisited))
            visited[randomNeighbour] = True
            current = randomNeighbour
            maze[currentCell].append({current : 1})
            maze[current].append({currentCell : 1})
        else:
            #if all neighbouring cells have been visited, pop the last cell in the stack, and mark as the current cell
            try:
                current = stack.pop(-1)
            except:
                print("")

        #rerun makePath with the newly selected cell
        if current != "":
            makePath(current, size)

    makePath(start, size)

    return maze


def printMaze(maze):

    size = int(len(maze)**(1/2))
    mazetxt = ""

    for y in range(1, size + 1):
        mazetxt += " _"
    mazetxt += "\n"

    for x in range(1,size+1):
        for y in range(1, size + 1):

            currentRow = chr(x+64)
            currentCol = y
            currentCell = currentRow + str(currentCol)
            neighbours = ""
            for walldict in maze[currentCell]:

                [(wall, distance)] = walldict.items()

                col = int(wall[1:])
                row = string.ascii_lowercase.index(wall[0].lower()) + 1
                if v:
                    print("x = " + str(x))
                    print("y = " + str(y))
                    print("col = " + str(col))
                    print("row = " + str(row))
                    print("currentCol+1 = " + str(currentCol + 1))

                if col == currentCol-1:
                    neighbours += "S"
                elif row == x+1:
                    neighbours += "W"
            if currentCell == start:
                text = " S"
            elif currentCell == end:
                text = " E"
            else:
                if neighbours == "SW" or neighbours == "WS":
                    text = "  "
                elif neighbours == "S":
                    text = " _"
                elif neighbours == "W":
                    text = "| "
                else:
                    text = "|_"

            if v:
                print(text)

            mazetxt += text

        mazetxt += "|\n"
    print(mazetxt)


def printPath(path, maze):
    print("\n")
    pathdict = {}
    for x in maze:
        pathdict[x] = " * "

    for count, x in enumerate(path):
        if len(str(count)) == 1:
            pathdict[x] = " " + str(count) + " "
        elif len(str(count)) == 2:
            pathdict[x] = " " + str(count)
        else:
            pathdict[x] = str(count)

    pathdict[start] = "GO!"
    if path[-1] == end:
        pathdict[path[-1]] = "END"
    else:
        pathdict[path[-1]] = "XXX"

    size = int(len(maze)**(1/2))

    for count, x in enumerate(pathdict):
        print(pathdict[x] + " ", end = "")
        if (count+1) % size == 0:
            print("\n")


#test out the maze creator
graph = makeBlank(20)

#create unvisited queue
def createQueue(graph, start):
    q = {}
    for x in graph:
        q[x] = float("inf")

    q[start] = 0

    if v:
        print("Queue Created with starting node " + start)
        print(str(q) + "\n")

    return (q)


def dijkstra(graph, q):
    if v:
        print("Running Dijkstra...\n")
    current = ("", 0)
    visited = []

    while q:
        # sort the queue by value by creating a list of tuples
        sorted_q = sorted(q.items(), key=operator.itemgetter(1))

        #pop the current node
        current = sorted_q.pop(0)

        #recreate dictionary
        q = dict(sorted_q)

        #grab the neighbouring nodes to the current node
        nodes = graph[current[0]]
        # loop through nodes and update the distance values in the queue
        for node in nodes:
            [(nodeKey, nodeValue)] = node.items()
            newDistance = node[nodeKey] + current[1]
            if nodeKey in q:
                if newDistance < q[nodeKey]:
                    q[nodeKey] = newDistance
                    if v:
                        print("Updating " + str(nodeKey) + " to the shortest distance value " + str(newDistance))
                    sorted_q = sorted(q.items(), key=operator.itemgetter(1))
                    q = dict(sorted_q)

        #keep track of all the visited notes in order of smallest to largest
        visited.append(current)
    if v:
        print("\nTotal number of distances calculated via Dijkstra: " + str(len(graph)))
        print("The shorttest Distances for each node are: \n" + str(visited))

    return visited

def searchGraph(visited, end):
    #find the shortest path from A to B
    if v:
        print("\nSearching graph for shortest path between " + start + " and " + end + "...\n")

    shortestPath = []
    def search(trace):
        if v:
            print(trace)
            if trace != end and trace != start:
                print("The next closest node is " + trace)
            elif trace == start:
                print("Finishing on the starting node of " + start)

        dict_visited = dict(visited)
        shortest = float("inf")

        if trace == end:
            shortestPath.insert(0, trace)

        for node in graph[trace]:
            [(nodeKey, nodeValue)] = node.items()
            if dict_visited[nodeKey] < shortest:
                shortest = dict_visited[nodeKey]
                trace = nodeKey

        shortestPath.insert(0, trace)

        if shortestPath[0] != end:
            if trace != start:
                search(trace)
            elif trace == start:
                if v:
                    print("Finishing on the starting node of " + start)
        else:
            print("Error finding shortest path")

    if v:
        print("Starting with node " + end + "...")

    search(end)

    #convert the list of tuples to a dictionary to enable an easy search
    pathLen = dict(visited)

    if v:
        print("\nShortest path to " + end + ": " + str(pathLen[end]))

    #print this line regardless of verbose flag
    print("Nodes of shortest path from " + start + " to " + end + ": " + str(shortestPath))

    return shortestPath

def bestGuess(node1, node2):

    guessPath = []

    def guess(guessNode, lowestDist):
        #heuristic approach to picking the next node based on straight line distance to the end node.

        if guessNode == node1 or len(graph[guessNode]) != 1:

            if v:
                if guessNode != node2:
                    print("Best guess neighbour options: " + str(guessNode) + " : " + str(graph[guessNode]))
                    if graph[guessNode]:
                        print("Checking each neighbour to calculate closest distance...")
                    else:
                        print("The node has no neighbouring nodes and we have failed to find the end node.\n")
                        print("We finished " + str(round(lowestDist,1)) + " squares away from " + end + ".\n")

            # append the guessed node to the guessPath list
            guessPath.append(guessNode)

            best = ""
            lowestDist = float("inf")

            for node in graph[guessNode]:
                [(nodeKey, nodeValue)] = node.items()


                run = False

                if guessNode == node1:
                    run = True

                if nodeKey not in guessPath:
                    run = True

                if run == True:
                    # splits the string into column and row. Converts the letter to a column number
                    row1 = int(nodeKey[1:])
                    col1 = string.ascii_lowercase.index(nodeKey[0].lower()) + 1

                    row2 = int(node2[1:])
                    col2 = string.ascii_lowercase.index(node2[0].lower()) + 1

                    # calculated the difference between row values and column values
                    rowDif = abs(row1 - row2)
                    colDif = abs(col1 - col2)

                    if v:
                        print("row difference = " + str(rowDif) + ", column difference = " + str(colDif))

                    #pythagorean formulae to calculate the distance
                    dist = sqrt(rowDif ** 2 + colDif ** 2)

                    if v:
                        print("Straight line distance from " + str(nodeKey) + " to the end node (" + str(node2) +") = " + str(round(dist, 1)))


                    if dist < lowestDist:
                        lowestDist = dist
                        best = nodeKey


            if best != node2:
                if v:
                    print("best guess: " + best + "\n")
                    print("")

                #reall the guessPath using the new node
                guess(best,lowestDist)
            else:
                print(str(best) + " : " + "END NODE \n")

    if v:
        print("\nCalling best guess algorithm... \n")
    guess(node1, float("inf"))

    #print this line regardless of verbose flag
    print("Path of best guess: " + str(guessPath))

    return guessPath


def guessPercent(correctPath, guessPath):
    correct = 0
    for count, x in enumerate(guessPath):
        if correctPath[count] == x:
            correct += 1
    percentage = (correct / len(correctPath)) * 100
    return percentage


#check that the start and end nodes exist in the graph before continuing
if start in graph and end in graph:
    #run dijkstra
    visited = dijkstra(graph, createQueue(graph, start))

    # search graph with given start and end point
    shortestPath = searchGraph(visited, end)

    #print a visual of the path
    printPath(shortestPath, graph)

    if takeGuess == True:
        # testing the straight line distance
        guessPath = bestGuess(start, end)
        printPath(guessPath, graph)

        #print a small message in verbose mode to suggest a different end point if the guess algorithm was 100% accurate

        if shortestPath == guessPath:
            print("\nThe guess algorithm was spot on! Not bad!")
        else:
            print("\nThe guess algorithm didn't get it quite right. \nWhy don\'t you refresh and see if it improves next time.")
            percentage = guessPercent(shortestPath,guessPath)
            print("The guessing algorithm was " + str(round(percentage,2)) + "% the same as Dijstra.")

else:
    print("Please check your start and end nodes at the top of code ensuring they are in the graph and have been given in CAPITALS. Thank you.")

