import numpy as np
from manim import *

# Number of rows and columns in the grid
ROWS = 9       # Must be an odd number
COLS = 9       # Must be an odd number
XSPACE = 1.0
YSPACE = 1.0
RECT_WIDTH = 1.10
RECT_HEIGHT = RECT_WIDTH/1.5
CIRCLE_RADIUS = 0.3*RECT_HEIGHT
PATH_WIDTH = 3
TIP_LENGTH = 0.2

# Class of the grid points
class GridPoint:
    def __init__(self, x, y):
        self.x = x                          # x position in the grid
        self.y = y                          # y position in the grid
        self.state = 0                      # 0-empty, 1-block, 2-summing point, 3-line
        self.object = NullElement(x, y)     # Object contained by this point of the grid

# Invisible elements that are used as default in an empty grid point
class NullElement:
    def __init__(self, x, y):
        self.body = Circle(radius = 0).shift(x*XSPACE*RIGHT + y*YSPACE*UP)

# Rectangular blocks of the block diagram
class Block:
    def __init__(self):
        self.body = VMobject()          # VMobj of the rectangle of this block
        self.innertext = Tex(r'')       # VMobj of the text inside this block
        self.uppertext = Tex(r'')       # VMobj of the text above this block
        self.belowtext = Tex(r'')       # VMobj of the text below this block

# Circular summing points of the block diagram
class SummingPoint:
    def __init__(self):
        self.body = VMobject()          # VMobj of the circle of this summing point
        self.downsymbol = Tex(r'')      # VMobj of the down symbol of this summing point
        self.upsymbol = Tex(r'')        # VMobj of the up symbol of this summing point
        self.leftsymbol = Tex(r'')      # VMobj of the left symbol of this summing point
        self.rightsymbol = Tex(r'')     # VMobj of the right symbol of this summing point

# Element used to connect two other elements of the block diagram
class Path:
    def __init__(self):
        self.body = VMobject()          # VMobj of the line of this line
        self.uppertext = Tex(r'')       # VMobj of the upper text of this line
        self.belowtext = Tex(r'')       # VMobj of the below text of this line

# Class of the block diagram itself
class BlockDiagram:
    def __init__(self):
        self.grid = []
        for i in range(ROWS):
            for j in range(COLS):
                self.grid.append(GridPoint(-(ROWS-1)/2+i, -(COLS-1)/2+j))

    # Get grid point
    def _getGridPoint(self, x, y):
        match = None
        for point in self.grid:
            if ((point.x == x) and (point.y == y)):
                match = point
                break
        return match

    # Get VMobject in a certain point of the grid
    def get(self, x, y):
        point = self._getGridPoint(x, y)
        if (point.state == 0): # Null element (circle of radius 0)
            return point.object.body
        if (point.state == 1): # Block
            return VGroup(point.object.body, point.object.innertext, point.object.uppertext, point.object.belowtext)
        if (point.state == 2): # Summing point
            return VGroup(point.object.body, point.object.upsymbol, point.object.downsymbol, point.object.leftsymbol, point.object.rightsymbol)
        if (point.state == 3): # Path
            return VGroup(point.object.body, point.object.uppertext, point.object.belowtext)
        else:
            return None

    def getNROWS(self):
        return ROWS

    def getNCOLS(self):
        return COLS

    # Insert rectangular block in a certain point of the grid
    def InsertBlock(self, x, y, **kwargs):
        if ((x % 2 != 0) or (y % 2 != 0)): # Blocks can only be placed in even points of the grid
            return -2
        point = self._getGridPoint(x, y)
        if (point.state != 0):
            return -1 # This point is already occupied
        point.state = 1
        # Create the VMobject
        block = Block()
        block.body = Rectangle(color = WHITE, height = RECT_HEIGHT, width = RECT_WIDTH).shift(XSPACE*x*RIGHT + YSPACE*y*UP)
        block.innertext = kwargs.get('innertext', Tex(r'')).move_to(block.body.get_center())
        block.uppertext = kwargs.get('uppertext', Tex(r'')).next_to(block.body, UP, buff = 0.3)
        block.belowtext = kwargs.get('belowtext', Tex(r'')).next_to(block.body, DOWN, buff = 0.3)
        point.object = block
        return 0

    def InsertSummingPoint(self, x, y, **kwargs):
        if ((x % 2 != 0) or (y % 2 != 0)): # Summing points can only be placed in even points of the grid
            return -2
        point = self._getGridPoint(x, y)
        if (point.state != 0):
            return -1 # This point is already occupied
        point.state = 2
        # Create the VMobject
        summing = SummingPoint()
        summing.body = Circle(color = WHITE, radius = CIRCLE_RADIUS).shift(XSPACE*x*RIGHT + YSPACE*y*UP)
        summing.upsymbol = Tex(r'')
        summing.downsymbol = kwargs.get('downsymbol', Tex(r'')).shift(XSPACE*x*RIGHT + YSPACE*y*UP).shift(1.5*CIRCLE_RADIUS*LEFT+0.2*DOWN)
        summing.leftsymbol = kwargs.get('leftsymbol', Tex(r'')).shift(XSPACE*x*RIGHT + YSPACE*y*UP).shift(1.5*CIRCLE_RADIUS*LEFT+0.2*UP)
        summing.rightsymbol = Tex(r'')
        point.object = summing
        return 0

    def InsertPath(self, x, y, arrow = 0, **kwargs):
        if (((x % 2 == 0) and (y % 2 == 0)) or ((x % 2 == 1) and (y % 2 == 1))):
            return -1
        elif (x % 2 == 1):
            x1 = x-1
            x2 = x+1
            y1 = y
            y2 = y
            d1 = RIGHT 
            d2 = LEFT
        else:
            x1 = x
            x2 = x
            y1 = y-1
            y2 = y+1
            d1 = UP
            d2 = DOWN
        element1 = self._getGridPoint(x1, y1)
        element2 = self._getGridPoint(x2, y2)
        point = self._getGridPoint(x, y)
        path = Path()
        if arrow == 0:
            path.body = Line(start = element1.object.body.get_corner(d1), end = element2.object.body.get_corner(d2), stroke_width = PATH_WIDTH, buff = 0)
        if arrow == +1:
            path.body = Arrow(start = element1.object.body.get_corner(d1), end = element2.object.body.get_corner(d2), stroke_width = PATH_WIDTH, tip_length = TIP_LENGTH, buff = 0)
        if arrow == -1:
            path.body = Arrow(start = element2.object.body.get_corner(d2), end = element1.object.body.get_corner(d1), stroke_width = PATH_WIDTH, tip_length = TIP_LENGTH, buff = 0)
        point.object = path
        path.uppertext = kwargs.get('uppertext', Tex(r'')).move_to(path.body.get_center()).shift(0.2*UP)
        point.state = 3