
class GameState:
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


    # return a list of all successors which are chaged [row, column, stone] indexes of the current self.game_board
    def successor_row_col_index(self, maximizingPlayer, stone):
        successor_list = []
        for row in range(len(self.game_board)):
            for column in range(len(self.game_board)):
                if self.game_board[row][column] == "-":
                    # instead of storing the whole self.game_board, store the row and column index only?!
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



    # check whether the game is terminated or not, and give the utility value;
    # game_state is the board in the game tree, row is the updated row compared with the previous step, column is the updated column compared with the previous step
    def game_state_row_col_utility(self, stone, threshold):
        
        row = self.row
        column = self.column

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
                            self.utility = threshold
                            return
                        elif duplicate_count == threshold and board_row[index] != stone: 
                            self.game_over = True
                            self.utility = -threshold
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
                        self.utility = threshold
                        return
                    elif duplicate_count == threshold and board_column[index] != stone: 
                        self.game_over = True
                        self.utility = -threshold
                        return

            # check positive diagonal(\), first_r is the most upper left position whose element is equal to self.game_board[row][column]
            first_r = row
            for r in range(row - 1, -1, -1):
                update = r - row
                new_column = column + update
                if new_column >= 0:
                    if self.game_board[r][new_column] == self.game_board[row][column]:
                        first_r = r
                    else:
                        break
            
            # check number of consecutive elements, from the upper left to the lower right
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
                    self.utility = threshold
                    return
            elif duplicate_count == threshold and self.game_board[row][column] != stone: 
                    self.game_over = True
                    self.utility = -threshold
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
                self.utility = threshold
                return
            elif duplicate_count == threshold and self.game_board[row][column] != stone: 
                self.game_over = True
                self.utility = -threshold
                return

        # give utility values for game states that have not terminated
        for row in self.game_board:
            if "-" in row:
                self.game_over = False
                return

        self.game_over = True
        self.utility = 0

    # Limitation: not consider broken 3 threat, double threats!!!
    def heuristic_row_col_utility(self):
         # 1) If AI can win this turn, AI does so, award = positive infinity!!!
         # 2) AI defends:
            # No. of opponent's, award = n_defend_1 * w_defend_1)
            # No. of opponent's 2, award = n_defend_2 * w_defend_2
            # No. of opponent's 3, award = n_defend_3 * w_defend_3
            # No. of opponent's 4, award = n_defend_4 * w_defend_4
        # 3) AI attacks:
            # No. of self's 2, award = n_attack_2 * w_attack_2
            # No. of self's 3, award = n_attack_3 * w_attack_3
            # No. of self's 4, award = n_attack_4 * w_attack_4

