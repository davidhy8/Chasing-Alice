#David Yang, UCID 30043476, all parts solved
import random


def initialinput(x, y, text=None ):
    """ x and y = is the range for a input number
        text = a prompt for the input and can be omitted if not required
        This function accepts an integer between x and y, and also ensures that numbers or characters
        are not accepted if not desirable or not in the range. """       

    while True:                 
        n = input(text)                                 #asks for input with prompt text    
        try:
            n = int (n)                                 #makes input a integer 
            if (n >= x and n <= y ):                    #Checks if input is in the given range
                return n                                #if true, returns input
            else:
               print("Please enter an integer between", x," and ", y,".") 
        except ValueError:                              #If any other value is entered, exception handle does not accepts and asks for another input
            print("Please enter an integer between", x," and ", y,)

    
def gameover(n):
    """ n = amount of nuts on the table
        This function is used to determine if the game has ended by detecting the variable n, which is the amount of nuts on the table."""

    if (n<=0):                                          #If n<=0 that means the there is no nuts on the table and the game is over
        return True
    else:                                               #If not, then the game continues
        return False


def humanvshuman(n):
    """ n = the number of nuts on the table initially.
        The function allows two players to play against each other with n number of nuts that is passed into the function"""

    p1tx= "\nPlayer 1: How many nuts do you take (1-3)?" #Creates text that will be printed by initialinput(x,y,text=None) to ask player 1 to make a move
    p2tx= "\nPlayer 2: How many nuts do you take (1-3)?" #Creates text that will be printed by initialinput(x,y,text=None) to ask player 2 to make a move    
    while True:                                         
        play1 = initialinput(1,3, p1tx)                 #initialinput(1,3,p1tx) asks for input of an integer between 1 and 3 with the prompt: p1tx
        if gameover(n-play1):                           #If gameover(n-play1) returns True, player loses as p1 took the last nut
            pl = "Player 1,"                            #A text to record that player 1 lost
            break                                       #Game is over, so break is used to exit the while loop
        else:                                           
            n= n-play1                                  #Game continues, the number of nuts on the table is reduced by play1 and saved as n
            print("There are ",n, " nuts on the board") 

        play2 = initialinput(1,3,p2tx)                  #An input from player 2 of an integer between 1 and 3 with the text prompt p2tx
        if gameover(n-play2):                           #If gameover(n-play2) returns True, player 2 loses as p2 took the last nut
            pl = "Player 2,"                            #A text to record that player 2 lost
            break                                       #Game is over, so break is used to exit the while loop
        else:                                           
            n= n-play2                                  #Game continues, the number of nuts on the table is reduced by play2 and saved as n
            print("There are ", n, " nuts on the board")
    print (pl, ": You lost")                           #Prints who lost


def createai(n):
    """ Cited code from a3 assignment Create A machine player which is a 3 item list
        n = the number of nuts on the table initially
        The function creates a table in a form of a nested list, hats. Each item in hats contains
        another list of the form [1,1,1]. """
    
    hats = []                                           #Creates empty list: hats
    for i in range(n):                                  #A for loop that is ran n number of times
        row = [1, 1, 1]                                 
        hats += [row]                                   #row is added to hat in each iteration
    return hats                                         #The hats list is returned 


def select(p):
    """ Cited code from a3 assignment.
        p = a list of three integers, where each integer represents the probability of obtaining a move.
        The index p[0],p[1],p[2] is equal to the probability of getting move 0,1,2 respectively. The function then returns a move
        propotional to the probabilities."""

    total = p[0] + p[1] + p[2]                          #Adds the three integers together to get the upper limit for the probability
    r_int = random.randint(1, total)                    
    if (r_int <= p[0]):                                 #The random number falls in the range of p[0] probability
        move = 0                                        
    elif (r_int <= p[0] + p[1]):                        #The random number falls in the range of p[1] probability
        move = 1                                        
    else:                                               #The random number falls in the range of p[2] probability
        move = 2                                        
    return move                                         #Returns move value obtained


def humanvsai(n, ai):
    """ n = number of nuts
        ai = AI choosen to play against
        This function allows a player to play an in a game with ai, a specific AI, with n number of nuts."""

    p1tx= "\nPlayer 1: How many nuts do you take (1-3)?" #Text prompt used in gameinput(1,3,p1tx) function for player 1 to enter an integer 
    p2tx= "\nAI select ?"                               #Text to show player that the AI is making a decision
    while True:
        play1 = initialinput(1,3, p1tx)                 #Player 1 inputs a integer between 1-3 with text prompt p1tx
        if gameover(n-play1):                           #Checks if there are no nuts after play1.
            pl = "Player 1,"                            #If true,"Player 1" is recorded as loser
            break                                       #Quits while loop as game is over
        else:
            n= n-play1                                  #Game continues, the number of nuts on the table reduced by play1
            print("There are ",n, " nuts on the board")
        aiselect=select(ai[n-1])                        #select(ai[n-1]) returns a move specific to that nut amount and probability
        print("\nAI select ", aiselect+1)               
        if gameover(n-aiselect-1):                      #Checks if there are no nuts after aiselect
            pl = "AI,"                                  #If true,"AI" is recorded as loser
            break                                       #Quits while loop as game is over
        else: 
            n= n-aiselect-1                             #Game continues, the number of nuts on the table reduced by aiselect
            print("There are ", n, " nuts on the board")
    print (pl, ": You lost")
    return


def trained(ai, winner):
    """ai = The ai that is being trained
       winner = The steps of the winning AI in a list
       The function updates ai with the winner list that contains steps- that give the AI a higher probability of winning."""

    for trace in winner:                                #Go through each individual step in winner list
        item = ai[trace[0]]                             #Find which index in the ai list to update
        item[trace[1]]= item[trace[1]]+1                #In the list at trace[0] index, update its smaller list's index:trace[1]
        ai[trace[0]]=item                               #Assign the updated value back to ai list
        

def aivsai(ai1, ai2, n):
    """ai1 = ai machine 1
       ai2 = ai machine 2
       n =  the number of nuts initially
       The function trains an ultimate AI by making two ai's play against each other and
       recording the steps that result in the win as either trace1 or trace2"""

    trace1= []                                          #Records the steps (hat number, nuts taken) tooken by ai1
    trace2= []                                          #Records the steps (hat number, nuts taken) tooken by ai2
    while True:
        aiselect=select(ai1[n-1])                       #ai1 selects a move
        if gameover(n-aiselect-1):                      #Detects if game is over
            player = 1                                  #If true, records ai1 as the loser
            break                                       #Exits loop with break
        else:
            steps= [n-1, aiselect]                      #Records the steps(hat number, nuts taken) in this step
            n= n-aiselect-1
            trace1.append(steps)                        #Puts steps into the list
        aiselect=select(ai2[n-1])                       #ai2 selects a move
        if gameover(n-aiselect-1):                      #Detects if game is over
            player = 2                                  #If true, records ai2 as the loser
            break                                       #Exits loop with break
        else:
            steps= [n-1, aiselect]                      #Records the steps(hat number, nuts taken) in this step
            n= n-aiselect-1
            trace2.append(steps)                        #Puts steps into the list
    if (player == 1):
        return trace2                                   #Play1 lost, return winner list to training Machine (ai2)
    else:
        return trace1                                   #Play2 lost, return winner list to training Machine (ai1)
    
    
def trainingai(n):
    """n = number of nuts initially
       The function trains the AI TRAIN_TIMES number of times with n number of nuts"""

    TRAIN_TIMES = 100000                                #Number of times the AI will be trained as required
    print ("Training AI, please wait...")               #Tells player waiting while AI is being trained 
    ai1 = createai(n)                                   #Create ai machine 1
    ai2 = createai(n)                                   #Create ai machine 2
    trainedai = ai1                                     #Initialize trained machine as ai1 at beginning
    for x in range(TRAIN_TIMES):                        #Training ai TRAIN_TIMES of times
        trace = aivsai(ai1,ai2,n)                       #Machine ai1 vs machine ai2 and return winning ai trace
        trained(trainedai,trace)                        #Update trained ai with winner ai's trace
    return trainedai                                    #Return the trained ai



def option_menu(n):
    """n = number of nuts initially
       The function creates an option menu for the user to choose which game
       mode they want to play by entering integer 1,2, or 3."""

    print("Options:")
    print("  Play against a friend (1) \n  Play against the computer (2)\n  Play against the trained computer (3)")
    text = "Which option do you take (1-3)?"
    op = initialinput(1,3,text)                         #Asks user to choose game mode using integer input 1,2,3
    print("\nThere are", n, " nuts on the board.")
    return op
#Return option choosen
   


def main():
    """Main function that allows user to input number of nuts to play with between 10-100. The function also allows user to choose
       to play against another user, play against untrained ai, and play against a trained ai. The function also allows the game
       to be played again."""

    print ("Welcome to the game of nuts!")
    tryagain = 1                                            #try again = 1 to initialize game start
    text = "\nHow many nuts are there on the table initially (10-100)? "
    num = initialinput(10,100, text)                        #Asks user for how many nuts they want to play with
    havetrained = 0                                         #to indicate that the ai has not been trained yet
                                 
    while tryagain == 1:                                    #only runs when user enters 1 to play again
        op = option_menu(num)                               #Obtains user selection for game mode
        if (op == 1):
            humanvshuman(num)                               #user choose option 1, play against another player
        elif (op == 2):
            ai = createai(num)
            humanvsai(num,ai)                               #user choose option 2, play against an untrained ai
            print(ai)                                      #COMMENTED PRINT STATEMENT
        elif  (op== 3):                                     #user choose option 2, play against an trained ai
            if (havetrained == 0):                          #Check if ai has been trained or not
                trainedai = trainingai(num)                 #training ai 
                havetrained = 1                             #once ai is trained, a flag is returned to indicate it is trained
            humanvsai(num,trainedai)                        #user choose option 3, play against an already trained ai
            print(trainedai)                               #COMMENTED PRINT STATEMENT 
        text = "\nPlay again (1 = yes, 0 = no)?"            
        tryagain = initialinput(0,1,text)                   #User selects if they want to play again


main()

