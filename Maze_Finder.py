from graphics import *
import random
import time

grid_side = 45
win = GraphWin("Pacman's Quick Quest", grid_side * 15, grid_side * 15)

# Function to generate random walls
def generate_random_walls(start, end):
    walls_list = []
    for _ in range(75):  # Increase the number of walls
        y = random.randint(0, 12)
        x = random.randint(0, 12)

        # Ensure that the generated wall is not at the start or end point
        if (y, x) != start and (y, x) != end:
            walls_list.append((y, x))
    return walls_list


# Randomly generate starting and ending points
startPoint = (random.randint(3, 10), random.randint(3, 10))
endPoint = (random.randint(2, 9), random.randint(2, 9))
wallsList = generate_random_walls(startPoint, endPoint)

adjacencyDict = {}

nodeVisit = [[False for _ in range(14)] for _ in range(14)]
nodeVisit[startPoint[0]][startPoint[1]] = True

parent = [[None for _ in range(14)] for _ in range(14)]
gValue = [[None for _ in range(14)] for _ in range(14)]
fValue = [[None for _ in range(14)] for _ in range(14)]

path = []
visitQueue = []

# Global variables for OPEN heap
openNodesListHeap = [""]
openMinHeap = [""]
openHeapSize = 0

# Global variables for CLOSED list
closedNodesList = [""]
closedNodesVals = [""]


def openHeapParent(i):
    return int(i / 2)


def openHeapLeftChild(i):
    return 2 * i


def openHeapRightChild(i):
    return 2 * i + 1


def openHeapSiftUp(i):
    global openMinHeap
    global openNodesListHeap
    while i > 1 and openMinHeap[openHeapParent(i)] >= openMinHeap[i]:
        temp1 = openMinHeap[openHeapParent(i)]
        openMinHeap[openHeapParent(i)] = openMinHeap[i]
        openMinHeap[i] = temp1

        temp2 = openNodesListHeap[openHeapParent(i)]
        openNodesListHeap[openHeapParent(i)] = openNodesListHeap[i]
        openNodesListHeap[i] = temp2

        i = openHeapParent(i)


def openHeapSiftDown(i):
    global openMinHeap
    global openHeapSize
    global openNodesListHeap

    minIndex = i
    l = openHeapLeftChild(i)
    if l <= openHeapSize and openMinHeap[l] <= openMinHeap[minIndex]:
        minIndex = l

    r = openHeapRightChild(i)
    if r <= openHeapSize and openMinHeap[r] <= openMinHeap[minIndex]:
        minIndex = r

    if i != minIndex:
        temp1 = openMinHeap[i]
        openMinHeap[i] = openMinHeap[minIndex]
        openMinHeap[minIndex] = temp1

        temp2 = openNodesListHeap[i]
        openNodesListHeap[i] = openNodesListHeap[minIndex]
        openNodesListHeap[minIndex] = temp2

        openHeapSiftDown(minIndex)


def openHeapInsert(node, val):
    global openMinHeap
    global openHeapSize
    global openNodesListHeap

    openHeapSize += 1

    if len(openMinHeap) > openHeapSize:
        openMinHeap[openHeapSize] = val
        openNodesListHeap[openHeapSize] = node
    else:
        openMinHeap.append(val)
        openNodesListHeap.append(node)

    openHeapSiftUp(openHeapSize)


def openHeapExtractMin():
    global openMinHeap
    global openHeapSize
    global openNodesListHeap

    result = (openNodesListHeap[1], openMinHeap[1])
    openMinHeap[1] = openMinHeap[openHeapSize]
    openNodesListHeap[1] = openNodesListHeap[openHeapSize]

    openHeapSize -= 1

    openHeapSiftDown(1)

    return result


def openHeapChangePriority(i, p):
    global openMinHeap
    oldP = openMinHeap[i]
    openMinHeap[i] = p

    if p < oldP:
        openHeapSiftUp(i)
    else:
        openHeapSiftDown(i)


def createAdjacencyDict():
    for y in range(1, 12):
        for x in range(1, 12):
            point = (y, x)
            if point in wallsList:
                continue
            else:
                adjacencyDict[point] = []
                if y - 1 != 0:
                    if (y - 1, x) not in wallsList:
                        currList = adjacencyDict[point]
                        currList.append((y - 1, x))
                if y + 1 != 11:
                    if (y + 1, x) not in wallsList:
                        currList = adjacencyDict[point]
                        currList.append((y + 1, x))
                if x - 1 != 0:
                    if (y, x - 1) not in wallsList:
                        currList = adjacencyDict[point]
                        currList.append((y, x - 1))
                if x + 1 != 11:
                    if (y, x + 1) not in wallsList:
                        currList = adjacencyDict[point]
                        currList.append((y, x + 1))


def isGoalNode(point):
    return point == endPoint


def heuristic(a, b):
    y1, x1 = a
    y2, x2 = b
    return abs(y1 - y2) + abs(x1 - x2)


def aStarSearch(start):
    global nodeVisit
    global parent
    global gValue
    global fValue
    global visitQueue

    createAdjacencyDict()

    openHeapInsert(start, 0)
    gValue[start[0]][start[1]] = 0
    fValue[start[0]][start[1]] = heuristic(start, endPoint)

    while openHeapSize > 0:
        current, fVal = openHeapExtractMin()

        if isGoalNode(current):
            path.append(current)
            while current != start:
                path.append(parent[current[0]][current[1]])
                current = parent[current[0]][current[1]]
            path.reverse()
            return

        nodeVisit[current[0]][current[1]] = True

        for neighbour in adjacencyDict[current]:
            if not nodeVisit[neighbour[0]][neighbour[1]]:
                tempGValue = gValue[current[0]][current[1]] + 1

                if gValue[neighbour[0]][neighbour[1]] is None:
                    gValue[neighbour[0]][neighbour[1]] = tempGValue
                    fValue[neighbour[0]][neighbour[1]] = tempGValue + heuristic(neighbour, endPoint)
                    openHeapInsert(neighbour, fValue[neighbour[0]][neighbour[1]])
                    parent[neighbour[0]][neighbour[1]] = current
                elif tempGValue < gValue[neighbour[0]][neighbour[1]]:
                    gValue[neighbour[0]][neighbour[1]] = tempGValue
                    fValue[neighbour[0]][neighbour[1]] = tempGValue + heuristic(neighbour, endPoint)
                    parent[neighbour[0]][neighbour[1]] = current
                    openHeapChangePriority(openNodesListHeap.index(neighbour), fValue[neighbour[0]][neighbour[1]])
                    # ^^^ Here, we use index() to find the index of neighbour in openNodesListHeap

    return False

def drawGrid():
    global win
    for i in range(13):
        for j in range(13):
            rect = Rectangle(Point(j * grid_side, i * grid_side), Point((j + 1) * grid_side, (i + 1) * grid_side))
            rect.setWidth(2)
            rect.draw(win)
            # Display cost function value at each block
            cost_text = Text(Point((j + 0.5) * grid_side, (i + 0.5) * grid_side), "")
            if fValue[i + 1][j + 1] is not None:
                cost_text.setText(str(fValue[i + 1][j + 1]))
            cost_text.setTextColor("black")  # Change the text color to black
            cost_text.setSize(15)
            cost_text.draw(win)



def drawWalls(walls):
    global win
    for wall in walls:
        rect = Rectangle(Point(wall[1] * grid_side, wall[0] * grid_side), Point((wall[1] + 1) * grid_side, (wall[0] + 1) * grid_side))
        rect.setFill("blue")
        rect.draw(win)


def drawPath(path):
    global win
    for p in path:
        center = Point((p[1] + 0.5) * grid_side, (p[0] + 0.5) * grid_side)
        pacman = Circle(center, grid_side / 3)
        pacman.setFill("yellow")
        pacman.draw(win)
        # Display the value of the cost function
        text = Text(center, f"{fValue[p[0]][p[1]]:.2f}")
        text.setSize(8)
        text.draw(win)


def drawStartAndEndPoints(start, end):
    global win
    # Draw starting point block (green)
    start_block = Rectangle(Point(start[1] * grid_side, start[0] * grid_side), Point((start[1] + 1) * grid_side, (start[0] + 1) * grid_side))
    start_block.setFill("green")
    start_block.draw(win)


    # Draw end point block (original color)
    end_block = Rectangle(Point(end[1] * grid_side, end[0] * grid_side), Point((end[1] + 1) * grid_side, (end[0] + 1) * grid_side))
    end_block.setFill("red")
    end_block.draw(win)

def drawPath(path):
    global win
    pacman_radius = grid_side / 3
    pacman = Circle(Point((startPoint[1] + 0.5) * grid_side, (startPoint[0] + 0.5) * grid_side), pacman_radius)
    pacman.setFill("green")
    pacman.draw(win)

    flg =1
    for p in path:
        flg = 2
        print (p)
        center = Point((p[1] + 0.5) * grid_side, (p[0] + 0.5) * grid_side)
        dx = (center.getX() - pacman.getCenter().getX()) / 15
        dy = (center.getY() - pacman.getCenter().getY()) / 15
        for _ in range(14):
            new_x = pacman.getCenter().getX() + dx
            new_y = pacman.getCenter().getY() + dy

            if 0 <= new_x <= 14 * grid_side and 0 <= new_y <= 14 * grid_side:  # Check if within window boundaries
                pacman.move(dx, dy)
                time.sleep(0.05)  # Add a delay to slow down the animation
                # Fill the block with yellow color
                #if (round(new_x / grid_side), round(new_y / grid_side)) == endPoint:
                #    break  # Break if we reached one block before the endpoint
                block_x = int(new_x / grid_side)
                block_y = int(new_y / grid_side)
                rect = Rectangle(Point(block_x * grid_side, block_y * grid_side),
                                 Point((block_x + 1) * grid_side, (block_y + 1) * grid_side))
                rect.setFill("yellow")
                rect.draw(win)

            else:
                break


   # print("FINISHED")
    #end_block.setFill("red")
    #end_block.draw(win)

        # if (round(pacman.getCenter().getX() / grid_side), round(pacman.getCenter().getY() / grid_side)) == endPoint:
        #     end_block.setFill("red")
        #     rect.draw(win)
        #     break

    drawStartAndEndPoints(startPoint, endPoint)


    if flg==1:
        print("IMPOSSIBLE")

    win.getMouse()
    win.close()


def main():
    global path
    drawGrid()
    drawWalls(wallsList)
    drawStartAndEndPoints(startPoint, endPoint)
    aStarSearch(startPoint)
    drawPath(path)



main()
