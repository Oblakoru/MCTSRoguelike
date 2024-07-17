from TurnBasedRogueLike.Character import Character

class GameState:

    #Inicializacija igre
    def __init__(self, player, enemy, current_turn='player'):
        self.player = player
        self.enemy = enemy
        self.current_turn = current_turn

    #Pridobimo vse legalne poteze
    def get_legal_moves(self):
        character = self.player if self.current_turn == 'player' else self.enemy
        return character.get_available_moves()

    #Naredimo potezo
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

    #Preverimo, če je igra končana
    def is_game_over(self):
        return not (self.player.is_alive() and self.enemy.is_alive())

    #Preverimo, kdo je zmagal in vrnemo rezultat
    def get_result(self):
        if self.player.is_alive():
            return 1
        elif self.enemy.is_alive():
            return -1
        return 0

    #Kopiramo trenutno stanje igre
    def copy(self):
        return GameState(
            Character(self.player.name, self.player.health, self.player.mana, self.player.base_damage, silent=True),
            Character(self.enemy.name, self.enemy.health, self.enemy.mana, self.enemy.base_damage, silent=True),
            self.current_turn
        )

