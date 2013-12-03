import search
import random
import tetris

class TetrisSearchProblem(SearchProblem):
    def __init__(self):
        # Generate random sequence of pieces for offline tetris
        NUM_PIECES = 50
        self.all_pieces = [random.choice(tetris.SHAPES) for i in xrange(NUM_PIECES)]

        # Taken from tetris.py: initial board setup
        self.initial_board = []  
        HEIGHT = 20
        WIDTH = 10
        for i in range(HEIGHT):
            self.initial_board.append([])
            for j in range(WIDTH):
                self.initial_board[i].append(None)   


    def getStartState(self):
        return { "pieces": self.all_pieces, "board": self.initial_board }

    def isGoalState(self, state):
        pass

    def getSuccessors(self, state):
        """
        Return a list of successor nodes
        using the board and current piece. 
        """
        if len(state["pieces"]) == 0:
            return None
        
        new_piece_type = state["pieces"][0]
        grid = state["board"]

        successors = []

        TOTAL_ROTATIONS = 4  # 0, 90, 180, 270
        for num_cw_rotations in xrange(TOTAL_ROTATIONS): 
            new_piece = tetris.Block(new_piece_type)

            # Short circuit logic for rotations
            # This is probably buggy because we can rotate CW _and_ CCW
            could_rotate = True
            for i in xrange(num_cw_rotations):
                if new_piece.can_CW(grid):
                    new_piece.rotate_CW(grid)
                else:
                    could_rotate = False

            if not could_rotate:
                continue

            # For each successive board configuration, create a successor state


    def getCostOfActions(self, actions):
        pass


def main():
    search_problem = TetrisSearchProblem()

if __name__ == '__main__':
    main()
