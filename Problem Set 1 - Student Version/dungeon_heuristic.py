from os import stat
from dungeon import DungeonProblem, DungeonState
from mathutils import Direction, Point, euclidean_distance, manhattan_distance
from helpers import utils
import heapq


# This heuristic returns the distance between the player and the exit as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal


def weak_heuristic(problem: DungeonProblem, state: DungeonState):
    return euclidean_distance(state.player, problem.layout.exit)

# TODO: Import any modules and write any functions you want to use


def get_next_state(problem: DungeonProblem, state: DungeonState, action: Direction) -> DungeonState:
    player = state.player + action.to_vector()
    remaining_coins = state.remaining_coins
    if player not in problem.layout.walkable:
        return state
    if player in remaining_coins:
        remaining_coins -= {player}
    return DungeonState(state.layout, player, remaining_coins)


def bfs(problem, start, goal_point, dist):
    frontier = [(start, [])]
    explored = set()

    while frontier:
        state, path = frontier.pop(0)
        if state not in explored:
            if state.player == goal_point:
                for i in range(len(path)):
                    dist[(path[i].player, state.player)] = len(path[i:])
                break

            explored.add(state)

            for action in problem.get_actions(state):
                successor = get_next_state(problem, state, action)
                frontier.append((successor, path + [successor]))

    return dist


def strong_heuristic(problem: DungeonProblem, state: DungeonState) -> float:
    # TODO: ADD YOUR CODE HERE
    # IMPORTANT: DO NOT USE "problem.is_goal" HERE.
    # Calling it here will mess up the tracking of the explored nodes count
    # which is considered the number of is_goal calls during the search
    # NOTE: you can use problem.cache() to get a dictionary in which you can store information that will persist between calls of this function
    # This could be useful if you want to store the results heavy computations that can be cached and used across multiple calls of this function
    dist = problem.cache()

    h = manhattan_distance(state.player, problem.layout.exit)

    frontier = [state]
    explored = set()
    paths = {state: []}

    while frontier:
        current_state = frontier.pop(0)

        if current_state.player == problem.layout.exit:
            return max(h, len(paths[current_state]))

        explored.add(current_state)

        for action in problem.get_actions(current_state):
            successor = get_next_state(
                problem, current_state, action)
            if successor not in explored:
                frontier.append(successor)
                paths[successor] = paths[current_state] + [action]

    return h
