class Field:

    def __init__(self, row, column, value=0):
        self.row = row
        self.column = column
        self.square = self.set_square(self.row, self.column)
        self.value = value
        self.possible_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    @staticmethod
    def set_square(row, column):
        if row <= 3:
            square = 1
        elif 3 < row <= 6:
            square = 2
        else:
            square = 3

        if 3 < column <= 6:
            square += 1
        elif 6 < column <= 9:
            square += 2
        return square

    def update_possible_values(self, taken=[]):
        for value in taken:
            self.possible_values.remove(value)


class FieldGroup:

    def __init__(self):
        self.fields = []
        self.taken_values = []
        self.empty_fields = False

    def resolve_values(self):
        self.empty_fields = False
        for field in self.fields:
            if field.value == 0:
                if len(field.possible_values) == 1:
                    field.value = field.possible_values.pop()
                else:
                    field.update_possible_values(self.taken_values)
                    self.empty_fields = True
            elif field.value not in self.taken_values:
                self.taken_values.append(field.value)


class Board:

    def __init__(self, value_tuples):
        self.rows = self.init_list_of_lists(9)
        self.columns = self.init_list_of_lists(9)
        self.squares = self.init_list_of_lists(9)
        for row in range(9):
            for column in range(9):
                field = Field((row + 1), (column + 1), 0)
                print("{0}.row, {0}.column, {0}.square, {0}.value".format(field))
                self.rows[row].fields.append(field)
                self.columns[column].fields.append(field)
                self.squares[field.square].fields.append(field)
        for row, column, value in value_tuples:
            for field in self.rows[row].fields:
                if field.row == row and field.column == column:
                    field.value = value

    @staticmethod
    def init_list_of_lists(size):
        list_of_lists = list()
        for index in range(size):
            list_of_lists.append(FieldGroup())
        return list_of_lists

    def solve(self):
        solved = False
        while not solved:
            solved = True
            for row_of_fields in self.rows:
                row_of_fields.resolve_values()
                if row_of_fields.empty_fields:
                    solved = False

    def print_board(self):
        for row_of_fields in self.rows:
            row_printout = " | "
            for fld in row_of_fields.fields:
                row_printout.join("{0}".format(fld.row))
                #print(row_of_fields.fields)
            print(row_printout)
            print("====================================")


board = Board([(1, 3, 5)])
#board.print_board()
