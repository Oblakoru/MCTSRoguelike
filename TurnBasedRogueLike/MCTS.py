import math
import random
from TurnBasedRogueLike.Node import Node


class MCTS:

    #Nastavimo težo raziskovanja
    def __init__(self, exploration_weight=1.4):
        self.exploration_weight = exploration_weight

    def select(self, node):
        best_score = -float('inf')
        best_child = []

        for child in node.children:
            if child.visits == 0:
                score = float('inf')
            else:
                exploit = child.wins / child.visits
                explore = math.sqrt(math.log(node.visits) / child.visits)
                score = exploit + self.exploration_weight * explore
            if score > best_score:
                best_score = score
                best_child = [child]
            elif score == best_score:
                best_child.append(child)
        return random.choice(best_child)

    def expand(self, node, game):
        if len(node.children) == len(game.get_legal_moves()):
            return

        for move in game.get_legal_moves():
            if move not in [child.move for child in node.children]:
                new_state = game.copy()
                new_state.apply_move(move)
                child_node = Node(move=move, parent=node, state=new_state)
                node.add_child(child_node)

    def simulate(self, game):
        while not game.is_game_over():
            move = random.choice(game.get_legal_moves())
            game.apply_move(move)
        return game.get_result()

    def backpropagate(self, node, result):
        while node is not None:
            node.update(result)
            node = node.parent

    def vrniPotezo(self, root, game):
        for _ in range(100):

            #Izberemo root vozlišče - za vsako iteracijo gremo od root navzdol
            node = root

            #Naredimo kopijo igre, da ne spremenimo originalne igre
            game_copy = game.copy()

            #Izbiramo vozlišča, dokler ne pridemo do koncai igre ali pa list drevesa
            while node.children and not game_copy.is_game_over():

                node = self.select(node)
                game_copy.apply_move(node.move)

            #Se v kodi zgodi le, če še ni vozlišče dokončno razširjeno - se zgodi le 1x na vozlišče
            if not game_copy.is_game_over():
                self.expand(node, game_copy)

            ### Še treba preverit
            if node.children:
                node = random.choice(node.children)
                game_copy.apply_move(node.move)
            result = self.simulate(game_copy)

            self.backpropagate(node, result)

        best_child = max(root.children, key=lambda c: c.visits)
        return best_child.move
