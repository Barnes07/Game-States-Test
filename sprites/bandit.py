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

        

        self.fov_width = 90
        self.half_fov_width = self.fov_width/2
        self.fov_distance = 500
        self.facing_angle = 0

        self.actual_map_width = actual_map_width
        self.actual_map_height = actual_map_height

        self.directions = [(0,1), (0,-1), (1,0), (-1,0)]
        

        

        

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
    
    def create_node_grid(self):
        grid = []
        for x in range (0, self.actual_map_width):
            new_array = []
            for y in range (0, self.actual_map_height):
                node = Node(self.game, self.game_world, x, y, self.actual_map_width, self.actual_map_height)
                new_array.append(node)
            grid.append(new_array)

    def pathfind(self, player, end, map): #end is end position
        if self.check_detection(player) == True:
            open_set = []
            closed_set = set()
            start_node = Node(None, (self.x//self.game.block_size, self.y//self.game.block_size) )
            heapq.heappush(open_set, (0, start_node))

            while len(open_set) > 0:
                (current_g_score, current_node) = heapq.heappop(open_set) 
            
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
                
                    if 0 <= neighbour_pos[0] < self.actual_map_width and 0 <= neighbour_pos[1] < self.actual_map_height and map[neighbour_pos[0]][neighbour_pos[1]] == 1 and neighbour_pos not in closed_set:
                        
                        temp_g_score = current_g_score + 1
                        f_score = temp_g_score + self.heuristic(neighbour_pos, end) 
                        neighbour_node = Node(current_node, neighbour_pos)
                        heapq.heappush(open_set, (f_score, neighbour_node)) #This adds a tuple (Total_cost,neighbour_node) to the priority queue. Since the heapq module orders elements based on the first element of each tuple, this means that the priority queue is ordered by the Total_cost (from lowest to highest)
                
                    
            return(None)                    
            


            

    
    def update(self):
        pass
        
        

        

