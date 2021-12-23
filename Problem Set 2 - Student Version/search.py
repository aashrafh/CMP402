from typing import Tuple
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented

# TODO: Import any modules you want to use
import math

# All search functions take a problem, a state, a heuristic function and the maximum search depth.
# If the maximum search depth is -1, then there should be no depth cutoff (The expansion should not stop before reaching a terminal state)

# All the search functions should return the expected tree value and the best action to take based on the search results

# This is a simple search function that looks 1-step ahead and returns the action that lead to highest heuristic value.
# This algorithm is bad if the heuristic function is weak. That is why we use minimax search to look ahead for many steps.


def greedy(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    agent = game.get_turn(state)

    terminal, values = game.is_terminal(state)
    if terminal:
        return values[agent], None

    actions_states = [(action, game.get_successor(state, action))
                      for action in game.get_actions(state)]
    value, _, action = max((heuristic(game, state, agent), -index, action)
                           for index, (action, state) in enumerate(actions_states))
    return value, action

# Apply Minimax search and return the tree value and the best action


def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    agent = game.get_turn(state)   # Get the current player

    # Check if you're in a terminal state, then no action is needed
    terminal, values = game.is_terminal(state)
    if terminal:
        return values[0], None

    # If you reached the maximum depth,
    # use a heuristic to evaluate the value of the terminla state and no extra actions is needed
    if max_depth == 0:
        return heuristic(game, state, 0), None

    # Get all children of the current node combined with its action
    actions_states = [(action, game.get_successor(state, action))
                      for action in game.get_actions(state)]
    if agent == 0:  # Max player
        # Get the best action that achieves the best/maximum value
        value, _, action = max((minimax(game, state, heuristic, max_depth-1)[
                               0], -index, action) for index, (action, state) in enumerate(actions_states))
    else:           # Min player
        # Get the best action that achieves the best/minimum value
        value, _, action = min((minimax(game, state, heuristic, max_depth-1)[
                               0], index, action) for index, (action, state) in enumerate(actions_states))
    return value, action


# Apply Alpha Beta pruning and return the tree value and the best action

def _alphabeta(game, state, heuristic, max_depth, alpha, beta, sort=False):
    agent = game.get_turn(state)  # Get the current player

    # Check if you're in a terminal state, then no action is needed
    terminal, values = game.is_terminal(state)
    if terminal:
        return values[0], None

    # If you reached the maximum depth,
    # use a heuristic to evaluate the value of the terminla state and no extra actions is needed
    if max_depth == 0:
        return heuristic(game, state, 0), None

    # Get all children of the current node combined with its action
    actions_states = [(action, game.get_successor(state, action))
                      for action in game.get_actions(state)]

    # In case of alpha-beta pruning with move ordering, you need to sort all possible actions/states/nodes
    # depending on the evaluated heuristic
    if sort:
        actions_states = sorted(
            actions_states, key=lambda item: -heuristic(game, item[1], agent))

    if agent == 0:  # Max player
        results = []
        value, action = -math.inf, None
        # Get the best action that achieves the best/maximum value
        for index, (action, state) in enumerate(actions_states):
            cur_value = _alphabeta(game, state, heuristic,
                                   max_depth - 1, alpha, beta, sort)[0]

            results.append((cur_value, -index, action))
            value, _, action = max(results)  # Maximum value for the MAX player

            # If the current value is greater than or equal to beta,
            # prune the search and return the best value with best action
            if value >= beta:
                return value, action

            # Update alpha with maximum possible value
            alpha = max(alpha, value)

    else:           # Min player
        results = []
        value, action = math.inf, None
        # Get the best action that achieves the best/minimum value
        for index, (action, state) in enumerate(actions_states):
            cur_value = _alphabeta(game, state, heuristic,
                                   max_depth - 1, alpha, beta, sort)[0]

            results.append((cur_value, -index, action))
            value, _, action = min(results)  # Minimum value for the MIN player

            # If the current value is less than or equal to alpha,
            # prune the search and return the best value with best action
            if value <= alpha:
                return value, action

            # Update beta with minimum possible value
            beta = min(beta, value)

    return value, action


def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    return _alphabeta(game, state, heuristic, max_depth, -math.inf, math.inf)

# Apply Alpha Beta pruning with move ordering and return the tree value and the best action


def alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    return _alphabeta(game, state, heuristic, max_depth, -math.inf, math.inf, True)

# Apply Expectimax search and return the tree value and the best action


def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    def _expectimax(game, state, heuristic, max_depth, chance) -> Tuple[float, A]:
        agent = game.get_turn(state)  # Get the current player

        # Check if you're in a terminal state, then no action is needed
        terminal, values = game.is_terminal(state)
        if terminal:
            return values[0], None

        # If you reached the maximum depth,
        # use a heuristic to evaluate the value of the terminla state and no extra actions is needed
        if max_depth == 0:
            return heuristic(game, state, 0), None

        # Get all children of the current node combined with its action
        actions_states = [(action, game.get_successor(state, action))
                          for action in game.get_actions(state)]

        if chance and agent != 0:  # Chance Node
            _sum = 0
            _num = len(actions_states)
            # Get the average value of all children for the current node
            for action, state in actions_states:
                value, action = _expectimax(
                    game, state, heuristic, max_depth-1, False)
                _sum += value
            value = _sum / _num
        elif agent == 0:  # Max player
            # Get the best action that achieves the best/maximum value
            value, _, action = max((_expectimax(game, state, heuristic, max_depth-1, True)[0], -index, action)
                                   for index, (action, state) in enumerate(actions_states))
        else:           # Min player
            # Get the best action that achieves the best/minimum value
            value, _, action = min((_expectimax(game, state, heuristic, max_depth-1, True)[0], index, action)
                                   for index, (action, state) in enumerate(actions_states))
        return value, action

    return _expectimax(game, state, heuristic, max_depth, False)
