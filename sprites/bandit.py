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
        self.x = 2000
        self.y = 2000
        self.current_image = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "player", "player_down1.png")).convert_alpha()
        self.rect = self.current_image.get_rect(center = (self.x, self.y))
        self.speed = 200

        self.detection_radius = 2000 
        self.chase_radius = 250
        self.waypoints = []
        self.actual_pos = pygame.math.Vector2(self.rect.centerx//self.game.block_size, self.rect.centery//self.game.block_size)


        self.actual_map_width = actual_map_width
        self.actual_map_height = actual_map_height

        self.time_since_last_move = 0
        self.time_to_move_to_waypoint = 1
        self.current_waypoint = 0

        self.previous_position = pygame.math.Vector2()       

    def check_detection(self, player):
        check = False
        distance_to_player = self.get_distance_to_player(player)
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
            g_scores = {}
            f_scores = {}

            positions_added_to_open_set = set()

            start_node = Node(None, (self.rect.centerx//self.game.block_size, self.rect.centery//self.game.block_size))
            start_pos = (start_node.position)
            g_scores[start_pos] = 0
            f_scores[start_pos] = 0 + self.heuristic(start_pos, end)

            heapq.heappush(open_set, (0, start_node))

            while len(open_set) > 0: #while there are still nodes to be visited
                (current_f_score, current_node) = heapq.heappop(open_set) #was origionally setting current_g_score not current_f_score 
            
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
                        temp_g_score = g_scores[current_node.position] + 1
                        
                        if neighbour_pos not in g_scores or temp_g_score < g_scores[neighbour_pos]: #will create a neighbour node if the node does not yet have a g score or if a smaller one has been found
                            g_scores[neighbour_pos] = temp_g_score
                            f_scores[neighbour_pos] = temp_g_score + self.heuristic(neighbour_pos, end)

                            if neighbour_pos not in positions_added_to_open_set:
                                neighbour_node = Node(current_node, neighbour_pos) #instantiates a new node with the current node as a parent and the neighbour's position
                                heapq.heappush(open_set, (f_scores[neighbour_pos], neighbour_node)) #adds a tuple (Total_cost,neighbour_node) to the priority queue. Since the heapq module orders elements based on the first element of each tuple, this means that the priority queue is ordered by the Total_cost (from lowest to highest) 
                                positions_added_to_open_set.add(neighbour_pos)

            return(None) #returns none if open set is empty and therefore no path has been found                    
            
    def set_waypoints(self, path):
        self.waypoints = path

    def create_path(self):
        path = self.pathfind(self.game_world.player, self.game_world.player.actual_pos, self.game_world.map.final_map)
        self.set_waypoints(path)

    def check_chase(self,player):
        check = False
        distance_to_player = self.get_distance_to_player(player)
        if distance_to_player <= self.chase_radius:
            check = True
        return(check)

    def follow_waypoints(self, delta_time):
        self.time_since_last_move += delta_time
        if self.time_since_last_move > self.time_to_move_to_waypoint and self.waypoints:
            if self.current_waypoint < len(self.waypoints) - 1:
                self.time_since_last_move = 0  
                self.current_waypoint += 1
                self.rect.centerx = self.waypoints[self.current_waypoint][0] * self.game.block_size
                self.rect.centery = self.waypoints[self.current_waypoint][1] * self.game.block_size
                self.actual_pos = pygame.math.Vector2(self.rect.centerx//self.game.block_size, self.rect.centery//self.game.block_size)
            else:
                self.waypoints = []
                self.current_waypoint = 0
                self.time_since_last_move = 0
    
    def find_start_coordinates(self, map):
        found = False
        #iterate through all blocks in the map grid
        for a in range (self.game_world.actual_map_width, 0, -1):
            for b in range(self.game_world.actual_map_height, 0, -1):
                wall_count = 0
                #iterate through neighbouring 8 blocks
                for x in range (a-1, a+2):
                    for y in range(b-1, b+2):
                        #check if the block is within map bounds
                        if 0 <= x < self.game_world.actual_map_width and 0 <= y < self.game_world.actual_map_height:
                            #check if block is a wall
                            if map[x][y] == 0:
                                wall_count = wall_count + 1
                        else:
                            wall_count = wall_count + 1
                if wall_count == 0:
                    #set bandit starting coordinates to those stored in a and b
                    a = a * self.game.block_size
                    b = b * self.game.block_size
                    if found == False:
                        self.set_coordinates(a, b)
                        found = True
                        print("Starting cooridnates found at ", a, b)

                    
    def set_coordinates(self, x, y):
        self.rect = self.current_image.get_rect(center = (x, y))

    def get_distance_to_player(self, player): #method to calculate distance between player and enemy
        enemy_vector = pygame.math.Vector2(self.rect.centerx, self.rect.centery) 
        player_vector = pygame.math.Vector2(player.rect.centerx, player.rect.centery)
        distance_to_player = player_vector.distance_to(enemy_vector)
        return(distance_to_player)
    
    def predict_player_future_position(self, player): #method to estimate the player's coordinates during the next frame
        future_position_x = player.rect.centerx + player.velocity.x * self.game.delta_time
        future_position_y = player.rect.centery + player.velocity.y * self.game.delta_time #these lines calculate the estimated future coordinates of player
        return((future_position_x, future_position_y))

    def pursue(self, player): 
        enemy_vector = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
        player_future_vector = pygame.math.Vector2(self.predict_player_future_position(player))
        vector_to_future_player = pygame.math.Vector2(player_future_vector.x - enemy_vector.x, player_future_vector.y - enemy_vector.y) #vector to estimated player position
        
        if vector_to_future_player.magnitude() == 0: #check if vector is zero to prevent error when attempting to normalise vector with 0 magnitude
            required_velocity = pygame.math.Vector2(0,0)
        else:
            required_velocity = vector_to_future_player.normalize() * self.speed #calculate the speed and direction needed to move towards estimated player position

        steering = pygame.math.Vector2(required_velocity.x - self.velocity.x, required_velocity.y - self.velocity.y) #steering vector used to alter bandit's direction of travel

        self.velocity.x += steering.x #update x component of velocity
        self.velocity.y += steering.y #update y component of velocity
    
    def check_player_collision(self, player):
        if pygame.sprite.collide_rect(self, player):
            return(True)


        
    def update(self, delta_time):
        velocity_x = self.rect.centerx - self.previous_position.x
        velocity_y = self.rect.centery - self.previous_position.y
        self.velocity = pygame.math.Vector2(velocity_x, velocity_y) #need to calculate velocity at start of update method

        if self.check_chase(self.game_world.player):
            self.pursue(self.game_world.player)
            self.waypoints = [] #reset self.waypoints
            self.current_waypoint = 0 #reset self.current_waypoint
            self.rect.centerx += self.velocity.x * delta_time
            self.rect.centery += self.velocity.y * delta_time

        else:
            if not self.waypoints:
                self.create_path()
            self.follow_waypoints(delta_time)

        

        self.previous_position = pygame.math.Vector2(self.rect.centerx, self.rect.centery) #need to update the previous position at the end of the update method


        

