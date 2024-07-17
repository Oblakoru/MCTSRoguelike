import random
import math
import matplotlib.pyplot as plt

class Character:
    SUPER_ATTACK_MANA_COST = 20
    SUPER_ATTACK_MULTIPLIER = 2
    HEAL_MANA_COST = 10
    HEAL_AMOUNT = 20
    GUARD_DAMAGE_REDUCTION = 0.75

    def __init__(self, name, health=100, mana=50, base_damage=10, silent=False):
        self.name = name
        self.health = health
        self.max_health = health
        self.mana = mana
        self.base_damage = base_damage
        self.silent = silent
        self.guarded = False

    def is_alive(self):
        return self.health > 0

    def attack(self, other):
        damage = self.base_damage
        other.take_damage(damage)
        if not self.silent:
            print(f"{self.name} napade {other.name} za {damage} škode")

    def super_attack(self, other):
        if self.mana >= self.SUPER_ATTACK_MANA_COST:
            damage = self.base_damage * self.SUPER_ATTACK_MULTIPLIER
            other.take_damage(damage)
            self.mana -= self.SUPER_ATTACK_MANA_COST
            if not self.silent:
                print(f"{self.name} uporabi močan napad {other.name} za {damage} škode.")
        else:
            if not self.silent:
                print(f"{self.name} nima dovolj mane za močan napad.")

    def heal(self):
        if self.mana >= self.HEAL_MANA_COST:
            heal_amount = min(self.HEAL_AMOUNT, self.max_health - self.health)
            self.health += heal_amount
            self.mana -= self.HEAL_MANA_COST
            if not self.silent:
                print(f"{self.name} se pozdravi za {heal_amount}.")
        else:
            if not self.silent:
                print(f"{self.name} nima dovolj mane za zdravljenje.")

    def guard(self):
        self.guarded = True
        if not self.silent:
            print(f"{self.name} se zaščiti!")



    def take_damage(self, damage):
        if self.guarded:
            damage = int(damage * self.GUARD_DAMAGE_REDUCTION)
            self.guarded = False
            if not self.silent:
                print(f"{self.name} se je ubranil napada, narejeno le {damage} škode.")
        else:
            if not self.silent:
                print(f"{self.name} napade za {damage} škode.")

        self.health -= damage
        self.health = max(self.health, 0)

        if self.health == 0:
            if not self.silent:
                print(f"{self.name} je bil premagan!")

class GameState:
    def __init__(self, player, enemy, current_turn='player'):
        self.player = player
        self.enemy = enemy
        self.current_turn = current_turn

    #def get_legal_moves(self):
       # return ['attack', 'super_attack', 'heal', 'guard']

    def get_legal_moves(self):
        moves = ['attack', 'guard']

        if self.current_turn == 'player':
            if self.player.mana >= 20:
                moves.append('super_attack')
            if self.player.mana < 10:
                moves.append('heal')
        elif self.current_turn == 'enemy':
            if self.enemy.mana >= 20:
                moves.append('super_attack')
            if self.enemy.mana < 10:
                moves.append('heal')

        return moves


    def apply_move(self, move):
        if self.current_turn == 'player':
            if move == 'attack':
                self.player.attack(self.enemy)
            elif move == 'super_attack':
                self.player.super_attack(self.enemy)
            elif move == 'heal':
                self.player.heal()
            elif move == 'guard':
                self.player.guard()
            self.current_turn = 'enemy'
        else:
            if move == 'attack':
                self.enemy.attack(self.player)
            elif move == 'super_attack':
                self.enemy.super_attack(self.player)
            elif move == 'heal':
                self.enemy.heal()
            elif move == 'guard':
                self.enemy.guard()
            self.current_turn = 'player'


    def is_game_over(self):
        return not (self.player.is_alive() and self.enemy.is_alive())

    def get_result(self):
        if self.player.is_alive():
            return 1
        elif self.enemy.is_alive():
            return -1
        return 0

    def copy(self):
        return GameState(
            Character(self.player.name, self.player.health, self.player.mana, self.player.base_damage, silent=True),
            Character(self.enemy.name, self.enemy.health, self.enemy.mana, self.enemy.base_damage, silent=True),
            self.current_turn
        )

class Node:
    def __init__(self, move=None, parent=None, state=None):
        self.move = move
        self.parent = parent
        self.state = state
        self.wins = 0
        self.visits = 0
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def update(self, result):
        self.visits += 1
        self.wins += result

class MCTS:
    def __init__(self, exploration_weight=1.4):
        self.exploration_weight = exploration_weight

    def select(self, node):
        best_score = -float('inf')
        best_child = None

        for child in node.children:
            if child.visits == 0:
                score = float('inf')
            else:
                exploit = child.wins / child.visits
                explore = math.sqrt(math.log(node.visits) / child.visits)
                score = exploit + self.exploration_weight * explore
            if score > best_score:
                best_score = score
                best_child = child
        return best_child

    def expand(self, node, game):
        if len(node.children) == len(game.get_legal_moves()):
            return

        for move in game.get_legal_moves():
            if move not in [child.move for child in node.children]:
                new_state = game.copy()
                new_state.apply_move(move)
                child_node = Node(move=move, parent=node, state=new_state)
                node.add_child(child_node)
                break

    def simulate(self, game):
        while not game.is_game_over():
            move = random.choice(game.get_legal_moves())
            game.apply_move(move)
        return game.get_result()

    def backpropagate(self, node, result):
        while node is not None:
            node.update(result)
            node = node.parent

    def best_move(self, root, game):
        for _ in range(200):
            node = root
            game_copy = game.copy()

            while node.children and not game_copy.is_game_over():
                node = self.select(node)
                game_copy.apply_move(node.move)

            if not game_copy.is_game_over():
                self.expand(node, game_copy)

            if node.children:
                node = random.choice(node.children)
                game_copy.apply_move(node.move)
            result = self.simulate(game_copy)
            self.backpropagate(node, result)

        best_child = max(root.children, key=lambda c: c.visits)
        return best_child.move

def random_turn(player, enemy):
    move = random.choice(['attack', 'super_attack', 'heal', 'guard'])
    if move == 'attack':
        player.attack(enemy)
    elif move == 'super_attack':
        player.super_attack(enemy)
    elif move == 'heal':
        player.heal()
    elif move == 'guard':
        player.guard()

def mcts_turn(player, enemy, mcts, current_turn):
    root_state = GameState(player, enemy, current_turn)
    root_node = Node(state=root_state)
    best_move = mcts.best_move(root_node, root_state)
    root_state.apply_move(best_move)
    return best_move

def game_turn(player, enemy, player_type):
    mcts = MCTS()
    while player.is_alive() and enemy.is_alive():
        if player.is_alive() and enemy.is_alive():
            if player_type == 'human':
                player_turn(player, enemy)
            else:
                random_turn(player, enemy)
        if player.is_alive() and enemy.is_alive():
            mcts_turn(player, enemy, mcts, 'enemy')

    if player.is_alive():
        return 'Nakljucni'
    else:
        return 'MCTS'

def player_turn(player, enemy):
    print(f"{player.name}'s turn!")
    print(f"{player.name} - Health: {player.health}, Mana: {player.mana}")
    print(f"{enemy.name} - Health: {enemy.health}, Mana: {enemy.mana}")
    move = input("Choose your move: attack, super_attack, heal, guard: ").strip()
    if move == 'attack':
        player.attack(enemy)
    elif move == 'super_attack':
        player.super_attack(enemy)
    elif move == 'heal':
        player.heal()
    elif move == 'guard':
        player.guard()
    else:
        print("Invalid move! Try again.")
        player_turn(player, enemy)

def run_simulations(num_games):
    results = {'Nakljucni': 0, 'MCTS': 0}

    for _ in range(num_games):
        player = Character(name="Nakljucni")
        enemy = Character(name="MCTS")
        winner = game_turn(player, enemy, 'random')
        results[winner] += 1

    return results

def plot_results(results):
    labels = list(results.keys())
    counts = list(results.values())

    plt.bar(labels, counts, color=['blue', 'red'])
    plt.xlabel('Izid igre')
    plt.ylabel('Število zmag')
    plt.title('Naključni AI proti MCTS agentom')
    plt.show()

def main():
    print("Choose player type:")
    print("1. Human")
    print("2. Random AI")
    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == '1':
        player = Character(name="Player")
        enemy = Character(name="Enemy")
        winner = game_turn(player, enemy, 'human')
        print(f"{winner} wins!")
    elif choice == '2':
        num_games = 100
        results = run_simulations(num_games)
        print(f"Results after {num_games} games:")
        print(f"Player wins: {results['Nakljucni']}")
        print(f"Enemy wins: {results['MCTS']}")
        plot_results(results)
    else:
        print("Invalid choice! Please enter 1 or 2.")

if __name__ == "__main__":
    main()
