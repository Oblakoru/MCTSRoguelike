class Character:
    def __init__(self, name, health=100, mana=50, silent=False):
        self.name = name
        self.health = health
        self.mana = mana
        self.silent = silent

    def is_alive(self):
        return self.health > 0

    def attack(self, other):
        damage = 10
        other.health -= damage
        if not self.silent:
            print(f"{self.name} attacks {other.name} for {damage} damage.")

    def super_attack(self, other):
        if self.mana >= 20:
            damage = 30
            other.health -= damage
            self.mana -= 20
            if not self.silent:
                print(f"{self.name} uses a super attack on {other.name} for {damage} damage.")
        else:
            if not self.silent:
                print(f"{self.name} does not have enough mana for a super attack.")

    def heal(self):
        if self.mana >= 10:
            heal_amount = 20
            self.health += heal_amount
            self.mana -= 10
            if not self.silent:
                print(f"{self.name} heals for {heal_amount}.")
        else:
            if not self.silent:
                print(f"{self.name} does not have enough mana to heal.")


class Game:
    def __init__(self):
        self.player = Character(name="Player")
        self.enemy = Character(name="Enemy")

    def is_over(self):
        return not self.player.is_alive() or not self.enemy.is_alive()

    def display(self):
        print(f"Player - Health: {self.player.health}, Mana: {self.player.mana}")
        print(f"Enemy - Health: {self.enemy.health}, Mana: {self.enemy.mana}")
        print()

    def apply_move(self, state, move, silent=False):
        player, enemy = state
        new_player = Character(player.name, player.health, player.mana, silent)
        new_enemy = Character(enemy.name, enemy.health, enemy.mana, silent)

        if move == "attack":
            new_enemy.attack(new_player)
        elif move == "super_attack":
            new_enemy.super_attack(new_player)
        elif move == "heal":
            new_enemy.heal()

        return (new_player, new_enemy)

    # def get_possible_moves(self, state):
    #     return ["attack", "super_attack", "heal"]

    def get_possible_moves(self, state):
        player, enemy = state
        possible_moves = ["attack"]
        if player.mana >= 20:
            possible_moves.append("super_attack")
        if player.mana >= 10:
            possible_moves.append("heal")
        return possible_moves

    def is_terminal(self, state):
        player, enemy = state
        return not player.is_alive() or not enemy.is_alive()

    def get_winner(self, state):
        player, enemy = state
        if player.is_alive() and not enemy.is_alive():
            return 1
        elif enemy.is_alive() and not player.is_alive():
            return -1
        else:
            return 0

    def player_turn(self):
        print("Player's turn:")
        print("1: Attack")
        print("2: Super Attack")
        print("3: Heal")
        move = int(input("Choose your move: "))
        if move == 1:
            self.player.attack(self.enemy)
        elif move == 2:
            self.player.super_attack(self.enemy)
        elif move == 3:
            self.player.heal()
        else:
            print("Invalid move. Try again.")
            self.player_turn()

    def copy_state(self):
        new_player = Character(name=self.player.name, health=self.player.health, mana=self.player.mana, silent=True)
        new_enemy = Character(name=self.enemy.name, health=self.enemy.health, mana=self.enemy.mana, silent=True)
        return (new_player, new_enemy)

    def enemy_turn(self, mcts):
        print("Enemy's turn:")
        root = Node(state=(self.enemy, self.player))
        move = mcts.best_move(
            root,
            self.get_possible_moves,
            lambda state, move: self.apply_move(state, move, silent=True),  # Silent mode for simulations
            self.get_possible_moves,
            lambda state, move: self.apply_move(state, move, silent=True),  # Silent mode for simulations
            self.is_terminal,
            self.get_winner,
        )
        if move == "attack":
            self.enemy.attack(self.player)
        elif move == "super_attack":
            self.enemy.super_attack(self.player)
        elif move == "heal":
            self.enemy.heal()
        print()

    def play(self):
        mcts = MCTS()
        while not self.is_over():
            self.display()
            self.player_turn()
            if not self.is_over():
                self.enemy_turn(mcts)
        self.display()
        if self.player.is_alive():
            print("Player wins!")
        else:
            print("Enemy wins!")

import math
import random

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
        best_score = float('-inf')
        best_child = None

        for child in node.children:
            if child.visits == 0:
                score = float('inf')  # Unexplored child gets high score for initial exploration
            else:
                exploit = child.wins / child.visits
                explore = math.sqrt(math.log(node.visits) / child.visits)
                score = exploit + self.exploration_weight * explore
            if score > best_score:
                best_score = score
                best_child = child
        return best_child

    def expand(self, node, game):
        if len(node.children) == len(game.get_possible_moves(node.state)):
            return  # All possible moves already explored

        for move in game.get_possible_moves(node.state):
            if move not in [child.move for child in node.children]:
                new_state = game.copy_state(node.state)  # Create a copy to avoid modifying original state
                child_node = Node(move=move, parent=node, state=new_state)
                node.add_child(child_node)

    def simulate(self, game):
        while not game.is_over():
            move = random.choice(game.get_possible_moves(game.state))
            game.apply_move(move, silent=True)  # Simulate move silently

        # Reward function can be adjusted based on your game's goals
        # Here, we reward remaining health for both player and enemy (normalized)
        player_reward = (game.player.health / 100)
        enemy_reward = (game.enemy.health / 100)
        return player_reward - enemy_reward  # Positive reward for player advantage

    def backpropagate(self, node, reward):
        while node is not None:
            node.update(reward)
            node = node.parent

    def best_move(self, root, game):
        for _ in range(200):  # Number of simulations (iterations)
            node = root
            game_copy = game.copy_state(root.state)  # Create copy for simulation

            # Selection
            while node.children and not game_copy.is_over():
                node = self.select(node)
                game_copy.apply_move(node.move, silent=True)

            # Expansion
            if not game_copy.is_over():
                self.expand(node, game_copy)

            # Simulation
            if node.children:
                node = random.choice(node.children)
                game_copy.apply_move(node.move, silent=True)
            result = self.simulate(game_copy)

            # Backpropagation
            self.backpropagate(node, result)

        best_child = max(root.children, key=lambda c: c.visits)
        return best_child.move


# class MCTS:
#     def __init__(self, exploration_weight=1.4):
#         self.exploration_weight = exploration_weight
#
#     def select(self, node):
#         best_score = -float('inf')
#         best_child = None
#         for child in node.children:
#             if child.visits == 0:
#                 score = float('inf')  # Choose unvisited nodes first
#             else:
#                 exploit = child.wins / child.visits
#                 explore = math.sqrt(math.log(node.visits) / child.visits)
#                 score = exploit + self.exploration_weight * explore
#             if score > best_score:
#                 best_score = score
#                 best_child = child
#         return best_child
#
#     def expand(self, node, possible_moves, get_new_state):
#         for move in possible_moves:
#             new_state = get_new_state(node.state, move)
#             child_node = Node(move=move, parent=node, state=new_state)
#             node.add_child(child_node)
#
#     def simulate(self, state, get_possible_moves, apply_move, is_terminal, get_winner):
#         while not is_terminal(state):
#             move = random.choice(get_possible_moves(state))
#             state = apply_move(state, move)
#         return get_winner(state)
#
#     def backpropagate(self, node, result):
#         while node is not None:
#             node.update(result)
#             result = -result  # switch result for the opponent
#             node = node.parent
#
#     def best_move(self, root, possible_moves, get_new_state, get_possible_moves, apply_move, is_terminal, get_winner, iterations=20000):
#         for _ in range(iterations):
#             node = root
#             state = node.state
#
#             # Selection
#             while node.children and not is_terminal(state):
#                 node = self.select(node)
#                 state = apply_move(state, node.move)
#
#             # Expansion
#             if not is_terminal(state):
#                 self.expand(node, get_possible_moves(state), get_new_state)
#
#             # Simulation
#             if node.children:
#                 node = random.choice(node.children)
#                 state = apply_move(state, node.move)
#             result = self.simulate(state, get_possible_moves, apply_move, is_terminal, get_winner)
#
#             # Backpropagation
#             self.backpropagate(node, result)
#
#         best_child = max(root.children, key=lambda c: c.visits)
#         return best_child.move


game = Game()
game.play()