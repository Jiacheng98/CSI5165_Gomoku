from Board import Board
from Player import *

import random
from datetime import datetime
# random.seed(1)
random.seed(datetime.now())

import numpy as np
import time
import globals
from statistics import mean
from GameState import GameState

class Gomoku:
    def __init__(self, board_size, suceed_threshold, player1, player2, player1_depth = float('inf'), player2_depth = float('inf')):
        # initialize the board
        self.board = Board(board_size)
        print(f"Initialize the board: \n{self.board}")

        # initialize the game_state
        self.game_state = GameState(self.board.board)

        # initialize white(W)/black(B) stone 
        stone = ['W', 'B']
        player1_stone = random.choice(stone)
        stone.remove(player1_stone)
        player2_stone = stone[0]
        print(f"Player1: {player1_stone}, strategy: {player1}, seach tree depth: {player1_depth}\
              \nPlayer2: {player2_stone}, strategy: {player2}, search tree depth: {player2_depth}")

        # initialize player
        if player1 == "minimax":
            self.player1 = MinimaxPlayer("Player1", player1_stone, player1_depth, suceed_threshold)
        if player2 == "minimax":
          self.player2 = MinimaxPlayer("Player2", player2_stone, player2_depth, suceed_threshold)

        if player1 == "minimax_alph_beta_prune":
            self.player1 = MinimaxAlphaBetaPrunePlayer("Player1", player1_stone, player1_depth, suceed_threshold)
        if player2 == "minimax_alph_beta_prune":
            self.player2 = MinimaxAlphaBetaPrunePlayer("Player2", player2_stone, player2_depth, suceed_threshold)

        # start the game
        self.game_start()


    def game_start(self):
        print("Game Start! Black plays first!")

        while True:
            # black plays first
            if self.player1.stone == "B":
                first, second = self.player1, self.player2
            else:
                first, second = self.player2, self.player1
            
            game_over = self.game_play(first)
            if game_over: 
                break
            game_over = self.game_play(second)
            if game_over: 
                break


    def game_play(self, player):
        print(f"{player.name}'s turn:")

        globals.init()
        start_time = time.time()
        # place_stone() method returns the next game_state object
        self.game_state = player.place_stone(self.game_state, player.depth, True)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(self.game_state)
        print(f"Number of visited game states: {globals.count}, dictionary size: {len(globals.game_state_dict)}")
        print(f"{player.name} elapsed time: {end_time - start_time}")
        player.elapsed_time_list.append(elapsed_time)

        print(self.game_state.game_board, self.game_state.row, self.game_state.column)
        print(self.game_state.game_over)        
        if self.game_state.game_over:
            if self.game_state.utility > 0:
                player.succeed_flag = True
                if player == self.player1:
                    self.player2.succeed_flag = False
                elif player == self.player2:
                    self.player1.succeed_flag = False
                print(f" Congratulations! {player.name} wins!")
                return True
            elif self.game_state.utility < 0:
                player.succeed_flag = False
                if player == self.player1:
                    self.player2.succeed_flag = True
                elif player == self.player2:
                    self.player1.succeed_flag = True
                print(f" Congratulations! {player.name} wins!")
                return True
            else:
                self.player1.succeed_flag = "Draw"
                self.player2.succeed_flag = "Draw"
                print(f"Game over! Draw!")
                return True

        return False

    def game_statistics(self):
        return mean(self.player1.elapsed_time_list), self.player1.succeed_flag, mean(self.player2.elapsed_time_list), self.player2.succeed_flag

