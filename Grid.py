#!/usr/bin/python
from graphics import *


class Grid:
    def __init__(self, nsize):

        self.__nsize = nsize
        self.__tsize = pow(self.__nsize, 2)
        self.__screen_size = self.__nsize * 100
        self.__square_size = self.__screen_size / self.__nsize
        self.__nmovements = 0
        self.__movements = {
            -1: "Left",
             1: "Right",
            -3: "Up",
             3: "Down"
        }
        self.__my_state = None

    def printEmptyGrid(self):
        self.__win = GraphWin("nPuzzle", self.__screen_size, self.__screen_size)
        self.__win.setBackground("black")
        for y in range(self.__nsize):
            for x in range(self.__nsize):
                rect = Rectangle(Point(self.__square_size * x, self.__square_size * y),
                                 Point(self.__square_size * (x + 1), self.__square_size * (y + 1)))
                rect.setOutline("white")
                rect.draw(self.__win)
        return

    def printGrid(self, state):
        if self.__my_state is not None:
            i = 0
            for y in range(self.__nsize):
                for x in range(self.__nsize):
                    message = Text(Point(self.__square_size * x + self.__square_size / 2,
                                          self.__square_size * y + self.__square_size / 2), str(self.__my_state[i]))
                    message.setSize(35)
                    message.setTextColor("black")
                    message.draw(self.__win)
                    i = i + 1
        i = 0
        for y in range(self.__nsize):
            for x in range(self.__nsize):
                message = Text(Point(self.__square_size * x + self.__square_size / 2,
                                     self.__square_size * y + self.__square_size / 2), str(state[i]))
                message.setSize(35)
                if state[i] == 0:
                    message.setTextColor("green")
                else:
                    message.setTextColor("gray")
                message.draw(self.__win)
                i = i + 1
        self.__my_state = list(state)

        time.sleep(0.3)
        return

    @staticmethod
    def newState(state, move):
        if state is not None:
            pos_0 = list(state).index(0)
            pos_mv = pos_0 + move
            state[pos_0] = state[pos_mv]
            state[pos_mv] = 0

        return state

    def printMove(self, move):
        if move != 0:
            print self.__movements[move]
            self.__nmovements = self.__nmovements + 1
            print (self.__nmovements)
        return

    def getMove(self, move):
        return self.__movements[move]

    def quit(self):
        self.__win.close()
        return
