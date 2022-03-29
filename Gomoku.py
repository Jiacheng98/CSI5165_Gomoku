from Board import Board
from Player import *

import random
import numpy as np
import time

class Gomoku:
    def __init__(self, board_size, player1, player2, player1_depth = float('inf'), player2_depth = float('inf')):
        # initialize the board
        self.board = Board(board_size)
        print(f"Initialize the board: \n{self.board}")

        # initialize white(W)/black(B) stone 
        stone = ['W', 'B']
        player1_stone = random.choice(stone)
        stone.remove(player1_stone)
        player2_stone = stone[0]
        print(f"Player1: {player1_stone}, strategy: {player1}, seach tree depth: {player1_depth}\
              \nPlayer2: {player2_stone}, strategy: {player2}, search tree depth: {player2_depth}")

        # initialize player
        if player1 == "minimax":
            self.player1 = MinimaxPlayer("Player1", player1_stone, player1_depth)

        if player2 == "minimax":
          self.player2 = MinimaxPlayer("Player2", player2_stone, player2_depth)

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
        start_time = time.time()
        self.board.board, value = player.place_stone(self.board.board, player.depth, True)
        end_time = time.time()
        print(f"{player.name} elapsed time: {end_time - start_time}")
        print(self.board)
        print(player.game_state_utility(self.board.board)[0])
        
        if player.game_state_utility(self.board.board)[0] == True:
            if player.game_state_utility(self.board.board)[1] > 0:
                print(f" Congratulations! {player.name} wins!")
                return True
            elif player.game_state_utility(self.board.board)[1] < 0:
                print(f" Congratulations! Player2 wins!")
                return True
            elif player.game_state_utility(self.board.board)[1] == 0:
                print(f"Game over! Draw!")
                return True

        return False
