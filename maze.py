"""Implemention of the Maze ADT using a 2-D array."""
from arrays import Array2D
from lliststack import Stack


class Maze:
    """Define constants to represent contents of the maze cells."""
    MAZE_WALL = "*"
    PATH_TOKEN = "x"
    TRIED_TOKEN = "o"
    POSSIBLE_MOVES = ((-1, 0), (0, 1), (1, 0), (0, -1))

    def __init__(self, num_rows, num_cols):
        """Creates a maze object with all cells marked as open."""
        self._maze_cells = Array2D(num_rows, num_cols)
        self._start_cell = None
        self._exit_cell = None

    def num_rows(self):
        """Returns the number of rows in the maze."""
        return self._maze_cells.num_rows()

    def num_cols(self):
        """Returns the number of columns in the maze."""
        return self._maze_cells.num_cols()

    def set_wall(self, row, col):
        """Fills the indicated cell with a "wall" marker."""
        assert 0 <= row < self.num_rows() \
               and 0 <= col < self.num_cols(), "Cell index out of range."
        self._maze_cells[row, col] = self.MAZE_WALL

    def set_start(self, row, col):
        """Sets the starting cell position."""
        assert 0 <= row < self.num_rows() \
               and 0 <= col < self.num_cols(), "Cell index out of range."
        self._start_cell = _CellPosition(row, col)

    def set_exit(self, row, col):
        """Sets the exit cell position."""
        assert 0 <= row < self.num_rows() \
               and 0 <= col < self.num_cols(), "Cell index out of range."
        self._exit_cell = _CellPosition(row, col)

    def find_path(self):
        """
        Attempts to solve the maze by finding a path from the starting cell
        to the exit. Returns True if a path is found and False otherwise.
        """
        stack = Stack()
        stack.push(self._start_cell)

        self._mark_path(self._start_cell.row, self._start_cell.col)

        while True:
            if stack.is_empty():
                return False

            last = stack.pop()
            self._mark_tried(last.row, last.col)


            for move in self.POSSIBLE_MOVES:
                cell = _CellPosition(last.row + move[0], last.col + move[1])

                if self._valid_move(cell.row, cell.col):
                    self._mark_path(last.row, last.col)
                    stack.push(last)

                    self._mark_path(cell.row, cell.col)
                    stack.push(cell)

                    if self._exit_found(cell.row, cell.col):
                        return True

                    break

    def reset(self):
        """Resets the maze by removing all "path" and "tried" tokens."""
        for i in range(self.num_rows()):
            for j in range(self.num_cols()):
                cell = self.MAZE_WALL if self._maze_cells[i, j] == self.MAZE_WALL else None
                self._maze_cells[i, j] = cell

    def __str__(self):
        """Returns a text-based representation of the maze."""
        result = ""

        for i in range(self.num_rows()):
            temp = ""
            for j in range(self.num_cols()):
                temp += (self._maze_cells[i, j] or "_") + ' '

            result += temp + '\n'

        return result.strip() + " "

    def _valid_move(self, row, col):
        """Returns True if the given cell position is a valid move."""
        return 0 <= row < self.num_rows() \
               and 0 <= col < self.num_cols() \
               and self._maze_cells[row, col] is None

    def _exit_found(self, row, col):
        """Helper method to determine if the exit was found."""
        return row == self._exit_cell.row and col == self._exit_cell.col

    def _mark_tried(self, row, col):
        """Drops a "tried" token at the given cell."""
        self._maze_cells[row, col] = self.TRIED_TOKEN

    def _mark_path(self, row, col):
        """Drops a "path" token at the given cell."""
        self._maze_cells[row, col] = self.PATH_TOKEN


class _CellPosition(object):
    """Private storage class for holding a cell position."""
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __str__(self) -> str:
        return f"row: {self.row}, col: {self.col}"
