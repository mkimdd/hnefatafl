import os

from Square import Square
from refs import Character, KingEndState, MoveStatus, SquareType, GameState

class Game:
    """Represents Hnefatafl game."""

    def __init__(self):
        """Intializes Game fields."""

        # represents how many turns have been played
        self.clock = 0

        # holds all the Squares representing the board
        self.board = {}
        for y in range(1, 12):
            for x in range(1, 12):
                self.board[(x, y)] = Square((x, y))

        # holds all the locations of attackers, defenders, refuge squares, and the king
        self.attackers = []
        self.defenders = []
        self.refuge = []
        self.king = (6, 6)

        # what the current game state is
        self.game_state = GameState.ACTIVE

        self.moves = [
            (1, 0),
            (0, 1),
            (-1, 0),
            (0, -1)
        ]

    def setup_board(self):
        """Sets up the board with a predefined starting arrangement."""
        # setup refuge squares
        refuge_lox = [
            (1, 1),
            (1, 11),
            (11, 1),
            (11, 11),
            (6, 6)
        ]
        for loc in refuge_lox:
            self.board[loc].set_type(SquareType.REFUGE)
            self.refuge.append(loc)
        # setup squares with attackers
        attacker_lox = [
            (1, 4),
            (1, 5),
            (1, 6),
            (1, 7),
            (1, 8),
            (2, 6),
            (4, 1),
            (4, 11),
            (5, 1),
            (5, 11),
            (6, 1),
            (6, 2),
            (6, 10),
            (6, 11),
            (7, 1),
            (7, 11),
            (8, 1),
            (8, 11),
            (10, 6),
            (11, 4),
            (11, 5),
            (11, 6),
            (11, 7),
            (11, 8)
        ]
        for loc in attacker_lox:
            self.board[loc].set_character(Character.ATTACKER)
            self.attackers.append(loc)
        # setup squares with defenders
        defender_lox = [
            (4, 6),
            (5, 5),
            (5, 6),
            (5, 7),
            (6, 4),
            (6, 5),
            (6, 7),
            (6, 8),
            (7, 5),
            (7, 6),
            (7, 7),
            (8, 6)
        ]
        for loc in defender_lox:
            self.board[loc].set_character(Character.DEFENDER)
            self.defenders.append(loc)
        # setup square with king
        self.board[(6, 6)].set_character(Character.KING)

    def check_path(self, source: tuple, destination: tuple) -> MoveStatus:
        """Checks if the given move is legal."""

        # make sure destination is not the same spot
        if source == destination:
            return MoveStatus.SAME_LOCATION

        # make sure destination is a possible square to go to
        if source[0] != destination[0] and source[1] != destination[1]:
            return MoveStatus.OFF_AXIS

        # make sure destination is a possible square to go to
        if destination[0] < 1 or destination[0] > 11 or destination[1] < 1 or destination[1] > 11:
            return MoveStatus.OUT_OF_BOUNDS

        # make sure nothing is in the way of the character as it attempts to move
        if source[0] == destination[0]:
            x = source[0]
            direction = 1 if source[1] < destination[1] else -1
            for y in range(source[1]+direction, destination[1]+direction, direction):
                if self.board[(x, y)].get_occupied() != Character.EMPTY:
                    return MoveStatus.PATH_OCCUPIED
        else:
            y = source[1]
            direction = 1 if source[0] < destination[0] else -1
            for x in range(source[0]+direction, destination[0]+direction, direction):
                if self.board[(x, y)].get_occupied() != Character.EMPTY:
                    return MoveStatus.PATH_OCCUPIED

        return MoveStatus.AVAILABLE

    def attacker_play(self) -> bool:
        """Performs attacker move."""
        # TODO fix smell, command input wacked out
        try:
            move = input("Command >>> ")
            move.strip()
            pox = move.split(' ')
            source = pox[0].split(',')
            source = (int(source[0]), int(source[1]))
            dest = pox[1].split(',')
            dest = (int(dest[0]), int(dest[1]))
        except:
            print("INVALID COMMAND... EXITING")
            exit()

        # makes the Attacker move is possible
        if self.board[source].get_occupied() == Character.ATTACKER:
            if self.board[dest].is_available_for_attacker():
                status = self.check_path(source, dest)
                if status == MoveStatus.AVAILABLE:
                    self.board[dest].move_attacker_here()
                    self.attackers.remove(source)
                    self.attackers.append(dest)
                    self.board[source].clear()
                    return True
                else:
                    print(f"Unable to perform move... Status: {status}")
        
        return False

    def defender_play(self) -> bool:
        """Performs defender move."""
        return True

    def plus_position(self, loc: tuple, mod: tuple) -> tuple:
        return (loc[0] + mod[0], loc[1] + mod[1])

    def check_king(self) -> KingEndState:
        """Check if the king has been captured or saved."""
        captured = True
        for move in self.moves:
            if self.board[self.plus_position(self.king, move)].get_occupied() != Character.ATTACKER:
                captured = False
                break
        if captured:
            return KingEndState.CAPTURED

        corners = {(1, 1), (1, 11), (11, 1), (11, 11)}
        if self.king in corners:
            return KingEndState.SAVED

        return KingEndState.NOTHING

    def check_capture(self, loc: tuple, type: Character) -> bool:
        """Checks if a piece has been captured."""
        if type == Character.ATTACKER:
            target = Character.DEFENDER
        else:
            target = Character.ATTACKER

        left = (loc[0]-1, loc[1])
        right = (loc[0]+1, loc[1])
        up = (loc[0], loc[1]+1)
        down = (loc[0], loc[1]-1)

        try:
            if self.board[left].get_occupied() == target and self.board[right].get_occupied() == target:
                return True
        except KeyError:
            pass

        try:
            if self.board[up].get_occupied() == target and self.board[down].get_occupied() == target:
                return True
        except KeyError:
            pass

        return False

    def check_pieces(self):
        for attacker in self.attackers:
            if self.check_capture(attacker, Character.ATTACKER):
                self.attackers.remove(attacker)
                self.board[attacker].clear()
        for defender in self.defenders:
            if self.check_capture(defender, Character.DEFENDER):
                self.defenders.remove(defender)
                self.board[defender].clear()

    def check_state(self) -> GameState:
        king_status = self.check_king()
        if king_status == KingEndState.CAPTURED:
            self.game_state = GameState.ATTACKERS_WON
            return GameState.ATTACKERS_WON
        if king_status == KingEndState.SAVED:
            self.game_state = GameState.DEFENDERS_WIN
            return GameState.DEFENDERS_WIN
        
        self.check_pieces()
        return GameState.ACTIVE

    def add_turn(self):
        """Adds a turn to the Game clock."""
        self.clock += 1

    def get_clock(self) -> int:
        return self.clock

    def display(self):
        """Handles the 'graphics' of the Game."""
        os.system('cls' if os.name == 'nt' else 'clear') # this will only work for Windows
        for y in range(1, 12):
            for x in range(1, 12):
                print(f"{self.board[(x, y)].to_string()}   ", end='')
            print()
            print()
        print()
        print(f"Game Status: {self.game_state}")