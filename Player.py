import numpy as np
import globals
from GameState import GameState

class Player:
    """
    A class to represent a player. Each player contains a name, stone, threshold, elapsed_time_list, and success flag.

    ...

    Attributes
    ----------
    name : str
    stone : str
        "B" (black) or "W" (white)
    threshold : int
        3 in a row or 5 in a row?

    """
    def __init__(self, name, stone, threshold = 5):
        self.name = name
        self.stone = stone
        self.threshold = threshold
        self.elapsed_time_list = []
        self.succeed_flag = False

'''
    # Check the whole board, each row/column/diagonal!!!!!
    # check whether the game is terminated or not, and give the utility value;
    # game_state is a state in the game tree

    def game_state_utility(self, game_state):
        # check row
        for row in range(len(game_state)):
            board_row = game_state[row]
            duplicate_count = 1
            if board_row.count('W') >= self.threshold or board_row.count('B') >= self.threshold:
                for index in range(1, len(board_row)):
                        if board_row[index] != "-" and board_row[index] == board_row[index - 1]:
                            duplicate_count += 1
                        else:
                            duplicate_count = 1
                        if duplicate_count == self.threshold and board_row[index] == self.stone: return (True, self.threshold)
                        elif duplicate_count == self.threshold and board_row[index] != self.stone: return (True, -self.threshold)


        # check column
        for column in range(len(game_state)):
            board_column = []
            for index in range(len(game_state)):
                board_column.append(game_state[index][column])
            duplicate_count = 1
            if board_column.count('W') >= self.threshold or board_column.count('B') >= self.threshold:
                for index in range(1, len(board_column)):
                    if board_column[index] != "-" and board_column[index] == board_column[index - 1]:
                        duplicate_count += 1
                    else:
                        duplicate_count = 1
                    if duplicate_count == self.threshold and board_column[index] == self.stone: return (True, self.threshold)
                    elif duplicate_count == self.threshold and board_column[index] != self.stone: return (True, -self.threshold)


        # check diagonal
        numpy_board = np.matrix(game_state)
        all_diagnoal_list = [numpy_board[::-1,:].diagonal(i) for i in range(-numpy_board.shape[0]+1,numpy_board.shape[1])]
        all_diagnoal_list.extend(numpy_board.diagonal(i) for i in range(numpy_board.shape[1]-1,-numpy_board.shape[0],-1))
        all_diagnoal_list = [n.tolist()[0] for n in all_diagnoal_list]
        for each_diagnoal_list in all_diagnoal_list:
            # print(f"Each diagonal: {each_diagnoal_list}")
            duplicate_count = 1
            if each_diagnoal_list.count('W') >= self.threshold or each_diagnoal_list.count('B') >= self.threshold:
                for index in range(1, len(each_diagnoal_list)):
                    if each_diagnoal_list[index] != "-" and each_diagnoal_list[index] == each_diagnoal_list[index - 1]:
                        duplicate_count += 1
                    else:
                        duplicate_count = 1
                    if duplicate_count == self.threshold and each_diagnoal_list[index] == self.stone: return (True, self.threshold)
                    elif duplicate_count == self.threshold and each_diagnoal_list[index] != self.stone: return (True, -self.threshold)
        
        # give utility values for game states that have not terminated
        for row in game_state:
            if "-" in row:
                return (False, None)
        
        return (True, 0)
'''


class MinimaxPlayer(Player):
    """
    A class to represent a Minimax player.

    """

    def __init__(self, name, stone, depth, threshold):
        super().__init__(name, stone, threshold)
        self.depth = depth

    # search the game tree
    def place_stone(self, game_state, depth, maximizingPlayer):


        # the globals.game_state_dict stores all searched game states in the current turn, avoiding duplicate searching.
        if game_state in globals.game_state_dict:
            if game_state.next_best_state: return game_state.next_best_state 
            else: return game_state

        globals.count += 1

        if depth == float('inf'):
            # when the search depth is inf, the search game tree is complete, and thus only terminal states have utilities
            # the game_state_row_col_utility can be used for Tic Tac Toe, where the search space is small
            game_state.game_state_row_col_utility(self.stone, self.threshold)
        else:
            # game_state_heuristic_row_col_utility() method is only used for Gomoku, where the serch depth is limited
            game_state.game_state_heuristic_row_col_utility(self.stone)

        # base case
        if game_state.game_over or depth == 0:
            globals.game_state_dict[game_state] = ''
            # return the next best game state
            if game_state.next_best_state: return game_state.next_best_state 
            else: return game_state

        if maximizingPlayer:
            maxValue = -float('inf')
            successor_list = game_state.successor_row_col_index(maximizingPlayer, self.stone)
            for next_state in successor_list:
                self.place_stone(next_state, depth - 1, False)
                if next_state.utility > maxValue:
                    maxValue = next_state.utility
                    game_state.next_best_state = next_state

            game_state.utility = maxValue
            globals.game_state_dict[game_state] = ''
            if game_state.next_best_state: return game_state.next_best_state 
            else: return game_state

        else:
            minValue = float('inf')
            successor_list = game_state.successor_row_col_index(maximizingPlayer, self.stone)
            for next_state in successor_list:
                self.place_stone(next_state, depth - 1, True)
                if next_state.utility < minValue:
                    minValue = next_state.utility
                    game_state.next_best_state = next_state

            game_state.utility = minValue
            globals.game_state_dict[game_state] = ''
            if game_state.next_best_state: return game_state.next_best_state 
            else: return game_state




class MinimaxAlphaBetaPrunePlayer(MinimaxPlayer):

    """
    A class to represent a Minimax Alpha Beta Pruning player.

    """

    def place_stone(self, game_state, depth, maximizingPlayer, alpha = -float('inf'), beta = float('inf')):

        game_state.alpha = alpha
        game_state.beta = beta

        if game_state in globals.game_state_dict:
            if game_state.next_best_state: return game_state.next_best_state 
            else: return game_state

        globals.count += 1
        if depth == float('inf'):
            game_state.game_state_row_col_utility(self.stone, self.threshold)
        else:
            game_state.game_state_heuristic_row_col_utility(self.stone)

        if game_state.game_over or depth == 0:
            globals.game_state_dict[game_state] = ''
            if game_state.next_best_state: return game_state.next_best_state 
            else: return game_state

        if maximizingPlayer:
            successor_list = game_state.successor_row_col_index(maximizingPlayer, self.stone)
            for next_state in successor_list:
                self.place_stone(next_state, depth - 1, False, game_state.alpha, game_state.beta)
                if next_state.utility > game_state.alpha:
                    game_state.alpha = next_state.utility
                    game_state.next_best_state = next_state
                if game_state.beta <= game_state.alpha:
                    break

            game_state.utility = game_state.alpha
            globals.game_state_dict[game_state] = ''
            if game_state.next_best_state: return game_state.next_best_state 
            else: return game_state

        else:
            successor_list = game_state.successor_row_col_index(maximizingPlayer, self.stone)
            for next_state in successor_list:
                self.place_stone(next_state, depth - 1, True, game_state.alpha, game_state.beta)
                if next_state.utility < game_state.beta:
                    game_state.beta = next_state.utility
                    game_state.next_best_state = next_state
                if game_state.beta <= game_state.alpha:
                    break

            game_state.utility = game_state.beta
            globals.game_state_dict[game_state] = ''
            if game_state.next_best_state: return game_state.next_best_state 
            else: return game_state


class BaselinePlayer(Player):
    """
    A class to represent a Baseline player. The Baseline player does only attacks, not defend.

    """

    def __init__(self, name, stone, threshold):
        super().__init__(name, stone, threshold)
        self.depth = 1

    # Only search one step further
    def place_stone(self, game_state, depth = 1, maximizingPlayer = True):

        globals.count += 1
        game_state.game_state_heuristic_row_col_utility(self.stone, baseline = True)
        if game_state.game_over or depth == 0:
            if game_state.next_best_state: return game_state.next_best_state 
            else: return game_state

        maxValue = -float('inf')
        successor_list = game_state.successor_row_col_index(maximizingPlayer, self.stone)
        for next_state in successor_list:
            self.place_stone(next_state, depth - 1, False)
            if next_state.utility > maxValue:
                maxValue = next_state.utility
                game_state.next_best_state = next_state

        game_state.utility = maxValue
        if game_state.next_best_state: return game_state.next_best_state 
        else: return game_state


