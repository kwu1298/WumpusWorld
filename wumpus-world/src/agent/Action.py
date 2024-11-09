from enum import Enum

class Action(Enum):
    LEFT = 0
    RIGHT = 1
    FORWARD = 2
    GRAB = 3
    SHOOT = 4
    CLIMB = 5


    def description (self) -> str:    # Return a dictionary mapping each action to a descriptive string
            return{
            Action.LEFT: 'Turn left',  
            Action.RIGHT: 'Turn right',  
            Action.FORWARD: 'Move forward',  
            Action.GRAB: 'Grab the gold',  
            Action.SHOOT: 'Shoot the arrow',  
            Action.CLIMB: 'Climb out' 
        }[self]  
    
    def __str__(self) -> str:
        # Return the action's description when converting to string (used for printing)
        return self.description()
