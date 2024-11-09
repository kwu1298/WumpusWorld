import sys
import os

# Add the src folder to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))


from env.Environment import Environment #Imported the environment class
from agent.NaiveAgent import NaiveAgent #Imported the Naive Agent Class 
from agent.Action import Action #Imported the action class
from env.Percept import Percept #Imported the percept class
import time

def main():
    # Initialize the environment
    allow_climb_without_gold = True  # Allow the agent to climb out without the gold
    pit_prob:float = 0.2
    environment = Environment(allow_climb_without_gold=allow_climb_without_gold, pit_prob=pit_prob)

    # Initialize the agent
    agent = NaiveAgent()
    cumulative_reward = 0  # Track the cumulative reward for the agent

    # Initial percept from the environment
    percept = environment.step(Action.FORWARD)  # Initial action to get the percept
 
    # Run the game until it ends
    while not percept.done:
        # Visualize the current state of the environment
        environment.visualize()
        print('Percept:', percept)

        # Agent chooses an action
        action = agent.choose_action()
        print('Action:', action)

        # Step the environment with the chosen action and receive a new percept
        percept = environment.step(action)
        cumulative_reward += percept.reward

        # Delay to simulate time passing for better visualization (optional)
        time.sleep(1)

    # Final state visualization and summary
    environment.visualize()
    print('Percept:', percept)
    print('Cumulative reward:', cumulative_reward)

if __name__ == "__main__":
    main()