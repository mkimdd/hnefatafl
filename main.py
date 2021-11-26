from Game import Game

from refs import GameState

def play():
    game = Game()
    game.setup_board()
    while(True):
        game.display()
        while not game.attacker_play():
            continue
        game.add_turn()
        state = game.check_state()
        if state != GameState.ACTIVE:
            break
        game.display()
        while not game.defender_play():
            continue
        game.add_turn()
        state = game.check_state()
        if state != GameState.ACTIVE:
            break
    print(f"Game is over with final result: {state} in {game.get_clock()} turns.")

if __name__ == "__main__":
    play()