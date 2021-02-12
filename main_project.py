# Izge Bayyurt
# CS152
# Project 11
# main_project.py
# This is the game file for the main code, the first demo of the asteroids game

import graphics as gr
import physics_objects as pho
import collision as coll
import ship
import random
import math
import time

def bubbleSort(list,i):
    """ Sorts a list of numbers in increasing order.
    The parameter is is the length of the list. """

    if i == 1:
        return list

    else:
        for k in range(i - 1):
            if list[k] > list[k+1]:
                list[k], list[k+1] = list[k+1], list[k]

        bubbleSort(list,i-1)

def angleSort(list,quadrant,length):
    """ Sorts vectors based on their angle
        Added error handling for cases with zero division error
        Length parameter is the length of the list (for recursion) """

    if quadrant == 1:
        if length == 0 or length == 1: # base case
            return list

        for i in range(length-1):
            try:
                if list[i][1]/list[i][0] > list[i+1][1]/list[i+1][0]:
                    list[i], list[i+1] = list[i+1], list[i]
            except ZeroDivisionError:
                continue

        angleSort(list,quadrant,length-1) # recursive call

    elif quadrant == 2:
        if length == 0 or length == 1: # base case
            return list

        for i in range(length-1):
            try:
                if list[i][1]/list[i][0] > list[i+1][1]/list[i+1][0]:
                    list[i], list[i+1] = list[i+1], list[i]
            except ZeroDivisionError:
                continue

        angleSort(list,quadrant,length-1) # recursive call

    elif quadrant == 3:
        if length == 0 or length == 1: # base case
            return list

        for i in range(length-1):
            try:
                if list[i][1]/list[i][0] > list[i+1][1]/list[i+1][0]:
                    list[i], list[i+1] = list[i+1], list[i]
            except ZeroDivisionError:
                continue

        angleSort(list,quadrant,length-1) # recursive call

    elif quadrant == 4:
        if length == 0 or length == 1: # base case
            return list

        for i in range(length-1):
            try:
                if list[i][1]/list[i][0] > list[i+1][1]/list[i+1][0]:
                    list[i], list[i+1] = list[i+1], list[i]
            except ZeroDivisionError:
                continue

        angleSort(list,quadrant,length-1) # recursive call

    return list

def vectorsToPoints(vectorList,points):
    """ This function adds vectors end to end to gather points of the polygon """
    """ It takes in a list of vectors and an empty points list (for recursion) """

    if len(points) == 0: # first call
        points.append([vectorList[0][0],vectorList[0][1]])
        vectorsToPoints(vectorList[1:],points)
    else:
        points.append([round(points[-1][0]+vectorList[0][0],2),
                       round(points[-1][1]+vectorList[0][1],2)])
        if len(vectorList) == 1: # base case
            return
        else:
            vectorsToPoints(vectorList[1:],points) # recursive call

    return points

def asteroidCreator(numCorner,win):
    """ This function creates asteroids with numCorner amount of corners """

    xCoor = []
    yCoor = []

    # Creating coordinates of the points
    coorRange = [i for i in range(-10,10) if i not in [0]] # to avoid 0

    for i in range(numCorner):
        xCoor.append(round(random.choice(coorRange)*random.uniform(0.01,1),2))
        yCoor.append(round(random.choice(coorRange)*random.uniform(0.01,1),2))

    # Sorting the coordinates
    bubbleSort(xCoor,len(xCoor))
    bubbleSort(yCoor,len(yCoor))


    # Isolating the extreme points
    xSmallest = xCoor.pop(0)
    xLargest = xCoor.pop()

    ySmallest = yCoor.pop(0)
    yLargest = yCoor.pop()

    # Shuffle the coordinates
    random.shuffle(xCoor)
    random.shuffle(yCoor)

    # Divide them into two sets
    xCoorLower = xCoor[:len(xCoor)//2]
    xCoorUpper = xCoor[len(xCoor)//2:]

    yCoorLower = yCoor[:len(yCoor)//2]
    yCoorUpper = yCoor[len(yCoor)//2:]

    # Append back the extreme points, and sort them again
    xCoorLower.append(xSmallest)
    xCoorLower.append(xLargest)
    xCoorUpper.append(xSmallest)
    xCoorUpper.append(xLargest)

    yCoorLower.append(ySmallest)
    yCoorLower.append(yLargest)
    yCoorUpper.append(ySmallest)
    yCoorUpper.append(yLargest)

    bubbleSort(xCoorLower,len(xCoorLower))
    bubbleSort(xCoorUpper,len(xCoorUpper))
    bubbleSort(yCoorLower,len(yCoorLower))
    bubbleSort(yCoorUpper,len(yCoorUpper))

    # Getting the vector lengths out of the points
    # We will get vectors in 4 directions from 4 lists
    xVectorLengths = []
    yVectorLengths = []

    for i in range(len(xCoorLower)-1):
        xVectorLengths.append(xCoorLower[i]-xCoorLower[i+1])
    for i in range(len(xCoorUpper)-1):
        xVectorLengths.append(xCoorUpper[i+1]-xCoorUpper[i])
    for i in range(len(yCoorLower)-1):
        yVectorLengths.append(yCoorLower[i]-yCoorLower[i+1])
    for i in range(len(yCoorUpper)-1):
        yVectorLengths.append(yCoorUpper[i+1]-yCoorUpper[i])

    random.shuffle(xVectorLengths)
    random.shuffle(yVectorLengths)

    # Creating the vectors
    vectors = []
    defaultVector = [0,0]

    for i in range(len(xVectorLengths)):
        defaultVector[0] = round(xVectorLengths[i],2)
        defaultVector[1] = round(yVectorLengths[i],2)
        vectors.append(defaultVector.copy())

    # Sorting vectors by their angle
    sortedVectors = []
    quadrant1 = []
    quadrant2 = []
    quadrant3 = []
    quadrant4 = []

    ### Dividing them by quadrants
    for vector in vectors:
        if vector[0] >= 0 and vector[1] >= 0:
            quadrant1.append(vector)
        elif vector[0] <= 0 and vector[1] >= 0:
            quadrant2.append(vector)
        elif vector[0] <= 0 and vector[1] <= 0:
            quadrant3.append(vector)
        elif vector[0] >= 0 and vector[1] <= 0:
            quadrant4.append(vector)

    ### Sorting them inside the quadrants
    quadrant1 = angleSort(quadrant1,1,len(quadrant1))
    quadrant2 = angleSort(quadrant2,2,len(quadrant2))
    quadrant3 = angleSort(quadrant3,3,len(quadrant3))
    quadrant4 = angleSort(quadrant4,4,len(quadrant4))

    ### Adding them up in order
    for vector in quadrant1:
        sortedVectors.append(vector)
    for vector in quadrant2:
        sortedVectors.append(vector)
    for vector in quadrant3:
        sortedVectors.append(vector)
    for vector in quadrant4:
        sortedVectors.append(vector)

    # Creating the points for the polygon
    points = []
    points = vectorsToPoints(sortedVectors,points)

    rightEdge = 0
    leftEdge = 0
    upperEdge = 0
    lowerEdge = 0

    # getting the boundaries for the asteroid
    for point in points:
        if point[0] > rightEdge:
            rightEdge = point[0]
        elif point[0] < leftEdge:
            leftEdge = point[0]
        if point[1] > upperEdge:
            upperEdge = point[1]
        elif point[1] < lowerEdge:
            lowerEdge = point[1]

    # Width and height are only required since it is a child of rotating_block class
    width = rightEdge - leftEdge
    height = upperEdge - lowerEdge

    centerPoint = [(rightEdge + leftEdge) / 2 , (upperEdge + lowerEdge) / 2]

    asteroid = pho.Asteroid(win,width,height,points,centerPoint[0],centerPoint[1])

    return asteroid

def asteroidSpawner(frame,rate,win):

    """ Spawns asteroids from different sides of the screen """
    """ Rate parameter specifies how often to spawn asteroids """

    if frame % rate == 0:

        # Getting width and height of the screen
        h = win.getHeight()
        w = win.getWidth()

        # Dividing them by the scale we are using (10)
        h /= 10
        w /= 10

        asteroid = asteroidCreator(random.randint(5,12),win)

        side = random.randint(1,4) # picking a random side to spawn

        # rotational velocity range, when 0
        # rotate method is not called, causing bugs
        rotRange = [i for i in range(-40,40) if i not in [0]]

        if side == 1: # Left
            asteroid.setPosition([random.randint(-20,-15),random.randint((h/2)-10,(h/2)+10)])
            asteroid.setVelocity([random.randint(5,10),random.randint(-5,5)])
            asteroid.setRotVelocity(random.choice(rotRange))
            asteroid.initiate()


        if side == 2: # Top
            asteroid.setPosition([random.randint((w/2)-10,(w/2)+10),random.randint(h+15,h+20)])
            asteroid.setVelocity([random.randint(-5,5),random.randint(-10,-5)])
            asteroid.setRotVelocity(random.choice(rotRange))
            asteroid.initiate()


        if side == 3: # Right
            asteroid.setPosition([random.randint(w+15,w+20),random.randint((h/2)-10,(h/2)+10)])
            asteroid.setVelocity([random.randint(-10,-5),random.randint(-5,5)])
            asteroid.setRotVelocity(random.choice(rotRange))
            asteroid.initiate()

        if side == 4: # Bottom
            asteroid.setPosition([random.randint((w/2)-10,(w/2)+10),random.randint(-20,-15)])
            asteroid.setVelocity([random.randint(-5,5),random.randint(5,10)])
            asteroid.setRotVelocity(random.choice(rotRange))
            asteroid.initiate()

        return asteroid

def ccw(A,B,C):
    """ Checks if the two lines are counterclockwise or not """
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

def intersect(A,B,C,D):
    """ Returns true if line segments AB and CD intersect """
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def collisionDetecter(shipPoints,asteroidPoints):
    """ This function detects collisions between asteroids and the spaceship """

    # Getting ship's corners
    sP1 = shipPoints[0]
    sP2 = shipPoints[1]
    sP3 = shipPoints[2]

    # Here, we check for every possible combination of line intersections
    # If one of them is crossing, then we have a crossing
    # If none of them are crossing, then we don't have a crossing
    for i in range(len(asteroidPoints)-1):

        intersectTest = intersect(sP1,sP2,asteroidPoints[i],asteroidPoints[i+1])
        if intersectTest == True:
            return True

        intersectTest = intersect(sP1,sP3,asteroidPoints[i],asteroidPoints[i+1])
        if intersectTest == True:
            return True

        intersectTest = intersect(sP2,sP3,asteroidPoints[i],asteroidPoints[i+1])
        if intersectTest == True:
            return True

    # These specific cases check for the line between last point and first point
    intersectTest = intersect(sP1,sP2,asteroidPoints[-1],asteroidPoints[0])
    if intersectTest == True:
        return True

    intersectTest = intersect(sP1,sP3,asteroidPoints[-1],asteroidPoints[0])
    if intersectTest == True:
        return True

    intersectTest = intersect(sP2,sP3,asteroidPoints[-1],asteroidPoints[0])
    if intersectTest == True:
        return True

    return False

def main():
    """ Main loop """

    win = gr.GraphWin("Asteroids",700,700,False)

    # Intro texts
    welcomeText = gr.Text(gr.Point(350,310),"Welcome to Asteroids!")
    welcomeText.setSize(30)
    welcomeText.draw(win)

    welcomeText2 = gr.Text(gr.Point(350,350),"Press space to start")
    welcomeText2.setSize(20)
    welcomeText2.draw(win)

    key = ""
    frame = 0

    # Flickering effect
    while key != "space":
        key = win.checkKey()
        if  key != "space" and frame % 3000 == 100:
            welcomeText2.undraw()
        elif frame % 3000 == 1000:
            welcomeText2.draw(win)
        frame += 1

    welcomeText2.undraw()
    welcomeText.undraw()

    # Creating the spaceship
    spaceship = ship.Ship(win,35,35)
    spaceship.draw()

    # Variables for the game:

    asteroids = [] # List of asteroids
    frame = 0 # Frame number
    key = "" # Current pressed key
    dt = 0.01 # Update time
    delta = 3 # Thrust rate
    gamma = 60 # Turn rate
    points = 0

    while key != "q":

        key = win.checkKey()
        collided = False

        # spawn asteroids
        asteroid = asteroidSpawner(frame,120,win)

        # left turn
        if key == "Left":
            spaceship.setRotVelocity(spaceship.getRotVelocity()+gamma)
            spaceship.setFlickerColor(["yellow","orange"])
            spaceship.setFlickerOn()

        # right turn
        elif key == "Right":
            spaceship.setRotVelocity(spaceship.getRotVelocity()-gamma)
            spaceship.setFlickerColor(["yellow","orange"])
            spaceship.setFlickerOn()

        # thrust
        elif key == "Up":
            a = spaceship.getAngle()
            theta = a * math.pi / 180
            v = spaceship.getVelocity()

            v_new_x = v[0] + math.cos(theta) * delta
            v_new_y = v[1] + math.sin(theta) * delta

            spaceship.setVelocity([v_new_x,v_new_y])

            spaceship.setFlickerColor(["yellow","orange"])
            spaceship.setFlickerOn()

        # if we are not pressing any key, decrease the rotational velocity
        if key == "":
            if spaceship.getRotVelocity() != 0:
                spaceship.setRotVelocity(spaceship.getRotVelocity()*0.99)

        # if we create an asteroid, append it to the list
        if asteroid != None:
            asteroids.append(asteroid)

        # update the spaceship
        spaceship.update(dt)

        # update the asteroids
        for asteroid in asteroids:
            asteroid.update(dt)

        # getting the corners of the spaceship
        spaceshipCorners = spaceship.getBodyPoints()

        # checking for collisions
        for asteroid in asteroids:
            astCenter = asteroid.getAnchor()
            shipCenter = spaceship.getPosition()
            dx = (astCenter[0]-shipCenter[0])**2
            dy = (astCenter[1]-shipCenter[1])**2
            # if the centers are close enough, we can check for collisions
            if dx + dy < 400:
                astPts = asteroid.getCorners()
                collision = collisionDetecter(spaceshipCorners,astPts)
                if collision == True:
                    collided = True

        # if there is a collision
        if collided == True:
            score = frame
            key = win.checkKey()

            spaceship.undraw()

            for asteroid in asteroids:
                asteroid.undraw()

            endingText = gr.Text(gr.Point(350,290),"Game over...")
            endingText.setSize(30)
            endingText.draw(win)

            instructions = gr.Text(gr.Point(350,370),"Press q to quit")
            instructions.setSize(18)
            instructions.draw(win)

            finalScore = gr.Text(gr.Point(350,330),"Your score: " + str(score//10))
            finalScore.setSize(18)
            finalScore.draw(win)

            while key != "q":
                 key = win.checkKey()

            if key == "q":
                break

        # mechanism for making the ship stay inside screen
        moveit = False
        p = spaceship.getPosition()

        if p[0] < 0:
            p[0] += win.getWidth()/10
            moveit = True
        elif p[0] > win.getWidth()/10:
            p[0] -= win.getWidth()/10
            moveit = True

        if p[1] < 0:
            p[1] += win.getHeight()/10
            moveit = True
        elif p[1] > win.getHeight()/10:
            p[1] -= win.getHeight()/10
            moveit = True

        if moveit:
            spaceship.setPosition(p)
            moveit = False

        if frame % 10 == 0:
            win.update()
            time.sleep(dt*0.5)

        frame += 1

    win.close()

if __name__ == "__main__":
    main()

# References
# http://cglab.ca/~sander/misc/ConvexGeneration/convex.html
# https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
