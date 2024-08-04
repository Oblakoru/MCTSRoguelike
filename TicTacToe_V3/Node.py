class Node:
    def __init__(self, move=None, parent=None, state=None):
        self.move = move # Poteza, ki je privedla do tega vozlišča
        self.parent = parent
        self.state = state # Stanje igre
        self.wins = 0
        self.visits = 0
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def update(self, result):
        self.visits += 1
        self.wins += result



