

class State():
    def __init__(self, game):
        self.game = game 
        self.previous_state = None #Points to the state below the curent state in the states_stack

    def update(self, delta_time, actions):
        pass #Polymorphism will chnage these functions so that they perform differnt operations for each state
    def render (self, surface):
        pass

    def enter_state(self):
        if len(self.game. states_stack) > 1:
            self.previous_state = self.game.states_stack[len(self.game.states_stack)-1]
        self.game.states_stack.append(self)

    def exit_state(self):
        self.game.states_stack.pop()



