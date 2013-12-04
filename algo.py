import search
import random
import tetris
import copy
import platform

# fix for windows
if platform.system() == "Windows":
    from colorama import init
    init()

"""
What you need to know:
    - Board is represented by a two dimensional matrix, `grid`
    - A state is represented by a dict with keys "board" and "pieces", 
      where "pieces" is the remaining pieces (thus piece[0] is the next piece)
    - print_grid for a beautiful ASCII representation of your configuration
"""

GRID_HEIGHT = 20
GRID_WIDTH = 10

def print_grid(grid, block=None):
    """
    Print ASCII version of our tetris for debugging
    """
    for y in xrange(GRID_HEIGHT):
        for x in xrange(GRID_WIDTH):
            block = grid[y][x]
            if block:
                print block,
            else:
                print ".",
        print  # Newline at the end of a row

def merge_grid_block(grid, block):
    """
    Given a grid and a block, add the block to the grid.
    This is called to "merge" a block into a grid. You can
    think of the grid as the static part of pieces that have already
    been placed down. `block` is the current piece that you're looking to 
    place down.

    See settle_block() from tetris.py. Same thing, except without game logic

    Returns:
        Nothing, modifies grid via side-effects
    """
    for square in block.squares:
        y, x = square.y / tetris.FULL_WIDTH, square.x / tetris.FULL_WIDTH
        if grid[y][x]:
            raise Exception("Tried to put a Tetris block where another piece already exists")
        else:
            grid[y][x]=square
    return

def get_height(grid):
    """
    Given a grid, calculates the maximum height of any column
    Returns:
        int representing the maximum height of any column
    """
    heights = []
    for index in range(GRID_WIDTH):
        temp = [i for i, x in enumerate([col[index] for col in grid][::-1]) if x != None]
        heights.append(0 if len(temp) == 0 else max(temp)+1) # 0-indexed lol
    return max(heights)

def get_num_holes(g):
    """
    Given a grid, calculates the number of ''holes'' in the placed pieces
    Returns:
        int - number of holes
    """
    grid = copy.deepcopy(g)
    holes = []
    # first for loop finds initial underhangs
    for i in range(len(grid)-1, 0, -1): # row
        for j in range(len(grid[i])): # col
            if i-1 >= 0 and grid[i][j] is None and grid[i-1][j] is not None:
                holes.append((i, j))
    # for each find earlier keep digging down to see how many holes additionally there are
    for i, j in holes:
        while i+1 < len(grid) and grid[i+1][j] is None:
            holes.append((i+1, j))
            i += 1
    return len(holes)


""" gets best successor based on state score """
def getBestSuccessor(problem, state):
    successors = problem.getSuccessors(state)
    cur_max = float("-inf")
    cur_best = None
    if len(successors) == 0:
        print "Error"
        return None
    for s in successors:
        temp = evaluateState(s['board'])
        if temp > cur_max:
            cur_best = s
            cur_max = temp
    return cur_best

""" evaluates state based on some evaluation function """
def evaluateState(grid):
    return -(10*get_num_holes(grid) + get_height(grid))

class TetrisSearchProblem(search.SearchProblem):
    def __init__(self):
        # Generate random sequence of pieces for offline tetris
        NUM_PIECES = 50
        self.all_pieces = [random.choice(tetris.SHAPES) for i in xrange(NUM_PIECES)]

        # Taken from tetris.py: initial board setup
        self.initial_board = []  
        for i in range(GRID_HEIGHT):
            self.initial_board.append([])
            for j in range(GRID_WIDTH):
                self.initial_board[i].append(None)   


    def getStartState(self):
        return { "pieces": self.all_pieces, "board": self.initial_board }

    def isGoalState(self, state):
        # TODO: Define this -- depends on what approach we want to take
        # Is it just if the state is ready to tetris and the next piece is a line piece?
        return len(state["pieces"]) == 45

    def _generateRotations(self, piece, grid):
        """
        Args:
            piece: Block() object
        Returns:
            List of Block objects for the possible rotations
        """
        rotated_pieces = []
        TOTAL_ROTATIONS = 4  # 0, 90, 180, 270
        for num_cw_rotations in xrange(TOTAL_ROTATIONS): 
            # Make a copy of the piece so we can manipulate it
            new_piece = copy.deepcopy(piece)

            # Short circuit logic for rotating the correct number of times CW
            # This might be buggy...not really sure what his can_CW function checks for
            did_rotate = True
            for _ in xrange(num_cw_rotations):
                if new_piece.can_CW(grid):
                    new_piece.rotate_CW(grid)
                else:
                    did_rotate = False

            # By default, tetris.py instantiates pieces in the middle.
            # Move it all the way to the left. move_left() side-effects.
            while new_piece.move_left(grid): pass

            if not did_rotate:
                continue
            else:
                rotated_pieces.append(new_piece)

        return rotated_pieces

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

        new_piece = tetris.Block(new_piece_type)

        # Because we're leveraging tetris.py, we have a lot of 
        # side-effecting code going on -- have to be careful


        possible_rotations = self._generateRotations(new_piece, grid)

        # Starting from the left-hand side this moves the 
        # piece to the right one column (i.e. every horizontal position).
        # Then we move the piece all the way down.
        # In this way, we enumerate all possible subsequent configurations.
        for rotated_piece in possible_rotations:
            can_move_right = True
            while can_move_right:
                # Copying the grids here might explode memory, but I think keeping
                # a reference to the same grid repeatedly is going to be really dangerous
                piece_copy = copy.deepcopy(rotated_piece)
                grid_copy = copy.deepcopy(grid)

                # Move the piece all the way down
                while piece_copy.move_down(grid_copy): pass

                # Add the block to the grid
                merge_grid_block(grid_copy, piece_copy)

                # Register the piece into the grid
                successors.append({
                    "board": grid_copy,
                    "pieces": state["pieces"][1:] 
                })

                # Try the next configuration
                can_move_right = rotated_piece.move_right(grid)  # has side-effects

        return successors

    def getCostOfActions(self, actions):
        pass

def main():
    example()

def example():
    """
    Saagar, Brandon: call this function and you'll get a concrete idea of how
    the next configurations are being generated
    """
    search_problem = TetrisSearchProblem()

    start = search_problem.getStartState()
    succ = search_problem.getSuccessors(start)
    for s in succ:
        print_grid(s["board"])
        print

    print "Now, let's look at the successors for just one of these states"
    more_succ = search_problem.getSuccessors(succ[0])
    for s in more_succ:
        print_grid(s["board"])
        print

    print "*******************brandon and saagar's testing*******************"
    print "next piece:"
    print more_succ[0]['pieces'][0]
    print_grid(more_succ[0]["board"])
    print
    print_grid(getBestSuccessor(search_problem, more_succ[0])['board'])
    
if __name__ == '__main__':
    main()
