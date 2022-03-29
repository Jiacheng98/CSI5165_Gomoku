import numpy as np

class Player:
    def __init__(self, name, stone, threshold = 3):
        self.name = name
        # 'stone': white('W')/black('B')
        self.stone = stone
        self.threshold = threshold

    # check whether the game is terminated or not, and give the utility value;
    # game_state is the board in the game tree
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

    # return a list of all successor boards of the current board, maximizingPlayer is a boolean,
    # if it is true, it means the current player's turn is self.stone, otherwise, it's the opponent's turn
    def successor_board(self, board, maximizingPlayer):
        successor_list = []
        for row in range(len(board)):
            for column in range(len(board)):
                if board[row][column] == "-":
                    # instead of storing the whole board, store the row and column index only?!
                    # copy_board = [row[:] for row in board]
                    # if maximizingPlayer:
                    #     copy_board[row][column] = self.stone
                    # elif self.stone == "W":
                    #     copy_board[row][column] = "B"
                    # else:
                    #     copy_board[row][column] = "W"

                    # successor_list.append(copy_board)

        return successor_list



class MinimaxPlayer(Player):
    def __init__(self, name, stone, depth):
        super().__init__(name, stone)
        self.depth = depth

    # search the game tree
    def place_stone(self, board, depth, maximizingPlayer):
        # game is terminated or depth == 0
        if self.game_state_utility(board)[0] == True or depth == 0:
            return (board, self.game_state_utility(board)[1])
        if maximizingPlayer:
            maxValue = -float('inf')
            maxBoard = None
            successor_list = self.successor_board(board, True)
            for each_board in successor_list:
                value = self.place_stone(each_board, depth - 1, False)[1]
                if value > maxValue:
                    maxValue = value
                    maxBoard = each_board
            return (maxBoard, maxValue)
        else:
            minValue = float('inf')
            minBoard = None
            successor_list = self.successor_board(board, False)
            for each_board in successor_list:
                value = self.place_stone(each_board, depth - 1, True)[1]
                if value < minValue:
                    minValue = value
                    minBoard = each_board
            return (minBoard, minValue)
