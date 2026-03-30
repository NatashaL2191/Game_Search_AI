class TicTacToe:
    def __init__(self):
        # Initialize an empty 3x3 board.
        # Board is a list of 9 elements:
        # 0 = empty, 1 = X, -1 = O
        # X always moves first.
        self.board = [0] * 9
        self.current_player = 1
       
    def get_legal_moves(self):
        # Return a list of indices (0 through 8)
        # corresponding to the empty squares.
        legal = []
        for i in range(0, len(self.board)):
            if self.board[i] == 0:
                legal.append(i)
        return legal

    def make_move(self, move):
        # Place the current player's mark at the
        # given index. Return a NEW TicTacToe
        # object; do not modify self.
        if move in self.get_legal_moves():
            new_Game = TicTacToe()
            new_Board = self.board[:]
            new_Game.board = new_Board
            new_Game.board[move] = self.current_player
            new_Game.current_player = self.current_player * -1
            return new_Game
        


    def is_terminal(self):
        # Return True if the game is over, either
        # because someone has won or because all
        # squares are filled (a draw).

        # The eight winning lines are: rows (0,1,2), (3,4,5), (6,7,8); columns (0,3,6), (1,4,7), (2,5,8);
        # and diagonals (0,4,8), (2,4,6).   
    
        winner = self.check_winner()
        if winner == 1 or winner == -1:
            return True
        if len(self.get_legal_moves()) == 0:
            return True
        return False

    
        

    def utility(self):
        # Return +1 if X has won, -1 if O has won,
        # or 0 for a draw. Only valid when
        # is_terminal() returns True.
        if self.is_terminal() == True:
            X_O = self.check_winner()
            if X_O == 1:
                return 1
            elif X_O == -1:
                return -1
            return 0

    def check_winner(self):
        # Return 1 if X has three in a row, -1 if
        # O has three in a row, or 0 otherwise.
        winners = [[self.board[0], self.board[1], self.board[2]],
            [self.board[3], self.board[4], self.board[5]],
            [self.board[6], self.board[7], self.board[8]],
            [self.board[0], self.board[3], self.board[6]],
            [self.board[1], self.board[4], self.board[7]],
            [self.board[2], self.board[5], self.board[8]],
            [self.board[0], self.board[4], self.board[8]],
            [self.board[2], self.board[4], self.board[6]]]
        
        for i in winners:
            if i == [1, 1, 1]:
                return 1
            elif i ==[-1, -1, -1]:
                return -1
        return 0
        

    def display(self):
        # Print the board in a readable 3x3 format.
        # Use 'X' for 1, 'O' for -1, '.' for 0.
        for i in range(0, len(self.board)):
            if i != 0 and i %3 == 0:
                print()
            if self.board[i] == 1:
                print('X', end = ' ')
            elif self.board[i] == -1:
                print('O', end = ' ')
            else:
                print('.', end = ' ')
        print()
