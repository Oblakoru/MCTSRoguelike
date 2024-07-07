class TicTacToe:
    def __init__(self):
        self.board = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # 0 - prazno, 1 - X(igralec), 2 - O(računalnik)
        self.current_player = 1

    def make_move(self, move):
        if not 0 <= move < 9:
            raise ValueError("Poteza mora biti med 0 in 8!")
        if self.board[move] != 0:
            raise ValueError("Polje je že zasedeno!")
        #Nastavimo polje na vrednost trenutnega igralca 1-igralec, 2-računalnik
        self.board[move] = self.current_player
        self.current_player = 3 - self.current_player  #Zamenjamo igralca (1 -> 2, 2 -> 1)


    #Pridobivanje legalnih potez
    def get_legal_moves(self):
        legal_moves = []
        for square in range(9):
            if self.board[square] == 0:
                legal_moves.append(square)
        return legal_moves

        #return [i for i in range(9) if self.board[i] == 0]

    #Preverjanje zmagovalca
    def is_winner(self, player):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Vrstica
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Stolpci
            [0, 4, 8], [2, 4, 6]              # Diagonale
        ]
        #Se sprehodimo skozi vse možne zmagovalne kombinacije
        for condition in win_conditions:
            #Če so vsa polja v kombinaciji enaka trenutnemu igralcu, potem je ta igralec zmagal
            if all(self.board[pos] == player for pos in condition):
                return True
        return False

    def is_draw(self):
        #Če ni več prostih polj, je izid igre neodločen
        return all(pos != 0 for pos in self.board)


    def game_over(self):
        #Preverimo, če je igra prišla do končnega stanja
        return self.is_winner(1) or self.is_winner(2) or self.is_draw()




