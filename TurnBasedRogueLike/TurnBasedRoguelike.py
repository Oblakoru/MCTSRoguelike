
import random
import matplotlib.pyplot as plt
import time
from TurnBasedRogueLike.Character import Character
from TurnBasedRogueLike.GameState import GameState
from TurnBasedRogueLike.MCTS import MCTS
from TurnBasedRogueLike.Node import Node


# Funkcija, ki izbere naključno potezo za Random AI iz legalnih potez
def random_turn(player, enemy):
    moves = player.get_available_moves()
    move = random.choice(moves)

    if move == 'attack':
        player.attack(enemy)
    elif move == 'super_attack':
        player.super_attack(enemy)
    elif move == 'heal':
        player.heal()
    elif move == 'guard':
        player.guard()


# Funkcija, ki izbere najboljšo potezo za MCTS agenta
def mcts_turn(player, enemy, mcts, current_turn):
    root_state = GameState(player, enemy, current_turn)
    root_node = Node(state=root_state)

    start_time = time.time()
    best_move = mcts.vrniPotezo(root_node, root_state)
    end_time = time.time()

    root_state.apply_move(best_move)

    move_time = (end_time - start_time) * 1000  # Convert to milliseconds
    return best_move, move_time


# Funkcija, ki omogoča igralcu, da izbere svojo potezo
def player_turn(player, enemy):
    print("--------------------------------------")
    print(f"{player.name} je na vrsti!")
    print(f"{player.name} - Zdravje: {player.health}, Mana: {player.mana}")
    print(f"{enemy.name} - Zdravje: {enemy.health}, Mana: {enemy.mana}")
    move = input("Izberi svojo potezo: napad(1), super napad(2), zdravljenje(3), obramba(4): ").strip()
    if move == '1':
        player.attack(enemy)
    elif move == '2':
        player.super_attack(enemy)
    elif move == '3':
        player.heal()
    elif move == '4':
        player.guard()
    else:
        print("Napačna poteza, izberi ponovno.")
        player_turn(player, enemy)

    print("--------------------------------------")


# Igralna funkcija
def game_turn(player, enemy, player_type, mcts_move_times):
    # Naredimo novo instanco MCTS
    mcts = MCTS()
    game_move_times = []

    # Preverimo, če sta oba igralca še živa - začetek vsakega "turna"
    while player.is_alive() and enemy.is_alive():
        if player_type == 'human':
            player_turn(player, enemy)
        else:
            random_turn(player, enemy)

        # Preverjamo, če je nasprotnik še živ
        if enemy.is_alive():
            best_move, move_time = mcts_turn(player, enemy, mcts, 'enemy')
            game_move_times.append(move_time)

    if player.is_alive():
        winner = 'Igralec/Random AI'
    else:
        winner = 'MCTS'

    average_game_time = sum(game_move_times) / len(game_move_times) if game_move_times else 0
    mcts_move_times.append(average_game_time)
    return winner


# Funkcija, ki zažene simulacije 100 iger proti Random AI agentu in MCTS agentu - za prikaz rezultatov na grafu
def run_simulations(num_games):
    results = {'Igralec/Random AI': 0, 'MCTS': 0}
    mcts_move_times = []

    for _ in range(num_games):
        player = Character(name="Igralec")
        enemy = Character(name="MCTS")
        winner = game_turn(player, enemy, 'random', mcts_move_times)
        results[winner] += 1

    return results, mcts_move_times


# Funkcija za prikaz rezultatov
def plot_results(results, mcts_move_times):
    # Plot win/loss results
    labels = list(results.keys())
    counts = list(results.values())

    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.bar(labels, counts, color=['blue', 'red'])
    plt.xlabel('Izid igre')
    plt.ylabel('Število zmag')
    plt.title('Naključni AI proti MCTS agentom')

    # Plot average MCTS move times for each game
    plt.subplot(1, 2, 2)
    plt.plot(range(1, len(mcts_move_times) + 1), mcts_move_times, marker='o', color='green')
    plt.xlabel('Številka igre')
    plt.ylabel('Povprečni čas poteze (ms)')
    plt.title('Povprečni čas poteze MCTS za vsako igro (100 simulacij)')

    plt.tight_layout()
    plt.show()


def main():
    print("Izberi način igranja:")
    print("1. Človek")
    print("2. Naključni AI")
    choice = input("Izberi (1 ali 2): ").strip()

    if choice == '1':
        player = Character(name="Junak")
        enemy = Character(name="Temačni Lord")
        winner = game_turn(player, enemy, 'human', [])
        print(f"{winner} je zmagovalec!")
    elif choice == '2':
        num_games = 100
        results, mcts_move_times = run_simulations(num_games)
        print(f"Rezultati po {num_games} igrah:")
        print(f"Igralec/Random AI zmaga z {results['Igralec/Random AI']}")
        print(f"Nasprotnik zmaga z: {results['MCTS']}")
        print(f"Povprečni čas poteze MCTS: {sum(mcts_move_times) / len(mcts_move_times)} ms")
        plot_results(results, mcts_move_times)
    else:
        print("Napačna izbira! Poskusi ponovno.")


if __name__ == "__main__":
    main()
