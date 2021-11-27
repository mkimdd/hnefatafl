from Game import Game

from refs import GameState
from Move import Move

def play():
    game = Game()
    game.setup_board()
    while(True):
        game.display()
        attacker_move = None
        while attacker_move == None:
            attacker_move = game.get_move_input()
        game.attacker_play(attacker_move)
        game.add_turn()
        state = game.check_state()
        if state != GameState.ACTIVE:
            break
        #-----
        game.display()
        defender_move = game.get_ai_input()
        game.defender_play(defender_move)
        game.add_turn()
        state = game.check_state()
        if state != GameState.ACTIVE:
            break
    print(f"Game is over with final result: {state} in {game.get_clock()} turns.")

if __name__ == "__main__":
    play()