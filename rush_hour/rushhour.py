import sys
import io


class Car(object):
    """ Car class used to create object with car position (x,y) on a 6x6 grid.
        The orientation of the car is either h = horizontal, or v = vertical.
        Two sizes for the cars: 2 and 3 """
        
    def __init__(self, carid=0,x=0, y=0, size=2, orientation="h"):
        """ carID: identification of car, integer number
            x,y = coordinates of car
            size = car size
            orientation = car movable direction
            Initialize object car  """
        self.carid = carid
        self.x = x
        self.y = y
        self.size = size
        self.orientation = orientation
        

           
class Game:
    """Create a game class that includes functions to create a text game board,
       load cars, move cars, and detect if the game is over. """

    
    def __init__(self, board=[], cars=[], cnumbers=0):
        """ board = 6x6 grid that lists all the cars locations
            cars = all car's information
            cnumbers = number of cars
            Initialize game board variables to be used."""
        self.board = board
        self.cars = cars
        self.cnumbers = cnumbers


    def addCar(self, car):
        """ car = car object to add to the board
            To add a car to the game board""" 
        if (car.orientation == "h"):                            #Add a horizontal car
            self.board[car.x][car.y] = car.carid                        
            self.board[car.x][car.y+1] = car.carid
            if car.size == 3:                                   #Check if it is a big car
                self.board[car.x][car.y+2] = car.carid              
        else: 
            self.board[car.x][car.y] = car.carid                #Add a vertical car
            self.board[car.x+1][car.y] = car.carid
            if car.size == 3:                                   #Check if it is a big car
                self.board[car.x+2][car.y] = car.carid
       
        
    def loadGame(self):
        """ Load a puzzle from a file a given file containing car
            information. Also loads car to the game board."""
        puzzleinfo = ""                     
        try:                                                    #Collect puzzle information from game file
            myfile = open(sys.argv[1], "r")                     #Input game file from command line
            puzzleinfo= myfile.readlines()
            myfile.close
        except IOError:
            print ("Could not open or read the file ???")       #Check if file is valid
        carinfostr = []
        for pinfo in puzzleinfo:
            if (pinfo !=  '\n'):                                
                carinfostr.append(pinfo.rstrip('\n'))           #Put all game puzzle information on one line
        for (i, car) in enumerate(carinfostr):
            eachcar=removeastr(carinfostr[i], ",")
            newcar = Car(i,int(eachcar[2]), int(eachcar[3]), int(eachcar[1]), eachcar[0])   #Create each car object
            self.cars.append(newcar)
            self.addCar(newcar)                                 #Load car to the game board
        self.cnumbers = len(self.cars)  
        self.printState()                                       #Print game board state


    def printState(self):
        """Print game board state"""
        for state in self.board:
            print('{:>5}{:>5}{:>5}{:>5}{:>5}{:>5}'.format(*state))        


    def findcar( self, carid):
        """carid = car's identification
           For a given carid, find the related car with the ID. """
        for car in self.cars:
            if car.carid == carid:                              #Find desired car
                return car
        return []                                               #No car found


    def caculateSteps(self, xcol, ycol, car):
        """ xcol = target column to be moved to
            ycol = target row to be moved to
            car = the car to be moved
            Check how many steps required to move the car to the position: xcol,ycol"""
        moves = []                                              #Initialize list to save move steps
        if car.orientation =="h":                               #Check if direction of possible movement is horizontal
            mvsteps= ycol-car.y
            if (mvsteps == 0):                                  #No move, the target position is occupied or invalid
                return []    
            if mvsteps < 0:                                     #Get steps to move left
                for i in range(abs(mvsteps)):                   #Obtain row and column of each moving steps needed to reach target position
                    step = ( xcol, car.y-i-1)
                    moves.append(step)
            else: 
                if car.size  == 2:
                    for i in range(int(mvsteps-1)):             #Get steps to move right for size 2 cars
                        step = ( xcol, car.y+2+i)               
                        moves.append(step)
                else:
                    for i in range(abs(mvsteps)-2):             #Get steps to move right for size 3 car
                        step = ( xcol, car.y+i+3)               
                        moves.append(step)
        if car.orientation =="v":                               #Check if direction of possible movement is vertical
            mvsteps= xcol-car.x
            if mvsteps < 0:                                     #Get steps to move up
                for j in range(abs(mvsteps)):
                    step = (car.x-j-1,ycol)
                    moves.append(step)
            else:
                if car.size == 2:
                    for j in range(abs(mvsteps)-1):             #Get steps to move down for car size 2
                        step = (car.x+j+2,ycol)  
                        moves.append(step)
                else:
                    for j in range(abs(mvsteps)-2):             #Get steps to move down for car size 3
                        step = (car.x+j+3,ycol)  
                        moves.append(step)   
        return moves
    
    
    def moveCar(self, xcol, ycol, carid):
        """ xcol = row to move car to
            ycol = column to move car to
            carid = car to be moved
            Get car name and move it to xcol,ycol if valid and correct."""
        car = self.findcar(carid)
        if car == []:
            #print ("Invalid carid: ", carid, "carid must be between 0 and ", self.cnumbers)
            return 0
        mvsteps = self.caculateSteps(xcol, ycol, car)
        if mvsteps == []:
            #print ("Invalid position provided , xcol= , ycol=",xcol, ycol )
            return 0
        for step in mvsteps:
            validcode= self.validmove(car, step[0], step[1])    #Check if the position to be moved to is occupied or not
            if validcode == 0:
                #print ("Cannot move car, the specified position is invalid or has been occupied")
                return 0
            elif validcode == 1:                                #Move car left
                self.board[car.x][car.y-1] = car.carid
                if car.size == 3:                               #Update game board position according to car size
                    self.board[car.x][car.y+2] = "."
                else:
                    self.board[car.x][car.y+1] = "."
                car.y = car.y-1                                 #Update car column cordinate
            elif  validcode == 2:                               #Move a small car right
                self.board[car.x][car.y] = "."
                self.board[car.x][car.y+2] = car.carid
                car.y = car.y+1                                 #Update  car column cordinate
            elif validcode == 3:                                #Move a big car right  
                self.board[car.x][car.y+3] = car.carid
                self.board[car.x][car.y] = "."
                car.y = car.y+1                                 #Update  car column cordinate
            elif validcode == 4:                                #Move a small car up
                self.board[car.x-1][car.y] = car.carid
                if car.size == 3:
                    self.board[car.x+2][car.y] = "."
                else:
                    self.board[car.x+1][car.y] = "."
                car.x = car.x-1                                 #Update  car row cordinate
            elif validcode == 5:                                #Move a small car down
                self.board[car.x+2][car.y] = car.carid
                self.board[car.x][car.y] = "."
                car.x = car.x+1                                 #Update car row cordinate       
            elif validcode == 6:                                #Move a big car down
                self.board[car.x+3][car.y] = car.carid
                self.board[car.x][car.y] = "."
                car.x = car.x+1                                 #Update car row cordinate
        if validcode != 0:                                      #Return if move is valid
            return 1
        else :
            return 0

    
    def validmove(self, car, xcol, ycol):
        """ car = car information
            xcol = row position to be moved to
            ycol = column position to be moved to
            Check if car movement is valid """
        if ( xcol<0 or xcol>5): 
            return 0                                            #Invalid move, out of board
        if ( ycol<0 or ycol>5):
            return 0                                            #Invalid move, out of board
        if (car.orientation =="h" and car.x == xcol):
            if (car.y-1 == ycol and car.y-1>=0 and self.board[car.x][car.y-1] == "."): #Check movement left while not out of board
                return 1
            elif (car.size == 2 and car.y+2 == ycol and  car.y+2<6 and self.board[car.x][ycol] == "."):   # Check movement right for a small car while not out of board
                return 2
            elif (car.size == 3 and car.y+3 == ycol and car.y+3 <6 and self.board[car.x][ycol] == "."):  #Check movement rigth for a big car while not out of board
                return 3
            else:                                               #Invalid move    
                return 0
        elif (car.orientation =="v" and car.y == ycol):
            if (car.x-1 == xcol and self.board[xcol][car.y] == "."):                    #Check movement up while not out of board
                return 4
            elif (car.size == 2 and car.x+2 <= 5 and car.x+2 == xcol and self.board[xcol][car.y] == "."):   #Check movement down for a small car while not out of board
                return 5
            elif (car.size == 3 and car.x+3 <= 5 and car.x +3 == xcol and self.board[xcol][car.y] == "."):  #Check movement down for a big car while not out of board
                return 6
            else:                                               #Invalid move
                  return 0

        else:                                                   #Invalid move
            return 0


    def isgameover(self,xcol, ycol,carid):
        """xcol = target car row
           ycol = target car column
           carid = target car id
           Check if the target car has reached the finish line at 2,5."""
        if ( carid == 0 and xcol == 2 and (xcol == 4 or ycol == 5)):
            return True
        else:
            return False
        
    
    def whichcarmoving(self):
        """ Used to input a position row and column where the carid will move to.
            Position must be in range [0, 5]"""
        while True:
            while True:
                try:
                    carid = int(input ( "which car you want to move :",))
                except ValueError:
                    continue
                if (carid >=0 and carid < self.cnumbers):
                    break
            while True:
                try:
                    x = int(input("Please enter: Row Position: "))
                except ValueError:
                    continue
                if( x>=0 and x<= 5 ):
                    break
            while True:
                try:
                    y = int(input("Please enter: Column position:"))
                except ValueError:
                    continue
                if( y>=0 and y<= 5):
                    break               
            return (x,y,carid)
    
                   
def removeastr(str1, rmstr):
    """str1 = string to be modified
       rmstr=segment to be removed
       To remove rmstr from str1."""
    restr=[]
    for s in str1:
        if ( s != rmstr and s != " "):
            restr+=s
    return restr


if __name__ == "__main__":                                       #Only run if main
    running = True                              
    while running:
        """ star play game,  initial a game board as 6x6 grid"""
        board = [['.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.']]                #Initialize game board
    
        gaming= Game(board)                                     #Create game board object
        gaming.loadGame()                                       #Load all cars from input file onto game board
        move_count = 0
        while True:
            (xcol, ycol, carid) = gaming.whichcarmoving()       #User input for car movement
            move_count += gaming.moveCar(xcol,ycol,carid)       #Move car to specified target if valid and note move count
            if (carid == 0 and gaming.isgameover(xcol, ycol, carid)):   #Check if game over
                print ("gameover! You win! the total valid steps you entered is: ",move_count, "\n" )
                running =False
                gaming.printState()
                break
            gaming.printState()                                 #Print game state

        
            
    
