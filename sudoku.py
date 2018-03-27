
from copy import deepcopy

""" A representation of a single field in sudoku board """
class Field:
    """ Create a field with coordinates of row and column, with square assignment
    ( sudoku borad is divided into 9 squares )
    @param row: row number
    @param column: column number
    @param value: field's value"""
    def __init__(self, row, column, value=0):
        self.row = row
        self.column = column
        self.square = self.set_square(self.row, self.column)
        self.value = value
        self.possible_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        if self.row not in self.possible_values:
            raise ValueError("Invalid row number {0}".format(self.row))
        if self.column not in self.possible_values:
            raise ValueError("Invalid column number {0}".format(self.column))
        if self.value != 0 and self.value not in self.possible_values:
            raise ValueError("field in row {0}, column {1} has invalid value".format(self.row, self.column))

    """ Assign square number to a field based on which row and column the field belongs to """
    @staticmethod
    def set_square(row, column):
        if column <= 3:
            square = 1
        elif 3 < column <= 6:
            square = 2
        else:
            square = 3

        if 3 < row <= 6:
            square += 3
        elif 6 < row <= 9:
            square += 6
        return square

    """ Remove values form the list of possible values the field can have, based on values that have already been
        assigned to other fields in the same row, column or square 
        @param taken: list of values already taken in the group this field belongs to """
    def update_possible_values(self, taken):
        for value in taken:
            try:
                self.possible_values.remove(value)
            except ValueError:
                pass

    """ Set a specific value to the field and delete the list of possible values """
    def set_value(self, value):
        print("Setting value {0} for field {1}, {2}".format(value, self.row, self.column))
        print("Possible values were {0}".format(self.possible_values))
        self.value = value
        self.possible_values = []
        input("")

    """ A representation of group of fields on the board, either a row, a column or a square. """


class FieldGroup:

    """ Create a group of fields with a list of fields assigned to it """
    def __init__(self):
        self.fields = []
        self.taken_values = []
        self.solved = False

    """ Update value of every field in this group. Either set a value if there's only
        one possible value, or update list of possible values for that field
        return """
    def resolve_values(self):
        value_changed = False
        self.solved = True
        for field in self.fields:
            if field.value == 0:
                self.solved = False
                if len(field.possible_values) == 1:
                    field.value = field.possible_values.pop()
                    value_changed = True
                else:
                    field.update_possible_values(self.taken_values)
            elif field.value not in self.taken_values:
                self.taken_values.append(field.value)
        if len(self.taken_values) == 9:
            self.solved = True
        return value_changed

    def set_field_value(self, field, value):
        if value not in self.taken_values:
            self.taken_values.append(field.value)
            field.set_value(value)
        else:
            field.update_possible_values(self.taken_values)



""" A sudoku board, consisting of fields in 9 rows and 9 columns, additionaly divided into nine 3 by 3 squares"""


class Board:
    """ Create a board, assigning fields to corresponding rows, columns and squares. Set values to fields according to
    given tuples
    @param value_tuples: A list of tuples. Each tuple consists of a row number, column number and value."""
    def __init__(self, value_tuples):
        self.rows = self.init_list_of_lists(9)
        self.columns = self.init_list_of_lists(9)
        self.squares = self.init_list_of_lists(9)
        self.solved = False

        for row in range(9):
            for column in range(9):
                field = Field((row + 1), (column + 1), 0)
                self.rows[row].fields.append(field)
                self.columns[column].fields.append(field)
                self.squares[(field.square - 1)].fields.append(field)
        for field_params in value_tuples:
            row = field_params[0]
            column = field_params[1]
            value = field_params[2]
            self.set_value(row, column, value)

    """ Create a list of custom objects.
    @param size: size of a new list"""
    @staticmethod
    def init_list_of_lists(size):
        list_of_lists = list()
        for index in range(size):
            list_of_lists.append(FieldGroup())
        return list_of_lists

    """Attempt to solve the board - update the values in each row, column and square accoring to the rules
    @return changed: return True if any field on the board was changed"""
    def solve(self):
        changed = False
        self.solved = True #Temporarily set boards' solved flag to true. Change back to false if any row isn't solved
        for row_of_fields in self.rows:
            if not row_of_fields.solved:
                changed = row_of_fields.resolve_values()
                #self.print_board()
                self.solved = False
        for column_of_fields in self.columns:
            if not column_of_fields.solved:
                changed = column_of_fields.resolve_values()
                #self.print_board()
        for square_of_fields in self.squares:
            if not square_of_fields.solved:
                changed = square_of_fields.resolve_values()
                #self.print_board()
        #print("STEP NUMBER {0}".format(step))
        self.print_board()
        return changed

    """Print current state fo the board to screen"""
    def print_board(self):
        for row_of_fields in self.rows:
            row_printout = ""
            for fld in row_of_fields.fields:
                if fld.value > 0:
                    val = str(fld.value)
                else:
                    val = " "
                row_printout = row_printout + " | " + val
                #print(row_of_fields.fields)
            print(row_printout)
        print("=====================================")

    """Set value of a field in given row and column"""
    def set_value(self, row, column, value):
        for field in self.rows[row - 1].fields:
            if field.row == row and field.column == column:
                field.set_value(value)
                #for other_field in self.rows[field.row - 1]:
                    #other_field


class TreeNode:

    def __init__(self, board, parent):
        self.board = board
        self.parentNode = parent
        self.children = []

        value_changed = True
        while value_changed:
            value_changed = self.board.solve()

        if not self.board.solved:
            for row in self.board.rows:
                for field in row.fields:
                   if  field.value == 0:
                       for value in field.possible_values:
                           new_board = deepcopy(self.board)
                           new_board.set_value(field.row, field.column, value)
                           self.create_child(new_board)
                           #new_board.print_board()
        else:
            self.board.print_board()


    def create_child(self, board):
        self.children.append(TreeNode(board, self))

    def tree_solve(self):
        solved = False
        while not solved:
            if not self.board.solve():
                self.create_child(self.board)


def main():
    board = Board([(1, 1, 5), (1, 2, 3), (1, 5, 7),
                   (2, 1, 6), (2, 4, 1), (2, 5, 9), (2, 6, 5),
                   (3, 2, 9), (3, 3, 8), (3, 8, 6),
                   (4, 1, 8), (4, 5, 6), (4, 9, 3),
                   (5, 1, 4), (5, 4, 8), (5, 6, 3), (5, 9, 1),
                   (6, 1, 7), (6, 5, 2), (6, 9, 6),
                   (7, 2, 6), (7, 7, 2), (7, 8, 8),
                   (8, 4, 4), (8, 5, 1), (8, 6, 9), (8, 9, 5),
                   (9, 5, 8), (9, 7, 1), (9, 9, 9)
                   ])

    board.print_board()
    root = TreeNode(board, None)

if __name__ == "__main__":
    main()




