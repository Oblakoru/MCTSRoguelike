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

    plt.bar(labels, counts)
    plt.xlabel('Rezultat')
    plt.ylabel('Število zmag')
    plt.title('Rezultati iger: Random AI vs MCTS AI (100 iteracij)')
    plt.show()


if __name__ == "__main__":
    print("Izberi način igranja:")
    print("1: Človek")
    print("2: Nakjlučni AI")
    opponent = int(input("Vnesi 1 ali 2: "))

    if opponent == 2:
        num_games = 50
        results = simulate_games(num_games, opponent)
        print(f"Results after {num_games} games: {results}")
        plot_results(results)
    else:
        play_game(opponent)





#Ostanek od prejšnjega poskusa
# def simulate_games(num_games, opponent, exploration_weight):
#     results = {"X": 0, "O": 0, "D": 0}
#
#     for _ in range(num_games):
#         result = play_game(opponent, exploration_weight)
#         results[result] += 1
#
#     return results
#
# def plot_results(results, exploration_weights):
#     labels = list(results[0].keys())
#     for label in labels:
#         counts = [result[label] for result in results]
#         plt.scatter(exploration_weights, counts, label=label)
#
#     plt.xlabel('Exploration Weight')
#     plt.ylabel('Count')
#     plt.title('Results of Tic-Tac-Toe Games: Random AI vs MCTS AI with varying Exploration Weights')
#     plt.legend()
#     plt.show()
#
#
# if __name__ == "__main__":
#     print("Choose your opponent:")
#     print("1: Human")
#     print("2: Random AI")
#     opponent = int(input("Enter 1 or 2: "))
#
#     if opponent == 2:
#         num_games = 10
#         exploration_weights = [round(x * 0.2, 1) for x in range(11)]  # 0 to 2 with increment of 0.2
#         all_results = []
#
#         for weight in exploration_weights:
#             print(f"Simularanje iger s težo exploracije: {weight}")
#             results = simulate_games(num_games, opponent, weight)
#             print(f"Rezultati simulacij s težo exploracije {weight}: {results}")
#             all_results.append(results)
#
#         plot_results(all_results, exploration_weights)
#     else:
#         play_game(opponent, exploration_weight=1.4)  # Default exploration weight for human play
