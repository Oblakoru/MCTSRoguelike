class Node:
    def __init__(self, move=None, parent=None, state=None):
        self.move = move
        self.parent = parent
        self.state = state

        if self.state.game_over():
            self.is_terminal = True
        else:
            self.is_terminal = False

        self.is_full_expanded = self.is_terminal

        self.wins = 0
        self.visits = 0
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def update(self, result):
        self.visits += 1
        self.wins += result



