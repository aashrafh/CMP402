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

    def _compute_bellman(self, state, actions):
        values = []
        for action in actions:
            successors = self.mdp.get_successor(state, action)
            value = 0
            for next_state, p in successors.items():
                reward = self.mdp.get_reward(state, action, next_state)
                value += p * (reward + self.discount_factor *
                              self.utilities[str(next_state)])
            values.append((value, action))
        values.sort(key=lambda item: (-item[0], item[1]))
        return values[0]

    # Given a state, compute its utility using the bellman equation
    # if the state is terminal, return 0
    def compute_bellman(self, state: S) -> float:
        if self.mdp.is_terminal(state):  # if the state is terminal, return 0
            return 0
        return self._compute_bellman(state, self.mdp.get_actions(state))[0]

    # This function applies value iteration starting from the current utilities stored in the agent and stores the new utilities in the agent
    # NOTE: this function does incremental update and does not clear the utilities to 0 before running
    # In other words, calling train(M) followed by train(N) is equivalent to just calling train(N+M)
    def train(self, iterations: int = 1):
        for i in range(iterations):
            utilities = {str(state): 0 for state in self.mdp.get_states()}
            for state in self.mdp.get_states():
                utilities[str(state)] = self.compute_bellman(state)
            self.utilities = utilities.copy()

    # Given an environment and a state, return the best action as guided by the learned utilities and the MDP
    # If the state is terminal, return None
    def act(self, env: Environment[S, A], state: S) -> A:
        if self.mdp.is_terminal(state):
            return None
        return self._compute_bellman(state, env.actions())[1]

    # Save the utilities to a json file
    def save(self, file_path: str):
        with open(file_path, 'w') as f:
            json.dump(self.utilities, f, indent=2, sort_keys=True)

    # loads the utilities from a json file
    def load(self, file_path: str):
        with open(file_path, 'r') as f:
            self.utilities = json.load(f)
