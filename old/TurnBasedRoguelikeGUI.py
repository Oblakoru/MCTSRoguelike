import pygame
import sys
import random
import math
import matplotlib.pyplot as plt
from pygame.locals import *

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
FPS = 30

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
            print(f"{self.name} attacks {other.name} for {damage} damage.")

    def super_attack(self, other):
        if self.mana >= self.SUPER_ATTACK_MANA_COST:
            damage = self.base_damage * self.SUPER_ATTACK_MULTIPLIER
            other.take_damage(damage)
            self.mana -= self.SUPER_ATTACK_MANA_COST
            if not self.silent:
                print(f"{self.name} uses a super attack on {other.name} for {damage} damage.")
        else:
            if not self.silent:
                print(f"{self.name} does not have enough mana for a super attack.")

    def heal(self):
        if self.mana >= self.HEAL_MANA_COST:
            heal_amount = min(self.HEAL_AMOUNT, self.max_health - self.health)
            self.health += heal_amount
            self.mana -= self.HEAL_MANA_COST
            if not self.silent:
                print(f"{self.name} heals for {heal_amount}.")
        else:
            if not self.silent:
                print(f"{self.name} does not have enough mana to heal.")

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

        if self.health == 0:
            if not self.silent:
                print(f"{self.name} has fallen!")

class GameState:
    def __init__(self, player, enemy, current_turn='player'):
        self.player = player
        self.enemy = enemy
        self.current_turn = current_turn

    def get_legal_moves(self):
        return ['attack', 'super_attack', 'heal', 'guard']

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
            return 1  # Player wins
        elif self.enemy.is_alive():
            return -1  # Enemy wins
        return 0  # Draw or both are dead (shouldn't normally happen in this context)

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
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)
        draw_text(screen, f"{player.name} - Health: {player.health}, Mana: {player.mana}", font, BLACK, 20, 20)
        draw_text(screen, f"{enemy.name} - Health: {enemy.health}, Mana: {enemy.mana}", font, BLACK, 20, 60)

        if player.is_alive() and enemy.is_alive():
            if player_type == 'human':
                player_turn(player, enemy)
            else:
                random_turn(player, enemy)

        if player.is_alive() and enemy.is_alive():
            mcts_turn(player, enemy, mcts, 'enemy')

        pygame.display.update()
        fps_clock.tick(FPS)

    if player.is_alive():
        return 'Player'
    else:
        return 'Enemy'

def player_turn(player, enemy):
    draw_text(screen, f"{player.name}'s turn!", font, BLACK, 20, 100)
    draw_text(screen, f"Choose your move:", font, BLACK, 20, 140)
    draw_text(screen, "1. Attack", font, BLACK, 20, 180)
    draw_text(screen, "2. Super Attack", font, BLACK, 20, 220)
    draw_text(screen, "3. Heal", font, BLACK, 20, 260)
    draw_text(screen, "4. Guard", font, BLACK, 20, 300)

    pygame.display.update()

    move = None
    while move is None:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_1:
                    move = 'attack'
                elif event.key == K_2:
                    move = 'super_attack'
                elif event.key == K_3:
                    move = 'heal'
                elif event.key == K_4:
                    move = 'guard'

    if move == 'attack':
        player.attack(enemy)
    elif move == 'super_attack':
        player.super_attack(enemy)
    elif move == 'heal':
        player.heal()
    elif move == 'guard':
        player.guard()

def run_simulations(num_games):
    results = {'Player': 0, 'Enemy': 0}

    for _ in range(num_games):
        player = Character(name="Player")
        enemy = Character(name="Enemy")
        winner = game_turn(player, enemy, 'random')
        results[winner] += 1

    return results

def plot_results(results):
    labels = list(results.keys())
    counts = list(results.values())

    plt.bar(labels, counts, color=['blue', 'red'])
    plt.xlabel('Outcome')
    plt.ylabel('Number of Games')
    plt.title('Simulation Results: Random AI vs. MCTS')
    plt.show()

def draw_text(surface, text, font, color, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def main():
    pygame.init()
    global screen, font, fps_clock
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Turn-Based Game with Pygame')
    font = pygame.font.Font(None, 32)
    fps_clock = pygame.time.Clock()

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
        print(f"Player wins: {results['Player']}")
        print(f"Enemy wins: {results['Enemy']}")
        plot_results(results)
    else:
        print("Invalid choice! Please enter 1 or 2.")

    pygame.quit()

if __name__ == "__main__":
    main()
