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
    # A FIFO queue to store the next states to explore. initial_state is the only element at the begining
    frontier = [(initial_state, [])]
    explored = set()                    # An empty set to mark/store the visited nodes

    while frontier:  # while there are more nodes to explore, do:
        # Choose the shallowest node in the frontier
        state, path = frontier.pop(0)
        if state not in explored:   # If unexplored node
            # If you reached the goal, then return the path.
            if problem.is_goal(state):
                return path
            # Otherwise, add the current state to the explored set
            explored.add(state)

            # and loop over all the next states
            for action in problem.get_actions(state):
                successor = problem.get_successor(state, action)
                # Append the next states to the frontier to get explored
                frontier.append((successor, path + [action]))

    # If there is no solution, return None
    return None


def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    # A LIFO stack to store the next states to explore. initial_state is the only element at the begining
    frontier = [(initial_state, [])]
    explored = set()                    # An empty set to mark/store the visited nodes

    while frontier:  # while there are more nodes to explore, do:
        state, path = frontier.pop()    # Choose the deepest node in the frontier
        if state not in explored:       # If unexplored node
            # If you reached the goal, then return the path.
            if problem.is_goal(state):
                return path
            # Otherwise, add the current state to the explored set
            explored.add(state)

            # and loop over all the next states
            for action in problem.get_actions(state):
                successor = problem.get_successor(state, action)
                # Append the next states to the frontier to get explored
                frontier.append((successor, path + [action]))

    # If there is no solution, return None
    return None


def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    # TODO: ADD YOUR CODE HERE
    utils.NotImplemented()


def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    # TODO: ADD YOUR CODE HERE
    utils.NotImplemented()


def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    # TODO: ADD YOUR CODE HERE
    utils.NotImplemented()
