import operator

#start and end variables
start = "A"
end = "BO"

#graph representation of https://i.redd.it/qzmfijn9kewz.gif
graph = {
    "A": [{"B": 8}, {"DA": 11}],
    "DA": [{"AK": 30}, {"AL": 1}],
    "B": [{"C": 14}, {"D": 1}],
    "C": [{"G": 8}, {"H": 3}],
    "D": [{"E": 1}, {"F": 5}],
    "E": [],
    "F": [],
    "G": [{"I": 5}, {"J": 6}],
    "H": [],
    "I": [{"M": 3}, {"N": 11}],
    "J": [{"K": 2}, {"L": 3}],
    "K": [],
    "L": [],
    "M": [],
    "N": [{"O": 15}, {"P": 9}],
    "O": [{"U": 1}, {"V": 9}],
    "P": [{"Q": 6}, {"R": 7}],
    "Q": [{"AI": 1}, {"AJ": 2}],
    "R": [{"T": 5}, {"S": 2}],
    "S": [],
    "T": [],
    "U": [],
    "V": [{"W": 1}, {"X": 5}],
    "W": [],
    "X": [{"Y": 7}, {"Z": 9}],
    "Y": [{"AA": 1}, {"AB": 4}],
    "Z": [{"AE": 4}, {"AF": 37}],
    "AA": [{"AC": 2}, {"AD": 1}],
    "AB": [],
    "AC": [],
    "AD": [],
    "AE": [{"AG": 1}, {"AH": 1}],
    "AF": [],
    "AG": [],
    "AH": [],
    "AI": [],
    "AJ": [],
    "AK": [{"AM": 2}, {"AN": 5}],
    "AL": [],
    "AM": [],
    "AN": [{"DB": 1}, {"DC": 5}],
    "DB": [],
    "DC": [{"AP": 7}, {"AO": 4}],
    "AO": [{"BA": 9}, {"BB": 2}],
    "AP": [{"AQ": 1}, {"AR": 2}],
    "AQ": [],
    "AR": [{"AS": 1}, {"AT": 3}],
    "AS": [],
    "AT": [{"AU": 1}, {"AV": 2}],
    "AU": [],
    "AV": [{"AW": 4}, {"AX": 3}],
    "AW": [],
    "AX": [{"AY": 6}, {"AZ": 4}],
    "AY": [],
    "AZ": [],
    "BA": [{"BE": 4}, {"BF": 5}],
    "BB": [{"BD": 2}, {"BC": 1}],
    "BC": [],
    "BD": [],
    "BE": [{"BG": 1}, {"BH": 1}],
    "BF": [{"BI": 2}, {"BJ": 1}],
    "BG": [],
    "BH": [],
    "BI": [{"BK": 3}, {"BL": 2}],
    "BJ": [],
    "BK": [{"BM": 1}, {"BN": 8}],
    "BL": [],
    "BM": [],
    "BN": [{"BO": 2}, {"BP": 14}],
    "BO": [],
    "BP": [{"BQ": 2}, {"BR": 11}],
    "BQ": [{"BY": 1}, {"BZ": 4}],
    "BR": [{"BS": 5}, {"BT": 1}],
    "BS": [],
    "BT": [{"BU": 2}, {"BV": 5}],
    "BU": [],
    "BV": [{"BX": 2}, {"BW": 1}],
    "BW": [],
    "BX": [],
    "BY": [],
    "BZ": [{"CA": 3}, {"CB": 1}],
    "CA": [{"CC": 3}, {"CD": 4}],
    "CB": [],
    "CC": [{"CE": 1}, {"CF": 1}],
    "CD": [],
    "CE": [{"CH": 1}, {"CG": 1}],
    "CF": [],
    "CG": [],
    "CH": []
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


def dykstra(graph, q):

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

#run dykstra
previous, visited = dykstra(graph, createQueue(graph, start))

# search graph with given start and end point
searchGraph(previous, visited, end)
