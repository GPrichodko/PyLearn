class Field:

    def __init__(self, row, column, value=0):
        self.row = row
        self.column = column
        self.square = self.set_square(self.row, self.column)
        self.value = value
        self.possible_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]

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

    def update_possible_values(self, taken):
        for value in taken:
            try:
                self.possible_values.remove(value)
            except ValueError:
                pass


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
                self.rows[row].fields.append(field)
                self.columns[column].fields.append(field)
                self.squares[(field.square - 1)].fields.append(field)
        for field_params in value_tuples:
            row = field_params[0]
            column = field_params[1]
            value = field_params[2]
            for field in self.rows[row - 1].fields:
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
        step = 1
        while not solved:
            solved = True
            for row_of_fields in self.rows:
                row_of_fields.resolve_values()
                if row_of_fields.empty_fields:
                    solved = False
            print("STEP NUMBER {0}".format(step))
            step += 1
            self.print_board()

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
            #print("=====================================")


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
board.solve()
