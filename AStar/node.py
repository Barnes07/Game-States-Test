class Node():
    def __init__ (self, parent, position):
        self.parent = parent
        self.position = position

    def __lt__(self, other): #ensures heapqcan compare and order the list based on f_scores
        return(False)
        






        

        