# Izge Bayyurt
# CS152
# Project 11
# asteroids.py
# This is the game file for full asteroids game

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

def asteroidEraser(asteroids):
    """ Checks if the asteroids are outside the screen by a big amount
        Erases them if so """

    newAsteroidsList = []

    for asteroid in asteroids:

        if -100 < asteroid.getAnchor()[0] < 100:
            if -100 < asteroid.getAnchor()[1] < 100:
                newAsteroidsList.append(asteroid)
            else:
                asteroid.undraw()
        else:
            asteroid.undraw()

    return(newAsteroidsList)

def respawn(win,livesLeft,asteroids,spaceship):
    """ Ship respawning mechanics """

    if len(livesLeft) > 0:
        livesLeft[-1].undraw()
        del(livesLeft[-1])

    for asteroid in asteroids: # undraw the asteroids
        asteroid.undraw()

    asteroids = [] # empty the asteroid list

    # place the spaceship in the middle of the screen
    spaceship.setPosition([win.getWidth()/20,win.getWidth()/20])

    # reset the velocity
    spaceship.setVelocity([0,0])

    # reset the rotational velocity
    spaceship.setRotVelocity(0)

    # reset the starting rotation
    spaceship.rotate(math.pi * 2 / 180 - spaceship.getAngle())

    # draw the spaceship
    spaceship.draw()

    return asteroids, livesLeft

def lifeCreator(amount,win):
    """ Creates the lives and their visuals """

    lives = []

    for amount in range(amount):
        lives.append(ship.Ship(win,8+amount*3,67,radius=1))

    for life in lives:
        life.rotate(90)
        life.draw()
        life.lifeModifier()

    return lives

def main():
    """ Main loop """

    win = gr.GraphWin("Asteroids",700,700,False)
    win.setBackground("black")

    # Intro texts
    welcomeText = gr.Text(gr.Point(350,310),"Welcome to Asteroids!")
    welcomeText.setSize(30)
    welcomeText.setTextColor("white")
    welcomeText.draw(win)

    welcomeText2 = gr.Text(gr.Point(350,400),"Press space to start")
    welcomeText2.setSize(20)
    welcomeText2.setTextColor("white")
    welcomeText2.draw(win)

    controlsText1 = gr.Text(gr.Point(350,350),"Use up, right, and left arrow keys to move. Press space to use your boost.")
    controlsText1.setSize(20)
    controlsText1.setTextColor("white")
    controlsText1.draw(win)

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
    controlsText1.undraw()

    # Lives text
    livesText = gr.Text(gr.Point(50,30),"Lives: ")
    livesText.setTextColor("white")
    livesText.draw(win)

    # Boost text
    boostText = gr.Text(gr.Point(550,30),"Boost: ")
    boostText.setTextColor("white")
    boostText.draw(win)

    # Boost bar
    boostBar = pho.Bar(win,58,66,10,2)
    boostBar.setColor("blue")
    boostBar.draw()

    # Boost bar's outline
    boostBarOutline = pho.Bar(win,57.9,65.9,10.2,2.25)
    boostBarOutline.setOutline("white")
    boostBarOutline.draw()

    # Creating the spaceship
    spaceship = ship.Ship(win,35,35)
    spaceship.draw()

    # Creating the lives
    livesLeft = lifeCreator(3,win)

    # Variables for the game:

    asteroids = [] # List of asteroids
    explosions = [] # List for explosion animation
    frame = 0 # Frame number
    key = "" # Current pressed key
    dt = 0.01 # Update time
    delta = 3 # Thrust rate
    gamma = 60 # Turn rate
    zeta = 8 # Boost rate
    respawnFrame = -1000 # When to respawn the ship (initially set to small number)
    expRad = 60 # Explosion radius variable
    boostRemaining = 100 # Remaining boost
    gameOver = False # If the player dies enough times, we call closing scene
    score = 0 # Player's score

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

        # boost (if there is boost and the ship is not dead)
        elif key == "space" and boostRemaining > 10 and respawnFrame < 0:
            a = spaceship.getAngle()
            theta = a * math.pi / 180
            v = spaceship.getVelocity()

            v_new_x = v[0] + math.cos(theta) * zeta
            v_new_y = v[1] + math.sin(theta) * zeta

            spaceship.setVelocity([v_new_x,v_new_y])

            spaceship.setFlickerColor(["light blue","dark blue"])
            spaceship.setFlickerOn()
            boostRemaining -= 10

        # if we have less than 100 boost, we update the bar
        # and then increment the remaining boost (if the ship is alive)
        if boostRemaining < 100 and respawnFrame < 0:
            boostBar.setWidth((boostRemaining/100)*10)
            boostBar.update()
            boostRemaining += 0.1

        # if we are not pressing any key, decrease the rotational velocity
        if key == "":
            if spaceship.getRotVelocity() != 0:
                spaceship.setRotVelocity(spaceship.getRotVelocity()*0.99)

        # if we create an asteroid, append it to the list
        if asteroid != None:
            asteroids.append(asteroid)

        # update asteroids and set their color to white
        for asteroid in asteroids:
            asteroid.update(dt)
            asteroid.setOutline("white")
            asteroid.setFill("black")

        # update the spaceship
        spaceship.update(dt)

        # erase out-of-bounds asteroids every 120 frames
        # also increment score by 100 for each deleted asteroid
        if frame % 120 == 0:
            numAsteroids = len(asteroids)
            asteroids = asteroidEraser(asteroids)
            newNumAsteroids = len(asteroids)
            score += 100 * (numAsteroids - newNumAsteroids)

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
                    score += frame

        # if there is a collision
        if collided == True:
            respawnFrame = frame
            dyingPoint = spaceship.getPosition()
            spaceship.undraw()
            # we set body points to somewhere distant so we don't get extra collisions
            spaceship.setBodyPoints([[1000,1000],[1000,1000],[1000,1000]])
            expRad = 0

        # if explosion happens
        if expRad < 60:

            # vary the color of the explosion between 2 colors
            if expRad % 2 == 0:
                explosion = pho.Ball(win,dyingPoint[0],dyingPoint[1],expRad/10)
                explosion.setColor("dark red")
                explosion.draw()
                explosions.append(explosion)
            else:
                explosion = pho.Ball(win,dyingPoint[0],dyingPoint[1],expRad/10)
                explosion.setColor("orange")
                explosion.draw()
                explosions.append(explosion)
            # increase the radius
            expRad += 1

            if expRad == 60: # when we reach full size, delete the explosions
                for explosion in explosions:
                    explosion.undraw()

        if frame == respawnFrame + 90: # 90 frames after death:

            asteroids, livesLeft = respawn(win,livesLeft,asteroids,spaceship)

            if len(livesLeft) == 0: # if the player is out of lives

                key = win.checkKey()

                # Undraw all the elements
                spaceship.undraw()
                livesText.undraw()
                boostBar.undraw()
                boostBarOutline.undraw()
                boostText.undraw()

                # Print ending texts
                endingText = gr.Text(gr.Point(350,290),"Game over...")
                endingText.setSize(30)
                endingText.setTextColor("white")
                endingText.draw(win)

                finalScore = gr.Text(gr.Point(350,330),"Your score: " + str(score//10))
                finalScore.setSize(18)
                finalScore.setTextColor("white")
                finalScore.draw(win)

                instructions1 = gr.Text(gr.Point(350,360),"Press p to play again")
                instructions1.setSize(18)
                instructions1.setTextColor("white")
                instructions1.draw(win)

                instructions2 = gr.Text(gr.Point(350,390),"Press q to quit")
                instructions2.setSize(18)
                instructions2.setTextColor("white")
                instructions2.draw(win)

                # Check for response
                while key != "p":

                    key = win.checkKey()

                    if key == "q":
                        break

                if key == "p": # draw everything back, set everything back

                    # draw the necessary items
                    spaceship.draw()
                    livesText.draw(win)
                    boostBar.draw()
                    boostBarOutline.draw()
                    boostText.draw(win)

                    # undraw ending texts
                    endingText.undraw()
                    instructions1.undraw()
                    instructions2.undraw()
                    finalScore.undraw()

                    # set the variables
                    boostRemaining = 100
                    boostBar.setWidth(10)
                    boostBar.update()
                    livesLeft = lifeCreator(3,win) # giving player 3 lives
                    respawnFrame = -1000 # setting it to something small
                    frame = 0 # resetting the frame
                    score = 0 # resetting the score
                    continue

                if key == "q": # quit the game
                    break

            # set the respawn frame to something very small
            respawnFrame = -1000

            # reset the frame count
            frame = 0

            # reset the remaining boost and the boostbar
            boostRemaining = 100
            boostBar.setWidth((boostRemaining/100)*10)
            boostBar.update()

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
