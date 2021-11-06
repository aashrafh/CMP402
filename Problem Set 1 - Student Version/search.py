from os import stat
from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers import utils

# TODO: Import any modules or write any helper functions you want to use

# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution


def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    if problem.is_goal(initial_state):
        return []

    actions = [[]]
    frontier = [initial_state]
    explored = []

    while frontier:
        state = frontier.pop(0)
        explored.append(state)
        path = actions.pop(0)

        for action in problem.get_actions(state):
            successor = problem.get_successor(state, action)

            if successor not in explored and successor not in frontier:
                new_path = list(path)
                new_path.append(action)
                actions.append(new_path)

                if problem.is_goal(successor):
                    path.append(action)
                    return path

                frontier.append(successor)

    return None


def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    # TODO: ADD YOUR CODE HERE
    utils.NotImplemented()


def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    # TODO: ADD YOUR CODE HERE
    utils.NotImplemented()


def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    # TODO: ADD YOUR CODE HERE
    utils.NotImplemented()


def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    # TODO: ADD YOUR CODE HERE
    utils.NotImplemented()
