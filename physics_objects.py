# Izge Bayyurt
# CS152 Fall 2018
# Project 10
# 11.16.18
#
# physics_object.py
# This file handles every graphical object we will use in the main code
import graphics as gr
import math

class Thing:
    """ Thing is the skeleton of each class we will create. We are initializing
        our variables and methods here and we will be inheriting this class
        when we create our child classes, not repeating code.
    """

    def __init__(self,win,the_type,x0=0,y0=0,radius = 1):
        self.type = the_type # setting the type (ball, floor, wall, or block)
        self.mass = 1 # mass of the object
        self.radius = radius # radius of the object (only used for balls)
        self.pos = [x0,y0] # position of the object
        self.velocity = [0,0] # velocity of the object
        self.acceleration = [0,0] # acceleration of the object
        self.force = [0,0] # force on the object
        self.elasticity = 1 # elasticity determines how the velocity after collisions will be
        self.scale = 10 # scale that we use to turn physics coordinates into graphic coordinates
        self.win = win # the graphics window
        self.vis = [] # objects that we create

    def undraw(self): # Erasing the items
        for item in self.vis:
            item.undraw()
        self.vis = []

    def setColor(self,color): # Changes the color of the object in self.vis
        for item in self.vis:
            item.setFill(color)
            item.setOutline(color)

    def setOutline(self,color):
        for item in self.vis:
            item.setOutline(color)

    def setFill(self,color):
        for item in self.vis:
            item.setFill(color)              

    def getMass(self): # Returns the mass of the object as a scalar value
        return self.mass

    def setMass(self, m): # m is the new mass of the object
        self.mass = m

    def getRadius(self): # Returns the radius of the object as a scalar value
        return self.radius

    def setRadius(self, m): # r is the new radius of the object
        self.radius = m

    def getPosition(self): # returns a 2-element tuple with the x, y position.
        return self.pos[:]

    def setPosition(self, p): # p is a 2-element list with the new x,y values
        self.pos[0] = p[0]
        self.pos[1] = p[1]

    def getVelocity(self): # returns a 2-element tuple with the x and y velocities.
        return self.velocity[:]

    def setVelocity(self, v): # v is a 2-element list with the new x and y velocities
        self.velocity = v

    def getAcceleration(self): # returns a 2-element tuple with the x and y acceleration values.
        return self.acceleration[:]

    def setAcceleration(self, a): # a is a 2-element list with the new x and y accelerations.
        self.acceleration = a

    def getForce(self): # returns a 2-element tuple with the current x and y force values.
        return self.force[:]

    def setForce(self, f): # f is a 2-element list with the new x and y force values.
        self.force = f

    def getElasticity(self): # returns elasticity of the object
        return self.elasticity

    def setElasticity(self, e): # sets the elasticity to a custom value
        self.elasticity = e

    def getType(self): # returns the type of the object
        return self.type

    def setType(self, t): # sets the type of the object to custom value
        self.type = t

    def draw(self): # draws the objects in self.vis in win
        for obj in self.vis:
            obj.draw(self.win)

    def update( self, dt, colliding=False ):
        """Computes the object's next state and updates the object
        visualization on the screen. If colliding is True, then
        acceleration will not be applied."""

        # Turn off acceleration during collisions to keep ball
        # from sinking through the floor:
        if colliding:
            a = [0,0]
        else:
            a = self.acceleration

        # How much the ball will move (in physics coordinates) during
        # this timestep, based on its current velocity and acceleration:
        dx = self.velocity[0] * dt + 0.5 * a[0] * dt**2
        dy = self.velocity[1] * dt + 0.5 * a[1] * dt**2

        # Ball's new position in physics coordinates:
        self.pos[0] += dx
        self.pos[1] += dy

        # Ball visualization's new position in graphics coordinates
        for shape in self.vis:
            shape.move(dx*self.scale, -dy*self.scale)

        # Update velocity:
        self.velocity[0] += a[0] * dt
        self.velocity[1] += a[1] * dt

        # An applied force produces a temporary acceleration:
        self.velocity[0] += dt * self.force[0] / self.mass
        self.velocity[1] += dt * self.force[1] / self.mass

        # Simulate damping by reducing x and y velocities:
        # self.velocity[0] *= 0.998
        # self.velocity[1] *= 0.998

class Ball(Thing):
    """ Ball class. Ball is a round object that has the ability to move (it has
    a setPosition method.) It has some radius that we can pass in through the
    parameters.
    """

    def __init__(self, win, x0=0, y0=0, radius = 1):
        # x0,y0 is the center of the ball
        Thing.__init__(self,win,"ball",x0,y0,radius=radius) # inherit the Thing class
        self.vis = [gr.Circle(gr.Point(self.pos[0]*self.scale,
        win.getHeight()-self.pos[1]*self.scale), self.radius * self.scale )]

    def setPosition(self, p): # p is a 2-element list with the new x,y values
        self.pos[0] = p[0]
        self.pos[1] = p[1]

        for obj in self.vis:
            c = obj.getCenter()
            dx = self.scale * p[0] - c.getX()
            dy = self.win.getHeight() - (self.scale * p[1]) - c.getY()
            obj.move(dx,dy)

class Floor(Thing):
    """ Floor class inherits Thing.
        It will make the bottom and upper part of the screen.
    """

    def __init__(self,win,x0,y0,width,height):
        Thing.__init__(self,win,"floor",x0,y0) # inherit the Thing class
        # x0, y0 is the right middle part of the rectangle
        self.width = width
        self.height = height
        self.vis = [gr.Rectangle(gr.Point(x0*self.scale, self.win.getHeight() - (y0 + height/2)*self.scale),
        gr.Point((x0 + width)*self.scale, self.win.getHeight() - (y0 - height/2)*self.scale))]

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

class Wall(Thing):
    """ Wall class inherits Thing.
        It will make left and right part of the screen.
    """

    def __init__(self,win,x0,y0,width,height):
        Thing.__init__(self,win,"wall",x0,y0) # inherit the Thing class
        # x0, y0 is the bottom middle part of the rectangle
        self.width = width
        self.height = height
        self.vis = [gr.Rectangle(gr.Point((x0 - width/2)*self.scale, self.win.getHeight() - y0*self.scale),
        gr.Point((x0 + width/2)*self.scale, self.win.getHeight() - self.scale*(y0 + height)))]

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

class Block(Thing):
    """ Block class inherits Thing.
        It will work as an obstacle in the screen, so we will handle collisions
        from all 4 sides.
    """

    def __init__(self,win,x0,y0,width,height):
        Thing.__init__(self,win,"block",x0,y0)
        # x0, y0 is the center of the block
        self.width = width
        self.height = height
        self.vis = [gr.Rectangle(gr.Point((x0 - width/2)*self.scale, win.getHeight()- (y0 - height/2)*self.scale),
        gr.Point((x0 + width/2)*self.scale, win.getHeight() - (y0 + height/2)*self.scale))]

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

class Bumper(Thing):
    """ Bumper is a circle like object which has more elasticity than normal,
        so it can "bump" the moving objects.
    """
    def __init__(self,win,x0,y0,radius):
        Thing.__init__(self,win,"ball",x0,y0)
        # x0, y0 is the center of the bumper
        self.radius = radius # passing the radius
        self.elasticity = 1.5 # we increase the elasticity since its a bumper
        self.vis = [gr.Circle(gr.Point(self.pos[0]*self.scale,
        win.getHeight()-self.pos[1]*self.scale), self.radius * self.scale )]

class RotatingBlock(Thing):
    """ This class creates a rotating block.
    """

    def __init__(self,win,x0,y0,width,height,Ax = None,Ay = None,the_type="rotating_block"):
        Thing.__init__(self,win,the_type,x0,y0)
        self.width = width
        self.height = height
        if Ax != None and Ay != None:
            self.anchor = [Ax,Ay] # The anchor point for the rotation
        else:
            self.anchor = [x0,y0] # The anchor point for the rotation
        # The order of these points matter when the shape is drawn
        self.points = [[-width/2, -height/2], [width/2, -height/2], [width/2, height/2], [-width/2, height/2]]
        self.angle = 0.0 # Angular orientation of the line
        self.rvel = 0.0 # Rotational velocity (in degrees/s)
        self.drawn = False # Boolean value, indicating if the object has been drawn
        self.corners = []

    def render(self):
        """ This function renders the Line object so it rotates around some axis
        """

        theta = self.angle*math.pi/180.0
        cth = math.cos(theta)
        sth = math.sin(theta)
        pts = []
        cornerpts = []

        for vertex in self.points:
            x = vertex[0] + self.pos[0] - self.anchor[0]
            y = vertex[1] + self.pos[1] - self.anchor[1]

            xt = x * cth - y * sth
            yt = x * sth + y * cth

            x = xt + self.anchor[0]
            y = yt + self.anchor[1]

            cornerpts.append([x,y])
            pts.append(gr.Point(self.scale * x, self.win.getHeight() - self.scale*y))

        self.corners = cornerpts
        self.vis = [gr.Polygon(pts)]

    def update(self,dt):
        """ Updates the object's state """

        da = self.rvel * dt # calculating how much the angle changes
        if da != 0:
            self.rotate(da)
        Thing.update(self,dt)


    def draw(self):
        """ Draws the items in self.vis to the screen """

        for item in self.vis:
            item.undraw()
        self.render()
        for item in self.vis:
            item.draw(self.win)
        self.drawn = True

    def getAngle(self):
        """ Returns the angle """
        return self.angle

    def setAngle(self,a):
        """ Sets the angle and if the object is drawn, redraws it """
        self.angle = a
        if self.drawn == True:
            self.draw()

    def getAnchor(self):
        """ Returns the anchor point """
        return self.anchor

    def setAnchor(self,a):
        """ Sets the anchor point """
        self.anchor = a

    def getRotVelocity(self):
        """ Returns rotational velocity """
        return self.rvel

    def setRotVelocity(self,r):
        """ Sets the rotational velocity """
        self.rvel = r

    def rotate(self,amount):
        """ Rotates the object for some given amount of angle """
        self.angle += amount
        if self.drawn == True:
            self.draw()

class Asteroid(RotatingBlock):

    def __init__(self,win,width,height,points,Ax = None,Ay = None,x0=0,y0=0,the_type="asteroid"):
        RotatingBlock.__init__(self,win,x0,y0,width,height,Ax,Ay)
        self.Ax = Ax
        self.Ay = Ay
        self.points = points

    def initiate(self):
        """ Initiates the asteroid by creating and drawing it"""
        pts = []
        for point in self.points:
            pt = gr.Point(point[0],point[1])
            pts.append(pt)

        self.vis = [gr.Polygon(pts)]

        self.draw()

    def getCorners(self):
        """ Returns corners of the asteroid """
        return self.corners

    def setPosition(self,p):
        self.pos = p
        self.anchor = [self.pos[0]+self.anchor[0],self.pos[1]+self.anchor[1]]

    def getAnchor(self):
        return self.anchor[:]

    def showAnchor(self):
        """ Optional method to visually see the anchor point """
        dot =  gr.Circle(gr.Point(self.anchor[0]*self.scale,
        self.win.getHeight()-self.anchor[1]*self.scale), self.radius * self.scale)
        dot.draw(self.win)

    def update(self,dt):
        """ Updates the object's state """

        da = self.rvel * dt # calculating how much the angle changes
        if da != 0:
            self.rotate(da)
        self.anchor = [self.pos[0]+self.Ax,self.pos[1]+self.Ay]
        Thing.update(self,dt)

class Bar(Block):

    def __init__(self,win,x0,y0,width,height):
        Block.__init__(self,win,x0,y0,width,height)
        self.vis = [gr.Rectangle(gr.Point(x0*self.scale, win.getHeight()- y0*self.scale),
        gr.Point((x0 + width)*self.scale, win.getHeight() - (y0 + height)*self.scale))]
        self.color = "blue"

    def setWidth(self,w):
        self.width = w

    def update(self):
        for item in self.vis:
            item.undraw()
        self.vis = [gr.Rectangle(gr.Point(self.pos[0]*self.scale, self.win.getHeight()- self.pos[1]*self.scale),
        gr.Point((self.pos[0] + self.width)*self.scale, self.win.getHeight() - (self.pos[1] + self.height)*self.scale))]
        for item in self.vis:
            item.setFill(self.color)
            item.setOutline(self.color)
        self.draw()
