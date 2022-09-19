from project import check_columns, check_rows, check_squares, check_empty_numbers, is_valid_sudoku


invalid_board = [
        [7, 8, 1,   3, 4,  4,  5, 9, 6],
        [3, 4, 5,   6, 1, 9,   7, 2, 8],
        [6, 2, 9,   5, 7, 8,   4, 1, 3],

        [9, 1, 7,   4, 2, 6,   8, 3, 5],
        [2, 6, 3,   1, 8, 5,   9, 7, 4],
        [8, 5, 4,   9, 3,  3,  2, 6, 1],

        [1, 9, 2,   8, 6, 4,    0,0, 7],
        [5, 3,  9,  7, 9, 1,   6, 4, 2],
        [4,  1,6,   2, 5, 3,   1, 8,  0]
    ]

valid_board = [
    [3, 9, 7, 2, 8, 1, 6, 4, 5],
    [4, 1, 2, 9, 6, 5, 7, 3, 8],
    [8, 6, 5, 3, 7, 4, 1, 2, 9],
    [2, 4, 9, 8, 5, 7, 3, 1, 6],
    [6, 7, 1, 4, 9, 3, 5, 8, 2],
    [5, 3, 8, 1, 2, 6, 4, 9, 7],
    [7, 8, 4, 5, 1, 2, 9, 6, 3],
    [9, 5, 3, 6, 4, 8, 2, 7, 1],
    [1, 2, 6, 7, 3, 9, 8, 5, 4]
]


def test_check_columns():
    results = list(check_columns(invalid_board))
    assert len(results) == 3
    assert results[0] == {"col": 1, "dup_list": [1]}
    assert results[1] == {"col": 2, "dup_list": [9]}
    assert results[2] == {"col": 5, "dup_list": [3, 4]}


def test_check_rows():
    results = list(check_rows(invalid_board))
    assert len(results) == 4
    assert results[0] == {"row": 0, "dup_list": [4]}
    assert results[1] == {"row": 5, "dup_list": [3]}
    assert results[2] == {"row": 7, "dup_list": [9]}
    assert results[3] == {"row": 8, "dup_list": [1]}


def test_check_squares():
    results = list(check_squares(invalid_board))
    assert len(results) == 3
    assert results[0] == {"squr": (0, 1), "dup_list": [4]}
    assert results[1] == {"squr": (1, 1), "dup_list": [3]}
    assert results[2] == {"squr": (2, 0), "dup_list": [1, 9]}


def test_check_empty_numbers():
    results = list(check_empty_numbers(invalid_board))
    assert len(results) == 3
    assert results[0] == (6, 6)
    assert results[1] == (6, 7)
    assert results[2] == (8, 8)


def test_is_valid_sudoku():
    assert is_valid_sudoku(invalid_board) == False
    assert is_valid_sudoku(valid_board) == True
