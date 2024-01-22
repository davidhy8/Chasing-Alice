import pygame
from rushhour import Game
import time


class CarSprite:
    """Create a class that allows allows all the car information to be loaded
       onto the pygame graphical game board."""

    
    def __init__(self, img="", target_posn=0,orientation=0, carid = None):
        """ img = cars images to be loaded
            target_posn = position to load car
            oreintation = car orientation to load car
            carid = car to be loaded
            Create and initialize a queen for this target position on the board"""
        self.image = img
        self.posn = target_posn
        self.orientation= orientation
        self.carid= carid

        
    def update(self, carid,tp):
        """carid = update pygame graphical game board state based on car id
           tp = position to move car to
           Update pygame graphical game board state with car movement"""
        uptimes= 0                                                      #number of updated moves
        for sprite in car_sprites:                                      #Find the moving car
                if sprite.carid == carid:
                      sprite.posn = tp
                      uptimes+=1
        return uptimes
                      

    def loadcar(self, target_surface):
        """target_surface = loaction to load image
           Load image at target_surface."""
        target_surface.blit(self.image,self.posn )

        
    def getTargetPosition(self, direct):
        """ direct = movement indication to move car
            Find the valid position for the car to move to based on the car's position,
            size and orientation"""
        (x, y) = self.posn                                          #Current car position
        (new_x_pos,new_y_pos) = (x,y)                               #Position of rear of car to be moved to (rear = right side/bottom)
        (nextpox, nextpoy) = (x,y)                                  #Position of front of car to be moved to (front = top/leftside)

        my_height = self.image.get_height()                         #Retrieve image size
        my_width = self.image.get_width()

        if self.orientation == "h":                                 #Click onto a horizontal vehicle
            if direct == 1:                                         #Push mouse left click = move left		
                if (x-sq_sz >= 0):                                 
                    new_x_pos = x-sq_sz                             
                    nextpox = x-sq_sz
            else:                                                   #Mouse right click and scroller click = move right
                if (x + my_width <surface_sz):
                    new_x_pos = x+ my_width                         
                    nextpox =x + sq_sz                              
        elif (self.orientation == "v"):                             #Click onto a vertical vehicle
            if direct == 1:                                         #Push mouse right key and scroller click = move right	
                if y - sq_sz>=0:                                
                    new_y_pos= y - sq_sz                            
                    nextpoy = y - sq_sz
            else:
                if (y + my_height <surface_sz):
                    new_y_pos = y + my_height                       #Push mouse right key and scroller click = Move right
                    nextpoy = y + sq_sz  
        self.target_posn = (new_x_pos, new_y_pos)                   #Update position of rear and front of car
        next_posn = (nextpox , nextpoy)
        return (self.target_posn, next_posn)
	
		
    def thereisacar(self, tp):
        """tp = target position to move car to
            Check if the target position is occupied or not"""
        for sprite in car_sprites:                                  #Find the moving car
                if sprite.contains_point(tp):
                    return sprite                                   #Return car if target position if unoccupied
                    break
        return []                                                   #Didn't find any car in this position                                
            	

    def contains_point(self, pt):
        """ pt = clicked position
            Return true if grid on graphical game board contains point pt """
        (my_x, my_y) = self.posn
        my_width = self.image.get_width()
        my_height = self.image.get_height()
        (x, y) = pt
        return ( x >= my_x and x < my_x + my_width and              
                 y >= my_y and y < my_y + my_height)                #True if click is on a car

if __name__ == "__main__":
    board = [['.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.']]                    #Initialize text board

    game= Game(board)                                               #Initialize game board
    game.loadGame()                                                 #Load cars to game board
    
    pygame.init()
    colors = [(128,128,128), (192,192,192)]                         #Set up board background colors
    my_font = pygame.font.SysFont("Courier", 16)
    gameover_font = pygame.font.SysFont("Courier", 64)              #Initialize fonts
    n = 6                                                           #Create 6x6 board

    surface_sz = 480                                                #Proposed physical surface size.
    sq_sz = surface_sz // n                                         #Sq_sz is length of each square.


    surface = pygame.display.set_mode((surface_sz, surface_sz))     #Create the surface of (width, height), and its window.

    ##Load car images according to orientation and size
    smallcarv = pygame.image.load("smallcarv.jpeg")                 
    smallcarh = pygame.image.load("smallcarh.jpeg")
    targetcar = pygame.image.load("targetcar.jpeg")
    bigcarv = pygame.image.load("bigcarv.jpeg")
    bigcarh = pygame.image.load("bigcarh.png")
    finishline= pygame.image.load("finished.png")
    
    car_sprites=[]
    ##Add all game cars according to its oreintation and car size to car_sprites
    for car in game.cars:       
        if car.orientation == "h":
            if car.size== 2:
                if (car.carid == 0):
                    a_car=CarSprite(targetcar,(car.y*sq_sz, car.x*sq_sz), car.orientation, car.carid)   #Create new CarSprite object
                else:
                    a_car=CarSprite(smallcarh,(car.y*sq_sz, car.x*sq_sz), car.orientation,car.carid)
            else:
                a_car=CarSprite(bigcarh,(car.y*sq_sz, car.x*sq_sz), car.orientation, car.carid)               
        elif car.orientation == "v":
            if car.size== 2:        
                a_car=CarSprite(smallcarv,(car.y*sq_sz, car.x*sq_sz), car.orientation,car.carid)
            else:
                a_car=CarSprite(bigcarv,(car.y*sq_sz, car.x*sq_sz),car.orientation,car.carid)
        car_sprites.append(a_car)
    goverx, govery = (0,0)              #Initialize position of target car to detect gameover
    tcarid = 100                        #Initialize target carID 
    move_count = 0
   
    while True:
        #Look for an event from keyboard, mouse, etc.
        ev = pygame.event.poll()                    
        if ev.type == pygame.QUIT:
            print ("pygame.QUIT")
            break
        
        if ev.type == pygame.MOUSEBUTTONDOWN:
            posn_of_click = ev.dict["pos"]    # Get the coordinates of click
            x,y = posn_of_click
            button_of_click = ev.dict["button"] #Get the button of the click(left click = move left, move up and right click = move down, move right)   
            
            clickcar = CarSprite()              #Initialize click car object
            clickcar = clickcar.thereisacar(posn_of_click)
            if clickcar == []:                  #Check if car is clicked
                print( "No car in this position")
                continue
            else:
                (tp, np) = clickcar.getTargetPosition(button_of_click)  #Get car's next move position
                (x, y) = np
                (nx,ny)= (int(x/sq_sz),int(y/sq_sz)) 
                (tpx, tpy) =tp
                goverx =int(tpx/sq_sz)
                govery =int(tpy/sq_sz)
                hascar = CarSprite()                                    #Initialize hascar object
                hascar = clickcar.thereisacar(tp)                       #Check if the position to be moved to is occupied or not
                if hascar == []:                                        #there is no car on this position
                    game.moveCar(nx,ny, clickcar.carid)
                    tcarid = clickcar.carid
                    move_count += clickcar.update(clickcar.carid, np)   #Move Car
                else:
                    print (" No space to move car")                
        
       	# Draw a fresh background game board
        for row in range(n):                                            # Draw each row of the board.
            c_indx = row % 2                                            # Alternate starting color
            for col in range(n):                                        # Run through cols drawing squares
                the_square = (col*sq_sz, row*sq_sz, sq_sz, sq_sz)
                surface.fill(colors[c_indx], the_square)
                # Now flip the color index for the next square
                c_indx = (c_indx + 1) % 2
        surface.blit(finishline, (400, 160))
        the_text = my_font.render("Move count(s) = {0}".format(move_count), True, (220,20,60))  #Text editing
        for spcar in car_sprites:                                   #Load car image onto board
            spcar.loadcar(surface)
        surface.blit(the_text, (10, 10))                            #Load text onto board      
        
        if(game.isgameover(govery, goverx, tcarid)):    
            surface.blit(finishline, (0, 80))
            time1= time.clock()
            
            gaveover_text1 = gameover_font.render("Game Over!", True, (51,210,255))
            gaveover_text2 = gameover_font.render(" You win!", True, (220,20,60))
            
            surface.blit(gaveover_text1, (20, 160))
            surface.blit(gaveover_text2, (0, 200))
            if int(time1) > 5:                 #Game ends in 5 seconds after game over     
                print ("Time up")
                break
        pygame.display.flip()

    pygame.quit()


        
    

    
