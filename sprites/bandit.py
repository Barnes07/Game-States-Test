import pygame 
import os
import math
from sprites.enemy import Enemy
import heapq
from AStar.node import Node



class Bandit(Enemy):
    def __init__ (self, game, group, actual_map_width, actual_map_height, game_world):
        super().__init__(game, group)
        self.game = game
        self.game_world = game_world
        self.group = group
        self.x = 1280
        self.y = 1280
        self.current_image = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "player", "player_down1.png")).convert_alpha()
        self.rect = self.current_image.get_rect(center = (self.x, self.y))
        self.speed = 100
        self.direction = pygame.math.Vector2()

        self.waypoints = []
        self.target_waypoint = 0
        self.actual_pos = pygame.math.Vector2(self.rect.centerx//self.game.block_size, self.rect.centery//self.game.block_size)
        

        
        #Player detection
        self.fov_width = 90
        self.half_fov_width = self.fov_width/2
        self.fov_distance = 500
        self.facing_angle = 0

        #Pathfinding 
        self.actual_map_width = actual_map_width
        self.actual_map_height = actual_map_height
        self.directions = [(0,1), (0,-1), (1,0), (-1,0)]

        #Follow path
        self.distance_to_node = self.game.block_size
        self.time_to_node = self.distance_to_node/self.speed
        self.time_since_last_node = 0

        
        

    def set_waypoints(self, new_waypoints):
        self.waypoints = new_waypoints
        self.target_waypoint = 0
    
    def create_path(self):
        path = self.pathfind(self.game_world.player, self.game_world.player.actual_pos, self.game_world.map.final_map)
        self.set_waypoints(path)
    
    def set_direction(self):
        if not self.waypoints or self.target_waypoint >= len(self.waypoints):
            self.direction = (0,0)
        else:
            self.target = pygame.math.Vector2(self.waypoints[self.target_waypoint]) 
            self.direction = self.target - self.actual_pos
            self.target_waypoint += 1
            print(self.direction)



        
            

        
        
    def check_detection(self, player):
        check = False
        enemy_vector = pygame.math.Vector2(self.x, self.y)
        player_vector = pygame.math.Vector2(player.rect.centerx, player.rect.centery)
        facing_vector = pygame.math.Vector2(1,0).rotate(self.facing_angle)
        direction_to_player = (player_vector - enemy_vector).normalize()
        angle_to_player = facing_vector.angle_to(direction_to_player)
        #normalisation if angle to player is a negative value. So that the angle is in the range 0-360.
        if angle_to_player < 0:
            angle_to_player = angle_to_player + 360
        
        if (360-self.half_fov_width) <= angle_to_player <= 360 or self.half_fov_width >= angle_to_player >= 0:
            distance_to_player = player_vector.distance_to(enemy_vector)
            if distance_to_player <= self.fov_distance:
                check = True
        return(check)
            
    def heuristic(self, start, end):
        startx = start[0]
        starty = start[1]
        endx = end[0]
        endy = end[1]
        #calculate manhatten distance
        return(abs(startx - endx)) + abs(starty - endy) 
    
    def pathfind(self, player, end, map): #end is end position
        if self.check_detection(player) == True:
            open_set = []
            closed_set = set()
            g_scores = {}
            f_scores = {}

            positions_added_to_open_set = set() #Sets have O(1) time complexity so checking if a neighbour is already in the open set is more effcient 

            start_node = Node(None, (self.rect.centerx//self.game.block_size, self.rect.centery//self.game.block_size)) #was using self.x instead of self.rect.centerx which meant the start node was incorrect each time. 
            start_pos = (start_node.position)
            g_scores[start_pos] = 0 
            f_scores[start_pos] = 0 + self.heuristic(start_pos, end)

            heapq.heappush(open_set, (0, start_node))

            while len(open_set) > 0:
                (current_f_score, current_node) = heapq.heappop(open_set) 
            
                if current_node.position == end:
                    path = []
                    while current_node != None:
                        path.append(current_node.position)
                        current_node = current_node.parent
                    return path[::-1]  # Return the reversed path
                
                closed_set.add(current_node.position)
                
                for count in range(0,4):
                    direction = self.directions[count]
                    neighbour_pos = (current_node.position[0] + direction[0], current_node.position[1] + direction[1])

                    #Check if neighbour is within map remits and is a floor object (1) and if it is not in the closed set. If it was in the closed set, then the shortest distance to that node has already been calculated
                    if 0 <= neighbour_pos[0] < self.actual_map_width and 0 <= neighbour_pos[1] < self.actual_map_height and map[neighbour_pos[0]][neighbour_pos[1]] == 1 and neighbour_pos not in closed_set:
                        temp_g_score = g_scores[current_node.position] + 1

                        if neighbour_pos not in g_scores or temp_g_score < g_scores[neighbour_pos]: #will create a new neigbour node it the node does not have a g_score or a lower g_score has been found
                            g_scores[neighbour_pos] = temp_g_score
                            f_scores[neighbour_pos] = temp_g_score + self.heuristic(neighbour_pos, end)
                            
                            if neighbour_pos not in positions_added_to_open_set:
                                neighbour_node = Node(current_node, neighbour_pos)
                                heapq.heappush(open_set, (f_scores[neighbour_pos], neighbour_node)) #This adds a tuple (Total_cost,neighbour_node) to the priority queue. Since the heapq module orders elements based on the first element of each tuple, this means that the priority queue is ordered by the Total_cost (from lowest to highest)
                                positions_added_to_open_set.add(neighbour_pos)
            return(None)                    
        
    def update(self, delta_time):
        self.actual_pos = pygame.math.Vector2(self.rect.centerx//self.game.block_size, self.rect.centery//self.game.block_size)
        player_pos = pygame.math.Vector2(self.game_world.player.actual_pos)
        distance_to_player = self.actual_pos.distance_to(player_pos)

        self.time_since_last_node += delta_time
        

        if distance_to_player < 5: #check distance to player to determine if pathfinding should take place
            pass

        else:
            if not self.waypoints:
                self.create_path()
                path = self.waypoints
                print(path)
                
                
            #needs revising
            if self.time_since_last_node > self.time_to_node and self.waypoints:
                self.time_since_last_node = 0
                if self.target_waypoint < len(self.waypoints):
                    if self.target_waypoint > 0:
                        self.rect.centerx = (self.waypoints[self.target_waypoint-1][0]) * self.game.block_size
                        self.rect.centery = (self.waypoints[self.target_waypoint-1][1]) * self.game.block_size
                        self.actual_pos = pygame.math.Vector2(self.rect.centerx//self.game.block_size, self.rect.centery//self.game.block_size)
                    self.set_direction()
                else:
                    self.waypoints = []
                    self.target_waypoint = 0

            


            
            

                
                
                
                





        

        

