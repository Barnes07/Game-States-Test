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
        self.x = 100
        self.y = 100
        self.current_image = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "player", "player_down1.png")).convert_alpha()
        self.rect = self.current_image.get_rect(center = (self.x, self.y))
        self.speed = 100
        self.direction = pygame.math.Vector2()

        

        self.fov_width = 90
        self.half_fov_width = self.fov_width/2
        self.fov_distance = 100000
        self.facing_angle = 0

        self.directions = [(0,1), (1,0), (0,-1), (-1,0)]
        self.open_set = []
        self.closed_set = set()
        self.actual_map_width = actual_map_width
        self.actual_map_height = actual_map_height

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
        return ((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2)


    def pathfind(self, player):
        #if self.check_detection(player) == True:
        start = ((self.rect.centerx//self.game.block_size, self.rect.centery//self.game.block_size,))
        end = ((player.rect.centerx//self.game.block_size, player.rect.centery//self.game.block_size))
        start_node = Node(None, start)
        heapq.heappush(self.open_set, (0, start_node)) 
        while len(self.open_set) > 0:
            (current_cost, current_node) = heapq.heappop(self.open_set)


            if current_node.position == end:
                path = []
                
                while current_node != None:
                    path.append(current_node.position)
                    current_node = current_node.parent
                return(path[::-1]) # Return the reversed path
                
            
                
            self.closed_set.add(current_node.position)
            for direction in self.directions:
                neighbour_position = (current_node.position[0] + direction[0], current_node.position[1] + direction[1])
                if 0 <= neighbour_position[0] < self.actual_map_width and 0 <= neighbour_position[1] < self.actual_map_height:
                    if self.game_world.map.final_map[neighbour_position[0]][neighbour_position[1]] == 0:
                        if neighbour_position not in self.closed_set:
                            neighbour_node = Node(current_node, neighbour_position)
                            neighbour_node.g = current_node.g + 1
                            neighbour_node.h = self.heuristic(neighbour_node.position, end)
                            neighbour_node.f = neighbour_node.g + neighbour_node.h

                            if any(open_node for open_node in self.open_set if neighbour_node.position == open_node[1].position and neighbour_node.g > open_node[1].g):
                                pass
                            else:
                                heapq.heappush(self.open_set, (neighbour_node.f, neighbour_node))#This adds a tuple (neighbour_node.f,neighbour_node) to the priority queue. Since the heapq module orders elements based on the first element of each tuple, this means that the priority queue is ordered by the Total_cost (from lowest to highest)
        return(None)# If no path is found

            

            

    
    def update(self):
        pass
        
        

        

