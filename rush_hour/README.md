Start game by use of command line under python directory.

Text-version: python rushhour.py game2.txt

GUI-version:python rushhour_gui.py game2.txt

# Rules:
Instructions: Move the target car to the finish line by moving any cars in its way. If the car's orientation is vertical it can only move up or down. If the car's orientation is horizontal it can only move left or right.
	
Text version: The target car is the first car in the input text file which is given the ID: 0. The other cars ID's are based on the order they are added onto the board. The finish line is on the block row 2 column 5, where the grid numbers start from 0 and goes to 5 (eg: 0,1,2,3,4,5). 
	
Graphical version: The target car is the fighter jet. The finish line is the block with a finish line on it.


# Controls:
Text Version: 
- The grid is printed out on a grid whose rows go: (0,1,2,3,4,5) and columns go (0,1,2,3,4,5).
- To move a car, enter its carID first, which is its number.
- Then enter the row number and column number that you want to move your car's closest side to.
	
Graphical version: 
- Movement controls include the of the left and right clicks of the mouse.
- To move a vertical car: Hover mouse over car and right click to move one block upwards and left click to move one block down.
- To move a horizontal car: Hover mouse over car and right click to move one block right and left click to move one block left.
- When the puzzle is solved, the graphics window will close in five seconds.
