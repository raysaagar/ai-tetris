class GameNode(object):
    def __init__(self, board, currentPiece, nextPieces):
        self.board = board 
        self.currentPiece = currentPiece
        self.nextPieces = nextPieces


class TetrisSearchProblem(object):
    def getSuccessors(self, node):
        """
        Return a list of successor nodes
        using the board and current piece. 
        """
        pass


def main():
    """
    Start laying down the pieces
    """

    # TODO: Randomly generate a first piece, then continuously
    # generate successors until nextPieces = [] (no more pieces left
    # in our offline version of Tetris)
    first_piece = None
    pass

if __name__ == '__main__':
    main()
