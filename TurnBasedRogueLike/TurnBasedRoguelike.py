import random
import math
import matplotlib.pyplot as plt
from TurnBasedRogueLike.Character import Character
from TurnBasedRogueLike.GameState import GameState
from TurnBasedRogueLike.MCTS import MCTS
from TurnBasedRogueLike.Node import Node


#Funkcija, ki izbere naključno potezo za Random AI iz legalnih potez
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

#Funkcija, ki izbere najboljšo potezo za MCTS agenta
def mcts_turn(player, enemy, mcts, current_turn):
    root_state = GameState(player, enemy, current_turn)
    root_node = Node(state=root_state)
    best_move = mcts.best_move(root_node, root_state)
    root_state.apply_move(best_move)
    return best_move


#Funkcija, ki omogoča igralcu, da izbere svojo potezo
def player_turn(player, enemy):
    print(f"{player.name}'s turn!")
    print(f"{player.name} - Health: {player.health}, Mana: {player.mana}")
    print(f"{enemy.name} - Health: {enemy.health}, Mana: {enemy.mana}")
    move = input("Choose your move: attack(1), super_attack(2), heal(3), guard(4): ").strip()
    if move == '1':
        player.attack(enemy)
    elif move == '2':
        player.super_attack(enemy)
    elif move == '3':
        player.heal()
    elif move == '4':
        player.guard()
    else:
        print("Invalid move! Try again.")
        player_turn(player, enemy)


#Igralna funkcija
def game_turn(player, enemy, player_type):
    #Nareidmo novo instanco MCTS
    mcts = MCTS()

    #Preverimo, če sta oba igralca še živa - začetek vsakega "turna"
    while player.is_alive() and enemy.is_alive():
        if player_type == 'human':
            player_turn(player, enemy)
        else:
            random_turn(player, enemy)

        # Preverjamo, če je nasprotnik še živ
        if enemy.is_alive():
            mcts_turn(player, enemy, mcts, 'enemy')

    if player.is_alive():
        return 'Igralec/Random AI'
    else:
        return 'MCTS'



#Funkcija, ki zažene simulacije 100 iger proti Random AI agentu in MCTS agentu
def run_simulations(num_games):
    results = {'Igralec/Random AI': 0, 'MCTS': 0}

    for _ in range(num_games):
        player = Character(name="Igralec")
        enemy = Character(name="MCTS")
        winner = game_turn(player, enemy, 'random')
        results[winner] += 1

    return results


#Funkcija za prikaz rezultatov
def plot_results(results):
    labels = list(results.keys())
    counts = list(results.values())

    plt.bar(labels, counts, color=['blue', 'red'])
    plt.xlabel('Izid igre')
    plt.ylabel('Število zmag')
    plt.title('Naključni AI proti MCTS agentom')
    plt.show()


def main():
    print("Izberi način igranja:")
    print("1. Človek")
    print("2. Naključni AI")
    choice = input("Izberi (1 ali 2): ").strip()

    if choice == '1':
        player = Character(name="Player")
        enemy = Character(name="Enemy")
        winner = game_turn(player, enemy, 'human')
        print(f"{winner} je zmagovalec!")
    elif choice == '2':
        num_games = 100
        results = run_simulations(num_games)
        print(f"Rezultati po {num_games} igrah:")
        print(f"Igralec/Random AI zmaga z {results['Igralec/Random AI']}")
        print(f"Nasprotnik zmaga z: {results['MCTS']}")
        plot_results(results)
    else:
        print("Napačna izbira! Poskusi ponovno.")


if __name__ == "__main__":
    main()
