class TicTacToe:
    def __init__(self):
        self.board = [0] * 9  # 0: empty, 1: X, 2: O
        self.current_player = 1

    def make_move(self, move):
        if not 0 <= move < 9:
            raise ValueError("Move must be between 0 and 8.")
        if self.board[move] != 0:
            raise ValueError("Invalid move! Position already taken.")
        self.board[move] = self.current_player
        self.current_player = 3 - self.current_player  # switch player

    # def undo_move(self, move):
    #     self.board[move] = 0
    #     self.current_player = 3 - self.current_player  # switch back

    def get_legal_moves(self):
        return [i for i in range(9) if self.board[i] == 0]


    #Preverjanje zmagovalca
    def is_winner(self, player):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Vrstica
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Stolpci
            [0, 4, 8], [2, 4, 6]              # Diagonale
        ]
        for condition in win_conditions:
            if all(self.board[pos] == player for pos in condition):
                return True
        return False

    def is_draw(self):
        return all(pos != 0 for pos in self.board)

    def game_over(self):
        return self.is_winner(1) or self.is_winner(2) or self.is_draw()




