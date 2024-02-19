from AStar.astar import Node
import heapq

class Astar():
    def __init__(self, map, start, end):
        self.map = map
        self.start = start
        self.end = end
        self.directions = [(0,1), (1,0), (0,-1), (-1,0)]
        self.open_set = []
        self.closed_set = set()
        self.start_node = Node(None, self.start)
        heapq.heappush(self.open_set, (0, self.start_node)) 

    def heuristic(self, start, end):
        # Euclidean distance heuristic
        return ((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2)

    def pathfind(self):
        while len(self.open_set) > 0:
            (current_cost, current_node) = heapq.heappop(self.open_set) 

            if current_node.position == self.end:
                path = []
                while current_node != None:
                    path.append(current_node.position)
                    current_node = current_node.parent
                return(path[::-1]) # Return the reversed path
            
            else:
                self.closed_set.add(current_node.position)
                for direction in self.directions:
                    neighbour_position = (current_node.position[0] + direction[0], current_node.position[1] + direction[1])
                    if 0 <= neighbour_position[0] < len(self.map) and 0 <= neighbour_position[1] < len(self.map[0]):
                        if self.map[neighbour_position[0]][neighbour_position[1]] == 1:
                            if neighbour_position not in self.closed_set:
                                neighbour_node = Node(current_node, neighbour_position)
                                neighbour_node.g = current_node.g + 1
                                neighbour_node.h = self.heuristic(neighbour_node.position, self.end)
                                neighbour_node.f = neighbour_node.g + neighbour_node.h

                                if any(open_node for open_node in self.open_set if neighbour_node.position == open_node.position and neighbour_node.g > open_node.g):
                                    pass
                                else:
                                    heapq.heappush(self.open_set, (neighbour_node.f, neighbour_node))#This adds a tuple (neighbour_node.f,neighbour_node) to the priority queue. Since the heapq module orders elements based on the first element of each tuple, this means that the priority queue is ordered by the Total_cost (from lowest to highest)
        return(None)# If no path is found


                            



    

