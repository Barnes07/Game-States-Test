import random
from map_generation.map_generator import MapGernerator


class CellularAutomata(MapGernerator):
    def __init__(self, map_height, map_width, actual_map_height, actual_map_width, iterations, wall_density, wall_count):
        super().__init__(map_height, map_width, actual_map_height, actual_map_width)
        self.noise_grid = []
        self.final_map = []
        self.iterations = iterations
        self.wall_density = wall_density
        self.wall_count = wall_count

    def GenerateNoiseGrid(self):
        for X in range(0,self.actual_map_width):
            NewArray = []
            for Y in range (0,self.actual_map_height):
                Decision = random.randint(1,100)
                if Decision <= self.wall_density:
                    NewArray.append(0) 
                else:
                    NewArray.append(1)
            self.noise_grid.append(NewArray)

    def CellularAutomata(self):
        for count in range (0, self.iterations):
            NewGrid = [row[:] for row in self.noise_grid]        #Research this line
            for a in range (0, self.actual_map_width-1):
                for b in range (1, self.actual_map_height-1):     #Starting the counts for a and b at 0 appears to create floor buffers on the left and top of the map
                    WallCount = 0
                    for x in range (a-1,a+1):
                        for y in range(b-1,b+1):
                            if x != a or y != b:
                                if 0 <= x < self.actual_map_width and 0 <= y < self.actual_map_height:
                                    if NewGrid[x][y] == 0:
                                        WallCount = WallCount + 1
                        else: 
                            WallCount = WallCount + 1
                        if WallCount > self.wall_count:
                            self.noise_grid[a][b] = 0
                        else:
                            self.noise_grid[a][b] = 1

        self.final_mapap = self.noise_grid

    def FillMap(self):
        for x in range(0,self.actual_map_height):
            for y in range(0,self.actual_map_height):
                if self.final_map[x][y] == 0:
                    #load wall class
                    WallSprite = Wall(x*BlockSize + BlockSize//2 , y*BlockSize + BlockSize//2, CameraGroup)
                    #WallGroup.add(WallSprite)
                    #The x coordinate is multiplied by Blocksize so that the blocks are not rendered ontop of eachother
                    #"BlockSize//2" is then added to each coordinate as the rectangle is rendered by the center and the left-hand edegs of the map would therefore not fit onto the screen
                    
                elif self.final_map[x][y] == 1:
                    #load floor class
                    Floor(x*BlockSize+ BlockSize//2, y*BlockSize+ BlockSize//2, CameraGroup)
                    ##Need to change this so that the ground is rendered once and covers the whole screen with the walls chnaging position over it to imporve perfomance 
    
    def FillTop(self):  #This function fills the top row with floors to prevent awkward diaganol strips. Screenshot saved in "Screenshots"
        for x in range (0, self.actual_map_width):
            self.final_map[x][0] = 1

    def FillEdges(self):                                        #Function that makes all edges except left-hand side into a wall to stop player going off map
        for x in range(0, self.actual_map_width):
            for y in range (0, self.actual_map_height):
                if y == 0:
                    self.final_map[x][y] = 0
                if x == self.actual_map_width-1 or y == self.actual_map_height-1:
                    self.final_map[x][y] = 0
                if x == 0:
                    self.final_map[x][y] = 1
       
    def Generate_CA_Map(self):
        self.GenerateNoiseGrid()
        self.CellularAutomata()
        self.FillMap()
        self.FillTop()
        self.FillEdges()
        return(self.final_map)