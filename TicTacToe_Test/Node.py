class Node:
    def __init__(self,  parent=None, board=None):

        self.parent = parent
        self.state = board

        ###########
        if self.state.game_over:
            self.isTerminal = True
        else:
            self.isTerminal = False

        self.isFullyExpanded = self.isTerminal
        ###########

        self.score = 0
        self.visits = 0
        self.children = []


    def add_child(self, child_node):
        self.children.append(child_node)

    def update(self, result):
        self.visits += 1
        self.score += result



