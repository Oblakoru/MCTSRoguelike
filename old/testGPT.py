class Node:
    def __init__(self, move=None, parent=None, state=None):
        self.move = move  # Move to reach this node (e.g., 'attack', 'super_attack', 'heal', 'guard')
        self.parent = parent  # Parent node
        self.state = state  # Game state associated with this node
        self.wins = 0  # Number of wins accumulated for this node
        self.visits = 0  # Number of times this node has been visited
        self.children = []  # List of child nodes
        self.untried_moves = self.state.get_legal_moves()[:]  # Untried moves from this node

    def add_child(self, child_node):
        self.children.append(child_node)

    def update(self, result):
        self.visits += 1
        self.wins += result

    def fully_expanded(self):
        return len(self.untried_moves) == 0

    def is_terminal(self):
        return self.state.is_game_over()


class Character:
    def __init__(self, name, health=100, mana=50, base_damage=10, silent=False):
        self.name = name
        self.health = health
        self.mana = mana
        self.base_damage = base_damage
        self.silent = silent
        self.max_health = health
        self.guarded = False

    def is_alive(self):
        return self.health > 0

    def attack(self, other):
        damage = self.base_damage
        other.take_damage(damage)
        if not self.silent:
            print(f"{self.name} attacks {other.name} for {damage} damage.")

    def super_attack(self, other):
        if self.mana >= self.SUPER_ATTACK_MANA_COST:
            damage = self.base_damage * self.SUPER_ATTACK_MULTIPLIER
            other.take_damage(damage)
            self.mana -= self.SUPER_ATTACK_MANA_COST
            if not self.silent:
                print(f"{self.name} uses a super attack on {other.name} for {damage} damage.")
            return True
        else:
            if not self.silent:
                print(f"{self.name} does not have enough mana for a super attack.")
            return False

    def heal(self):
        if self.mana >= self.HEAL_MANA_COST:
            heal_amount = min(self.HEAL_AMOUNT, self.max_health - self.health)
            self.health += heal_amount
            self.mana -= self.HEAL_MANA_COST
            if not self.silent:
                print(f"{self.name} heals for {heal_amount}.")
            return True
        else:
            if not self.silent:
                print(f"{self.name} does not have enough mana to heal.")
            return False

    def guard(self):
        self.guarded = True
        if not self.silent:
            print(f"{self.name} raises their guard!")

    def take_damage(self, damage):
        if self.guarded:
            damage = int(damage * self.GUARD_DAMAGE_REDUCTION)
            self.guarded = False
            if not self.silent:
                print(f"{self.name} blocks most of the attack, taking only {damage} damage.")
        else:
            if not self.silent:
                print(f"{self.name} takes {damage} damage.")

        self.health -= damage
        self.health = max(self.health, 0)

        if self.health == 0 and not self.silent:
            print(f"{self.name} has fallen!")

import math
import random

class MCTS:
    def __init__(self, exploration_weight=1.4):
        self.exploration_weight = exploration_weight

    def select(self, node):
        best_score = -float('inf')
        best_child = None

        for child in node.children:
            exploit = child.wins / child.visits if child.visits > 0 else 0
            explore = math.sqrt(math.log(node.visits) / child.visits) if child.visits > 0 else float('inf')
            score = exploit + self.exploration_weight * explore
            if score > best_score:
                best_score = score
                best_child = child

        return best_child

    def expand(self, node):
        if node.untried_moves:
            move = random.choice(node.untried_moves)
            node.untried_moves.remove(move)
            new_state = node.state.clone()  # Make a copy of the current game state
            new_state.perform_move(move)  # Apply the move to the new state
            new_node = Node(move=move, parent=node, state=new_state)
            node.add_child(new_node)
            return new_node
        return None

    def simulate(self, node):
        current_state = node.state.clone()

        while not current_state.is_game_over():
            # Random simulation policy
            move = random.choice(current_state.get_legal_moves())
            current_state.perform_move(move)

        # Return the result of the simulation
        return current_state.get_result(node.parent.state.current_player)

    def backpropagate(self, node, result):
        while node is not None:
            node.visits += 1
            node.wins += result
            node = node.parent

    def best_move(self, root):
        for _ in range(1000):  # Adjust the number of simulations as needed
            node = root

            # Selection
            while not node.is_terminal() and node.fully_expanded():
                node = self.select(node)

            # Expansion
            if not node.is_terminal():
                node = self.expand(node)

            # Simulation
            result = self.simulate(node)

            # Backpropagation
            self.backpropagate(node, result)

        # Select the best move based on the number of visits
        best_child = max(root.children, key=lambda c: c.visits)
        return best_child.move

def game_loop():
    hero = Character(name="Hero")
    villain = Character(name="Villain")
    mcts = MCTS()
    current_player = hero  # Start with hero

    while hero.is_alive() and villain.is_alive():
        if current_player == hero:
            # Hero's turn (replace with MCTS decision)
            move = mcts.best_move(root_node)
            perform_action(hero, villain, move)
        else:
            # Villain's turn (replace with MCTS decision)
            move = mcts.best_move(root_node)
            perform_action(villain, hero, move)

        # Switch turn
        current_player = villain if current_player == hero else hero

    # Determine the winner
    if hero.is_alive():
        print("Hero wins!")
    else:
        print("Villain wins!")

def perform_action(attacker, defender, move):
    if move == "attack":
        attacker.attack(defender)
    elif move == "super_attack":
        attacker.super_attack(defender)
    elif move == "heal":
        attacker.heal()
    elif move == "guard":
        attacker.guard()
