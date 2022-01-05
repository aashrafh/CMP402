# This file contains the options that you should modify to solve Question 2

def question2_1():
    # Seek the near terminal state (reward +1) via the short dangerous path (moving besides the row of -10 state).
    # Decrease the noise so the agent moves faster, and less discount factor so do not care much about the reward
    return {
        "noise": 0.002,
        "discount_factor": 0.09,
        "living_reward": -1
    }


def question2_2():
    # Seek the near terminal state (reward +1) via the long safe path (moving away from the row of -10 state).
    # Increase the noise so the agent takes thet longer path, and increase the discount factor more than the Q1
    return {
        "noise": 0.5,
        "discount_factor": 0.67,
        "living_reward": -1
    }


def question2_3():
    # Seek the far terminal state (reward +10) via the short dangerous path (moving besides the row of -10 state).
    # Same as Q1 but with higher discount factor to take care more about the reward
    return {
        "noise": 0.002,
        "discount_factor": 0.9,
        "living_reward": -1
    }


def question2_4():
    # Seek the far terminal state (reward +10) via the long safe path (moving away from the row of -10 state).
    # Increase the noise so the agent takes thet longer path and increase the reward along with the discount factor.
    return {
        "noise": 0.2,
        "discount_factor": 1,
        "living_reward": -0.1
    }


def question2_5():
    # Avoid any terminal state and keep the episode going on forever.
    # Increase the reward of going to non-terminal states and decrease the noise to increase probability of
    # going to non-terminal states.
    return {
        "noise": 0.02,
        "discount_factor": 0.99,
        "living_reward": 1
    }


def question2_6():
    # Seek any terminal state (even ones with the -10 penalty) and try to end the episode in the shortest time possible.
    # Decrease the reward very much so the agent doesn't care about the non-terminal states
    return {
        "noise": 0.2,
        "discount_factor": 0.99,
        "living_reward": -20
    }
