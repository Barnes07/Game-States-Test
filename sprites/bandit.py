import pygame 
import os
import math
from sprites.enemy import Enemy
import heapq
from AStar.node import Node

class Bandit(Enemy):
    def __init__ (self, game, group, actual_map_width, actual_map_height, game_world):
        super().__init__(game, group)
        self.game_world = game_world
        self.x = 1280
        self.y = 1280
        self.current_image = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "player", "player_down1.png")).convert_alpha()
        self.rect = self.current_image.get_rect(center = (self.x, self.y))
        self.speed = 100
        self.detection_radius = 10000


        self.actual_map_width = actual_map_width
        self.actual_map_height = actual_map_height
        
        

    def check_detection(self, player):
        check = False
        enemy_vector = pygame.math.Vector2(self.x, self.y)
        player_vector = pygame.math.Vector2(player.rect.centerx, player.rect.centery)
        distance_to_player = player_vector.distance_to(enemy_vector)
        if distance_to_player <= self.detection_radius:
            check = True
        return(check)
            
            
    def heuristic(self, start, end):
        startx = start[0]
        starty = start[1]
        endx = end[0]
        endy = end[1]
        return(abs(startx - endx)) + abs(starty - endy) #formula for manhatten distance
    

    def pathfind(self, player, end, map): #end is end position
        if self.check_detection(player) == True:
            directions = [(0,1), (0,-1), (1,0), (-1,0)]
            open_set = []
            closed_set = set()
            start_node = Node(None, (self.x//self.game.block_size, self.y//self.game.block_size))
            heapq.heappush(open_set, (0, start_node))

            while len(open_set) > 0: #while there are still nodes to be visited
                (current_g_score, current_node) = heapq.heappop(open_set) 
            
                if current_node.position == end:
                    path = []
                    while current_node != None:
                        path.append(current_node.position)
                        current_node = current_node.parent
                    return path[::-1]  # Return the reversed path
                
                closed_set.add(current_node.position) #marks the current node as visited by pushing it to the closed set
                
                for count in range(0,4):
                    direction = directions[count]
                    neighbour_pos = (current_node.position[0] + direction[0], current_node.position[1] + direction[1]) #calculates position of all neighbouring nodes (above, below to the left and right)

                    #check if the neighbour node is in the remits of the map, if it is a floor (1) and if it hasn't already been visited (in the closed set)
                    if 0 <= neighbour_pos[0] < self.actual_map_width and 0 <= neighbour_pos[1] < self.actual_map_height and map[neighbour_pos[0]][neighbour_pos[1]] == 1 and neighbour_pos not in closed_set:
                        
                        temp_g_score = current_g_score + 1
                        f_score = temp_g_score + self.heuristic(neighbour_pos, end) 
                        neighbour_node = Node(current_node, neighbour_pos) #instantiates a new node with the current node as a parent and the neighbour's position
                        heapq.heappush(open_set, (f_score, neighbour_node)) #adds a tuple (Total_cost,neighbour_node) to the priority queue. 
                
                    
            return(None) #returns none if open set is empty and therefore no path has been found                    
            



#Since the heapq module orders elements based on the first element of each tuple, this means that the priority queue is ordered by the Total_cost (from lowest to highest)

    
    def update(self):
        pass
        
        

        

