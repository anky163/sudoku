import math, itertools, random


class Sudoku():
    def __init__(self, board=[[0 for _ in range(9)] for _ in range(9)]):
        self.board = board
        self.game_board = board
        self.size = len(board)
        self.base = int(math.sqrt(len(board)))

    def empty(self):
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]

    def challenge(self, mode="easy", base=3):
        self.new_puzzle(base)
        base = self.base
        size = self.size
        
        game_board = [[self.board[i][j] for j in range(size)] for i in range(size)]

        if mode == "easy":
            number_of_empty_values = [3, 4]
        elif mode == "intermediate":
            number_of_empty_values = [4, 5, 6]
        elif mode == "hard":
            number_of_empty_values = [5, 6, 7]
        elif mode == "pro":
            number_of_empty_values = [6, 7]

        for r in range(base):
            for c in range(base):
                row0 = r * base
                col0 = c * base
                n = random.choice(number_of_empty_values)
                blank_values = random.sample([x + 1 for x in range(size)], n)
                for i in range(row0, row0 + base):
                    for j in range(col0, col0 + base):
                        if game_board[i][j] in blank_values:
                            game_board[i][j] = 0

        return game_board

    def new_puzzle(self, base=3):
        # Create empty board
        size = base * base
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.base = base
        self.size = size
        # Fill all empty subrows starting from board[0][0:base]
        self.create_sub_row(0, 0)

    def create_sub_row(self, r, c):
        """
        Create a subrow of (base) numbers once at a time

        example: 1, 9, 8,   0, 0, 0,    0, 0, 0
                 0, 0, 0,   0, 0, 0,    0, 0, 0
                 ...
        """

        size = self.size
        base = self.base

        # col0 is the first column (index) for current subrow
        #   c in [0, 1, 2] if base = 3,   [0, 1, 2, 3] if base = 4 etc.
        #   In case base = 3:
        #       c = 0  ->  col0 = 0
        #       c = 1  ->  col0 = 3
        #       c = 2  ->  col0 = 6
        col0 = c * base

        # The first row (index) of the square that contains current subrow
        row0 = r - (r % base)

        # All numbers != 0 inside the same row of current subrow
        row_list = [self.board[r][j] for j in range(size) if self.board[r][j] != 0]

        # The square that contains current subrow
        square_list = [self.board[i][j] for j in range(col0, col0 + base) for i in range(row0, row0 + base) if self.board[i][j] != 0]

        # All columns from [col0:col0 + base]
        columns_list = [[self.board[i][j] for i in range(r) if self.board[i][j] != 0] for j in range(col0, col0 + base)]

        # try, except ValueError
        try:
            # All numbers that are not in the same row and square as those number in board[r][col0:col0 + base]
            remainders = [x for x in [number + 1 for number in range(size)] if x not in (row_list + square_list)]

            # All possible permutations of those remainders in (base) postions of board[r][col0:col0 + base]
            permutations = [list(p) for p in list(itertools.permutations(remainders, base))]

            # Remove all permutations that has a number duplicated in it's column
            permutations = [p for p in permutations if not any (p[i] in columns_list[i] for i in range(base))]

            # Shuffle the permutations list
            random.shuffle(permutations)

            # Count all p in permutations that fails
            failed_counter = 0
            for p in permutations:
                try:
                    self.board[r][col0:col0 + base] = [x for x in p]
                    
                    # Base case (Perfect puzzle finished!)
                    if r == size - 1 and c == base - 1:
                        return True

                    # Try all possibliltiesd of all next subrows (with this specific permutation) until a perfect puzzle is created, then return True
                    else:
                        # If current subrow is the last subrow in a row, move to the next row
                        if c == base - 1:
                            if self.create_sub_row(r + 1, 0) == True:
                                return True

                            # If the current permutation leads to nowhere
                            else:
                                # Undo: Empty all positions have been filled starting from current subrow
                                self.board[r][col0:col0 + base] = [0 for _ in range(base)]
                                self.board[r + 1:size][0:size] = [[0 for _ in range(size)] for _ in range(r + 1, size, 1)]
                                failed_counter += 1
                                
                        else:
                            if self.create_sub_row(r, c + 1) == True:
                                return True

                            # If the current permutation leads to nowhere
                            else:
                                # Undo: Empty all positions have been filled starting from current subrow
                                self.board[r][col0:size] = [0 for _ in range(col0, size, 1)]
                                self.board[r + 1:size][0:size] = [[0 for _ in range(size)] for _ in range(r + 1, size, 1)]
                                failed_counter += 1

                # If current permutation causes the next subrow not have enough possible numbers
                except ValueError:
                    failed_counter += 1
                
            # If all permutations lead to nowhere, turn back to previous subrow, try another permutation of that subrow
            if failed_counter == len(permutations):
                return False
            
        except ValueError:
            return False

    def check_columns(self):
        for c in range(self.size):
            col = [self.board[r][c] for r in range(self.size) if self.board[r][c] != 0]
            if len(col) != len(set(col)):
                yield {"col": c, "dup_list": list(set([x for x in col if col.count(x) > 1]))}

    def check_rows(self):
        for r in range(self.size):
            row = [self.board[r][c] for c in range(self.size) if self.board[r][c] != 0]
            if len(row) != len(set(row)):
                yield {"row": r, "dup_list": list(set([x for x in row if row.count(x) > 1]))}

    def check_squares(self):
        # Big loop for 3x3 squares (each square contains 9 numbers from 1-9)
        for r in range(self.base):
            for c in range(self.base):
                square = []
                # Small loop for each square
                row0 = r * self.base
                col0 = c * self.base
                for i in range(row0, row0 + self.base, 1):
                    for j in range(col0, col0 + self.base, 1):
                        if self.board[i][j] != 0:
                            square.append(self.board[i][j])
                if len(square) != len(set(square)):
                    # print(f"Square {r, c}")
                    yield {"squr": (r, c), "dup_list": list(set([x for x in square if square.count(x) > 1]))}

    def check_empty_numbers(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 0:
                    yield {"emptyR": r, "emptyC": c}

    def is_valid_sudoku(self):       
        if len(list(self.check_columns())) + len(list(self.check_rows())) + len(list(self.check_squares())) + len(list(self.check_empty_numbers())) == 0:
            return True
        return False
    