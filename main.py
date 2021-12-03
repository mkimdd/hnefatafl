from Game2 import Game

from refs import GameState
from Move import Move

import pygame
from constants import BLACK, BLUE, GREEN, RED, WIDTH, HEIGHT, ROWS, COLS, SQUARE_SIZE, LIGHT_GREY, WHITE

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Hnefatafl')


def play():

    game = Game()
    game.setup_board()
    
    run = True
    clock = pygame.time.Clock()

    while(run):

        #Handle game loop and events
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

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
        game.display()
        
        #Core game logic
        attacker_move = game.get_random_attacker_input()
        #attacker_move = None
        #while attacker_move == None:
        #    attacker_move = game.get_move_input()
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
        

    print(f"Game is over with final result: {state} in {game.get_clock()} turns.")

if __name__ == "__main__":
    play()