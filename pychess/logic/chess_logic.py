class ChessLogic:
    def __init__(self):
        """
        Initialize the ChessLogic Object. External fields are board and result

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
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
        ]
        self.result = ""
        self.white_to_move = True

    def play_move(self, move: str) -> str:
        """
        Function to make a move if it is a valid move.
        """
        if len(move) > 4:
            return ""  # Invalid move

        start_col, start_row = move[0], move[1]
        end_col, end_row = move[2], move[3]

        if self.valid_move(start_row, start_col, end_row, end_col):
            # Update board (to be implemented)
            pass
        else:
            return ""  # Invalid move
        
        pass  # Implement this!

    def valid_move(self, start_row: str, start_col: str, end_row: str, end_col: str) -> bool:
        """
        Function to check whether a move is valid.
        """
        selected_pce = self.piece_at_loc(start_row, start_col)
        end_pos = self.piece_at_loc(end_row, end_col)

        start_row_idx = 8 - int(start_row)
        start_col_idx = ord(start_col) - ord('a')
        end_row_idx = 8 - int(end_row)
        end_col_idx = ord(end_col) - ord('a')

        if selected_pce == '':
            return False
        
        if start_row_idx == end_row_idx and start_col_idx == end_col_idx:
            return False

        if (self.white_to_move and selected_pce.islower()) or (not self.white_to_move and selected_pce.isupper()):
            return False
        
        if end_pos != '' and end_pos.isupper() == selected_pce.isupper():
            return False
        
        row_diff = end_row_idx - start_row_idx
        col_diff = end_col_idx - start_col_idx
        
        piece_type = selected_pce.upper()
        
        if piece_type == 'P':
            direction = 1 if selected_pce.islower() else -1
            initial_row = 1 if selected_pce.islower() else 6

            if col_diff == 0 and end_pos == '':
                if row_diff == direction:
                    return True
                elif row_diff == 2 * direction and start_row_idx == initial_row:
                    middle_row = start_row_idx + direction
                    return self.board[middle_row][start_col_idx] == ''
            elif abs(col_diff) == 1 and row_diff == direction and end_pos != '':
                return True
            
            return False
        
        elif piece_type == 'N':
            return (abs(row_diff) == 2 and abs(col_diff) == 1) or (abs(row_diff) == 1 and abs(col_diff) == 2)
        
        elif piece_type == 'B':
            if abs(row_diff) != abs(col_diff):
                return False
            step_row = 1 if row_diff > 0 else -1
            step_col = 1 if col_diff > 0 else -1
            for i in range(1, abs(row_diff)):
                if self.board[start_row_idx + i * step_row][start_col_idx + i * step_col] != '':
                    return False
            return True
        
        elif piece_type == 'R':
            if start_row_idx != end_row_idx and start_col_idx != end_col_idx:
                return False
            
            if start_row_idx == end_row_idx:
                direction = 1 if end_col_idx > start_col_idx else -1
                for col in range(start_col_idx + direction, end_col_idx, direction):
                    if self.board[start_row_idx][col] != '':
                        return False
            elif start_col_idx == end_col_idx:
                direction = 1 if end_row_idx > start_row_idx else -1
                for row in range(start_row_idx + direction, end_row_idx, direction):
                    if self.board[row][start_col_idx] != '':
                        return False
            
            return True
        
        elif piece_type == 'Q':
            return self.valid_move(start_row, start_col, end_row, end_col) or self.valid_move(start_row, start_col, end_row, end_col)
        
        return False

    def piece_at_loc(self, row: str, col: str) -> str:
        """
        Function to get the current piece at a board position.
        """
        curr_pce_col = ord(col) - ord('a')
        curr_pce_row = 8 - int(row)
        
        return self.board[curr_pce_row][curr_pce_col]
