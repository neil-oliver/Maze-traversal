import operator
import string
from math import sqrt

#start and end variables
start = "A15"
end = "P1"

#graph representation of https://i.redd.it/qzmfijn9kewz.gif
graph = {
    "A15": [{"B20": 8}, {"A11": 11}],
    "A11": [{"C9": 30}, {"A12": 1}],
    "B20": [{"G17": 14}, {"C20": 1}],
    "G17": [{"J20": 8}, {"I18": 3}],
    "C20": [{"C19": 1}, {"H20": 5}],
    "C19": [],
    "H20": [],
    "J20": [{"J17": 5}, {"N20": 6}],
    "I18": [],
    "J17": [{"K15": 3}, {"L14": 11}],
    "N20": [{"N18": 2}, {"Q20": 3}],
    "N18": [],
    "Q20": [],
    "K15": [],
    "L14": [{"R19": 15}, {"R15": 9}],
    "R19": [{"S19": 1}, {"T16": 9}],
    "R15": [{"P13": 6}, {"P16": 7}],
    "P13": [{"Q13": 1}, {"N13": 2}],
    "P16": [{"M16": 5}, {"P18": 2}],
    "P18": [],
    "M16": [],
    "S19": [],
    "T16": [{"T15": 1}, {"T13": 5}],
    "T15": [],
    "T13": [{"R8": 7}, {"P8": 9}],
    "R8": [{"R7": 1}, {"R10": 4}],
    "P8": [{"N10": 4}, {"T1": 37}],
    "R7": [{"T17": 2}, {"Q7": 1}],
    "R10": [],
    "T17": [],
    "Q7": [],
    "N10": [{"N9": 1}, {"M10": 1}],
    "T1": [],
    "N9": [],
    "M10": [],
    "Q13": [],
    "N13": [],
    "C9": [{"B8": 2}, {"E10": 5}],
    "A12": [],
    "B8": [],
    "E10": [{"D10": 1}, {"J10": 5}],
    "D10": [],
    "J10": [{"I12": 7}, {"H8": 4}],
    "H8": [{"M6": 9}, {"G9": 2}],
    "I12": [{"J12": 1}, {"H11": 2}],
    "J12": [],
    "H11": [{"I11": 1}, {"F12": 3}],
    "I11": [],
    "F12": [{"F11": 1}, {"F14": 2}],
    "F11": [],
    "F14": [{"G13": 4}, {"D15": 3}],
    "G13": [],
    "D15": [{"E14": 6}, {"B17": 4}],
    "E14": [],
    "B17": [],
    "M6": [{"K8": 4}, {"P4": 5}],
    "G9": [{"F8": 2}, {"H9": 1}],
    "H9": [],
    "F8": [],
    "K8": [{"L8": 1}, {"J8": 1}],
    "P4": [{"R4": 2}, {"P5": 1}],
    "L8": [],
    "J8": [],
    "R4": [{"R1": 3}, {"S5": 2}],
    "P5": [],
    "R1": [{"S1": 1}, {"N1": 8}],
    "S5": [],
    "S1": [],
    "N1": [{"P1": 2}, {"F3": 14}],
    "P1": [],
    "F3": [{"F1": 2}, {"J4": 11}],
    "F1": [{"G1": 1}, {"D3": 4}],
    "J4": [{"H5": 5}, {"K4": 1}],
    "H5": [],
    "K4": [{"K2": 2}, {"N4": 5}],
    "K2": [],
    "N4": [{"O3": 2}, {"M4": 1}],
    "M4": [],
    "O3": [],
    "G1": [],
    "D3": [{"A3": 3}, {"E3": 1}],
    "A3": [{"B1": 3}, {"C5": 4}],
    "E3": [],
    "B1": [{"C1": 1}, {"A1": 1}],
    "C5": [],
    "C1": [{"D1": 1}, {"C2": 1}],
    "A1": [],
    "C2": [],
    "D1": []
}

#create unvisitied queue
def createQueue(graph, start):
    q = {}
    for x in graph:
        q[x] = float("inf")

    q[start] = 0
    return (q)

#create list to store previous node
def createPrevious(graph):
    q = {}
    for x in graph:
        q[x] = ""

    return (q)


def dijkstra(graph, q):

    current = ("", 0)
    visited = []
    previous = createPrevious(graph)

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
            for x in node:
                newDistance = node[x] + current[1]
                if newDistance < q[x]:
                    previous[x] = current[0]
                    q[x] = newDistance
                    sorted_q = sorted(q.items(), key=operator.itemgetter(1))
                    q = dict(sorted_q)

                    #testing the straight line distance
                    distance(x, end)

        #keep track of all the visited notes. Not essential but nice for being able to print stats
        visited.append(current)

    print("Total nodes: " + str(len(graph)))
    return previous, visited


def searchGraph(previous, visited, end):
    #find the shortest path from A to B
    trace = end
    shortest = []
    while trace != "":
        shortest.insert(0, previous[trace])
        trace = previous[trace]
    #for some reason the while loop includes the last blank entry "" so we delete it
    del shortest[0]

    #convert the list of tuples to a dictionary to enable an easy search
    pathLen = dict(visited)

    print("Shortest path to " + end + ": " + str(pathLen[end]))
    print("Nodes of shortest path from " + start + " to " + end + ": " + str(shortest))

def distance(node1, node2):

    #splits the string into column and row. Converts the letter to a column number
    row1 = int(node1[1:])
    col1 = string.ascii_lowercase.index(node1[0].lower()) + 1

    row2 = int(node2[1:])
    col2 = string.ascii_lowercase.index(node2[0].lower()) + 1

    #calculated the difference between row values and column values
    rowDif = abs(row1 - row2)
    colDif = abs(col1 - col2)

    #pythagorean formulae to calculate the distance
    dist = sqrt(rowDif**2 + colDif**2)

    print("Straight line distance: " + str(round(dist,1)))

    return dist

#run dijkstra
previous, visited = dijkstra(graph, createQueue(graph, start))

# search graph with given start and end point
searchGraph(previous, visited, end)
