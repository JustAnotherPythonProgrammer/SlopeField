import pygame
from pygame.locals import *
from numpy import linspace, arange, interp, sqrt
from sys import exit as sysExit
pygame.init()

# EXPLANATION OF NUMPY IMPORTS
# linspace generates evenly spaced numbers through a range
# arange generates numbers increasing by a step size through a range
# interp takes a number in one range and scales it to the same position in another
# sqrt is just square root    :P


# Window stuff
WIDTH  = 1000
HEIGHT = 1000


display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slope Field!    :P")


# Colors
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
GREEN = (  0, 255,   0)
GRAY  = (100, 100, 100)


# Differential equation
equation = lambda x, y: 2 * x


segmentLength = 0.2 # Length of each slope line


# Graph variables
xStep = 0.25
yStep = 0.25

xMin = -5
xMax =  5
xTotal = abs(xMin) + abs(xMax)


yMin = -5
yMax =  5
yTotal = abs(yMin) + abs(yMax)


xCenter = interp(0, [xMin, xMax], [0, WIDTH])
yCenter = interp(0, [xMin, xMax], [0, WIDTH])


# Scale factors for converting cartesian coordinates to screen ones
xScale = interp(1, [xMin, xMax], [0, WIDTH])  - interp(0, [xMin, xMax], [0, WIDTH])
yScale = interp(1, [yMin, yMax], [0, HEIGHT]) - interp(0, [yMin, yMax], [0, HEIGHT])




class LatticePoint:
    """
    Class that handles Lattice Points.  Has a position in the cartestian plane, and a corresponding position for the screen.
    Has a color to draw the slope line and a dot at the lattice point.
    Has a slope.
    """
    def __init__(self, x, y, color=GREEN):
        self.x = x
        self.y = y

        self.slope = equation(x, y)
        
        self.color = color

        self.screenx, self.screeny = cartesianToScreen(self.x, self.y)



    def __repr__(self):
        """
        Display the cartesian data for the Lattice Point (DEBUGGING AHHHH).
        """
        return f"({self.x}, {self.y}) m={self.slope}"


    def drawCenter(self):
        """
        Draws a small dot on the lattice point.
        """
        pygame.draw.circle(display, self.color, (self.screenx, self.screeny), 1, 0)


    def drawSlope(self):
        """
        Calculates the end points for the slope segment and then draws it.
        """
        length = sqrt(1 + self.slope**2) # Length of the line segment over 1 x-unit
        xOffset = (segmentLength / length) / 2 # Figures out how many times the length of the 1 unit length fits into the desired length
                                               # then divides by 2 becuase half is on the left and half on the right of the center


        # Left end point
        xLeft = self.x - xOffset
        yLeft = (self.slope * (xLeft - self.x)) + self.y

        # Right end point
        xRight = self.x + xOffset
        yRight = (self.slope * (xRight - self.x)) + self.y


        # Converts the left and right end points from cartesian coordinates to screen coordinates
        left  = cartesianToScreen(xLeft ,  yLeft)
        right = cartesianToScreen(xRight, yRight)


        pygame.draw.aaline(display, self.color, left, right, 1) # DRAWS THE LINE AHHHHHHHHHHHHHHHHHH      :P



def cartesianToScreen(x, y):
    """
    Converts cartesian coordinates to screen coordinates.
    """
    screenx = xCenter + (x * xScale)
    screeny = yCenter + (y * yScale)
    screeny = HEIGHT - screeny

    return screenx, screeny




def getLatticePoints():
    """
    Generates all the lattice points that would be visible on screen.
    """
    latticePoints = []

    for y in arange(yMin, yMax + yStep, yStep):
        for x in arange(xMin, xMax + xStep, xStep):
            latticePoints.append(LatticePoint(x, y))

    
    return latticePoints




def drawGraph():
    """
    Draws the vertical and horizontal graph lines.
    """
    for x in linspace(0,  WIDTH, xTotal, False)[1:]:
        pygame.draw.line(display, GRAY, (x, 0), (x, HEIGHT), 1)

    for y in linspace(0, HEIGHT, yTotal, False)[1:]:
        pygame.draw.line(display, GRAY, (0, y), (WIDTH, y), 1)




def drawOrigin():
    """
    If the origin is on screen, draw it.
    """
    if xMin < 0 < xMax:
        if yMin < 0 < yMax:
            x, y = cartesianToScreen(0, 0)

            pygame.draw.line(display, WHITE, (x - 6, y),
                                             (x + 6, y), 3)

            pygame.draw.line(display, WHITE, (x, y - 6),
                                             (x, y + 6), 3)




def main():

    latticePoints = getLatticePoints()

    while True:
        display.fill(BLACK)


        drawGraph()
        drawOrigin()


        for point in latticePoints:

            point.drawCenter()
            point.drawSlope()
        


        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sysExit(0)
        
        pygame.display.update()




if __name__ == "__main__":
    main()