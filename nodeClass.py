class Node(object):
    __slots__ = ['parent', 'depth', 'move', 'heuristic']

    def __str__(self):
        return 'depth: %d move: %d heuristic: %d' % (self.depth, self.move, self.heuristic)

    """Main class
    
    Main class of this game.
    """




