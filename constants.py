import pygame

WIDTH, HEIGHT = 800, 800
ROWS = COLS = BOARD_SIZE = 7
SQUARE_SIZE = WIDTH//BOARD_SIZE

# serialized representation of the starting configuration of the board, 0 = empty, 1 = attacker, 2 = defender, 3 = king
START_STRING = "00011111000"\
                "00000100000"\
                "00000000000"\
                "10000200001"\
                "10002220001"\
                "11022322011"\
                "10002220001"\
                "10000200001"\
                "00000000000"\
                "00000100000"\
                "00011111000"

# RGB Values
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
LIGHT_GREY = (211, 211, 211)
BLACK = (0, 0, 0)