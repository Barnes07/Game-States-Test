import random
from map_generation.map_generator import MapGernerator
from sprites.floor import Floor
from sprites.wall import Wall


class Cellular_Automata(MapGernerator):
    def __init__(self, actual_map_height, actual_map_width, wall_density, camera_group, wall_count_variable, iterations, game):
        super().__init__(actual_map_height, actual_map_width,)


        self.game = game 
        self.block_size = self.game.block_size  
        self.wall_density = wall_density 
        self.noise_grid = []
        self.camera_group = camera_group
        self.wall_count_variable = wall_count_variable
        self.iterations = iterations

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
            new_grid = noise_grid

            for a in range (0,(self.actual_map_width)-1):
                for b in range (0,(self.actual_map_height)-1):
                    wall_count = 0
                    for x in range (a-1, a+1):
                        for y in range(b-1, b+1):
                            if x != a or y !=b:
                                if x >= 0 and x < self.actual_map_width and y >=0 and y < self.actual_map_height:
                                    if new_grid[x][y] == 0:
                                        wall_count = wall_count + 1
                                else:
                                    wall_count = wall_count + 1
                        if wall_count > self.wall_count_variable:
                            noise_grid[a][b] = 0
                        else:
                            noise_grid[a][b] = 1
        return(noise_grid)

            
    def update(self):
        if self.actual_map_height >= 0 and self.actual_map_width >= 0:
            noise_grid = self.generate_noise_grid()
            map = self.cellular_automata(noise_grid, self.iterations)
            self.fill_map(map)
           
        else:
            print("map cannot have negative dimensions")

        




