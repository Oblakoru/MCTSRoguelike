from Node import Node
from TicTacToe import TicTacToe
import math
import random

class MCTS:

    def __init__(self, exploration_weight=1.4):
        # Nastavimo težo za exploracijo, 0=ni exploracije, le exploitacija
        self.exploration_weight = exploration_weight

    def select(self, node):
        best_score = -float('inf')
        best_child = None
        for child in node.children:
            if child.visits == 0:
                score = float('inf')
            else:
                # UCT formula
                exploit = child.wins / child.visits
                explore = math.sqrt(math.log(node.visits) / child.visits)
                score = exploit + self.exploration_weight * explore
            if score > best_score:
                best_score = score
                best_child = child
        return best_child

    def expand(self, node, game):

        # Preverimo, če so vsi otroci že razširjeni
        if len(node.children) == len(game.get_legal_moves()):
            return  #Vrnemo, če so vsi otroci že razširjeni

        #Gremo skozi vse možne poteze in dodamo otroka, če še ni dodan
        for move in game.get_legal_moves():
            if move not in [child.move for child in node.children]:
                new_state = TicTacToe()
                new_state.board = node.state.board[:]
                new_state.current_player = node.state.current_player
                new_state.make_move(move)
                child_node = Node(move=move, parent=node, state=new_state)
                node.add_child(child_node)
                #break ### Dodamo samo enega otroka

        # for move in game.get_legal_moves():
        #     new_state = TicTacToe()
        #     new_state.board = node.state.board[:]
        #     new_state.current_player = node.state.current_player
        #     new_state.make_move(move)
        #     child_node = Node(move=move, parent=node, state=new_state)
        #     node.add_child(child_node)
    def simulate(self, game):
        while not game.game_over():
            move = random.choice(game.get_legal_moves())
            game.make_move(move)
        if game.is_winner(1):
            return 1
        elif game.is_winner(2):
            return -1
        else:
            return 0

    def backpropagate(self, node, result):
        while node is not None:
            node.update(result)
            result = -result
            node = node.parent

    def best_move(self, root, game):
        for _ in range(2000):  # Nastavimo število iteracij
            node = root
            game_copy = TicTacToe()
            game_copy.board = game.board[:]
            game_copy.current_player = game.current_player

            # Selekcija
            while node.children and not game_copy.game_over():
                node = self.select(node)
                game_copy.make_move(node.move)

            # Razširitev
            if not game_copy.game_over():
                self.expand(node, game_copy)

            # Simulacija
            if node.children:
                node = random.choice(node.children)
                game_copy.make_move(node.move)
            result = self.simulate(game_copy)

            # PovratnaPropagacija
            self.backpropagate(node, result)

        best_child = max(root.children, key=lambda c: c.visits)
        return best_child.move


