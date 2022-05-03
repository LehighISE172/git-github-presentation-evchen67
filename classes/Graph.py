#importing
import numpy as np
import pygame
import heapq

class Graph:

    def __init__(self, V, E): 
        """ 
        this should create some representation of the graph, 
        where  - V is list of vertices (with corresponding attributes)
               - E is list of edges (with corresponding attributes)
        """
        
        self.vertDict = V
        self.verticies = list(self.vertDict.keys()) # list of verticies
        for key in self.vertDict:
            x1 = self.vertDict[key][0] * 800 # scaling x-coordinate of vertex
            y1 = self.vertDict[key][1] * 800 # scaling y-coordinate of vertex
            self.vertDict[key] = x1, y1
        self.edges = E
        for edge in self.edges:
            cost = self.edges[edge][0]
            pos = []
            for x in range(0, len(self.edges[edge][1])):
                x1 = self.edges[edge][1][x][0] * 800 # scaling x-coordinate of initial point in edge
                y1 = self.edges[edge][1][x][1] * 800 # scaling x-coordinate of initial point in edge
                input = [x1, y1]
                pos.append(input)
            direction = self.edges[edge][2]
            self.edges[edge] = [cost, pos, direction]
        self.visited = []
        self.queue = []
        self.neighbors = {}
        for v in self.verticies:
            self.neighbors[v] = self.get_neigh(v) # get neighbors of each vertex
        self.shortestPath = {}
        for a in self.verticies:
            for b in self.verticies:
                self.shortestPath[a,b] = self.get_path(a,b) # find shortest path between any 2 verticies
        
    def getCost(self, fromV, toV):
        
        if (fromV, toV) in self.edges:
            return self.edges[fromV, toV][0] # return cost of edge between fromV and toV
        if (toV, fromV) in self.edges:
            return self.edges[toV, fromV][0] # return cost of edge between fromV and toV
        
    def get_node_list(self):
        return self.verticies
    
    def get_edge_list(self):
        return self.edges
    
    def get_neigh(self, v):
        neighbors = []
        keys = [k for k in self.edges if k[0] == v or k[1] == v]
        for x in keys:
            if v == x[0]: # check if vertex appears first or second in edge, then check directionality
                if self.edges[v, x[1]][-1] == 'B' or self.edges[v, x[1]][-1] == 'OneWayA':
                    neighbors.append(x[1])
            elif v == x[1]: # check if vertex appears first or second in edge, then check directionality
                if self.edges[x[0], v][-1] == 'B' or self.edges[x[0], v][-1] == 'OneWayB':
                    neighbors.append(x[0])
        return neighbors
    
    def get_time(self, prior, next):
        for edge in self.edges:
            if prior == edge[0] and next == edge[1]: # check order of prior and next in the edge
                time = self.edges[edge][0]
                return time
            elif prior == edge[1] and next == edge[0]: # check order of prior and next in the edge
                time = self.edges[edge][0]
                return time
            
    def get_speed(self, prior, next, carRect, time):
        xPrior, yPrior = self.vertDict[prior]
        xNext, yNext = self.vertDict[next]
        xCurr = carRect.centerx
        yCurr = carRect.centery
        xToGo = (xNext - xCurr)/time
        yToGo = (yNext - yCurr)/time
        speed = [xToGo, yToGo]    
        return speed
    
    def idleCar(self,j):
        car = pygame.image.load("data/idlecar%d.png"%(j)) # car 0 gets car0 picture, car 1 gets car1, etc.
        car = pygame.transform.scale(car, (20, 20)) 
        return car
    
    def movingCar(self, j):
        car = pygame.image.load("data/car%d.png"%(j)) # car 0 gets car0 picture, car 1 gets car1, etc.
        car = pygame.transform.scale(car, (20, 20)) 
        return car      
    def get_path(self, u, v):
        if u == v: # stop if both verticies are the same point
            return
        heap = []
        delta = {}
        permanent = {}
        pre = {}
        path = []
        for n in self.verticies:
            delta[n] = np.inf
            heapq.heappush(heap, (np.inf, n))
        delta[u] = 0
        heapq.heappush(heap, (0, u))
        
        i = 0
        while len(permanent) < len(delta):
            i+=1
            bestValue, bestNode = heapq.heappop(heap)
            permanent[bestNode] = True
            for neighbor in self.neighbors[bestNode]:
                if neighbor not in permanent:
                    previousEstimate = delta[neighbor]
                    proposedValue = bestValue + self.getCost(bestNode, neighbor)
                    if proposedValue < previousEstimate:
                        delta[neighbor] = proposedValue
                        pre[neighbor] = bestNode
                        heapq.heappush(heap, (proposedValue, neighbor))
                        
        path.append(v)
        while pre[v] != u:
            path.append(pre[v]) # path stored backwards from end to start
            v = pre[v]
        path.append(u)
        path = path[::-1] # flip path so it prints in the correct order
        
        return path