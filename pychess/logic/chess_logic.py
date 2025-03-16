class ChessLogic:
    def __init__(self):
        """
        Initalize the ChessLogic Object. External fields are board and result

        board -> Two Dimensional List of string Representing the Current State of the Board
            P, R, N, B, Q, K - White Pieces

            p, r, n, b, q, k - Black Pieces

            '' - Empty Square

        result -> The current result of the game
            w - White Win

            b - Black Win

            d - Draw

            '' - Game In Progress
        """
        self.board = [
			['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
			['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
			['','','','','','','',''],
			['','','','','','','',''],
			['','','','','','','',''],
			['','','','','','','',''],
			['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
			['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
		]
        self.result = "" 

    def play_move(self, move: str) -> str:
        """
        Function to make a move if it is a valid move. This function is called everytime a move in made on the board

        Args:
            move (str): The move which is proposed. The format is the following: starting_sqaure}{ending_square}
            
            i.e. e2e4 - This means that whatever piece is on E2 is moved to E4

        Returns:
            str: Extended Chess Notation for the move, if valid. Empty str if the move is invalid
        """
        if len(move) > 4:
            return "" # invalid move

        start_col, start_row = move[0], move[1]
        end_col, end_row = move[2], move[3]


        if self.valid_move(start_row, start_col, end_row, end_col):
            # update board
            pass
        else:
            return "" # invalid move

        #Implement this
        pass
    
    def valid_move(self, start_row: str, start_col: str, end_row: str, end_col: str) -> bool:
        """
        Function to check whether a move is valid

        Args:
            start_row (str): the row of the starting position

            start_col (str): the column of the starting position

            end_row (str): the row of the ending position

            end_col (str): the column of the ending position

        Returns:
            bool:
            True if the move is valid
            False if the move is not valid
        """
        
        selected_pce = self.piece_at_loc(start_row, start_col)
        end_pos = self.piece_at_loc(end_row, end_col)

        # To implement
        
        # check if there's a piece at the starting position
        if selected_pce == '':
            return False
        
        # check if it's the correct player's turn
        if (self.white_to_move and selected_pce.islower()) or (not self.white_to_move and selected_pce.isupper()):
            return False
        
        # check if the ending position contains a piece of the same color
        if end_pos != '' and end_pos.isupper() == selected_pce.isupper():
            return False 
        
        # handle piece-specific movement
        piece_type = selected_pce.upper()
 
        if piece_type == 'P':  # Pawn
            return self._valid_pawn_move(start_row, start_col, end_row, end_col, selected_pce)
        elif piece_type == 'R':  # Rook
            return self._valid_rook_move(start_row, start_col, end_row, end_col)
        elif piece_type == 'N':  # Knight
            return self._valid_knight_move(start_row, start_col, end_row, end_col)
        elif piece_type == 'B':  # Bishop
            return self._valid_bishop_move(start_row, start_col, end_row, end_col)
        elif piece_type == 'Q':  # Queen
            return self._valid_queen_move(start_row, start_col, end_row, end_col)
        elif piece_type == 'K':  # King
            return self._valid_king_move(start_row, start_col, end_row, end_col, selected_pce)
        
        return False

    def piece_at_loc(self, row: str, col: str) -> ord:
        """
        Function to get the current piece at a board position

        Args:
            row (str): the row of the position

            col (str): the column of the position
            
            i.e. e2 - the piece at E2

        Returns:
            ord: the piece at the specified board position
        """
        curr_pce_col = ord(col) - ord('a')
        curr_pce_row = 8 - int(row)
        
        return self.board[curr_pce_row][curr_pce_col]