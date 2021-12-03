from Game import Game
from time import time
from math import inf
from copy import deepcopy
from refs import Character, GameState
from random import shuffle

class AlphaBetaPlayer:

    # Get best move for defender
    def pick_move(game : Game):
        start = time()
        high = -inf
        chosen_move = game.get_random_move()
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
        if depth == 0 or game.check_state() != GameState.ACTIVE:
            return game.evaluateBoard(player)

        if player == Character.ATTACKER:
            availablemoves = game.get_attacker_moves()
        elif player == Character.DEFENDER:
            availablemoves = game.get_defender_moves()
        else:
            availablemoves = []
        shuffle(availablemoves)

        if current_player_maximizing:
            best = -inf
            for move in availablemoves:
                gamecopy = deepcopy(game)
                if player == Character.ATTACKER:
                    gamecopy.attacker_play(move)
                else:
                    gamecopy.defender_play(move)
                
                value = AlphaBetaPlayer.minimax(depth - 1, False, gamecopy, alpha, beta, player)
                best = max(best, value)
                alpha = max(alpha, best)

                if beta <= alpha: break
        else:
            best = inf
            for move in availablemoves:
                gamecopy = deepcopy(game)
                if player == Character.ATTACKER:
                    gamecopy.attacker_play(move)
                else:
                    gamecopy.defender_play(move)
                
                value = AlphaBetaPlayer.minimax(depth - 1, True, gamecopy, alpha, beta, player)
                best = min(best, value)
                beta = min(beta, best)

                if beta <= alpha: break

        return best