"""Code by David Yang"""


import turtle
import random
import math


def reachboundary(x,y,myboard):
	"""Determine if the turtles are in the canvas"""
	if ( abs(x) > myboard or abs(y) > myboard ):
		return True
	else:
		return False
		

def mycanvas_setup(high,wide,title,bg_color):
	"""Create a turtle canvas(my screen) of given size and color"""
	turtle.setup(high,wide)							# Determine the window size
	mycanvas = turtle.Screen()						# Get a reference to the window
	mycanvas.title(title)							# Setting title of canvas a given title
	mycanvas.bgcolor(bg_color)						# Setting background color of canvas as given color
	return mycanvas
	

def make_turtle(mycolor, x=None, y=None):
	"""create a turtle of given color; for later when creating Alex turtle in the middle of the canvas and Alice turtle located at a random location"""
	myturtle = turtle.Turtle()
	myturtle.color(mycolor)
	myturtle.shape("turtle")
	if (x != None and y != None):
		myturtle.goto(x,y)							# makes turtle goto location (x,y) if the coordinates for its start point is given
	return myturtle

		
def get_random_value(myrange):
	"""Obtain random number to spawn alice randomly in main function when going out of bounds or in the beginning"""
	rng = random.Random()
	ran_num = rng.randrange(-myrange,myrange)
	return ran_num

	
def onkey_move(t,cv,myrange):
	"""To move Alex as directed by the player using the keyboard.
			w: move forwards by 30 pixels
			a: turn left for 45 degrees
			s: move backwards by 30 pixels
			d: turn right for 45 degrees
		If Alex crosses the canvas's boundary which is given as myrange, he will also reappear at a random location on the canvas. Creates general function that allows any turtle named  t to be commanded by user"""
	inputKey = input(" Move Alex: ")
	while True:
		if inputKey == "w":
			t.forward(30)
			break
		elif inputKey == "a":
			t.left(45)
			break
		elif inputKey == "s":
			t.back(30)
			break
		elif inputKey == "d":
			t.right(45)
			break
		else:
			print("invalid input, please try again")
			inputKey = input(" Move Alex: ")											# If invalid input is obtained, a new one is asked for before Alice makes a move
		x = t.xcor()																	# Obtain x coordinate of Alex
		y = t.ycor()																	# Obtain y coordinate of Alex
	if (reachboundary(x,y,myrange)):													# Check to see if Alex is out of the Canvas
		x = get_random_value(myrange)													# Obtains random x value to relocate Alex at if out of bounds
		y = get_random_value(myrange)													# Obtains random y value to relocate Alex at if out of bounds
		t.goto(x,y)																		#Reset Alex's location
	
	
def random_move(t,myrange):
	"""To generate Alice's random moves where it is 1/3 chance of turning left or right by 90 degrees, and 2/3 chance of moving forward by 20 pixels. Creates general """
	t.speed(1)																			#Slower Alice's movement speed
	ran_mov = get_random_value(6)														# Obtaining the probability for Alice's movements
	if (ran_mov == 1):
		t.left(90)
	elif (ran_mov == 2):
		t.right(90)
	else:
		t.forward(20)
	x = t.xcor()
	y = t.ycor()
	if (reachboundary(x,y,myrange)):													# Like for Alex, if Alice goes out of bounds, Alice is relocated randomly inside canvas
		x = get_random_value(myrange)
		y = get_random_value(myrange)
		t.goto(x,y)


def write_screen(step,distance):
	"""  Show every step distance between Alex and Alice on the screen """
	arg = "Step# "+str(step)+" Distance between Alex and Alice:" + str(distance)		#creates text to write on the turtle screen
	turtle.goto(110,220)																#Tells turtle to location to write text
	turtle.clear()																		
	turtle.write(arg, move=False,align="right", font=("Arial", 9,"normal"))				# tells turtle to write text created
	turtle.hideturtle()																	#Hides turtle arrow
	

def main():
	"""Main Function that calls all the functions created and runs the game"""
	windowHeight = 500																	#window size required
	mycv = mycanvas_setup(windowHeight,windowHeight,"Chasing Alice!", "white")
	alex = make_turtle("blue")															# makes alex turtle with the make_turtle function created
	x = get_random_value(windowHeight/2)												# obtains value to spawn alex in the middle of the screen
	y = get_random_value(windowHeight/2)												# obtains value to spawn alex in the middle of the screen
	alice = make_turtle("red",x,y)														# makes alice turtle with the make_turtle function created
	step = 0
	distance = alex.distance(alice)
	print("game start: Distance between Alex and Alice: ", distance)
	while (distance>30):
		onkey_move(alex,mycv,windowHeight/2)											# makes alex the turtle that takes user command
		random_move(alice,windowHeight/2)												# makes alice turtle a turtle that randomly moves
		step = step + 1																	# Used to count the steps taken
		distance = alex.distance(alice)													# Used to calculated distance between alex and alice
		write_screen(step,distance)														# writes the step and distance on the turtle screen
	turtle.done()

	
main()																					# calls main function to play the game
