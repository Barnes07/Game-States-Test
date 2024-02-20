class Node():
    def __init__ (self, parent, position):
        self.parent = parent
        self.position = position



    def __lt__(self, other): #ensures heapq can compare and order nodes with the same f_score
        return(False)
        






        

        