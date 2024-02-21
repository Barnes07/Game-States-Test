class Node():
    def __init__ (self, parent, position):
        self.parent = parent
        self.position = position

        

    def __lt__(self, other): #overwrites in-built (<) operator so that heapq correctkly orders nodes by f_score
        return(False)
        






        

        