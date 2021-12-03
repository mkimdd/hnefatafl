from enum import Enum

class Character(Enum):
    EMPTY = 0
    DEFENDER = 2
    ATTACKER = 1
    KING = 3

class SquareType(Enum):
    NORMAL = 1
    REFUGE = 2

class MoveStatus(Enum):
    SAME_LOCATION = 1
    OFF_AXIS = 2
    PATH_OCCUPIED = 3
    AVAILABLE = 4
    OUT_OF_BOUNDS = 5

class GameState(Enum):
    ACTIVE = 1
    ATTACKERS_WON = 2
    DEFENDERS_WIN = 3
    DRAW = 4

class KingEndState(Enum):
    CAPTURED = 1
    SAVED = 2
    NOTHING = 3

class Mode(Enum):
    ATTACKING = 1
    DEFENDING = 2