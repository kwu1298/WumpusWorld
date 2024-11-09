from typing import List
from agent.Orientation import Orientation

class Location:
    x: int
    y: int
        
    def hello():
        return "Hello from module1!"

    def __init__(self, x: int, y: int):
        # initialize the coordinates of the location
        self.x = x
        self.y = y
        
    def __str__(self):
        # Return a string representation of the location
        return f'({self.x}, {self.y})'
       
    def is_adjacent_to(self, location: 'Location') -> bool:
        # Return True if self is adjacent to the given location (above, below, left, or right)
        return (
            self.is_left_of(location) or
            self.is_right_of(location) or
            self.is_above(location) or
            self.is_below(location)
        )
    
    def is_in_bounds(self) -> bool:
        # Check if the location is within grid boundaries 
        return 0 <= self.x < 4 and 0 <= self.y < 4

    def is_left_of(self, location: 'Location')->bool:
        # return True if self is just left of given location
        return self.x == location.x - 1 and self.y == location.y
        
   
    def is_right_of(self, location: 'Location')->bool:
        # return True if self is just right of given location    
        return self.x == location.x + 1 and self.y == location.y
    
    def is_above(self, location: 'Location')->bool:
        # return True if self is immediately above given location    
        return self.x == location.x and self.y == location.y + 1
        
    def is_below(self, location: 'Location')->bool:
        # return True if self is immediately below given location   
        return self.x == location.x and self.y == location.y - 1
    
    def neighbours(self)->List['Location']:
        # return list of neighbour locations    
        neighbours = []
        if not self.at_left_edge():
            neighbours.append(Location(self.x - 1, self.y))  # Left neighbour
        if not self.at_right_edge():
            neighbours.append(Location(self.x + 1, self.y))  # Right neighbour
        if not self.at_bottom_edge():
            neighbours.append(Location(self.x, self.y - 1))  # Below neighbour
        if not self.at_top_edge():
            neighbours.append(Location(self.x, self.y + 1))  # Above neighbour
        return neighbours

    def __eq__(self, other: 'Location') -> bool:
        if isinstance(other, Location):
            return self.x == other.x and self.y == other.y
        return False


    def is_location(self, location: 'Location')->bool:
        # Return True if the given location matches this location
        return self.x == location.x and self.y == location.y
    
    def at_left_edge(self) -> bool:
    # return True if at the left edge of the grid   
        return self.x == 0
    
    
    def at_right_edge(self) -> bool:
        # return True if at the right edge of the grid    
        return self.x == 3
    
    def at_top_edge(self) -> bool:
        # return True if at the top edge of the grid    
        return self.y == 3

    def at_bottom_edge(self) -> bool:
     # return True if at the bottom edge of the grid    
        return self.y == 0
    
    def forward(self, orientation) -> bool:
    # modify self.x and self.y to reflect a forward move and return True if bumped a wall  
        if orientation == Orientation.NORTH:
            if self.y < 3:
                self.y += 1
                print(f"Moving NORTH to ({self.x}, {self.y})")  # Debugging line
                return False
            else:
                print("Bumped into northern wall")  # Debugging line
        elif orientation == Orientation.SOUTH:
            if self.y > 0:
                self.y -= 1
                print(f"Moving SOUTH to ({self.x}, {self.y})")  # Debugging line
                return False
            else:
                print("Bumped into southern wall")  # Debugging line
        elif orientation == Orientation.EAST:
            if self.x < 3:
                self.x += 1
                print(f"Moving EAST to ({self.x}, {self.y})")  # Debugging line
                return False
            else:
                print("Bumped into eastern wall")  # Debugging line
        elif orientation == Orientation.WEST:
            if self.x > 0:
                self.x -= 1
                print(f"Moving WEST to ({self.x}, {self.y})")  # Debugging line
                return False
            else:
                print("Bumped into western wall")  # Debugging line 
        return True  # Bumped into a wall
    
    def set_to(self, location: 'Location'):
    # set self.x and self.y to the given location  
        self.x = location.x
        self.y = location.y

        
    @staticmethod
    def from_linear(n: int) -> 'Location':
    # convert an index from 0 to 15 to a location
        return Location(n % 4, n // 4)
    
    
    def to_linear(self)->int:
    # convert self to an index from 0 to 15    
        return self.y * 4 + self.x
    
    
    @staticmethod
    def random() -> 'Location':
        # return a random location    
        return Location(randint(0, 3), randint(0, 3))