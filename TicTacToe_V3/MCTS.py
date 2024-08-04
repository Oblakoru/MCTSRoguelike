from Node import Node
from TicTacToe import TicTacToe
import math
import random

class MCTS:

    def __init__(self, exploration_weight=1.4):
        # Nastavimo težo za exploracijo, 0=ni exploracije, le exploitacija
        self.exploration_weight = exploration_weight

    def best_move(self, root):
        for _ in range(10):  # Nastavimo število iteracij
            node = root

            # Iteriramo, dokler ne pridemo do vozlišča, ki
            while len(node.children) != 0:
                node = self.select(node)

            #Preverimo, če je vozlišče list drevesa
            if len(node.children) == 0:
                if node.visits == 0:
                    result = self.simulate(node)
                else:
                    if node.state.game_over():
                        break

                    self.expand(node)
                    node = random.choice(node.children)
                    result = self.simulate(node)

                self.backpropagate(node, result)

        best_child = max(root.children, key=lambda c: c.wins)
        return best_child.move

    def select(self, node):

        #Nastavimo najboljšega otroka na None in najboljši rezultat na -inf
        best_score = -float('inf')
        best_child = []

        #Gremo skozi vse otroke in izračunamo UCT vrednost
        for child in node.children:
            #Če otrok še ni bil obiskan, nastavimo rezultat na neskončno, da ga bomo izbrali
            if child.visits == 0:
                score = float('inf')
            else:
                # UCT formula za izračun vrednosti
                #Wins - vrednost zmag otroka (zmage, porazi in neodločeno)
                exploit = child.wins / child.visits
                explore = math.sqrt(math.log(node.visits) / child.visits)
                score = exploit + self.exploration_weight * explore
            if score > best_score:
                best_score = score
                best_child = [child]
            elif score == best_score:
                best_child.append(child)

        return random.choice(best_child)

    def expand(self, node):

       steviloLegalnihPotez = len(node.state.get_legal_moves())
       # Preverimo, če so vsi otroci že razširjeni
       if len(node.children) == steviloLegalnihPotez:
           return node #Vrnemo, če so vsi otroci že razširjeni

       #Gremo skozi vse možne poteze in dodamo otroka, če še ni dodan
       for move in node.state.get_legal_moves():
           if move not in [child.move for child in node.children]:
               new_state = TicTacToe()
               new_state.board = node.state.board[:]
               new_state.current_player = node.state.current_player
               new_state.make_move(move)
               child_node = Node(move=move, parent=node, state=new_state)
               node.add_child(child_node)

       return node

    # def simulate(self, node):
    #     while not node.state.game_over():
    #         move = random.choice(node.state.get_legal_moves())
    #         node.state.make_move(move)
    #     if node.state.is_winner(1):
    #         return -2
    #     elif node.state.is_winner(2):
    #         return 1
    #     else:
    #         return 0

    def simulate(self, node):
        game_copy = TicTacToe()
        game_copy.board = node.state.board[:]  # Copy the board
        game_copy.current_player = node.state.current_player  # Copy the current player

        while not game_copy.game_over():
            move = random.choice(game_copy.get_legal_moves())
            game_copy.make_move(move)

        if game_copy.is_winner(1):
            return 1  # Return 1 for a win
        elif game_copy.is_winner(2):
            return -1  # Return -1 for a loss
        else:
            return 0  # Return 0 for a draw

    def backpropagate(self, node, result):
        while node is not None:
            node.update(result)
            node = node.parent


            #
            #     self.expand(node)
            #
            #
            #
            #
            # while node.children:
            #     node = self.select(node)
            #
            # # V primeru, da še vozlišče ni bilo obiskano, nanj naredimo simulacijo
            # if node.visits == 0:
            #     result = self.simulate(node)
            #     self.backpropagate(node, result)
            #     continue #Gremo ven iz trenutne zanke
            #
            #
            # # #Se preskoči, če root nima otrok - gre direktno v razširitev
            # # # Selekcija - izbiramo dokler ne pridemo do končnega stanja igre
            # # while node.children and not game_copy.game_over():
            # #     node = self.select(node)
            # #     game_copy.make_move(node.move)
            #
            # # Razširitev
            # if not game_copy.game_over():
            #     self.expand(node, game_copy)
            #
            # # Simulacija
            # if node.children:
            #     node = random.choice(node.children)
            #     game_copy.make_move(node.move)
            # result = self.simulate(game_copy)
            #
            # # Vzratna-posodobitev
            # self.backpropagate(node, result)

        #Izberemo najboljšega otroka - neke implementacije so vzele UCT nekatere pa najbolj obiskanega otroka
        # best_child = max(root.children, key=lambda c: c.visits)
        # return best_child.move












    # def select(self, node):
    #     #Nastavimo najboljšega otroka na None in najboljši rezultat na -inf
    #     best_score = -float('inf')
    #     best_child = None
    #
    #     #Gremo skozi vse otroke in izračunamo UCT vrednost
    #     for child in node.children:
    #         #Če otrok še ni bil obiskan, nastavimo rezultat na neskončno, da ga bomo izbrali
    #         if child.visits == 0:
    #             score = float('inf')
    #         else:
    #             # UCT formula za izračun vrednosti
    #             #Wins - vrednost zmag otroka (zmage, porazi in neodločeno)
    #             exploit = child.wins / child.visits
    #             explore = math.sqrt(math.log(node.visits) / child.visits)
    #             score = exploit + self.exploration_weight * explore
    #         if score > best_score:
    #             best_score = score
    #             best_child = child
    #     return best_child
    #
    # def expand(self, node, game):
    #
    #     # Preverimo, če so vsi otroci že razširjeni
    #     if len(node.children) == len(game.get_legal_moves()):
    #         return  #Vrnemo, če so vsi otroci že razširjeni
    #
    #     #Gremo skozi vse možne poteze in dodamo otroka, če še ni dodan
    #     for move in game.get_legal_moves():
    #         if move not in [child.move for child in node.children]:
    #             new_state = TicTacToe()
    #             new_state.board = node.state.board[:]
    #             new_state.current_player = node.state.current_player
    #             new_state.make_move(move)
    #             child_node = Node(move=move, parent=node, state=new_state)
    #             node.add_child(child_node)
    #
    # #Simuliramo igro dokler ni končana ter vrnemo rezultat (nagrado)
    # def simulate(self, game):
    #     while not game.game_over():
    #         move = random.choice(game.get_legal_moves())
    #         game.make_move(move)
    #     if game.is_winner(1):
    #         return -2
    #     elif game.is_winner(2):
    #         return 1
    #     else:
    #         return 0
    #
    #
    # #Posodabljamo vozlišča, dokler ne pridemo do korena
    # def backpropagate(self, node, result):
    #     while node is not None:
    #         node.update(result)
    #
    #         # Neke implementacije, so za vsak drugi nivo, obrnile rezultat
    #         #result = -result
    #         node = node.parent
    #
    # def best_move(self, root, game):
    #     for _ in range(100):  # Nastavimo število iteracij
    #         node = root
    #         game_copy = TicTacToe()
    #         # Kopiramo trenutno stanje igre
    #         game_copy.board = game.board[:]
    #
    #         game_copy.current_player = game.current_player
    #
    #         #Se preskoči, če root nima otrok - gre direktno v razširitev
    #         # Selekcija - izbiramo dokler ne pridemo do končnega stanja igre
    #         while node.children and not game_copy.game_over():
    #             node = self.select(node)
    #             game_copy.make_move(node.move)
    #
    #         # Razširitev
    #         if not game_copy.game_over():
    #             self.expand(node, game_copy)
    #
    #         # Simulacija
    #         if node.children:
    #             node = random.choice(node.children)
    #             game_copy.make_move(node.move)
    #         result = self.simulate(game_copy)
    #
    #         # Vzratna-posodobitev
    #         self.backpropagate(node, result)
    #
    #     #Izberemo najboljšega otroka - neke implementacije so vzele UCT nekatere pa najbolj obiskanega otroka
    #     best_child = max(root.children, key=lambda c: c.visits)
    #     return best_child.move


