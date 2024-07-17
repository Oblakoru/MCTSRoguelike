class Node:

    def __init__(self, move=None, parent=None, state=None):
        self.move = move
        self.parent = parent
        self.state = state
        self.wins = 0
        self.visits = 0
        self.children = []

    #Dodamo otroka
    def add_child(self, child_node):
        self.children.append(child_node)

    #Posodobimo število obiskov in rezultat izidov
    def update(self, result):
        self.visits += 1
        self.wins += result
