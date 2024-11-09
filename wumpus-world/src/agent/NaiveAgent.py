import random
from env.Environment import Environment
from agent.Action import Action

class NaiveAgent:
    
    def choose_action(self)-> Action :
        # return a randomly chosen action
        actions = [Action.FORWARD, Action.LEFT, Action.RIGHT, Action.GRAB, Action.SHOOT, Action.CLIMB]
        return random.choice(actions)