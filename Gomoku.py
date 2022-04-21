from Board import Board
from Player import *

import random
from datetime import datetime
# random.seed(1)

import numpy as np
import time
import globals
from statistics import mean
from GameState import GameState

class Gomoku:
    """
    A class to represent a game. Each game contains one board, multiple game states, player1 and player2.

    ...

    Attributes
    ----------
    board_size : int
    succeed_threshold : int
        3 in a row or 5 in a row?
    player1 : str
    player2: str
    player1_depth: float/int
    player2_depth: float/int
    output: str
        write output to a file

    """

    def __init__(self, board_size, succeed_threshold, player1, player2, player1_depth = float('inf'), player2_depth = float('inf'), output = None):
        # initialize the board
        self.board = Board(board_size)
        self.output = output
        if self.output != None:
            self.output.write(f"\nInitialize the board: \n{self.board}")
            # print(f"\nInitialize the board: \n{self.board}")
        # initialize the game_state
        self.game_state = GameState(self.board.board)

        # initialize white(W)/black(B) stone 
        stone = ['W', 'B']
        player1_stone = random.choice(stone)
        stone.remove(player1_stone)
        player2_stone = stone[0]
        if self.output != None:
            self.output.write(f"\nPlayer1: {player1_stone}, strategy: {player1}, seach tree depth: {player1_depth}\
              \nPlayer2: {player2_stone}, strategy: {player2}, search tree depth: {player2_depth}")
            # print(f"\nPlayer1: {player1_stone}, strategy: {player1}, seach tree depth: {player1_depth}\
                  # \nPlayer2: {player2_stone}, strategy: {player2}, search tree depth: {player2_depth}")

        # initialize players
        if player1 == "minimax":
            self.player1 = MinimaxPlayer("Player1", player1_stone, player1_depth, succeed_threshold)
        if player2 == "minimax":
            self.player2 = MinimaxPlayer("Player2", player2_stone, player2_depth, succeed_threshold)

        if player1 == "minimax_alpha_beta":
            self.player1 = MinimaxAlphaBetaPrunePlayer("Player1", player1_stone, player1_depth, succeed_threshold)
        if player2 == "minimax_alpha_beta":
            self.player2 = MinimaxAlphaBetaPrunePlayer("Player2", player2_stone, player2_depth, succeed_threshold)

        if player1 == "baseline":
            self.player1 = BaselinePlayer("Player1", player1_stone, succeed_threshold)
        if player2 == "baseline":
            self.player2 = BaselinePlayer("Player2", player2_stone, succeed_threshold)

        # start the game
        self.game_start()


    def game_start(self):

        if self.output != None:
            self.output.write("\nGame Start! Black plays first!")
            # print("\nGame Start! Black plays first!")
        while True:
            # black always plays first
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
        if self.output != None:
            self.output.write(f"\n{player.name}'s turn:")
            # print(f"\n{player.name}'s turn:")
        # initialize global variables for each turn
        globals.init()

        start_time = time.time()
        # place_stone(): returns the next game_state
        self.game_state = player.place_stone(self.game_state, player.depth, True)
        end_time = time.time()
        elapsed_time = end_time - start_time
        player.elapsed_time_list.append(elapsed_time)

        if self.output != None:
            self.output.write(f"\n{self.game_state}")
            # print(f"\n{self.game_state}")
        if self.output != None:
            self.output.write(f"\n{player.name} elapsed time: {end_time - start_time}")
            # print(f"\n{player.name} elapsed time: {end_time - start_time}")
        if self.output != None:
            self.output.write(f"\nNumber of visited game states: {globals.count}, dictionary size: {len(globals.game_state_dict)}")
            # print(f"\nNumber of visited game states: {globals.count}, dictionary size: {len(globals.game_state_dict)}")

        # check whether the current game_state is a terminal state
        if self.game_state.game_over:
            if self.game_state.utility > 0:
                player.succeed_flag = True
                if player == self.player1:
                    self.player2.succeed_flag = False
                elif player == self.player2:
                    self.player1.succeed_flag = False
                if self.output != None:
                    self.output.write(f"\n Congratulations! {player.name} wins!")
                    # print(f"\n Congratulations! {player.name} wins!")
                return True
            elif self.game_state.utility < 0:
                player.succeed_flag = False
                if player == self.player1:
                    self.player2.succeed_flag = True
                elif player == self.player2:
                    self.player1.succeed_flag = True
                if self.output != None:
                    self.output.write(f"\n Congratulations! {player.name} wins!")
                    # print(f"\n Congratulations! {player.name} wins!")
                return True
            else:
                self.player1.succeed_flag = "Draw"
                self.player2.succeed_flag = "Draw"
                if self.output != None:
                    self.output.write(f"\nGame over! Draw!")
                    # print(f"\nGame over! Draw!")
                return True

        return False

    def game_statistics(self):
        '''

        For player1 and player2, calculate the average search time per step and succeed/failed/draw.

        '''
        return mean(self.player1.elapsed_time_list), self.player1.succeed_flag, self.player1.stone, mean(self.player2.elapsed_time_list), self.player2.succeed_flag, self.player2.stone

