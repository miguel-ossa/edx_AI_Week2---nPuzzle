#!/usr/bin/python

import sys
import puzzle
import Grid
import time

def main(script, *args):
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print "Error in arguments!"
        sys.exit()

    grid = Grid.Grid(3)
    game = puzzle.Puzzle(3, sys.argv[1], grid)
    start_position = convert_arguments(sys.argv[2])
    game.solve_it(start_position)
    grid.printEmptyGrid()
    game.build_results()

    time.sleep(10)
    grid.quit()

def convert_arguments(arg):
    start = []
    i = 0
    for c in str(arg.split()).replace("'", ""):
        if (i % 2) != 0:
            start.append(ord(c) - 48)
        i += 1
    return start


main(*sys.argv)
