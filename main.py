import sys

from AlphaBetaPlayer import AlphaBetaPlayer
from Game import Game

from refs import GameState
from Move import Move
from time import time

import pygame
from constants import BLACK, BLUE, GREEN, RED, WIDTH, HEIGHT, ROWS, COLS, SQUARE_SIZE, LIGHT_GREY, WHITE

from arguments import get_arguments

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Hnefatafl')

def get_median(data):
    data.sort()

    length = len(data)

    if length % 2 == 0:
        first = data[length // 2]
        second = data[length // 2 - 1]
        result = (first + second) / 2
    elif length % 2 > 0:
        result = data[length // 2]

    return result

def run(args=None):
    if args is None:
        args = sys.argv[1:]

    # parse arguments
    arguments = get_arguments()

    # select which algorithm to use based on arguments
    if arguments.algorithm == 'mcts':
        print('mcts algorithm selected')
    elif arguments.algorithm == 'ab':
        print('alpha-beta algorithm selected')
    elif arguments.algorithm:
        print('invalid agent algorithm argument')
        exit(1)

    if arguments.data_mode:
        # statistics
        data = []

        while(True):
            play(arguments, data)
    else:
        play(arguments)

def play(arguments=None, data=None):
    game = Game()
    game.setup_board()
    
    run = True
    clock = pygame.time.Clock()

    loop_sum = 0
    loops = 0
    avg_loop = 0
    attack_sum = 0
    avg_attack = 0
    defense_sum = 0
    avg_defense = 0
    while(run):
        if not arguments.data_mode:
            print('\n\n')
        loops += 1
        dur = time()

        #Handle game loop and events
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                if arguments.data_mode:
                    exit(1)

        #Display game in console and GUI
        #Get serial string representation of board
        boardStr = game.serialize()

        #Draw blank board in window
        WIN.fill(WHITE)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(
                    WIN, 
                    LIGHT_GREY, 
                    (
                        row*SQUARE_SIZE, 
                        col*SQUARE_SIZE, 
                        SQUARE_SIZE, 
                        SQUARE_SIZE
                    )
                )

        #Draw pieces
        for i in range(len(boardStr)):
            ch = boardStr[i]
            if ch == '0': continue

            row = i // 7
            col = i % 7

            #red attacker, blue defender, green king
            color = BLACK
            if ch == '1':
                color = RED
            if ch == '2':
                color = BLUE
            elif ch == '3':
                color = GREEN

            r = SQUARE_SIZE//2 - 20 #padding = 10
            x = SQUARE_SIZE * col + SQUARE_SIZE // 2
            y = SQUARE_SIZE * row + SQUARE_SIZE // 2
                
            pygame.draw.circle(WIN, BLACK, (x, y), r + 2) #outline = 2
            pygame.draw.circle(WIN, color, (x, y), r)

        #Update display
        pygame.display.update()

        #Display in console
        #game.display()
        if not arguments.data_mode:
            print(f"avg loop time: {avg_loop}")
            print(f"avg attack time: {avg_attack}")
            print(f"avg defense time: {avg_defense}")
            print(f"turns: {loops}")
        
        #Core game logic
        attackdur = time()
        attacker_move = game.get_random_attacker_input()
        #attacker_move = None
        #while attacker_move == None:
        #    attacker_move = game.get_move_input()
        game.attacker_play(attacker_move)
        game.add_turn()
        attackdur = time() - attackdur
        attack_sum += attackdur
        avg_attack = attack_sum / loops

        state = game.check_state()
        if state != GameState.ACTIVE:
            break
        #-----
        
        defensedur = time()
        # select which algorithm to use based on arguments
        if arguments.algorithm == 'mcts':
            defender_move = game.get_ai_input()
        elif arguments.algorithm == 'ab':
            defender_move = AlphaBetaPlayer.pick_move(game, arguments=arguments)
        game.defender_play(defender_move)
        game.add_turn()
        defensedur = time() - defensedur
        defense_sum += defensedur
        avg_defense = defense_sum / loops

        state = game.check_state()
        if state != GameState.ACTIVE:
            break

        if arguments.data_mode:
            if game.king in [(1, 2), (2, 1), (6, 7), (7, 6), (1, 6), (6, 1), (2, 7), (7, 2)]:
                break

        dur = time() - dur
        loop_sum += dur
        avg_loop = loop_sum / loops

        
    if arguments.data_mode:
        num_moves = game.get_clock() + 1
        data.append(num_moves)
        mean = (sum(data) / len(data))
        move_range = (max(data) - min(data))
        median = get_median(data)
        print(f"{len(data)} - {arguments.algorithm} reached win state in {num_moves} moves. Mean: {mean} moves. Median: {median} moves. Range: {move_range} moves.")
    else:
        print(f"Game is over with final result: {state} in {game.get_clock()} turns.")
        #loop so player can see end state until closed manually
        while(run):
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

if __name__ == "__main__":
    run()