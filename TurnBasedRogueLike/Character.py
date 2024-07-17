class Character:

    def __init__(self, name, health=100, mana=50, base_damage=10, silent=False):
        self.name = name
        self.health = health
        self.mana = mana
        self.base_damage = base_damage
        self.silent = silent
        self.guarded = False

    #Preverimo, če je igralec še živ
    def is_alive(self):
        return self.health > 0

    def attack(self, other):
        damage = self.base_damage
        other.take_damage(damage)
        if not self.silent:
            print(f"{self.name} napade {other.name} za {damage} škode")

    def super_attack(self, other):
        if self.mana >= 20:
            damage = self.base_damage * 2
            other.take_damage(damage)
            self.mana -= 20
            if not self.silent:
                print(f"{self.name} uporabi močan napad {other.name} za {damage} škode.")
        else:
            if not self.silent:
                print(f"{self.name} nima dovolj mane za močan napad.")

    def heal(self):
        if self.mana >= 10:
            self.health += 20
            self.mana -= 10
            if not self.silent:
                print(f"{self.name} se pozdravi za {20} življenskih točk.")
        else:
            if not self.silent:
                print(f"{self.name} nima dovolj mane za zdravljenje.")

    def guard(self):
        self.guarded = True
        if not self.silent:
            print(f"{self.name} se zaščiti!")

    #Funkcija za računanje škode
    def take_damage(self, damage):
        if self.guarded:
            damage = int(damage * 0.75)
            self.guarded = False
            if not self.silent:
                print(f"{self.name} se je ubranil napada, narejeno le {damage} škode.")

        self.health -= damage
        self.health = max(self.health, 0)

        if self.health == 0 and not self.silent:
            print(f"{self.name} je bil premagan!")

    #Pridobimo vse možne legalne poteze
    def get_available_moves(self):
        moves = ['attack', 'guard']

        if self.mana >= 20:
           moves.append('super_attack')
        if self.mana >= 10:
           moves.append('heal')
        return moves
