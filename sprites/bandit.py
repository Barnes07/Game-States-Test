import pygame 
import os
import math
import random
from sprites.enemy import Enemy
import heapq
from AStar.node import Node

class Bandit(Enemy):
    def __init__ (self, game, group, actual_map_width, actual_map_height, game_world):
        super().__init__(game, group)
        self.game_world = game_world
        self.x = 2100
        self.y = 2282
        self.current_image = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "bandit", "bandit.png")).convert_alpha()
        self.rect = self.current_image.get_rect(center = (self.x, self.y))


        #pathfinding
        self.set_difficulty()
        

        #map dimensions
        self.actual_map_width = actual_map_width
        self.actual_map_height = actual_map_height

        #waypoints
        self.time_since_last_move = 0
        self.current_waypoint = 0
        self.waypoints = []
        self.actual_pos = pygame.math.Vector2(self.rect.centerx//self.game.block_size, self.rect.centery//self.game.block_size)

        self.previous_position = pygame.math.Vector2()    

        #Flute
        self.charmed = False   
        self.smoked = False

    def check_detection(self, player):
        check = False
        distance_to_player = self.get_distance_to_player(player)
        if distance_to_player <= self.detection_radius:
            #if the player is within the detection radius
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
            g_scores = {} #distance to a given node from the start 
            f_scores = {} #estimated distance to the end node

            positions_added_to_open_set = set() #coordinates of nodes that have been added to the open set

            start_node = Node(None, (self.rect.centerx//self.game.block_size, self.rect.centery//self.game.block_size)) #instantiate start node
            start_pos = (start_node.position)
            g_scores[start_pos] = 0 
            f_scores[start_pos] = 0 + self.heuristic(start_pos, end) 

            heapq.heappush(open_set, (0, start_node)) #add start node to the priority queue

            while len(open_set) > 0: #while there are still nodes to be visited
                (current_f_score, current_node) = heapq.heappop(open_set) #was origionally setting current_g_score not current_f_score 
            
                if current_node.position == end:
                    #if a path to the end node has been found
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
            #if player is within the chase radius of the bandit
            check = True
        return(check)

    def follow_waypoints(self, delta_time):
        self.time_since_last_move += delta_time #increments the time since the last move by the time elapsed since the last frame's execution 
        if self.time_since_last_move > self.time_to_move_to_waypoint and self.waypoints:
            #if sufficient time has elapsed and there are still waypoints to follow:
            if self.current_waypoint < len(self.waypoints) - 1:
                #if there is a waypoint to follow
                self.time_since_last_move = 0  
                self.current_waypoint += 1
                self.rect.centerx = self.waypoints[self.current_waypoint][0] * self.game.block_size #update x position to be eqaul to that specified by the waypoint
                self.rect.centery = self.waypoints[self.current_waypoint][1] * self.game.block_size #update y position to be eqaul to that specified by the waypoint
                self.actual_pos = pygame.math.Vector2(self.rect.centerx//self.game.block_size, self.rect.centery//self.game.block_size) #update actual position attribute
            else:
                #clear waypoints as the destination has been reached
                self.waypoints = []
                self.current_waypoint = 0 #rest pointer
                self.time_since_last_move = 0
    
    def find_start_coordinates(self, map):
        #Find a pair of random valid coordinates.
        found = False
        while found == False:
            #while valid starting coordinates have not been found, create new random coordinates
            random_x = random.randint(1, self.game_world.actual_map_width - 1)
            random_y = random.randint(1, self.game_world.actual_map_height - 1)
            if map[random_x][random_y] == 1:
                #return the coordinates if they are a floor (valid)
                found = True
                self.set_coordinates(random_x, random_y)
                 
    def set_coordinates(self, x, y):
        #update the rectangles x and y coordinates according to the x and y parameters
        self.rect = self.current_image.get_rect(center = (x * self.game.block_size, y * self.game.block_size))
        #x and y are multiplied by "block_size" so that the cooridnates are in terms of pixels

    def get_distance_to_player(self, player): #method to calculate distance between player and enemy
        enemy_vector = pygame.math.Vector2(self.rect.centerx, self.rect.centery) 
        player_vector = pygame.math.Vector2(player.rect.centerx, player.rect.centery)
        distance_to_player = player_vector.distance_to(enemy_vector) #finds distnace between two position vectors
        return(distance_to_player)
    
    def predict_player_future_position(self, player): #method to estimate the player's coordinates during the next frame
        future_position_x = player.rect.centerx + player.velocity.x * self.game.delta_time #future player x coordinate if it continues moving in the same direction nect frame
        future_position_y = player.rect.centery + player.velocity.y * self.game.delta_time #future player x coordinate if it continues moving in the same direction nect frame
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
         
    def check_flute_valid(self):
        if self.game_world.player.flute_picked_up:
            #if the player has collected the flute
            return(True)
        else:
            return(False)
    
    def player_noise(self, actions):
        if self.game.bandit_difficulty == 1:
            if actions["start"]:
                self.detection_radius = 3500
                self.chase_radius = 600
            else:
                self.detection_radius = 3000
                self.chase_radius = 500
        elif self.game.bandit_difficulty == 2:
            if actions["start"]:
                self.detection_radius = 4000
                self.chase_radius = 650
            else:
                self.detection_radius = 3500
                self.chase_radius = 600
        else:
            if actions["start"]:
                self.detection_radius = 3000
                self.chase_radius = 500
            else:
                self.detection_radius = 2000
                self.chase_radius = 250




                



    def set_difficulty(self):
        if self.game.bandit_difficulty == 1:
            self.detection_radius = 3000
            self.chase_radius = 500
            self.speed = 250
            self.time_to_move_to_waypoint = 0.5
            print("detection_radius:", self.detection_radius)
            print("chase_radius: ", self.chase_radius)
            print("speed: ", self.speed)
            print("time to waypoint: ", self.time_to_move_to_waypoint)

        elif self.game.bandit_difficulty == 2:
            self.detection_radius = 3500
            self.chase_radius = 600
            self.speed = 300
            self.time_to_move_to_waypoint = 0.25
            print("detection_radius:", self.detection_radius)
            print("chase_radius: ", self.chase_radius)
            print("speed: ", self.speed)
            print("time to waypoint: ", self.time_to_move_to_waypoint)

        else:
            self.detection_radius = 2000
            self.chase_radius = 250
            self.speed = 200
            self.time_to_move_to_waypoint = 1
            print("detection_radius:", self.detection_radius)
            print("chase_radius: ", self.chase_radius)
            print("speed: ", self.speed)
            print("time to waypoint: ", self.time_to_move_to_waypoint)

        



    def check_play_flute(self, actions):
        if actions["flute"]:
            #if the "f" key has been pressed
            if self.check_flute_valid:
                distance_to_player = self.get_distance_to_player(self.game_world.player)
                if distance_to_player < 300:
                    #if the player is within a radius of 300 pixels
                    self.charmed = True
                    self.game_world.player.flute_picked_up = False
    
    def update(self, delta_time, actions):
        velocity_x = self.rect.centerx - self.previous_position.x
        velocity_y = self.rect.centery - self.previous_position.y
        self.velocity = pygame.math.Vector2(velocity_x, velocity_y) 
        #velocity will always need to be calculated at the start of the update method as it needs to be accurate for the current frame

        self.check_play_flute(actions)

        self.player_noise(actions)

        if self.charmed == False and self.smoked == False:
            #if the bandit is not charmed, chase the player
            if self.check_chase(self.game_world.player):
                #if within chase distance
                self.pursue(self.game_world.player)
                self.waypoints = [] #reset self.waypoints
                self.current_waypoint = 0 #reset self.current_waypoint
                self.rect.centerx += self.velocity.x * delta_time
                self.rect.centery += self.velocity.y * delta_time

            else:
                #if greater than chase distance
                if not self.waypoints:
                    self.create_path()
                self.follow_waypoints(delta_time)

        

        self.previous_position = pygame.math.Vector2(self.rect.centerx, self.rect.centery) #need to update the previous position at the end of the update method


        

