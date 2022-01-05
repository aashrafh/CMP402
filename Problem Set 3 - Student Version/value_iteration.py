from typing import Dict
from agents import Agent
from environment import Environment
from mdp import MarkovDecisionProcess, S, A
import json
from helpers.utils import NotImplemented

# This is a class for a generic Value Iteration agent


class ValueIterationAgent(Agent[S, A]):
    mdp: MarkovDecisionProcess[S, A]  # The MDP used by this agent for training
    utilities: Dict[str, float]  # The computed utilities
    # The key is the string representation of the state and the value is the utility
    discount_factor: float  # The discount factor (gamma)

    def __init__(self, mdp: MarkovDecisionProcess[S, A], discount_factor: float = 0.99) -> None:
        super().__init__()
        self.mdp = mdp
        # We initialize all the utilities to be 0
        self.utilities = {str(state): 0 for state in self.mdp.get_states()}
        self.discount_factor = discount_factor

    # Given a state, compute its utility using the bellman equation
    # if the state is terminal, return 0
    def compute_bellman(self, state: S) -> float:
        if self.mdp.is_terminal(state):  # if the state is terminal, return 0
            return 0
        # Initialize the utilities with the current MDP's utilities
        utilities = self.utilities.copy()
        for action in self.mdp.get_actions(state):  # Loop over the actions
            # Get the next state with its probability
            (next_state, p) = self.mdp.get_successor(state, action)
            # Calculate the reward from state to next_state if we take the current action
            reward = self.mdp.get_reward(state, action, next_state)
            utilities[next_state] += p * \
                (reward + self.discount_factor *
                 utilities[next_state])  # Update the utility of the next_state using Bellman Equation

        # Return the maximum utility, depending on Bellman Equation
        return max(utilities.values())

    # This function applies value iteration starting from the current utilities stored in the agent and stores the new utilities in the agent
    # NOTE: this function does incremental update and does not clear the utilities to 0 before running
    # In other words, calling train(M) followed by train(N) is equivalent to just calling train(N+M)
    def train(self, iterations: int = 1):
        # Repeat the fitting/trainint iterations times
        for i in range(iterations):
            # Loop over all possible states in the MDP
            for state in self.mdp.get_states():
                # Calcualte the maximum utility for the state using Bellman Equation
                self.utilities[state] = self.compute_bellman(state)

    # Given an environment and a state, return the best action as guided by the learned utilities and the MDP
    # If the state is terminal, return None
    def act(self, env: Environment[S, A], state: S) -> A:
        # TODO: Complete this function
        # if more than one action has the maximum expected utility, return the one that appears first in the "actions" list
        if self.mdp.is_terminal(state):
            return None  # If the state is terminal, return None
        actions = env.actions()  # Get all the actions that can be taken in the current state
        for action in actions:   # Loop over all possible actions
            # get the next state from current state if we take action
            next_state, _, _, _ = env.step(action)
            # Return the action that achieves the best utility as calculated before in self.train()
            if self.utilities[state] == self.compute_bellman(next_state):
                return action

    # Save the utilities to a json file
    def save(self, file_path: str):
        with open(file_path, 'w') as f:
            json.dump(self.utilities, f, indent=2, sort_keys=True)

    # loads the utilities from a json file
    def load(self, file_path: str):
        with open(file_path, 'r') as f:
            self.utilities = json.load(f)
