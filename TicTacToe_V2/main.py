import random
import matplotlib.pyplot as plt
from MCTS import MCTS
from Node import Node
from TicTacToe import TicTacToe


def play_game(opponent):

    #Ustvarimo novo instanco igre
    game = TicTacToe()

    #Ustvarimo novo instanco MCTS
    mcts = MCTS()

    #Ponavljamo, dokler igra ni končana
    while not game.game_over():
        #Če je trenutni igralec X
        if game.current_player == 1:
            #Se odločimo ali bo igral človek ali računalnik (Random AI)
            if opponent == 1:
                possible_moves = game.get_legal_moves()
                move = int(input("Vnesi svojo potezo (0-8): "))
                while move not in possible_moves:
                    move = int(input("Neveljavna poteza. Vnesi svojo potezo (0-8):"))
            else:
                possible_moves = game.get_legal_moves()
                move = random.choice(possible_moves)
                print(f"Random AI je naredilo potezo na: {move}")

            #Naredimo potezo
            game.make_move(move)
        else:  # MCTS AI (0)
            #Ustvarimo novo instanco vozlišča, podamo trenutno stanje igre
            root = Node(state=game)
            #Izberemo najboljšo potezo
            move = mcts.best_move(root, game)
            print(f"MCTS AI (O) je naredil potezo na: {move}")
            game.make_move(move)
        print(game.board[0:3])
        print(game.board[3:6])
        print(game.board[6:9])
        print()

    if game.is_winner(1):
        print("Zmaga X!")
        return "X"
    elif game.is_winner(2):
        print("Zmaga O!")
        return "O"
    else:
        print("Neodločeno!")
        return "D"


# simuliranje iger za prikaz rezultatov
def simulate_games(num_games, opponent):
    results = {"X": 0, "O": 0, "D": 0}

    for _ in range(num_games):
        result = play_game(opponent)
        results[result] += 1

    return results

def plot_results(results):
    labels = results.keys()
    counts = results.values()

    # plt.bar(labels, counts)
    # plt.xlabel('Rezultat')
    # plt.ylabel('Število zmag')
    # plt.title('Rezultati iger: Random AI vs MCTS AI (100 iteracij)')
    #
    # plt.legend(['X = zmaga', ], loc='upper right')
    # plt.legend(['O = poraz', ], loc='upper right')
    # plt.legend(['D = neodločen'], loc='upper right')
    # plt.show()

    # Define the colors for each bar
    colors = ['blue', 'red', 'green']

    # Plot the bars with their respective colors
    bars = plt.bar(labels, counts, color=colors)
    plt.xlabel('Rezultat')
    plt.ylabel('Število zmag')
    plt.title('Rezultati iger: Random AI vs MCTS AI (100 iteracij)')

    # Create a custom legend
    plt.legend(bars, ['X = zmaga', 'O = poraz', 'D = neodločen'], loc='upper right')

    plt.show()


if __name__ == "__main__":
    print("Izberi način igranja:")
    print("1: Človek")
    print("2: Naključni AI")
    opponent = int(input("Vnesi 1 ali 2: "))

    if opponent == 2:
        num_games = 100
        results = simulate_games(num_games, opponent)
        print(f"Rezultati po {num_games} igrah: {results}")
        plot_results(results)
    else:
        play_game(opponent)


