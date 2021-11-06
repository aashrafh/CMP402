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
    if problem.is_goal(initial_state):  # Check if the initial state is the goal
        return []   # No actions are needed

    # A FIFO queue to store all the actions of all paths
    actions = [[]]
    # A FIFO queue to store the next states to explore. initial_state is the only element at the begining
    frontier = [initial_state]
    # An empty set to mark/store the visited nodes
    explored = []

    while frontier:  # while there are more nodes to explore, do:
        state = frontier.pop(0)  # Choose the shallowest node in the frontier
        explored.append(state)   # Mark the current state as visited/explored
        # Choose the shallowest path = shallowest sequence of actions
        path = actions.pop(0)

        # Loop over all possible actions from the current state
        for action in problem.get_actions(state):
            # Get the child node = the successor
            successor = problem.get_successor(state, action)

            if successor not in explored and successor not in frontier:
                # Update the current path
                new_path = list(path)
                new_path.append(action)
                actions.append(new_path)

                if problem.is_goal(successor):  # Test if this is the goal
                    # Append the last action taken
                    path.append(action)
                    return path
                
                frontier.append(successor) # Update the frontier with the next possible node to explore

    # If there is no solution, return None
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
