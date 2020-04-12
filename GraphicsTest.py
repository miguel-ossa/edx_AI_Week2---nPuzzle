#!/usr/bin/python

""""
Prueba de graficos con graphics.py, del libro:
Python Programming An Introduction to Computer Science

Migrar despues a Tkinter
https://docs.python.org/3/library/tkinter.html
"""

import sys
import time
from graphics import *


def main(script, *args):
    screen_size = 300
    square_size = screen_size / 3

    win = GraphWin("My square", screen_size, screen_size)
    for y in range(3):
        for x in range(3):
            rect = Rectangle(Point(square_size * x, square_size * y),
                             Point(square_size * (x + 1), square_size * (y + 1)))
            rect.draw(win)

    message = Text(Point(square_size / 2, square_size / 2), "0")
    message.setSize(35)
    message.draw(win)

    time.sleep(10)
    win.close()


main(*sys.argv)
