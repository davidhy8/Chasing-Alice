import sys
import io
#import copy
class Car(object):
    """ Car class represents car position with x,y coords in 6x6 grid.
        orientation: HORIZONTAL=0, VERTICAL=1
        Car siz = 2 small car and 3 big car """
        
    def __init__(self, carid=0,x=0, y=0, size=2, orientation="h"):
        """ Create a new point at x, y """
        self.carid = carid
        self.x = x
        self.y = y
        self.size = size
        self.orientation = orientation

    def getcarorientation():
        return self.orientation
        
           

class Game:
    """ """
    def __init__(self, board=[], cars=[], cnumbers=0):
        self.board = board
        self.cars = cars
        self.cnumbers = cnumbers

##    def __addlist__(self, another_car):         
##        return self.cars += car ) 

    def addCar(self, car):
        """ to add a car to the game""" 
        if (car.orientation == "h"):
            #print (type(car.x), car.x)
            self.board[car.x][car.y] = car.carid
            self.board[car.x][car.y+1] = car.carid
            if car.size == 3:   
                self.board[car.x][car.y+2] = car.carid              
        else: 
            self.board[car.x][car.y] = car.carid
            self.board[car.x+1][car.y] = car.carid
            if car.size == 3:   
                self.board[car.x+2][car.y] = car.carid
       
        
    def loadGame(self):
        """  to load a puzzle from a file"""
        puzzleinfo = ""
        try:
            myfile = open(sys.argv[1], "r")
            puzzleinfo= myfile.readlines()
            #print ("puzzleinfo=", puzzleinfo )
            #print (len(puzzleinfo))
            myfile.close
        except IOError:
            print ("Could not open or read the file ???")
        carinfostr = []
        #carinfo = []
        for pinfo in puzzleinfo:
            if (pinfo !=  '\n'):   ## git ride of the "\n" in the list for each line
                carinfostr.append(pinfo.rstrip('\n'))
        #print ("\ncarinfo= \n", carinfostr)
        for (i, car) in enumerate(carinfostr):
            #print(carinfostr[i])
            eachcar=removeastr(carinfostr[i], ",")
            #print(eachcar.carid,eachcar.x,eachcar.y,eachcar.size,eachcar.orientation)
            newcar = Car(i,int(eachcar[2]), int(eachcar[3]), int(eachcar[1]), eachcar[0])
            #print(newcar.carid,newcar.x,newcar.y,newcar.size,newcar.orientation)
        
            self.cars.append(newcar)
            #slef.cars += newcar
            self.addCar(newcar)
        self.cnumbers = len(self.cars)
    
        self.printState()


    def printState(self):
        for state in self.board:
            print(state[0], state[1], state[2],state[3], state[4], state[5])
            #print('{:>5}{:>5}{:>5}{:>5}{:>5}{:>5}'.format(*state))        

    def findcar( self, carid):
        """ for a given carid, find the related car """
        for car in self.cars:
            #print (car)
            if car.carid == carid: ## find the moving car
                return car
        return []


    def caculateSteps(self, xcol, ycol, car):
        """ check how many steps to move baced on the input xcol, ycol"""
        moves = []
        print ("car.orientation, car.carid=",car.orientation, car.carid)
        print ("xcol,ycol=",xcol,ycol)
        if car.orientation =="h": ## orientation move, will be move left or right, only Y col changes
            mvsteps= ycol-car.y
            print("mvsteps=", mvsteps)
            if (mvsteps == 0):  # No move, the target position is same as current car position
                return []    
            if mvsteps < 0:  # Move left
                print ("mvsteps =",abs(mvsteps)-1)
                for i in range(abs(mvsteps)):
                    step = ( xcol, car.y-i-1)
                    print( step)
                    moves.append(step)
            else: 
                if car.size  == 2:
                    print("size 2 car", mvsteps)
                    for i in range(int(mvsteps-1)):  # move right
                        step = ( xcol, car.y+2+i)  # car size is 2
                        moves.append(step)
                        print (step)
                else:
                    for i in range(abs(mvsteps)-2):  # move right
                        step = ( xcol, car.y+i+3)  #car size is 3
                        moves.append(step)
        if car.orientation =="v": ## Vertical move, will be move up or down, only X col changes
            mvsteps= xcol-car.x
            print(mvsteps)
            if mvsteps < 0:  # Move up
                for j in range(abs(mvsteps)):
                    step = (car.x-j-1,ycol)
                    moves.append(step)
            else:
                if car.size == 2:
                    print("size 2 car v")
                    for j in range(abs(mvsteps)-1):   # move down
                        step = (car.x+j+2,ycol)  # car size is 2
                        print(step)
                        moves.append(step)
                else:
                    print("size 3 car v")
                    for j in range(abs(mvsteps)-2):
                        step = (car.x+j+3,ycol)  #car size is 3
                        print(step)
                        moves.append(step)
                       
        return moves
     
    
    
    def moveCar(self, xcol, ycol, carid):
        """ Get car name and move it to up/down/back/forward
            The cars can move up/down or left/right in their column or row."""
        car = self.findcar(carid)
        print ("findcar =", car.carid)
        if car == []:
            print ("invalid carid: ", carid, "carid must be between 0 and ", self.cnumbers)
            return 0
        mvsteps = self.caculateSteps(xcol, ycol, car)
        print(" mvsteps=", mvsteps)
        if mvsteps == []:
            print ("invalid position provided , xcol= , ycol=",xcol, ycol )
            return 0
        
        for step in mvsteps:
            validcode= self.validmove(car, step[0], step[1])
            print("validcode=",validcode)
            if validcode == 0:
                print ("Cannot move car, the specified position is invalid or has been overoccupied")
                
            elif validcode == 1:  # Horizontal move left
                self.board[car.x][car.y-1] = car.carid
                if car.size == 3:   
                    self.board[car.x][car.y+2] = "."
                else:
                    self.board[car.x][car.y+1] = "."
                car.y = car.y-1   # update  car y cordinate
            elif  validcode == 2:  # Horizontal move a small car right
                print("2fff")
                self.board[car.x][car.y] = "."
                self.board[car.x][car.y+2] = car.carid
                car.y = car.y+1  # update  car y cordinate
            elif validcode == 3:  # Horizontal move a big car right right 
                self.board[car.x][car.y+3] = car.carid
                self.board[car.x][car.y] = "."
                car.y = car.y+1  # update  car y cordinate
            elif validcode == 4:# a small car vertical move up
                self.board[car.x-1][car.y] = car.carid
                if car.size == 3:
                    self.board[car.x+2][car.y] = "."
                else:
                    self.board[car.x+1][car.y] = "."
                car.x = car.x-1  # update  car y cordinate
            elif validcode == 5: # a small car vertical move down
                self.board[car.x+2][car.y] = car.carid
                self.board[car.x][car.y] = "."
                car.x = car.x+1  # update  car y cordinate       
            elif validcode == 6: # a small car vertical move down
                self.board[car.x+3][car.y] = car.carid
                self.board[car.x][car.y] = "."
                car.x = car.x+1  # update  car y cordinate
        if validcode != 0:
            return 1
        else :
            return 0
    
    def validmove(self, car, xcol, ycol):
        """ Check car back/forward/up/down if there are spaces """
    
        if ( xcol<0 or xcol>5): 
            #print ("xcol=", xcol)
            return 0  # invalid, out of board
        if ( ycol<0 or ycol>5):
            return 0  # invalid, out of board
            #print ("ycol=", ycol)
        #print("car.ori=", car.orientation, "car.x=",car.x, "car.y=", car.y, "xcol=", xcol,"ycol=",ycol)
        if (car.orientation =="h" and car.x == xcol):
            if (car.y-1 == ycol and car.y-1>=0 and self.board[car.x][car.y-1] == "."): # move left and not over board
                #print ("car.y-1=",car.y-1, "self.board[car.x][car.ycol] =",self.board[car.x][car.ycol])
                return 1
            elif (car.size == 2 and car.y+2 == ycol and  car.y+2<6 and self.board[car.x][ycol] == "."):   # move right for a small car and not over board
                return 2
            elif (car.size == 3 and car.y+3 == ycol and car.y+3 <6 and self.board[car.x][ycol] == "."):  # move right a big car
                return 3
            else:
                #print ( "h move", "c.ori=", car.orientation)
                return 0
        elif (car.orientation =="v" and car.y == ycol):
            #print("car.ori=", car.orientation, "car.x=",car.x, "car.y=", car.y, "xcol=", xcol,"ycol=",ycol)
            if (car.x-1 == xcol and self.board[xcol][car.y] == "."): # move up within board
                return 4
            elif (car.size == 2 and car.x+2 <= 5 and car.x+2 == xcol and self.board[xcol][car.y] == "."):   # move down for a small car
                return 5
            elif (car.size == 3 and car.x+3 <= 5 and car.x +3 == xcol and self.board[xcol][car.y] == "."):  # move down for a big car
                return 6
            else:
                  return 0

        else:
            return 0

    def gameOver(self):
        """  if we can move the target car: the first car 0 to position (2,5), then the game is over
             a test to help a game loop to know when the puzzle is solved """
        print("enter gaveover")
        targetCar= self.cars[0]
        empty = targetCar.y+2
        g_count=0
        while (self.board[targetCar.x][empty] == "."):
            if (empty == 5):
                print(" gaveover", targetCar.y)
                for j in range(g_count):
                    if (targetCar.y+2 == 6):
                        self.board[targetCar.x][targetCar.y+1] == 0
                        self.board[targetCar.x][targetCar.y-1] == "."
                        print("TTT")
                    elif (targetCar.y+2 <6):
                        print("MM")
                        self.moveCar(targetCar.x,targetCar.y+2,0)
                self.printState()
                return True
            else:
                empty+=1
                g_count+=1
        return False   # there are cars on the target car way

    def gameOver1(self):
        """  if we can move the target car: the first car 0 to position (2,5), then the game is over
             a test to help a game loop to know when the puzzle is solved """
        targetCar= self.cars[0]
        print("BB1",targetCar.x, targetCar.y)
        #ox, oy = copy.deepcopy(targetCar.x, targetCar.y)
        empty = targetCar.y+2
        while (self.board[targetCar.x][empty] == "."):
            if (empty == 5):
                #ox, oy = copy.deepcopy(targetCar.x, targetCar.y)
                #targetCar.y=4
                #self.board[2][4] = 0
                #self.board[2][5] = 0
                
                self.board[targetCar.x][targetCar.y]="."
                self.board[targetCar.x][targetCar.y+1]="."
                self.board[2][4] = 0
                self.board[2][5] = 0
                print("TT",targetCar.x, targetCar.y)
                print( "BB",self.board[2][4], self.board[2][5])
                targetCar.y=4
                self.printState()
                return True
            else:
                empty+=1  
        return False   # there are cars on the target car way

    def isgameover(self,xcol, ycol,carid):
        #gamevercar= self.cars[0]
        #print("isgameover", xcol, ycol, carid)
        #if ( gamevercar.x == 2 and (gamevercar.y == 4 or gamevercar.y == 5)):
        if ( carid == 0 and xcol == 2 and (xcol == 4 or ycol == 5)):
            return True
        else:
            return False
        
        
    

    def whichcarmoving(self):
        """ used to input a position x and y where the carid will move to
            x, y must be in range [0, 5]"""
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
    restr=[]
    for s in str1:
        if ( s != rmstr and s != " "):
            restr+=s

    return restr


if __name__ == "__main__":
#def main():
    running = True
    while running:
        """ star play game,  initial a game board as 6x6 grid"""
        board = [['.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.']]
    
        gaming= Game(board)
        gaming.loadGame()
        move_count = 0
        while True:
            #if(x.gameOver1()):
                #print ("gameover! You win! Total moves is ",  move_count+1)
                #break
            (xcol, ycol, carid) = gaming.whichcarmoving()
            
            move_count += gaming.moveCar(xcol,ycol,carid)
            print ("GGG",gaming.isgameover(xcol, ycol, carid))
            if (carid == 0 and gaming.isgameover(xcol, ycol, carid)):
                print ("gameover! You win! the total valid steps you enter is: ",move_count, "\n" )
                #gaming.printState()
                running =False
                break
            gaming.printState()
##        again = input ("Do you want to play again: Y/y to replay, others to quit ?")
##        if (again == "Y" or again == "y"):
##            continue
##        else:
##            break
        
        
            
    
