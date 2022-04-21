
class GameState:
    """
    A class to represent a game state.
    
    ...

    Attributes
    ----------
    game_board : matrix
        the current game state
    name : str
        the unique name of the current game_board
    utility : int
        the utility of the current game state, it is respect to the player who places the last stone
    row: int
        the row is the row where the last player places its stone
    colum: int
        the column is the position where the last player places its stone
    game_over: bool
        True/False
    next_best_state: GameState:
        the best game state in the next step
    alpha: float
    beta: float

    """

    def __init__(self, game_board):
        self.game_board = game_board
        self.name = ' '.join([str(elem2) for elem in self.game_board for elem2 in elem])
        
        self.utility = 0
        self.row = 0
        self.column = 0

        self.game_over = None
        self.next_best_state = None

        self.alpha = -float('inf')
        self.beta = float('inf')


    def __len__(self):
        return len(self.game_board)

    def __getitem__(self, row):
        return self.game_board[row]

    def __str__(self):
        return '\n'.join(' '.join(map(str, row)) for row in self.game_board) 

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    

    def successor_row_col_index(self, maximizingPlayer, stone):
        '''
        This function returns a list of all successors. Each element is a list of available [row, column] indexes.
        Instead of storing the whole game board, store only the row and column index.

        '''
        successor_list = []
        for row in range(len(self.game_board)):
            for column in range(len(self.game_board)):
                if self.game_board[row][column] == "-":
                    each_game_board = [row[:] for row in self.game_board]
                    if maximizingPlayer:
                        each_game_board[row][column] = stone
                    elif stone == "W": 
                        each_game_board[row][column] = "B"
                    else: 
                        each_game_board[row][column] = "W"

                    next_state = GameState(each_game_board)
                    next_state.row = row
                    next_state.column = column
                    successor_list.append(next_state)

        return successor_list



    def game_state_row_col_utility(self, stone, threshold):
        '''

        This function checks whether the game is terminated and gives the utility values for terminal states.
        Instead of checking the whole game board, check only the updated row and column index.
        
        Parameters:
        stone: str
            the current player who wants to search the game tree
        '''
        row = self.row
        column = self.column

        # row and column are the updated row and column in the last turn
        # stone may == or != self.game_board[row][column]
        if self.game_board[row][column] != "-":
            
            # check updated row
            board_row = self.game_board[row]
            duplicate_count = 1
            if board_row.count('W') >= threshold or board_row.count('B') >= threshold:
                for index in range(1, len(board_row)):
                        if board_row[index] != "-" and board_row[index] == board_row[index - 1]:
                            duplicate_count += 1
                        else:
                            duplicate_count = 1
                        if duplicate_count == threshold and board_row[index] == stone: 
                            self.game_over = True
                            self.utility = float('inf')
                            return
                        if duplicate_count == threshold and board_row[index] != stone: 
                                self.game_over = True
                                self.utility = -float('inf')
                                return

            # check updated column
            board_column = []
            for index in range(len(self.game_board)):
                board_column.append(self.game_board[index][column])
            duplicate_count = 1
            if board_column.count('W') >= threshold or board_column.count('B') >= threshold:
                for index in range(1, len(board_column)):
                    if board_column[index] != "-" and board_column[index] == board_column[index - 1]:
                        duplicate_count += 1
                    else:
                        duplicate_count = 1
                    if duplicate_count == threshold and board_column[index] == stone: 
                        self.game_over = True
                        self.utility = float('inf')
                        return
                    if duplicate_count == threshold and board_column[index] != stone: 
                            self.game_over = True
                            self.utility = -float('inf')
                            return

            # check positive diagonal(\), first_r is the most upper left position whose element is equal to self.game_board[row][column]
            first_r = row
            for r in range(row - 1, -1, -1):
                update = r - row
                new_column = column + update
                if new_column >= 0:
                    if self.game_board[r][new_column] == stone:
                        first_r = r
                    else:
                        break
            
            # check the number of consecutive elements, from the upper left to the lower right
            duplicate_count = 1
            for r in range(first_r + 1, len(self.game_board)):
                update = r - row
                new_column = column + update
                if new_column < len(self.game_board):
                    if self.game_board[r][new_column] == self.game_board[r - 1][new_column - 1]:
                        duplicate_count += 1
                    else:
                        break
                else:
                    break

            if duplicate_count == threshold and self.game_board[row][column] == stone: 
                    self.game_over = True
                    self.utility = float('inf')
                    return
            if duplicate_count == threshold and self.game_board[row][column] != stone: 
                    self.game_over = True
                    self.utility = -float('inf')
                    return


            # check backward diagonal(/), first_r is the most upper right position whose element is equal to self.game_board[row][column]
            first_r = row
            for r in range(row - 1, -1, -1):
                update = r - row
                new_column = column - update
                if new_column < len(self.game_board):
                    if self.game_board[r][new_column] == self.game_board[row][column]:
                        first_r = r
                    else:
                        break

            # check number of consecutive elements, from the upper right to the lower left
            duplicate_count = 1
            for r in range(first_r + 1, len(self.game_board)):
                update = r - row
                new_column = column - update
                if new_column >= 0:
                    if self.game_board[r][new_column] == self.game_board[r - 1][new_column + 1]:
                        duplicate_count += 1
                    else:
                        break
                else:
                    break
            if duplicate_count == threshold and self.game_board[row][column] == stone: 
                self.game_over = True
                self.utility = float('inf')
                return
            if duplicate_count == threshold and self.game_board[row][column] != stone: 
                    self.game_over = True
                    self.utility = -float('inf')
                    return

        # game isn't over, no utility
        for row in self.game_board:
            if "-" in row:
                self.game_over = False
                return

        self.game_over = True
        self.utility = 0


    def game_state_heuristic_row_col_utility(self, stone, baseline = False):
        '''

        This function checks whether the game is terminated or not and gives the utility value.
        It only checks the updated row and column.

        Unlike the function game_state_row_col_utility(), it gives utilities for all game states: immediate and terminal states.
        
        Limitation: Only give utility to the player when it's the player places the last stone, 
        # for example, when it is black's turn, but the white places a stone, the black will not get a utility, and vice versa
        # If it is black's turn and black places a stone, the game state's utility is calculated concerning the black player
        
        For a game state, the utility is calculated: 
         # 1) If AI can win this turn, AI does so, award = positive infinity!!!
         # 2) AI defends:
            # No. of opponent's, award = n_defend_1 * w_defend_1)
            # No. of opponent's 2 (break 2s or consecutive 2s), award = n_defend_2 * w_defend_2
            # No. of opponent's 3 (break 3s or consecutive 3s), award = n_defend_3 * w_defend_3
            # No. of opponent's 4 (break 4s or consecutive 4s), award = n_defend_4 * w_defend_4
        # 3) AI attacks:
            # No. of self's 2, award = n_attack_2 * w_attack_2
            # No. of self's 3, award = n_attack_3 * w_attack_3
            # No. of self's 4, award = n_attack_4 * w_attack_4
            # place a stone somewhere else, negative infinity!!!

        Parameters:
            stone (str): the utility is from the perspective of which player?
            baseline (bool): the baseline player or not
        
        '''

        # opponent's broken/consecutive
        # opponent1_no, opponent2_no, opponent3_no, opponent4_no = 0, 0, 0, 0
        opponent_no_list = [None, 0, 0, 0, 0, 0]
        opponent_weight_list = [None, 0.1, 0.2, 5, 10, -float('inf')]

        # self's consecutive
        # self1_no, self2_no, self3_no, self4_no = 0, 0, 0
        self_no_list = [None, 0, 0, 0, 0, 0]
        self_weight_list = [None, -1, 0.1, 0.2, 0.4, float('inf')]

        if baseline:
            # only attack, not defend
            opponent_weight_list = [None, -10, -10, -10, -10, -float('inf')]

            # only defend, not attack
            # self_weight_list = [None, -10, -10, -10, -10, -float('inf')]

            
        row = self.row
        column = self.column
        if self.game_board[self.row][self.column] != "-" and self.game_board[self.row][self.column] == stone:

            # only check a local area [current_index - 4, current_index + 4]
            def row_column_down_up_index(current_index):
                if current_index - 4 >= 0:  
                    down_index = current_index - 4 
                else: 
                    down_index = 0
                if current_index + 4 < len(self.game_board): 
                    up_index = current_index + 4
                else: 
                    up_index = len(self.game_board) - 1
                return down_index, up_index


            def defend(stone_list, current_index, down_index, up_index):
                opponent_max_left_consecutive = 0
                for i in range(current_index - 1, down_index - 1, -1):
                    if i >= 0: 
                        if stone_list[i] != '-' and stone_list[i] != stone:
                            opponent_max_left_consecutive += 1
                        else:
                            break

                opponent_max_right_consecutive = 0
                for i in range(current_index + 1, up_index + 1, 1):
                    if i < len(self.game_board):
                        if stone_list[i] != '-' and stone_list[i] != stone:
                            opponent_max_right_consecutive += 1
                        else:
                            break
                # consider both consecutive and broken 2/3/4 situations
                update_no(opponent_max_left_consecutive + opponent_max_right_consecutive, True)



            def attack(stone_list, current_index, down_index, up_index):
                opponent_max_consecutive_left_half = 0
                for i in range(current_index, down_index - 1, -1):
                    if stone_list[i] == stone:
                        opponent_max_consecutive_left_half += 1
                    else:
                        break

                opponent_max_consecutive_right_half = 0
                for i in range(current_index + 1, up_index + 1, 1):
                    if stone_list[i] == stone:
                        opponent_max_consecutive_right_half += 1
                    else:
                        break

                opponent_max_consecutive = opponent_max_consecutive_left_half + opponent_max_consecutive_right_half
                update_no(opponent_max_consecutive, False)


            # defend: true/false
            def update_no(max_consecutive_no, defend):
                # defend
                if defend and 1 <= max_consecutive_no <= 5:
                    opponent_no_list[max_consecutive_no] += 1
                # attack
                elif not defend and 1 <= max_consecutive_no <= 5:
                    self_no_list[max_consecutive_no] += 1


            # check row, extract the row from the game_board, but actually, the index is the column's index
            board_row = self.game_board[row]
            column_down_index, column_up_index = row_column_down_up_index(column)
            defend(board_row, column, column_down_index, column_up_index)
            attack(board_row, column, column_down_index, column_up_index)

            # check column, extract the column from the game_board, but actually, the index is the row's index
            board_column = []
            for index in range(len(self.game_board)):
                board_column.append(self.game_board[index][column])
            row_down_index, row_up_index = row_column_down_up_index(row)
            defend(board_column, row, row_down_index, row_up_index)
            attack(board_column, row,row_down_index, row_up_index)


            # check positive diagonal (\)
            board_positive_diagonal = []
            current_index_in_positive_diagonal_list = 0
            for new_row in range(row - 4, row + 5, 1):
                update = new_row - row
                new_column = column + update
                if new_row >= 0 and new_row < len(self.game_board) and new_column >= 0 and new_column < len(self.game_board):
                    board_positive_diagonal.append(self.game_board[new_row][new_column])
                    if new_row < row:
                        current_index_in_positive_diagonal_list += 1

            defend(board_positive_diagonal, current_index_in_positive_diagonal_list, 0, len(board_positive_diagonal) - 1)
            attack(board_positive_diagonal, current_index_in_positive_diagonal_list, 0, len(board_positive_diagonal) - 1)


            # check backward diagonal(/)
            board_backward_diagonal = []
            current_index_in_backward_diagonal_list = 0
            for new_row in range(row + 4, row - 5, -1):
                update = new_row - row
                new_column = column + update
                if new_row >= 0 and new_row < len(self.game_board) and new_column >= 0 and new_column < len(self.game_board):
                    board_backward_diagonal.append(self.game_board[new_row][new_column])
                    if new_row > row:
                        current_index_in_backward_diagonal_list += 1

            defend(board_backward_diagonal, current_index_in_backward_diagonal_list, 0, len(board_backward_diagonal) - 1)
            attack(board_backward_diagonal, current_index_in_backward_diagonal_list, 0, len(board_backward_diagonal) - 1)


            if self_no_list[5] != 0:
                self.game_over = True
                self.utility = float('inf')
                return
            elif opponent_no_list[5] != 0:
                self.game_over = True
                self.utility = -float('inf')
                return

            for each_opponent_no_index in range(len(opponent_no_list)):
                if opponent_no_list[each_opponent_no_index] != None and opponent_no_list[each_opponent_no_index] != 0:
                    self.utility += opponent_no_list[each_opponent_no_index] * opponent_weight_list[each_opponent_no_index]

            for each_self_no_index in range(len(self_no_list)):
                if self_no_list[each_self_no_index] != None and self_no_list[each_self_no_index] != 0:
                    self.utility += self_no_list[each_self_no_index] * self_weight_list[each_self_no_index]

        # game isn't over
        for row in self.game_board:
            if "-" in row:
                self.game_over = False
                return 

        self.game_over = True
        self.utility = 0
