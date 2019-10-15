# checkerboard.py
# Graphics utilities for drawing and manipulating checkerboards.
#
# This module was initially developed for the N-queens genetic algorithm.

from graphics import *

def add(win, x, rows=8, cols=8, size=45, margin=20):
    # Add queens (as circles) to the board.
    queens = []
    for row in range(len(x)):
        c = Circle(Point(margin+(x[row]+0.5)*size, margin+(row+0.5)*size), size//3)
        c.setOutline(colormap("queen"))
        c.setFill(colormap("queen"))
        c.draw(win)
        queens.append(c)
    
    return queens
    
def colormap(option):
    # Return the hexadecimal color for a GUI element.
    if option == "background":
        clr = "#FFFFFF"
    elif option == "lines":
        clr = "#000000"
    elif option == "1":
        clr = "#EEE4DA"
    elif option == "2":
        clr = "#BBADA0"
    elif option == "queen":
        clr = "#746E66"
    else:
        print("Cannot find color for option:", option)
    return clr

def draw(rows=8, cols=8, size=45, margin=20):
    # Initialize graphics window
    width = size * cols + 2 * margin
    height = size * rows + 2 * margin
    win = GraphWin(title="Checkerboard", width=width, height=height)
    win.setBackground(colormap("background"))
    
    # Add checkerboard
    rect = Rectangle(Point(margin, margin), Point(width - margin, height - margin))
    rect.setWidth(3)
    rect.setOutline(colormap("lines"))
    
    for row in range(rows):
        if row % 2 == 0:
            for col in range(0, cols, 2):
                p1 = Point(margin + col * size, margin + row * size)
                p2 = Point(margin + (col+1) * size, margin + (row+1) * size)
                r = Rectangle(p1, p2)
                r.setWidth(1)
                r.setOutline(colormap("1"))
                r.setFill(colormap("1"))
                r.draw(win)
        else:
            for col in range(1, cols, 2):
                p1 = Point(margin + col * size, margin + row * size)
                p2 = Point(margin + (col+1) * size, margin + (row+1) * size)
                r = Rectangle(p1, p2)
                r.setWidth(1)
                r.setOutline(colormap("1"))
                r.setFill(colormap("1"))
                r.draw(win)
    
    for row in range(rows):
        if row % 2 == 1:
            for col in range(0, cols, 2):
                p1 = Point(margin + col * size, margin + row * size)
                p2 = Point(margin + (col+1) * size, margin + (row+1) * size)
                r = Rectangle(p1, p2)
                r.setWidth(1)
                r.setOutline(colormap("2"))
                r.setFill(colormap("2"))
                r.draw(win)
        else:
            for col in range(1, cols, 2):
                p1 = Point(margin + col * size, margin + row * size)
                p2 = Point(margin + (col+1) * size, margin + (row+1) * size)
                r = Rectangle(p1, p2)
                r.setWidth(1)
                r.setOutline(colormap("2"))
                r.setFill(colormap("2"))
                r.draw(win)
    
    rect.draw(win)
    
    return win

def get(params, key):
    # Get a parameter value from the input dictionary; use defaults if key does not exist.
    try:
        return params[key]
    except:
        if key == 'rows':  # number of rows in the checkerboard
            return 8
        elif key == 'cols':  # number of columns in the checkerboard
            return 8
        elif key == 'size':  # size of each checkerboard square
            return 45
        elif key == 'margin':  # margin between figure boundary and checkerboard (in pixels)
            return 20
        else:
            raise KeyError('There is no default value for the key: ' + key)

def move(win, queens, x, rows=8, cols=8, size=45, margin=20):
    # Move queens to new locations (x) on the board.    
    for i in range(len(queens)):
        x0 = queens[i].getCenter().getX()
        col0 = (x0 - margin) / size - 0.5
        dx = (x[i] - col0) * size
        queens[i].move(dx, 0)

def remove(queens):
    # Undraw queens from board
    for queen in queens:
        queen.undraw()
        
