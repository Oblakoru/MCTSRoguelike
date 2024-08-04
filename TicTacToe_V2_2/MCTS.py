from Node import Node
from TicTacToe import TicTacToe
import math
import random

class MCTS:

    def __init__(self, exploration_weight=1.4):
        # Nastavimo težo za exploracijo, 0=ni exploracije, le exploitacija
        self.exploration_weight = exploration_weight

    def select(self, node):

        #Se preskoči, če root nima otrok - gre direktno v razširitev
        # Se zgodi v best_move funkciji, tuki ni potrebno
        # while not node.is_terminal:
        #     if node.is_fully_expanded:
        #         node = self.get_best_move(node)
        #     else:
        #         return self.expand(node)

        # return node


        # Nastavimo najboljšega otroka na None in najboljši rezultat na -inf
        best_score = -float('inf')
        best_child = []

        # Gremo skozi vse otroke in izračunamo UCT vrednost
        for child in node.children:
            # Če otrok še ni bil obiskan, nastavimo rezultat na neskončno, da ga bomo izbrali
            if child.visits == 0:
                score = float('inf')
            else:
                # UCT formula za izračun vrednosti
                # Wins - vrednost zmag otroka (zmage, porazi in neodločeno)
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

        # Preverimo, če so vsi otroci že razširjeni
        if len(node.children) == len(node.state.get_legal_moves()):
            node.is_fully_expanded = True

        #Gremo skozi vse možne poteze in dodamo otroka, če še ni dodan
        for move in node.state.get_legal_moves():

            # Preverimo, če je poteza že bila narejena
            # Če ni, naredimo novo stanje igre in dodamo otroka
            if move not in [child.move for child in node.children]:
                new_state = TicTacToe()
                new_state.board = node.state.board[:]
                new_state.current_player = node.state.current_player
                new_state.make_move(move)
                child_node = Node(move=move, parent=node, state=new_state)
                node.add_child(child_node)



    #Simuliramo igro dokler ni končana ter vrnemo rezultat (nagrado)
    def simulate(self, game):
        while not game.game_over():
            move = random.choice(game.get_legal_moves())
            game.make_move(move)

        if game.is_winner(1):
            return -1
        elif game.is_winner(2):
            return 1
        else:
            return 0


    #Posodabljamo vozlišča, dokler ne pridemo do korena
    def backpropagate(self, node, result):
        while node is not None:
            node.update(result)
            # Neke implementacije, so za vsak drugi nivo, obrnile rezultat
            #result = -result
            node = node.parent

    def best_move(self, root):
        for _ in range(100):  # Nastavimo število iteracij

            #Izberemo začečno vozlišče
            node = root

            #Kopiramo trenutno stanje igre, da ne spreminjamo originalnega stanja
            game_copy = TicTacToe()
            game_copy.board = root.state.board[:]
            game_copy.current_player = root.state.current_player

            #Se preskoči, če root nima otrok - gre direktno v razširitev
            # Selekcija - izbiramo dokler ne pridemo do končnega stanja igre

            while node.children and not game_copy.game_over():
                node = self.select(node)
                game_copy.make_move(node.move)

            # Razširitev
            if not game_copy.game_over():
                self.expand(node)

            # Simulacija
            result = self.simulate(game_copy)

            # if node.children:
            #     node = random.choice(node.children)
            #     game_copy.make_move(node.move)
            # result = self.simulate(game_copy)

            # Vzratna-posodobitev
            self.backpropagate(node, result)

        #Izberemo najboljšega otroka - neke implementacije so vzele UCT nekatere pa najbolj obiskanega otroka
        best_child = max(root.children, key=lambda c: c.wins)
        return best_child.move


