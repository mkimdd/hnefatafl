# NOT CURRENTLY USED

import random
import copy

from Node import Node
from Move import Move
from Game import Game
from refs import Mode, GameState

def selection(focus: Node) -> Node:
    """Returns the best node for Defense."""
    targets = focus.children
    targets.sort(key=lambda x: x.confidence(), reverse=True)
    return targets[0]

def expansion(game: Game, focus: Node, mode: Mode):
    """Expands given leaf node with all possible next states."""
    moves = game.get_attacker_moves() if mode == Mode.ATTACKING else game.get_defender_moves()
    for move in moves:
        novel = Node(focus, move)
        focus.children.append(novel)

def terminal(simulation: Game) -> bool:
    state = simulation.check_state()
    if state != GameState.ACTIVE:
        return True
    return False

def rollout(game: Game, mode: Mode) -> Game:
    """Performs a simulation from the current state of the given Game."""
    simulation = copy.deepcopy(game)
    
    while True:
        if mode == Mode.ATTACKING:
            attacker_move = random.choice(simulation.get_attacker_moves())
            simulation.perform(attacker_move)
            simulation.add_turn()
            if terminal(simulation):
                break
            mode = Mode.DEFENDING
        else:
            defender_move = random.choice(simulation.get_defender_moves())
            simulation.perform(defender_move)
            simulation.add_turn()
            if terminal(simulation):
                break
            mode = Mode.ATTACKING

    status = simulation.check_state()
    value = 0
    if status == GameState.ATTACKERS_WON:
        value = -1 * simulation.get_clock()
    elif status == GameState.DEFENDERS_WIN:
        value = simulation.get_clock()
    elif status == GameState.DRAW:
        value = -1
    return value

def backpropogate(focus: Node, result: int):
    while focus.parent != None:
        focus.update(result)
        focus = focus.parent

def best_move(focus: Node) -> Move:
    targets = focus.children
    targets.sort(key=lambda x: x.confidence(), reverse=True)
    return targets[0].get_move()

def monte_carlo_tree_search(game: Game, root: Node) -> Move:
    MAX_TIME = 100
    clock = 0
    focus = root
    current_mode = Mode.DEFENDING

    while clock < MAX_TIME:
        leaf = selection(focus)
        expansion(game, leaf, current_mode)
        leaf = random.choice(leaf.children)
        value = rollout(game, current_mode)
        backpropogate(focus, value)

        # update loop variables
        clock += 1
        if current_mode == Mode.DEFENDING:
            current_mode = Mode.ATTACKING
        else:
            current_mode = Mode.DEFENDING

    return best_move(focus)