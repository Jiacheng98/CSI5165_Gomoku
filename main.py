from Gomoku import Gomoku
from statistics import mean

from multiprocessing import Pool, freeze_support

def main():
    '''
    Experimentations:
    1) Tic Tac Toe, board size = 3
        - Minimax depth inf vs. Minimax Alpha Beta depth inf 
    2) Gomoku, board size = 9/15
        - Minimax depth 1 vs Baseline depth 1
        - Minimax depth 3 vs Minimax depth 5
        - Minimax depth 3 vs Minimax Alpha Beta depth 3
        - Minimax Alpha Beta depth 3 vs Minimax Alpha Beta depth 5

    For each experimentation, run running_time times.
    '''
    running_time = 20
    board_size = 9
    succeed_threshold = 5
    
    task1 = [
        ("minimax", "minimax_alpha_beta", float('inf'), float('inf'), 1, 3, 3),

        # # against a baseline player
        ("baseline", "baseline", 1, 1, running_time, board_size, succeed_threshold),
        ("minimax", "baseline", 1, 1, running_time, board_size, succeed_threshold),
        ("minimax", "baseline", 3, 1, running_time, board_size, succeed_threshold),
        ("minimax_alpha_beta", "baseline", 1, 1, running_time, board_size, succeed_threshold),
        ("minimax_alpha_beta", "baseline", 3, 1, running_time, board_size, succeed_threshold),
        ("minimax_alpha_beta", "baseline", 5, 1, running_time, board_size, succeed_threshold)
    ]

    with Pool() as pool:
        pool.starmap(start_experimentation, task1)

    task2 = [
        # against a minimax depth1 player
        ("baseline", "minimax", 1, 1, running_time, board_size, succeed_threshold),
        ("minimax", "minimax", 1, 1, running_time, board_size, succeed_threshold),
        ("minimax", "minimax", 3, 1, running_time, board_size, succeed_threshold),
        ("minimax_alpha_beta", "minimax", 1, 1, running_time, board_size, succeed_threshold),
        ("minimax_alpha_beta", "minimax", 3, 1, running_time, board_size, succeed_threshold),
        ("minimax_alpha_beta", "minimax", 5, 1, running_time, board_size, succeed_threshold)
    ]

    with Pool() as pool:
        pool.starmap(start_experimentation, task2)

    # against a baseline player
    start_experimentation("minimax_alpha_beta", "baseline", 7, 1, running_time, board_size, succeed_threshold)

    # against a minimax depth1 player
    start_experimentation("minimax_alpha_beta", "minimax", 7, 1, running_time, board_size, succeed_threshold)



def start_experimentation(player1_name,
                          player2_name,
                          player1_depth,
                          player2_depth,
                          running_time = 1,
                          board_size = 9,
                          succeed_threshold = 5):

    '''
    Start the experimentation

            Parameters:
                    player1_name (str): Player1's name
                    player1_depth (float/int): Player1's further search depth

                    player2_name (str): Player2's name
                    player2_depth (float/int): Player2's further search depth
    '''

    player1_time_list, player1_succeed_list, player1_stone_list, \
    player2_time_list, player2_succeed_list, player2_stone_list \
    = [], [], [], [], [], []

    f_name = f"{player1_name}_depth{player1_depth}_vs_{player2_name}_depth{player2_depth}"
    result = open(f"result/{f_name}", "w+")
    result.write(f"{player1_name} depth {player1_depth} vs. {player2_name} depth {player2_depth}")
    output = open(f"output/{f_name}", "w+")
    output.write(f"{player1_name} depth {player1_depth} vs. {player2_name} depth {player2_depth}")

    running_count = 0
    while running_count < running_time:
        if running_count <= 2:
            # only write some examples to file
            gomoku = Gomoku(board_size, succeed_threshold, player1_name, player2_name, player1_depth, player2_depth, output = output)
        else:
            gomoku = Gomoku(board_size, succeed_threshold, player1_name, player2_name, player1_depth, player2_depth)
        
        player1_mean_elapsed_time, player1_succeed_flag, player1_stone, player2_mean_elapsed_time, player2_succeed_flag, player2_stone = gomoku.game_statistics()
        player1_time_list.append(player1_mean_elapsed_time)
        player2_time_list.append(player2_mean_elapsed_time)

        player1_succeed_list.append(player1_succeed_flag)
        player2_succeed_list.append(player2_succeed_flag)

        player1_stone_list.append(player1_stone)
        player2_stone_list.append(player2_stone)
        running_count += 1

    player1_winning_count, player1_draw_count, player1_fail_count, player1_black_count,\
    player2_winning_count, player2_draw_count, player2_fail_count, player2_black_count\
    = player1_succeed_list.count(True), player1_succeed_list.count("Draw"), player1_succeed_list.count(False), player1_stone_list.count("B"),\
    player2_succeed_list.count(True), player2_succeed_list.count("Draw"), player2_succeed_list.count(False), player2_stone_list.count("B")
    player1_average_time, player2_average_time = mean(player1_time_list), mean(player2_time_list)
    result.write(f"\nPlayer1: {player1_name}:")
    result.write(f"\nblack stone ratio: {player1_black_count/running_count}, winning ratio: {player1_winning_count/running_count}, draw ratio: {player1_draw_count/running_count}, fail ratio: {player1_fail_count/running_count}, average time per step; {player1_average_time}s")
    result.write(f"\nPlayer2: {player2_name}:")
    result.write(f"\nblack stone ratio: {player2_black_count/running_count}, winning ratio: {player2_winning_count/running_count}, draw ratio: {player2_draw_count/running_count}, fail ratio: {player2_fail_count/running_count}, average time per step: {player2_average_time}s")
    
    result.close()
    output.close()


if __name__ == "__main__":
    main()