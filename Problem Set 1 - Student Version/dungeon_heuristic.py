from os import stat
from dungeon import DungeonProblem, DungeonState
from mathutils import Direction, Point, euclidean_distance, manhattan_distance
from helpers import utils
import heapq


# This heuristic returns the distance between the player and the exit as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal


def weak_heuristic(problem: DungeonProblem, state: DungeonState):
    return euclidean_distance(state.player, problem.layout.exit)

# TODO: Import any modules and write any functions you want to us


def strong_heuristic(problem: DungeonProblem, state: DungeonState) -> float:
    # TODO: ADD YOUR CODE HERE
    # IMPORTANT: DO NOT USE "problem.is_goal" HERE.
    # Calling it here will mess up the tracking of the explored nodes count
    # which is considered the number of is_goal calls during the search
    # NOTE: you can use problem.cache() to get a dictionary in which you can store information that will persist between calls of this function
    # This could be useful if you want to store the results heavy computations that can be cached and used across multiple calls of this function
    direct_distance = manhattan_distance(state.player, problem.layout.exit)

    # The idea is to get an intermediate point between the start and end goal so you can calculate more realistic distance to the goal
    intermediate_distance = 0
    for coin in state.remaining_coins:
        current_distance = manhattan_distance(
            state.player, coin) + manhattan_distance(coin, problem.layout.exit)
        if current_distance > intermediate_distance:
            intermediate_distance = current_distance

    if len(state.remaining_coins) >= 1:
        return intermediate_distance

    return direct_distance
