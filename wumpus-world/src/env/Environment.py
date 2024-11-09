import sys
import os

# Add the src directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import List # Import List for type hinting
from random import randint, random # Import randint and random for generating random locations and probabilities
from agent.Action import Action # Relative import of Action class from the agent module
from env.Percept import Percept # Relative import of Percept class from the environment module
from agent.Location import Location # Relative import of Location class from the agent module
from agent.Orientation import Orientation # Relative import of Orientation class from the agent module

class Environment:
    # Defining the attributes of the Environment Class
    wumpus_location: Location
    wumpus_alive: bool
    agent_location: Location
    agent_orientation: Orientation
    agent_has_arrow: bool
    agent_has_gold: bool
    done: bool
    gold_location: Location
    pit_location: List[Location]
    time_step: int
    performance: int
        
    def __init__(self, allow_climb_without_gold, pit_prob):
        # initialize the environment state variables (use make functions below)
        self.agent_location = Location (0,0)
        self.agent_orientation = Orientation.EAST
        self.agent_has_arrow = True # Agent starts with an arrow
        self.agent_has_gold = False # Agent does not have gold initially
        self.wumpus_alive = True # The Wumpus is alive at the beginning
        self.done = False # The game is not over initially 
        self.allow_climb_without_gold = allow_climb_without_gold # Configure whether the agent can climb without the gold
        self.time_step = 0 # Initialize the time step to 0 to track the number of actions taken by the agent.
        self.performance = 0 # Initialize the performance metric to 0, which could be used to track the agent's score or efficiency in the environment.
        self.pit_location = [] # Initialize an empty list to hold the locations of pits in the environment. The list will be populated by calling the make_pits method.
        self.make_wumpus() # Call the make_wumpus method to randomly place the Wumpus in the environment.
        self.make_gold() # Call the make_gold method to randomly place the gold in the environment.
        self.make_pits(pit_prob) # Call the make_pits method with the given probability (pit_prob) to randomly generate pit locations throughout the environment, except at the starting location.
        
    def make_wumpus(self):
        # choose a random location for the wumpus (not bottom left corner) and set it to alive
        while True:
            x = randint(0,3)
            y = randint (0,3)
            if (x,y) != (0,0):
                self.wumpus_location = Location(x,y)
                self.wumpus_alive = True
                break

        
    def make_gold(self):
        # choose a random location for the gold (not bottom left corner)
        while True: 
            x = randint(0, 3)  # Generate a random x-coordinate
            y = randint(0, 3)  # Generate a random y-coordinate
            if (x, y) != (0, 0):  # Ensure the gold isn't placed at the start location
                self.gold_location = Location(x, y)  # Set the gold location
                break  # Exit the loop once a valid location is assigned
        
    def make_pits(self, pit_prob: float):
        # create pits with prob pit_prob for all locations except the bottom left corner
        for x in range(4):
                for y in range (4):
                    if (x,y)!=(0,0) and random()<pit_prob: 
                        self.pit_location.append (Location(x,y))
        for pit in self.pit_location:
            print(f"Pit Location: ({pit.x}, {pit.y})")
        
    def is_pit_at(self, location: Location) -> bool:
        # return true if there is a pit at location
        return location in self.pit_location
        
    def is_pit_adjacent_to_agent(self) -> bool:
        # return true if there is a pit above, below, left or right of agent's current location
        return any(  
            pit.is_adjacent_to(self.agent_location)  
            for pit in self.pit_location
        )

    def is_wumpus_adjacent_to_agent(self) -> bool:
        # return true if there is a wumpus adjacent to the agent
        return self.wumpus_location.is_adjacent_to(self.agent_location)  # Check if the Wumpus is next to the agent

        
    def is_agent_at_hazard(self) -> bool:
        at_pit = self.is_pit_at(self.agent_location)
        at_wumpus = self.is_wumpus_at(self.agent_location) and self.wumpus_alive
        print(f"Checking for hazards at ({self.agent_location.x}, {self.agent_location.y}): Pit: {at_pit}, Wumpus: {at_wumpus}")
        return at_pit or at_wumpus

        
    def is_wumpus_at(self, location: Location) -> bool:
        # return true if there is a wumpus at the given location
        return self.wumpus_location == location  # Check if the Wumpus is at the given location
        
    def is_agent_at(self, location: Location) -> bool:
        # return true if the agent is at the given location
         return self.agent_location == location  # Check if the agent is at the given location
        
    def is_gold_at(self, location: Location) -> bool:
        # return true if the gold is at the given location
        return self.gold_location == location  # Check if the gold is at the given location

    def is_glitter(self) -> bool:
        # return true if the agent is where the gold is
        return self.is_gold_at(self.agent_location)  # Check if the agent is at the gold's location

    def is_breeze(self) -> bool:
        # return true if one or pits are adjacent to the agent or the agent is in a room with a pit
        return self.is_pit_adjacent_to_agent()  # If a pit is next to the agent, a breeze is perceived
        
    def is_stench(self) -> bool:
        # return true if the wumpus is adjacent to the agent or the agent is in the room with the wumpus
        return self.is_wumpus_adjacent_to_agent() or self.is_wumpus_at(self.agent_location)  # Check if the Wumpus is near
        
    def wumpus_in_line_of_fire(self) -> bool:
        # return true if the wumpus is a cell the arrow would pass through if fired
        if not self.agent_has_arrow:  # If the agent doesn't have an arrow, return False
            return False
        # Get the agent's current coordinates
        agent_x, agent_y = self.agent_location.x, self.agent_location.y
        # Get the Wumpus's current coordinates
        wumpus_x, wumpus_y = self.wumpus_location.x, self.wumpus_location.y

        # Check if the Wumpus is in line based on the agent's orientation
        if self.agent_orientation == Orientation.NORTH:  # If the agent is facing north
            return agent_x == wumpus_x and agent_y < wumpus_y  # The Wumpus is directly north
        if self.agent_orientation == Orientation.SOUTH:  # If the agent is facing south
            return agent_x == wumpus_x and agent_y > wumpus_y  # The Wumpus is directly south
        if self.agent_orientation == Orientation.EAST:  # If the agent is facing east
            return agent_y == wumpus_y and agent_x < wumpus_x  # The Wumpus is directly east
        if self.agent_orientation == Orientation.WEST:  # If the agent is facing west
            return agent_y == wumpus_y and agent_x > wumpus_x  # The Wumpus is directly west
        return False  # If none of the conditions match, the Wumpus is not in the line of fire

    def kill_attempt(self) -> bool:
        # return true if the wumpus is alive and in the line of fire
        # if so set the wumpus to dead
        if self.wumpus_alive and self.wumpus_in_line_of_fire():  # Check if the Wumpus is alive and in the agent's line of fire
            self.wumpus_alive = False  # If yes, kill the Wumpus
            return True  # Return True to indicate the Wumpus was killed
        return False  # If no, return False (no Wumpus killed)
        
    def step(self, action: Action) -> Percept:
        # for each of the actions, make any agent state changes that result and return a percept including the reward
        self.time_step += 1  # Increment the time step with each action the agent takes
        reward = -1  # Default reward (small penalty for taking any action)
        bump = False # Initialize bump to False (bump occurs if agent bumps into wall)
        scream = False  # Initialize scream to False (scream occurs if the Wumpus is killed)
        print(f"Agent action: {action}, current location: ({self.agent_location.x}, {self.agent_location.y}), orientation: {self.agent_orientation}")
          # Apply the agent's action based on the type of action
        if action == Action.FORWARD:  # If the action is to move forward
            bump = self.agent_location.forward(self.agent_orientation)  # Move agent in the direction it's facing
            if self.is_agent_at_hazard():  # Check if the agent encounters a hazard (pit or Wumpus)
                reward += -1000  # Large penalty for dying
                self.done = True  # End the game if the agent dies
                print(f"Game over! Agent encountered hazard at ({self.agent_location.x}, {self.agent_location.y})")
        elif action == Action.LEFT:  # If the action is to turn left
            self.agent_orientation = self.agent_orientation.turn_left()  # Change agent's orientation to the left
            print(f"Agent Orientation: {self.agent_orientation}")
        elif action == Action.RIGHT:  # If the action is to turn right
            self.agent_orientation = self.agent_orientation.turn_right()  # Change agent's orientation to the right
            print(f"Agent Orientation: {self.agent_orientation}")
        elif action == Action.GRAB:  # If the action is to grab gold
            if self.is_glitter():  # Check if agent is on the gold
                self.agent_has_gold = True  # Set agent's gold possession to True
                print(f"Agent grabbed the gold at ({self.agent_location.x}, {self.agent_location.y})")
        elif action == Action.SHOOT:  # If the action is to shoot the arrow
            if self.agent_has_arrow:  # Check if agent has an arrow
                self.agent_has_arrow = False  # Use the arrow (agent no longer has an arrow)
                reward += -10  # Small penalty for using the arrow (whether it kills or not)
                if self.kill_attempt():  # Check if the arrow hits and kills the Wumpus
                    scream = True  # Set scream to True (Wumpus dies)
                    print("The Wumpus has been killed!")
        elif action == Action.CLIMB:  # If the action is to climb out
            if self.agent_location == Location(0, 0):  # Agent must be at the starting location (0,0)
                if self.agent_has_gold:  # If agent has the gold
                    reward += 1000  # Big reward for winning with gold
                    print("Agent successfully climbed out with the gold!")
                elif self.allow_climb_without_gold:  # If allowed, the agent can climb without the gold
                    reward += 0  # No penalty for climbing without gold
                    print("Agent climbed out without the gold.")
                self.done = True  # End the game after climbing

        # Create a Percept object that reflects what the agent perceives
        percept = Percept(
            time_step=self.time_step,
            stench=self.is_stench(),  # Is there a stench (Wumpus nearby)?
            breeze=self.is_breeze(),  # Is there a breeze (pit nearby)?
            glitter=self.is_glitter(),  # Is there glitter (gold nearby)?
            bump=bump,  # Bump can be added if the agent hits a wall 
            scream=scream,  # Scream if the Wumpus dies
            done=self.done,  # Is the game over?
            reward=reward  # The reward for the action
        )

        return percept  # Return the percept to the agent
    
        
    # Visualize the game state
    def visualize(self):
        for y in range(3, -1, -1):
            line = '|'
            for x in range(0, 4):
                loc = Location(x, y)
                cell_symbols = [' ', ' ', ' ', ' ']
                if self.is_agent_at(loc): 
                    cell_symbols[0] = self.agent_orientation.symbol()
                if self.is_pit_at(loc): 
                    cell_symbols[1] = 'P'
                if self.is_wumpus_at(loc):
                    if self.wumpus_alive:
                        cell_symbols[2] = 'W'
                    else:
                        cell_symbols[2] = 'w'
                if self.is_gold_at(loc): 
                    cell_symbols[3] = 'G'
                for char in cell_symbols: 
                    line += char
                line += '|'
            print(line)