import random
from map_generation.map_generator import MapGernerator
from sprites.floor import Floor
from sprites.wall import Wall


class Cellular_Automata(MapGernerator):
    def __init__(self, actual_map_height, actual_map_width, wall_density, wall_count_variable, iterations, camera_group, game):
        super().__init__(actual_map_height, actual_map_width)


        self.game = game 
        self.block_size = self.game.block_size  
        self.wall_density = wall_density 
        self.noise_grid = []
        self.camera_group = camera_group
        self.wall_count_variable = wall_count_variable
        self.iterations = iterations
        self.final_map = []

    def generate_noise_grid(self):
        for x in range (0, self.actual_map_width):
            new_array = []
            for y in range (0, self.actual_map_height):
                decision = random.randint(1,100)
                if decision <= self.wall_density:
                    new_array.append(0)
                else:
                    new_array.append(1)
            self.noise_grid.append(new_array)
        return(self.noise_grid)
    
    def fill_map(self, map):
        for x in range (0, self.actual_map_width):
            for y in range (0, self.actual_map_height):
                if map[x][y] == 0: 
                    wall = Wall(x*self.block_size, y*self.block_size, self.camera_group, self.game)
                

                elif map[x][y] == 1:
                    floor = Floor(x*self.block_size, y*self.block_size, self.camera_group, self.game)
                    
    def cellular_automata(self, noise_grid, iterations):
        for count in range (0, iterations):
            new_grid = noise_grid.copy()
            for a in range (0,(self.actual_map_width)):
                for b in range (0,(self.actual_map_height)):
                    wall_count = 0
                    for x in range (a-1, a+2):
                        for y in range(b-1, b+2):
                            if x != a or y !=b:
                                if 0 <= x < self.actual_map_width and 0 <= y < self.actual_map_height:
                                    if new_grid[x][y] == 0:
                                        wall_count = wall_count + 1
                                else:
                                    wall_count = wall_count + 1
                    if wall_count > self.wall_count_variable:
                        noise_grid[a][b] = 0
                    else:
                        noise_grid[a][b] = 1
        return(noise_grid)

    def fill_edges(self, map):
        for x in range(0, self.actual_map_width):
            for y in range(0, self.actual_map_height):
                if x == 0 or x == self.actual_map_width-1:
                    map[x][y] = 0
                if y == 0 or y == self.actual_map_height-1:
                    map[x][y] = 0
        return(map)
    
    def check_map_validity(self):
        check = True
        if self.actual_map_height < 0 or self.actual_map_width < 0:
            check = False
            print("map cannot have negative dimensions")
        if self.wall_density < 0 or self.wall_density > 100:
            check = False
            print("the wall density for map generation is not in the expected range") 
        if self.iterations < 0:
            check = False
            print("iterations must be a positive value")
        if self.wall_count_variable < 0:
            check = False
            print("wall_count_variable must be a positive value")
        return(check)
    
    def find_player_starting_coordinates(self, map):
        for a in range (0, self.actual_map_width):
            for b in range (0, self.actual_map_height):
                wall_count = 0
                for x in range (a-1, a+2):
                    for y in range(b-1, b+2):
                        if 0 <= x < self.actual_map_width and 0 <= y < self.actual_map_height:
                            if map[x][y] == 0:
                                wall_count = wall_count + 1
                        else:
                            wall_count = wall_count + 1
                if wall_count == 0:
                    #set player starting coordinates to those stored in a and b
                    a = a * self.game.block_size
                    b = b * self.game.block_size
                    return(a, b)




    def update(self):
        if self.check_map_validity() == True:
            noise_grid = self.generate_noise_grid()
            cellular_automata_map = self.cellular_automata(noise_grid, self.iterations)
            self.final_map = self.fill_edges(cellular_automata_map)
            self.fill_map(self.final_map)
            
