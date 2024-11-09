from enum import Enum

class Orientation(Enum):
    EAST = 0 # East
    SOUTH = 1 # South
    WEST = 2 # West
    NORTH = 3 # North

    def symbol(self) -> str:
        # code for function to return the letter code ("E", "S", etc.) of this instance of an orientation
        # You could create a __str__(self) for this instead of the symbol function if you prefer
        return {
            Orientation.EAST: ">",
            Orientation.SOUTH: "v",
            Orientation.WEST: "<",
            Orientation.NORTH: "^"
        }[self]
    
    def turn_right(self) -> 'Orientation':
        # return a new orientation turned right
        return Orientation((self.value + 1) % 4)
    
    def turn_left(self) -> 'Orientation':
        # return a new orientation turned left
        return Orientation((self.value - 1) % 4)