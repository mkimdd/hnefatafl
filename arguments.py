import argparse

def get_arguments(arguments=None):
    parser = argparse.ArgumentParser(
        prog='main')

    parser.add_argument('-a', '--algorithm',
        default='mcts',
        help='game agent algorithm to use')

    parser.add_argument('-d', '--data_mode',
        action='store_true',
        help='run in data collection mode')

    ARGUMENTS = parser.parse_args(arguments)
    return ARGUMENTS