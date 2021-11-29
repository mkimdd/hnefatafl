import os
import random
import copy

from Square import Square
from refs import Character, KingEndState, MoveStatus, SquareType, GameState, Mode
from Move import Move
from Node import Node

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
        self.final = None

        # what the current game state is
        self.game_state = GameState.ACTIVE
        self.attackers_captured = 0
        self.defenders_captured = 0

    def get_board(self) -> dict:
        return self.board

    def get_attackers_captured(self) -> int:
        return self.attackers_captured

    def get_defenders_captured(self) -> int:
        return self.defenders_captured

    def perform(self, move: Move, mode: Mode):
        if mode == Mode.ATTACKING:
            self.attacker_play(move)
        else:
            self.defender_play(move)

    def get_ai_input(self) -> Move:
        return monte_carlo_tree_search(Node(g=self))

    def get_random_attacker_input(self) -> Move:
        return random.choice(self.get_attacker_moves())

    def in_bounds(self, destination: tuple) -> bool:
        if destination[0] < 1 or destination[0] > 11:
            return False
        if destination[1] < 1 or destination[1] > 11:
            return False
        return True

    def get_king_moves(self) -> list:
        moves = []
        defender = copy.deepcopy(self.king)
        # check upwards
        i = 1
        dest = (defender[0], defender[1]+i)
        while self.in_bounds(dest) and self.board[dest].is_available_for_king():
            moves.append(Move(defender, dest))
            i += 1
            dest = (defender[0], defender[1]+i)

        # check downwards
        i = 1
        dest = (defender[0], defender[1]-i)
        while self.in_bounds(dest) and self.board[dest].is_available_for_king():
            moves.append(Move(defender, dest))
            i += 1
            dest = (defender[0], defender[1]-i)
            
        # check left
        i = 1
        dest = (defender[0]-i, defender[1])
        while self.in_bounds(dest) and self.board[dest].is_available_for_king():
            moves.append(Move(defender, dest))
            i += 1
            dest = (defender[0]-i, defender[1])

        # check right
        i = 1
        dest = (defender[0]+i, defender[1])
        while self.in_bounds(dest) and self.board[dest].is_available_for_king():
            moves.append(Move(defender, dest))
            i += 1
            dest = (defender[0]+i, defender[1])
        return moves

    def get_attacker_moves(self) -> list:
        moves = []
        for attacker in self.attackers:

            # check upwards
            i = 1
            dest = (attacker[0], attacker[1]+i)
            while self.in_bounds(dest) and self.board[dest].is_available_for_attacker():
                moves.append(Move(attacker, dest))
                i += 1
                dest = (attacker[0], attacker[1]+i)

            # check downwards
            i = 1
            dest = (attacker[0], attacker[1]-i)
            while self.in_bounds(dest) and self.board[dest].is_available_for_attacker():
                moves.append(Move(attacker, dest))
                i += 1
                dest = (attacker[0], attacker[1]-i)
            
            # check left
            i = 1
            dest = (attacker[0]-i, attacker[1])
            while self.in_bounds(dest) and self.board[dest].is_available_for_attacker():
                moves.append(Move(attacker, dest))
                i += 1
                dest = (attacker[0]-i, attacker[1])

            # check right
            i = 1
            dest = (attacker[0]+i, attacker[1])
            while self.in_bounds(dest) and self.board[dest].is_available_for_attacker():
                moves.append(Move(attacker, dest))
                i += 1
                dest = (attacker[0]+i, attacker[1])
        
        return moves
    
    def get_defender_moves(self) -> list:
        moves = []
        for defender in self.defenders:

            # check upwards
            i = 1
            dest = (defender[0], defender[1]+i)
            while self.in_bounds(dest) and self.board[dest].is_available_for_defender():
                moves.append(Move(defender, dest))
                i += 1
                dest = (defender[0], defender[1]+i)

            # check downwards
            i = 1
            dest = (defender[0], defender[1]-i)
            while self.in_bounds(dest) and self.board[dest].is_available_for_defender():
                moves.append(Move(defender, dest))
                i += 1
                dest = (defender[0], defender[1]-i)
            
            # check left
            i = 1
            dest = (defender[0]-i, defender[1])
            while self.in_bounds(dest) and self.board[dest].is_available_for_defender():
                moves.append(Move(defender, dest))
                i += 1
                dest = (defender[0]-i, defender[1])

            # check right
            i = 1
            dest = (defender[0]+i, defender[1])
            while self.in_bounds(dest) and self.board[dest].is_available_for_defender():
                moves.append(Move(defender, dest))
                i += 1
                dest = (defender[0]+i, defender[1])

        king_moves = self.get_king_moves()
        for move in king_moves:
            moves.append(move)
        
        return moves

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

    def get_move_input(self) -> Move:
        try:
            move = input("Command >>> ")
            move.strip()
            pox = move.split(' ')
            source = pox[0].split(',')
            source = (int(source[0]), int(source[1]))
            dest = pox[1].split(',')
            dest = (int(dest[0]), int(dest[1]))
            return Move(source, dest)
        except:
            print("INVALID COMMAND... EXITING")
            exit()

    def attacker_play(self, move: Move) -> bool:
        """Performs attacker move."""
        source, dest = move.get_source(), move.get_destination()

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

    def defender_play(self, move: Move) -> bool:
        """Performs defender move."""
        source, dest = move.get_source(), move.get_destination()

        character = self.board[source].get_occupied()
        if character == Character.DEFENDER or character == Character.KING:
            if self.board[dest].is_available_for_defender():
                status = self.check_path(source, dest)
                if status == MoveStatus.AVAILABLE:
                    if character == Character.DEFENDER:
                        self.board[dest].move_defender_here()
                        self.defenders.remove(source)
                        self.defenders.append(dest)
                        self.board[source].clear()
                    else:
                        self.board[dest].move_king_here()
                        self.king = dest
                        self.board[source].clear()
                    return True
                else:
                    print(f"Unable to perform move... Status: {status}")

        return False

    def plus_position(self, loc: tuple, mod: tuple) -> tuple:
        return (loc[0] + mod[0], loc[1] + mod[1])

    def get_king_md_to_safe(self) -> int:
        """Returns the Manhattan Distance from the King to the nearest win Square."""
        safe_squares = [(1,1), (1,11), (11,1), (11,11)]
        mds = []
        for square in safe_squares:
            md = abs(self.final[0]-square[0]) + abs(self.final[1]-square[1])
            mds.append(md)
        return min(mds)

    def check_king(self) -> KingEndState:
        """Check if the king has been captured or saved."""
        moves = [
            (1, 0),
            (0, 1),
            (-1, 0),
            (0, -1)
        ]
        captured = True
        for move in moves:
            reach = self.plus_position(self.king, move)
            if self.in_bounds(reach):
                if self.board[self.plus_position(self.king, move)].get_occupied() != Character.ATTACKER:
                    captured = False
                    break
            else:
                captured = False
                break
        if captured:
            self.final = self.king
            self.king = None
            return KingEndState.CAPTURED

        corners = [(1, 1), (1, 11), (11, 1), (11, 11)]
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

        if self.in_bounds(left) and self.in_bounds(right):
            if self.board[left].get_occupied() == target and self.board[right].get_occupied() == target:
                return True

        if self.in_bounds(up) and self.in_bounds(down):
            if self.board[up].get_occupied() == target and self.board[down].get_occupied() == target:
                return True

        return False

    def check_pieces(self):
        for attacker in self.attackers:
            if self.check_capture(attacker, Character.ATTACKER):
                self.attackers.remove(attacker)
                self.board[attacker].clear()
                self.attackers_captured += 1
        for defender in self.defenders:
            if self.check_capture(defender, Character.DEFENDER):
                self.defenders.remove(defender)
                self.board[defender].clear()
                self.defenders_captured += 1

    def check_state(self) -> GameState:
        king_status = self.check_king()
        if king_status == KingEndState.CAPTURED:
            self.game_state = GameState.ATTACKERS_WON
            return GameState.ATTACKERS_WON
        if king_status == KingEndState.SAVED:
            self.game_state = GameState.DEFENDERS_WIN
            self.final = self.king
            return GameState.DEFENDERS_WIN
        
        self.check_pieces()

        if self.clock > 250:
            self.final = self.king
            return GameState.DRAW
        return GameState.ACTIVE

    def add_turn(self):
        """Adds a turn to the Game clock."""
        self.clock += 1

    def get_clock(self) -> int:
        return self.clock

    def display(self):
        """Handles the 'graphics' of the Game."""
        os.system('cls' if os.name == 'nt' else 'clear') # this will only work for Windows
        corner = "---"
        print(f"{corner:5}", end='')
        for i in range(1, 12):
            print(f"{str(i):5}", end='')
        print()
        print()
        for y in range(1, 12):
            print(f"{str(y):5}", end='')
            for x in range(1, 12):
                print(f"{self.board[(x, y)].to_string():5}", end='')
            print()
            print()
        print()
        print(f"Game Status: {self.game_state}")

def selection(focus: Node) -> Node:
    """Returns the best node for Defense."""
    targets = focus.children
    targets.sort(key=lambda x: x.confidence(), reverse=True)
    if not targets:
        return focus
    return targets[0]

def expansion(game: Game, focus: Node, mode: Mode):
    """Expands given leaf node with all possible next states."""
    n = 10
    moves = random.sample(game.get_attacker_moves(), n) if mode == Mode.ATTACKING else random.sample(game.get_defender_moves(), n)
    for move in moves:
        novel = Node(parent=focus, m=move, g=copy.deepcopy(game))
        focus.children.append(novel)

def terminal(simulation: Game) -> tuple:
    state = simulation.check_state()
    if state != GameState.ACTIVE:
        return (True, state)
    return (False, state)

def rollout(game: Game, mode: Mode) -> Game:
    """Performs a simulation from the current state of the given Game."""
    simulation = copy.deepcopy(game)
    ender = None
    
    while True:
        #print(">>>SIMULATION<<<")
        #simulation.display()
        if mode == Mode.ATTACKING:
            try:
                attacker_move = random.choice(simulation.get_attacker_moves())
            except IndexError:
                ender = (True, GameState.DEFENDERS_WIN)
                break
            simulation.perform(attacker_move, mode)
            simulation.add_turn()
            ender = terminal(simulation)
            if ender[0]:
                break
            mode = Mode.DEFENDING
            #print(simulation.king)
        else:
            try:
                defender_move = random.choice(simulation.get_defender_moves())
            except IndexError:
                ender = (True, GameState.ATTACKERS_WON)
                break
            simulation.perform(defender_move, mode)
            simulation.add_turn()
            ender = terminal(simulation)
            if ender[0]:
                break
            mode = Mode.ATTACKING
            #print(simulation.king)

    status = ender[1]
    value = 0
    if status == GameState.ATTACKERS_WON:
        value = -1 * simulation.get_clock()
    elif status == GameState.DEFENDERS_WIN:
        value = simulation.get_clock()
    elif status == GameState.DRAW:
        #value = (25 - simulation.get_defenders_captured()) + simulation.get_attackers_captured()
        value = 20 - simulation.get_king_md_to_safe()
    return value

def backpropogate(focus: Node, result: int):
    while focus.parent != None:
        focus.update(result)
        focus = focus.parent

def best_move(focus: Node) -> Move:
    targets = focus.children
    targets.sort(key=lambda x: x.get_n(), reverse=True)
    return targets[0].get_move()

def monte_carlo_tree_search(root: Node) -> Move:
    MAX_TIME = 100
    clock = 0
    leaf = root
    current_mode = Mode.DEFENDING

    while clock < MAX_TIME:
        #print(f"Starting cycle {clock} out of {MAX_TIME}...")
        #print("Defender selecting...")
        leaf = selection(leaf)
        #print("Defender expanding...")
        expansion(leaf.get_game(), leaf, current_mode)
        leaf = random.choice(leaf.children)
        #print("Defender simulating...")
        value = rollout(leaf.get_game(), current_mode)
        #print("Defender backpropogating...")
        backpropogate(leaf, value)

        # update loop variables
        clock += 1
        if current_mode == Mode.DEFENDING:
            current_mode = Mode.ATTACKING
        else:
            current_mode = Mode.DEFENDING

    return best_move(root)