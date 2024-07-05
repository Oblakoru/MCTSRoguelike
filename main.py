import random

from MCTS import MCTS
from Node import Node
from TicTacToe import TicTacToe


def play_game():

    #Ustvarimo novo instanco igre
    game = TicTacToe()

    #Ustvarimo novo instanco MCTS
    mcts = MCTS()

    print("Choose your opponent:")
    print("1: Human")
    print("2: Random AI")
    opponent = int(input("Enter 1 or 2: "))

    #Dokler igra ni končana
    while not game.game_over():
        #Če je trenutni igralec 1 (človek)
        if game.current_player == 1:  # X - clovek
            ### Na novo
            if opponent == 1:
                move = int(input("Vnesi svojo potezo (0-8): "))
                print(f"Human (X) made move at position {move}")
            else:
                move = random.choice(game.get_legal_moves())
                print(f"Random AI (X) made move at position {move}")
            #move = int(input("Vnesi svojo potezo (0-8): "))
            game.make_move(move)
        else:  # AI (0)
            #Ustvarimo novo instanco vozlišča
            root = Node(state=game)
            #Izberemo najboljšo potezo
            move = mcts.best_move(root, game)
            print(f"MCTS AI (O) made move at position {move}")
            game.make_move(move)
        print(game.board[0:3])
        print(game.board[3:6])
        print(game.board[6:9])
        print()

    if game.is_winner(1):
        print("X wins!")
    elif game.is_winner(2):
        print("O wins!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    play_game()

