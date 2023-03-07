############# Write Your Library Here ###########

from collections import deque

################################################

class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

class nod:
    def __init__(self, position=None):
        self.position = position
        
        self.cnt = 0
def search(maze, func):
    return {
        "bfs": bfs,
        "dfs":dfs,
        "astar": astar,
        "astar_four_circles": astar_four_circles,
        "astar_many_circles": astar_many_circles
    }.get(func)(maze)


def bfs(maze):
    """
    [Problem 01] 제시된 stage1 맵 세 가지를 BFS Algorithm을 통해 최단 경로를 return하시오.
    """
    start_point=maze.startPoint()
    path=[]
    ####################### Write Your Code Here ################################
    parent = []
    for i in range(maze.rows):
        pu = []
        for j in range(maze.cols):
            pu.append([-1,-1])
        parent.append(pu)
    queue = deque([])
    queue.append([start_point[0], start_point[1]])
    flag=0
    targetrow=0
    targetcol=0
    while queue:
        x, y = queue.popleft()
        neighbor = maze.neighborPoints(x, y)
        for r, c in neighbor:
            if parent[r][c] != [-1,-1]:
                continue
            if maze.isObjective(r,c):
                parent[r][c] = [x,y]
                targetrow=r
                targetcol=c
                flag=1
                break
            else:
                parent[r][c] = [x,y]
                queue.append([r, c])
        if flag:
            break
    # print("answer = ", targetrow, targetcol)
    # print("from = ", parent[targetrow][targetcol][1])
    # print("start = ", start_point[0], start_point[1])
    while True:
        #print(targetrow, targetcol)
        path.append([targetrow, targetcol])
        a=parent[targetrow][targetcol][0]
        b=parent[targetrow][targetcol][1]
        targetrow=a
        targetcol=b
        if a==start_point[0] and b==start_point[1]:
            path.append([a, b])
            break
    path.reverse()
    return path
    ############################################################################


def dfs(maze):
    """
    [Problem 02] 제시된 stage1 맵 세 가지를 DFS Algorithm을 통해 최단 경로를 return하시오.
    """
    start_point = maze.startPoint()
    path = []
    ####################### Write Your Code Here ################################
    parent = []
    for i in range(maze.rows):
        pu = []
        for j in range(maze.cols):
            pu.append([-1,-1])
        parent.append(pu)
    stack = deque([])
    stack.append(start_point)
    flag=0
    targetrow=0
    targetcol=0
    while True:
        x, y = stack.pop()
        neighbor = maze.neighborPoints(x, y)
        for r, c in neighbor:
            if parent[r][c] != [-1,-1]:
                continue
            if maze.isObjective(r, c):
                targetrow = r
                targetcol = c
                parent[r][c] = [x,y]
                flag=1
                break
            else:
                stack.append([r,c])
                parent[r][c] = [x,y]
        if flag==1:
            break
    while True:
        # print(targetrow, targetcol)
        #print([targetrow, targetcol])
        path.append([targetrow, targetcol])
        a=parent[targetrow][targetcol][0]
        b=parent[targetrow][targetcol][1]
        targetrow=a
        targetcol=b
        if a==start_point[0] and b==start_point[1]:
            path.append([a, b])
            break
    path.reverse()
    return path

    ############################################################################

def manhattan_dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def astar(maze):
    """
    [Problem 03] 제시된 stage1 맵 세가지를 A* Algorithm을 통해 최단경로를 return하시오.
    (Heuristic Function은 위에서 정의한 manhattan_dist function을 사용할 것.)
    """

    start_point = maze.startPoint()
    path = []

    ####################### Write Your Code Here ###########################
    for i in range(maze.rows):
        for j in range(maze.cols):
            if maze.isObjective(i, j):
                finishrow = i
                finishcol = j
                break
    canbe = []
    chosen = []
    startNode = Node(None, start_point)
    startNode.h = manhattan_dist(startNode.position, [finishrow, finishcol])
    startNode.f = startNode.h
    canbe.append(startNode)
    while canbe:
        currentNode = canbe[0]
        currentidx = 0  
        for idx, node in enumerate(canbe):
            if node.f<currentNode.f:
                currentidx = idx
                currentNode = node
        canbe.pop(currentidx)
        chosen.append(currentNode)
        check = 0

        if maze.isObjective(currentNode.position[0], currentNode.position[1]):
            #print("I found!!", currentNode.position[0], currentNode.position[1])
            while True:
                path.append(currentNode.position)
                currentNode = currentNode.parent
                if currentNode==None:
                    check = 1
                    break
        if check==1:
            break
    
        #print("check = ", currentNode.position[0], currentNode.position[1])
        neighbor = maze.neighborPoints(currentNode.position[0], currentNode.position[1])
        flag = 0
        for coor in neighbor:
            child = Node(currentNode, coor)
            flag1 = 0
            for node in chosen:
                if node.position == child.position:
                    flag1 = 1
                    break
            if flag1 == 1:
                continue
            child.g = currentNode.g+1
            child.h = manhattan_dist(child.position, [finishrow, finishcol])
            child.f = child.g+child.h
            for idx, node in enumerate(canbe):
                if node.position == child.position and node.f<=child.f: #되나??
                    flag=1
                elif node.position == child.position and node.f>child.f:
                    flag=1
                    canbe.append(child)
                    break
            if flag==0:
                canbe.append(child)
    
    path.reverse()
    return path

    ############################################################################



def stage2_heuristic(targets, p):
    min = abs(p[0]-targets[0][0])+abs(p[1]-targets[0][1])
    for x, y in targets:
        if min>abs(p[0]-x)+abs(p[1]-y):
            min = abs(p[0]-x)+abs(p[1]-y)
    return min


def astar_four_circles(maze):
    """
    [Problem 04] 제시된 stage2 맵 세 가지를 A* Algorithm을 통해 최단경로를 return하시오.
    (Heuristic Function은 직접 정의할것 )
    """
    start_point = maze.startPoint()
    path = []
    ####################### Write Your Code Here ################################
    minusflag=0
    found = 4
    target = []
    target1 = []
    cnt=0
    flag = 0
    for i in range(maze.rows):
        for j in range(maze.cols):
            if maze.isObjective(i, j):
                target.append((i, j))
                target1.append((i, j))
                cnt=cnt+1
                if cnt==4:
                    flag=1
                    break
        if flag==1:
            break
    
    canbe = []
    chosen = []
    startNode = Node(None, start_point)
    startNode.h = stage2_heuristic(target, start_point)
    startNode.f = startNode.h
    canbe.append(startNode)
    while canbe:
        currentNode = canbe[0]
        currentidx = 0
        for idx, node in enumerate(canbe):
            if node.f<currentNode.f:
                currentidx = idx
                currentNode = node
        canbe.pop(currentidx)
        chosen.append(currentNode)
        #print(currentNode.position)
        if maze.isObjective(currentNode.position[0], currentNode.position[1]):
            pos = currentNode.position
            #print("target", target)
            for idx, coor in enumerate(target):
                #print("coor", coor)
                #print("currentnode", currentNode.position)
                if coor[0] == currentNode.position[0] and coor[1] == currentNode.position[1]:
                    #print("?????????")
                    target.pop(idx)
                    break
            #print("after", target)
            found = found-1
            maze.setObjectives(target)
            segpath = []
            while True:
                #print(currentNode.position)
                segpath.append(currentNode.position)
                currentNode = currentNode.parent
                if currentNode==None:
                    break
            segpath.reverse()
            if minusflag==1:
                segpath.pop(0)
            path = path+segpath
            if minusflag==0:
                minusflag=1
            if found==0:
                break
            canbe.clear()
            chosen.clear()
            startNode = Node(None, pos)
            startNode.h = stage2_heuristic(target, pos)
            startNode.f = startNode.h
            chosen.append(startNode)
            currentNode = startNode


        if found==0:
            break

        neighbor = maze.neighborPoints(currentNode.position[0], currentNode.position[1])
        for coor in neighbor:
            child = Node(currentNode, coor)
            flag=0
            for node in chosen:
                if node.position == child.position:
                    flag=1
                    break
            if flag==1:   
                continue
            child.g = currentNode.g+1
            child.h = stage2_heuristic(target, child.position)
            child.f = child.g+child.h
            flag = 0
            for node in canbe:
                if node.position == child.position and node.f<=child.f:
                    flag=1
                elif node.position==child.position and node.f>child.f:
                    flag=1
                    canbe.append(child)
                    break
            if flag==0:
                canbe.append(child)
    maze.setObjectives(target1)
    return path
    ############################################################################

def find(a, parent):
    #print("a = ", a)
    if a == parent[a[0]][a[1]]:
        return a
    parent[a[0]][a[1]] = find(parent[a[0]][a[1]], parent)
    return parent[a[0]][a[1]]

def union(a, b, parent, size):
    if find(a, parent) == find(b, parent):
        return
    c = find(a, parent)
    d = find(b, parent)
    if size[c[0]][c[1]] <= size[d[0]][d[1]]:
        parent[c[0]][c[1]] = d
        size[d[0]][d[1]] += size[c[0]][c[1]]
    else:
        parent[d[0]][d[1]] = c
        size[c[0]][c[1]] += size[d[0]][d[1]]
    
def mst(edge, parent, size, finish):
    total = 0
    tree = []
    s = sorted(edge, key = lambda x:x[0])
    #print(s)
    cnt = 0
    for node in s:
        #print("node = ", node)
        #print("cmp", find(node[1], parent), find(node[2], parent))
        if find(node[1], parent) == find(node[2], parent):
            continue
        else:
            #print("inin:")
            union(node[1], node[2], parent, size)
            cnt = cnt+1
            total = total + node[0]
            tree.append((node[1], node[2], node[0]))
            tree.append((node[2], node[1], node[0]))
        if finish==cnt:
            break

    return tree, total

def stage3_heuristic(tree, p, dist):
    min = abs(tree[0][0]-p[0]) + abs(tree[0][1]-p[1])+dist[tree[0]]
    for coor in tree:
        cmp = abs(coor[0]-p[0])+abs(coor[1]-p[1])+dist[coor]
        if cmp<min:
            min = cmp
    return min

def astar_many_circles(maze):
    """
    [Problem 04] 제시된 stage3 맵 다섯 가지를 A* Algorithm을 통해 최단 경로를 return하시오.
    (Heuristic Function은 직접 정의 하고, minimum spanning tree를 활용하도록 한다.)
    """
    start_point = maze.startPoint()
    path = []
    ####################### Write Your Code Here ################################
    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]
    target = []
    target1 = []
    target2=[]
    finish = 0
    for i in range(maze.rows):
        for j in range(maze.cols):
            if maze.isObjective(i, j):
                target.append((i, j))
                target1.append((i, j))
                target2.append((i, j))
                finish = finish+1
    
    #print("target = ", target1)
    edge = []
    finish = len(target)
    visited = []
    for i in range(maze.rows):
        list1 = []
        for j in range(maze.cols):
            list1.append(0)
        visited.append(list1)
    parent=[]
    for i in range(maze.rows):    
        list1=[]
        for j in range(maze.cols):
            list1.append((i,j))
        parent.append(list1)
    size=[]
    for i in range(maze.rows):
        list1=[]
        for j in range(maze.cols):
            list1.append(1)
        size.append(list1)        
    ######################################################
    for idx, coor in enumerate(target):
        for i in range(maze.rows):
            visited[i] = [0 for i in range(maze.cols)]
        start = nod(coor)
        queue = deque([])
        queue.append(start)
        visited[coor[0]][coor[1]] = 1
        check = 1
        flag = 0
        while queue:
            current = queue.popleft()
            a = current.position[0]
            b = current.position[1]
            for i in range(4):
                x = a+dx[i]
                y = b+dy[i]
                if x<0 or y<0 or x>=maze.rows or y>=maze.cols or maze.isWall(x, y):
                    continue
                if visited[x][y] == 1:
                    continue
                if maze.isObjective(x,y):
                    if (x,y) in target:
                        edge.append((current.cnt+1, coor, (x,y)))
                    check=check+1
                    if check == finish:
                        flag = 1
                        break
                visited[x][y] = 1
                pu = nod((x, y))
                pu.cnt = current.cnt+1
                queue.append(pu) 
            if flag==1:
                break
        target.pop(idx)
    #print(edge)
    tree, total = mst(edge, parent, size, finish)
    dist = {}
    for coor in target1:
        before = (-1, -1)
        curr = coor
        curdist = 0
        while True:
            flag = 0
            for node in tree:
                if node[0]==curr and node[1]!=before:
                    curdist = curdist + node[2]
                    #print("curdist = ", curdist)
                    before = node[0]
                    curr = node[1]
                    flag = 1
                    break
            if flag==0:
                break
        if curdist > total/2:
            curdist = total-curdist
        dist[coor] = curdist*2 + (total-curdist)
    # print("///////////////////////////////////")
    # print(dist)
    # print("total - ", total)
                

    ########################## mst ###########################################
    canbe = []
    chosen = []
    found = len(target1)
    minusflag = 0
    startNode = Node(None, start_point)
    startNode.h = stage3_heuristic(target1, start_point, dist)
    startNode.f = startNode.h
    canbe.append(startNode)
    while canbe:
        currentNode = canbe[0]
        currentidx = 0
        for idx, node, in enumerate(canbe):
            if node.f<currentNode.f:
                currentidx = idx
                currentNode = node
        canbe.pop(currentidx)
        chosen.append(currentNode)

        if maze.isObjective(currentNode.position[0], currentNode.position[1]):
            pos = currentNode.position
            for idx, coor in enumerate(target1):
                if coor[0] == currentNode.position[0] and coor[1] == currentNode.position[1]:
                    target1.pop(idx)
                    break
            found = found-1
            maze.setObjectives(target1)
            segpath = []
            while True:
                segpath.append(currentNode.position)
                currentNode = currentNode.parent
                if currentNode == None:
                    break
            segpath.reverse()
            if minusflag == 1:
                segpath.pop(0)
            path = path+segpath
            if minusflag==0:
                minusflag = 1
            if found==0:
                break
            canbe.clear()
            chosen.clear()
            startNode = Node(None, pos)
            startNode.h = stage3_heuristic(target1, pos, dist)
            startNode.f = startNode.h
            chosen.append(startNode)
            currentNode = startNode
        
        if found==0:
            break

        neighbor = maze.neighborPoints(currentNode.position[0], currentNode.position[1])
        for coor in neighbor:
            child = Node(currentNode, coor)
            flag = 0
            for node in chosen:
                if node.position == child.position:
                    flag=1
                    break
            if flag==1:
                continue
            child.g = currentNode.g+1
            child.h = stage3_heuristic(target1, child.position, dist)
            child.f = child.g + child.h
            flag = 0
            for node in canbe:
                if node.position == child.position and node.f<=child.f:
                    flag = 1
                elif node.position == child.position and node.f>child.f:
                    flag = 1
                    canbe.append(child)
                    break
            if flag==0:
                canbe.append(child)
    maze.setObjectives(target2)
    return path


