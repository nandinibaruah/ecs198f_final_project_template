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
            start_row_idx = 8 - int(start_row)
            start_col_idx = ord(start_col) - ord('a')
            end_row_idx = 8 - int(end_row)
            end_col_idx = ord(end_col) - ord('a')

            moving_piece = self.board[start_row_idx][start_col_idx]

            capture = False
            if self.board[end_row_idx][end_col_idx] != '':
                capture = True                                    
            #pawn promotion edge case
            isPawn = False
            if moving_piece.upper() == 'P':
                isPawn = True
                #white is index 0
                #black is index 7
                if (moving_piece.isupper() and end_row_idx == 0) or (moving_piece.islower() and end_row_idx ==7):
                    promoted_p = 'Q' if moving_piece.isupper() else 'q'
                    self.board[end_row_idx][end_col_idx] = promoted_p
                    self.board[start_row_idx][start_col_idx] = ''
                    self.white_to_move = not self.white_to_move
                    # Return extended notation with promotion
                    if capture:
                        return move[0:2] + "x" + move[2:] + "=Q"
                    else: return move + "=Q"
                                                     
                                                     
            #do a regular move
            

            self.board[end_row_idx][end_col_idx] = moving_piece
            self.board[start_row_idx][start_col_idx] = ''
            self.white_to_move = not self.white_to_move

            if isPawn:
                if capture:
                    return move[0:2] + "x" + move[2:]
                else:
                    return move
            else:
                if capture:
                    return moving_piece + move[0:2] + "x" + move[2:]
                else:
                    return moving_piece + move
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

        # base cases

        # no selection for piece
        if selected_pce == '':
            return False
        
        # no selection for position
        if start_row_idx == end_row_idx and start_col_idx == end_col_idx:
            return False

        # ensuring selected piece matches current turn
        if (self.white_to_move and selected_pce.islower()) or (not self.white_to_move and selected_pce.isupper()):
            return False
        
        # makes sure end piece is not the same color as piece being moved
        if end_pos != '' and end_pos.isupper() == selected_pce.isupper():
            return False
        
        # calculate the position differences to use for individual type checks
        row_diff = end_row_idx - start_row_idx
        col_diff = end_col_idx - start_col_idx
        
        # convert piece type to upper for comparisons
        piece_type = selected_pce.upper()
        
        # pawn logic
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
        
        # knight logic
        elif piece_type == 'N':
            return (abs(row_diff) == 2 and abs(col_diff) == 1) or (abs(row_diff) == 1 and abs(col_diff) == 2)
        
        # bishop logic
        elif piece_type == 'B':
            if abs(row_diff) != abs(col_diff):
                return False
            step_row = 1 if row_diff > 0 else -1
            step_col = 1 if col_diff > 0 else -1
            for i in range(1, abs(row_diff)):
                if self.board[start_row_idx + i * step_row][start_col_idx + i * step_col] != '':
                    return False
            return True
        
        # king logic
        elif piece_type == 'K':
        # the king move one tile in any dir
            if abs(row_diff) <= 1 and abs(col_diff) <= 1:
                return True

            # here we have the edge cse for castling where king moves two sqaure horizontally
            if row_diff == 0 and abs(col_diff) == 2:
                # here we check if a sqaure is under adttack
                def is_square_attacked(r, c, color):
                    # here we look for the collor
                    if color == 'white':
                        e_pwn, e_kni, e_b, e_r, e_q, e_k = 'p', 'n', 'b', 'r',  'q', 'k'
                        # b pawn move set for att
                        if r - 1 >= 0:
                            if c - 1 >= 0 and self.board[r - 1][c - 1] ==  e_pwn:
                                return True
                            if c + 1 <  8 and self.board[r - 1][c + 1] == e_pwn:
                                return True
                    else:  # check for other color
                        e_pwn, e_kni, e_b, e_r, e_q, e_k = 'P', 'N', 'B', 'R', 'Q', 'K'
                        # white pwn
                        if r + 1 < 8:
                            if c - 1 >=  0 and self.board[r + 1][c - 1] == e_pwn:
                                return True
                            if c + 1 < 8 and self.board[r + 1][c + 1] == e_pwn:
                                return True

                    #now knight
                    knight_moves = [(-2, -1), (-2, 1), (-1, -2),  (-1, 2),
                                    (1, -2),  (1, 2),  (2, -1),  (2, 1)]
                    for dr, dc in knight_moves:
                        rr, cc = r + dr, c + dc
                        if 0 <= rr < 8 and  0 <= cc < 8:
                            if self.board[rr][cc] == e_kni:
                                return True

                    # the diagnoal case 
                    for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                        rr, cc = r + dr, c + dc
                        while 0 <= rr < 8 and 0 <= cc < 8:
                            if self.board[rr][cc] != '':
                                if self.board[rr][cc] in (e_b, e_q):
                                    return True
                                break
                            rr +=  dr
                            cc += dc

                    # straight lines
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        rr, cc = r + dr, c + dc
                        while 0 <= rr < 8 and 0 <= cc < 8:
                            if self.board[rr][cc] != '':
                                if self.board[rr][cc] in (e_r, e_q):
                                    return True
                                break
                            rr += dr
                            cc += dc

                    # sqaure next to king
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            rr, cc = r + dr, c + dc
                            if 0 <= rr < 8 and 0 <= cc < 8:
                                if self.board[rr][cc] == e_k:
                                    return True

                    return False

                # check color 
                king_color = 'white' if selected_pce.isupper() else 'black'
                
                if selected_pce.isupper():
                    
                    if start_row_idx != 7 or start_col_idx != 4:
                        return False

                    if col_diff == 2:
                        
                        if self.board[7][5] != '' or self.board[7][6] != '':
                            return False
                       
                        if self.board[7][7] != 'R':
                            return False
                        if (is_square_attacked(7, 4, king_color) or 
                            is_square_attacked(7, 5, king_color) or 
                            is_square_attacked(7, 6, king_color)):
                            return False
                        return True

                    # Queenside castling for White: e1 -> c1 (col_diff == -2).
                    elif col_diff == -2:
                        # d1 (7,3), c1 (7,2), and b1 (7,1) must be empty.
                        if self.board[7][3] != '' or self.board[7][2] != '' or self.board[7][1] != '':
                            return False
                        # Rook must be at a1 (7,0).
                        if self.board[7][0] != 'R':
                            return False
                        # Check that e1, d1, and c1 are not under attack.
                        if (is_square_attacked(7, 4, king_color) or 
                            is_square_attacked(7, 3, king_color) or 
                            is_square_attacked(7, 2, king_color)):
                            return False
                        return True

                else:
              
                    if start_row_idx != 0 or start_col_idx != 4:
                        return False
                    if col_diff == 2:
                        
                        if self.board[0][5] != '' or self.board[0][6] != '':
                            return False
                 
                        if self.board[0][7] != 'r':
                            return False
                        
                        if (is_square_attacked(0, 4, king_color) or 
                            is_square_attacked(0, 5, king_color) or 
                            is_square_attacked(0, 6, king_color)):
                            return False
                        return True

                    # Queenside castling for Black: e8 -> c8 (col_diff == -2).
                    elif col_diff == -2:
                   
                        if self.board[0][3] != '' or self.board[0][2] != '' or self.board[0][1] != '':
                            return False
                       
                        if self.board[0][0] != 'r':
                            return False
                        if (is_square_attacked(0, 4, king_color) or 
                            is_square_attacked(0, 3, king_color) or 
                            is_square_attacked(0, 2, king_color)):
                            return False
                        return True

            return False
        
        # rook logic
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
        
        # queen logic
        elif piece_type == 'Q':
            # Store original piece type
            original_piece = self.board[start_row_idx][start_col_idx]
    
            # Check if valid as a rook
            self.board[start_row_idx][start_col_idx] = 'R'
            rook_valid = self.valid_move(start_row, start_col, end_row, end_col)
    
            # Check if valid as a bishop
            self.board[start_row_idx][start_col_idx] = 'B'
            bishop_valid = self.valid_move(start_row, start_col, end_row, end_col)
    
            # Restore original piece
            self.board[start_row_idx][start_col_idx] = original_piece
    
            return rook_valid or bishop_valid
        


        #edge case: for the scenario where moving a piece would result in having the king in check

        if self.move_leads_check(start_row_idx, start_col_idx, end_row_idx, end_col_idx, selected_pce):
            return False
        

        return False #should be return True?


    def move_leads_check(self, sr, sc, er, ec,moving_piece) -> bool:
        #sr = start row....
        # we will simualte the move on an empty board 
        t_board = [row[:] for row in self.board]
        t_board[er][ec] = moving_piece
        t_board[sr][sc] = ''

        king_symb = 'K' if moving_piece.is_upper() else 'k'
        king_pos = None
        for i in range (8):
            for k in range(8):
                if t_board[i][k] == king_symb:
                    king_pos = (i,k)
                    break
                if king_pos is not None:
                    break
        
        if king_pos == None:
            return True
        
        moving_col = 'white' if moving_piece.is_upper() else 'black'
        return self.is_square_attacked_b(t_board, king_pos[0], king_pos[1], moving_col)

    #this function checks whether sqaure at pos is attacked by anything
    # same logic as used in the king piece--
    def is_square_attacked_b(self, board, r,c,color) -> bool:
        if color == 'white':
            e_pwn, e_k, e_b, e_r, e_q, e_k = 'p', 'n', 'b', 'r', 'q', 'k'
            # black pawn capture
            if r - 1 >= 0:
                if c - 1 >= 0 and board[r - 1][c - 1] == e_pwn:
                    return True
                if c + 1 < 8 and board[r - 1][c + 1] == e_pwn:
                    return True
        else:
            e_pwn, e_k, e_b, e_r,  e_q, e_k = 'P', 'N', 'B', 'R', 'Q', 'K'
            # now white pawn
            if r + 1 < 8:
                if c - 1 >= 0 and board[r + 1][c - 1] ==  e_pwn:
                    return True
                if c + 1 < 8 and board[r + 1][c + 1] == e_pwn:
                    return True

        # Knight
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                        (1, -2),  (1, 2), (2, -1), (2, 1)]
        for dr, dc in knight_moves:
            rr, cc = r + dr, c + dc
            if 0 <= rr < 8 and 0 <= cc < 8:
                if board[rr][cc] == e_k:
                    return True

        # for bishop and queen since this chekcs diagonls
        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            rr, cc = r + dr, c + dc
            while 0 <= rr < 8 and 0 <= cc < 8:
                if board[rr][cc] != '':
                    if board[rr][cc] in (e_b, e_q):
                        return True
                    break
                rr += dr
                cc += dc

        # straught line for rook and queen 
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            rr, cc = r + dr, c + dc
            while 0 <= rr < 8 and 0 <= cc < 8:
                if board[rr][cc] != '':
                    if board[rr][cc] in (e_r, e_q):
                        return True
                    break
                rr += dr
                cc += dc

        # next to king
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                rr, cc = r + dr, c + dc
                if 0 <= rr < 8 and 0 <= cc < 8:
                    if board[rr][cc] == e_k:
                        return True

        return False
        
    def piece_at_loc(self, row: str, col: str) -> str:
        """
        Function to get the current piece at a board position.
        """
        curr_pce_col = ord(col) - ord('a')
        curr_pce_row = 8 - int(row)
        
        return self.board[curr_pce_row][curr_pce_col]
