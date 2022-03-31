from Gomoku import Gomoku

def main():

    running_count = 0
    running_time = 1
    board_size = 2
    suceed_threshold = 2

    player1_time_list, player1_succeed_list, player2_time_list, player2_succeed_list = [], [], [], []
    while running_count < running_time:
        # gomoku = Gomoku(board_size, suceed_threshold, "minimax", "minimax")
        gomoku = Gomoku(board_size, suceed_threshold, "minimax_alph_beta_prune", "minimax_alph_beta_prune")
        player1_mean_elapsed_time, player1_succeed_flag, player2_mean_elapsed_time, player2_succeed_flag = gomoku.game_statistics()
        
        player1_time_list.append(player1_mean_elapsed_time)
        player2_time_list.append(player2_mean_elapsed_time)

        player1_succeed_list.append(player1_succeed_flag)
        player2_succeed_list.append(player2_succeed_flag)
        running_count += 1
    print(player1_time_list)
    print(player1_succeed_list)

    print(player2_time_list)
    print(player2_succeed_list)

if __name__ == "__main__":
    main()