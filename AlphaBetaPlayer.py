from Game import Game
from time import time
from math import inf
from copy import deepcopy
from Move import Move
from refs import Character, GameState
from random import shuffle

class AlphaBetaPlayer:

    # Get best move for defender
    def pick_move(game : Game) -> Move:
        start = time()
        high = -inf
        chosen_move = game.get_random_defender_move()
        for move in game.get_defender_moves():
            gamecopy = deepcopy(game)
            gamecopy.defender_play(move)
            value = AlphaBetaPlayer.minimax(2, False, gamecopy, -inf, inf, Character.DEFENDER)
            if value > high:
                high = value
                chosen_move = move

        end = time()
        print(f"Move chosen in {end-start} seconds.")
        return chosen_move

    
    def minimax(depth : int, current_player_maximizing : bool, game : Game, alpha : int, beta : int, player : Character):
        gamestate = game.check_state()
        if depth == 0 or gamestate != GameState.ACTIVE:
            h = game.get_board_heuristic(player)
            return h

        if current_player_maximizing: #defender
            availablemoves = game.get_defender_moves()
            shuffle(availablemoves)
            
            value = -inf
            for move in availablemoves:
                gamecopy = deepcopy(game)
                gamecopy.defender_play(move)
                
                newvalue = AlphaBetaPlayer.minimax(depth - 1, False, gamecopy, alpha, beta, player)
                value = max(value, newvalue)
                alpha = max(alpha, value)

                if value >= beta: break

        else: #attacker
            availablemoves = game.get_attacker_moves()
            shuffle(availablemoves)

            value = inf
            for move in availablemoves:
                gamecopy = deepcopy(game)
                gamecopy.attacker_play(move)
                
                newvalue = AlphaBetaPlayer.minimax(depth - 1, True, gamecopy, alpha, beta, player)
                value = min(value, newvalue)
                beta = min(beta, value)

                if value <= alpha: break

        return value