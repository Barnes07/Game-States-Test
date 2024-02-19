class Node():
    def __init__ (self, parent, position):
        self.parent = parent
        self.position = position
        self.f_score = float('inf')  # Default to infinity

    def __lt__(self, other):
        return self.f_score < other.f_score
        






        

        