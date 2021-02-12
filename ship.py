# Template by Bruce A Maxwell
# Fall 2018
# CS 152 Project 11
#
# Make an Asteroids-like ship move around
#
# slightly modified by Eric Aaron, Fall 2018
#
# import useful packages
import math
import time
import graphics as gr
import physics_objects as pho

# make a ship object, treat it as a ball
# but it needs to be able to rotate
# should probably have a parent rotator class that does most of this for you
class Ship(pho.Thing):
    def __init__(self, win, x0=0, y0=0, mass=1, radius=3):
        pho.Thing.__init__(self, win, "ball")
        # could use pho.Thing.__init__(self, win, "ball", mass=mass, radius=radius) instead, if Thing.__init__ has those defaults
        self.setMass(mass)
        self.setRadius(radius)
        self.setPosition([x0, y0])

        # anchor point is by default the center of the ship/circle so we don't need it
        self.angle = 0.
        self.dangle = 0.

        # visualization properties
        # This is a two-part visualization
        # the ship is a triangle
        self.bodypts = [ (radius, 0),
                         (- radius*0.5,   1.732*radius*0.5),
                         (- radius*0.5, - 1.732*radius*0.5) ]
        # the exhaust is another triangle
        self.flamepts = [ (- radius*0.5,   0.5*radius),
                          (- radius*0.5, - 0.5*radius),
                          (- radius*1.732, 0) ]

        self.corners = [[-1000,1000],[-1000,999],[-1000,998]]

        self.scale = 10.
        self.vis = []
        self.drawn = False

        # these are for handling the flicker of the exhaust
        self.flickertime = 6
        self.flicker = False
        self.countdown = 0

        # colors for flickers
        self.flickerColors = ["yellow","orange"]

    #########
    # these functions are identical to the rotating block
    # a smart coder would make a parent rotator class

    # draw the object into the window
    def draw(self):
        for item in self.vis:
            item.undraw()
        self.render()
        for item in self.vis:
            item.draw(self.win)
        self.drawn = True

    # undraw the object from the window
    def undraw(self):
        for item in self.vis:
            item.undraw()
        self.drawn = False

    # get and set the angle of the object
    # these are unique to rotators
    def getAngle(self):
        return self.angle

    # setAngle has to update the visualization
    def setAngle(self, a):
        self.angle = a
        if self.drawn:
            self.draw()

    # get and set rotational velocity
    def setRotVelocity(self, rv):
        self.dangle = rv # degrees per second

    def getRotVelocity(self):
        return self.dangle

    def getBodyPoints(self):
        return self.corners[:]

    def setBodyPoints(self,s):
        self.corners = s

    def getPosition(self):
        return self.pos[:]

    # incrementally rotate by da (in degrees)
    # has to update the visualization
    def rotate(self, da):
        self.angle += da
        if self.drawn:
            self.draw()

    # special ship methods
    def setFlickerOn(self, countdown = 20):
        self.flicker = True
        self.countdown = countdown

    def setFlickerOff(self):
        self.countdown = 0
        self.flicker = False

    # simplified render function since the ship always rotates around its center
    def render(self):

        # get the cos and sin of the current orientation
        theta = math.pi * self.angle / 180.
        cth = math.cos(theta)
        sth = math.sin(theta)

        # rotate each point around the object's center
        pts = []
        cornerpts = []
        for vertex in self.bodypts + self.flamepts:
            # move the object's center to 0, 0, which it is already in model coordinates
            xt = vertex[0]
            yt = vertex[1]

            # rotate the vertex by theta around the Z axis
            xtt = cth*xt - sth*yt
            ytt = sth*xt + cth*yt

            # move the object's center back to its original location
            xf = xtt + self.pos[0]
            yf = ytt + self.pos[1]

            # create a point with the screen space coordinates
            pts.append( gr.Point(self.scale * xf, self.win.getHeight() - self.scale * yf) )
            cornerpts.append([xf,yf])

        # make the two objects

        self.corners = cornerpts[:3]
        self.vis = [ gr.Polygon( pts[:3] ), gr.Polygon( pts[3:] ) ]
        self.vis[0].setFill("silver")
        self.vis[0].setOutline("dark red")
        self.vis[1].setOutline(self.flickerColors[0])

    def setFlickerColor(self,colors): # sets the flicker colors to colors
        self.flickerColors = colors

    def lifeModifier(self): # undraws the flames for life graphics
        try:
            self.vis[1].undraw()
        except IndexError:
            return

    # update the various state variables
    # add a unique flicker touch
    def update(self, dt):

        # update the angle based on rotational velocity
        da = self.dangle * dt
        if da != 0.0: # don't bother updating if we don't have to
            self.rotate( da )
        else: # but re-draw the ship anyway
            if self.drawn:
                self.draw()

        # flicker the flames
        # this should be a field of the object
        if self.flicker and self.countdown > 0:
            if self.countdown % self.flickertime < self.flickertime/2:
                self.vis[1].setFill(self.flickerColors[0])
            else:
                self.vis[1].setFill(self.flickerColors[1])
            self.countdown -= 1
        else:
            self.vis[1].undraw()


        # call the parent update for the rest of it
        pho.Thing.update(self, dt)

def main():
    # make a window
    win = gr.GraphWin('Ship', 500, 500, False)

    # make ship, draw it, wait for a mouse click
    ship = Ship(win, 25, 25)
    ship.draw()

    gamma = 10 # incrementation of rotational velocity
    delta = 1 # incrementation of acceleration

    winWidth = 50 # width of the window (scale is 10 so its 500/10)
    winHeight = 50 #  height of the window (scale is 10 so its 500/10)

    dt = 0.01
    frame = 0

    key = ""
    while key != "q":
        key = win.checkKey()

        ship.update(dt)

        if key == "Left":
            ship.setRotVelocity(ship.getRotVelocity()+gamma)
            ship.setFlickerOn()
        elif key == "Right":
            ship.setRotVelocity(ship.getRotVelocity()-gamma)
            ship.setFlickerOn()
        elif key == "space":
            a = ship.getAngle()
            theta = a * math.pi / 180
            v = ship.getVelocity()

            v_new_x = v[0] + math.cos(theta) * delta
            v_new_y = v[1] + math.sin(theta) * delta

            ship.setVelocity([v_new_x,v_new_y])
            ship.setFlickerOn()

        moveit = False
        p = ship.getPosition()

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
            ship.setPosition(p)
            moveit = False

        frame += 1

        if frame % 10 == 0:
            win.update()
            time.sleep(dt*0.5)

    # all done
    win.close()

if __name__ == "__main__":
    main()
