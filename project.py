import sys, math
import pygame
from sudoku import Sudoku


WIDTH, HEIGHT = 550, 580
background_color = (251, 247, 245)

# Color of unchangeable positions on SUDOKU board
original_grid_element_color = (35, 43, 43)
# Color of changeable positions on SUDOKU board
changeable_grid_element_color = "blue"

# Color of position that is clicked on, or a valid number on SUDOKU board
marker_color = (176, 224, 230)
# Color of wrong number
wrong_number_color = (255, 106, 116)

# Light shade of the submit button
light_color = (170, 170, 170)
# Dark shade of the submit button
dark_color = (100, 100, 100)


SUDOKU = Sudoku()
LEVEL = "easy"
SIZE = 9
BASE = 3
GAME_BOARD = []
BLANK = []
INVALID_INDEXES = []
CURRENT_INDEX = (0, 0)


######## FUNCTIONS THAT CHECK IF A SUDOKU BOARD IS VALID
def check_columns(board):
    size = len(board)
    for c in range(size):
        col = [board[r][c] for r in range(size) if board[r][c] != 0]
        if len(col) != len(set(col)):
            yield {"col": c, "dup_list": sorted(list(set([x for x in col if col.count(x) > 1])))}


def check_rows(board):
    size = len(board)
    for r in range(size):
        row = [board[r][c] for c in range(size) if board[r][c] != 0]
        if len(row) != len(set(row)):
            yield {"row": r, "dup_list": sorted(list(set([x for x in row if row.count(x) > 1])))}


def check_squares(board):
    size = len(board)
    base = int(math.sqrt(size))
    # Big loop for 3x3 squares (each square contains 9 numbers from 1-9)
    for r in range(base):
        for c in range(base):
            square = []
            # Small loop for each square
            row0 = r * base
            col0 = c * base
            for i in range(row0, row0 + base, 1):
                for j in range(col0, col0 + base, 1):
                    if board[i][j] != 0:
                        square.append(board[i][j])
            if len(square) != len(set(square)):
                # print(f"Square {r, c}")
                yield {"squr": (r, c), "dup_list": sorted(list(set([x for x in square if square.count(x) > 1])))}


def check_empty_numbers(board):
    size = len(board)
    for r in range(size):
        for c in range(size):
            if board[r][c] == 0:
                yield (r, c)


def is_valid_sudoku(board):       
    if len(list(check_columns(board))) + len(list(check_rows(board))) + len(list(check_squares(board))) + len(list(check_empty_numbers(board))) == 0:
        return True
    return False













######## BUILDING GAME

# Building SUDOKU puzzle
def game_on(window):
    # Clear old screen
    window.fill(background_color)

    string_font = pygame.font.SysFont('Comic Sans MS', 20)

    difficulty = string_font.render(f"Level: {LEVEL.capitalize()}", True, (0, 0, 0))
    window.blit(difficulty, (50, 20))

    global SUDOKU, SIZE, BASE, GAME_BOARD, BLANK, FIRST_BLANK

    SUDOKU.new_puzzle()
    SIZE = SUDOKU.size
    BASE = SUDOKU.base
    GAME_BOARD = SUDOKU.challenge(LEVEL)
    BLANK = [(row, col) for row in range(SIZE) for col in range(SIZE) if GAME_BOARD[row][col] == 0]
    FIRST_BLANK = BLANK[0]

    for i in range(SIZE):
        for j in range(SIZE):
            print(SUDOKU.board[i][j], end=" ")
            if (j + 1) % BASE == 0:
                print("  ", end="")
            if j == SIZE - 1:
                print("", end="\n")
        if (i + 1) % BASE == 0:
            print("", end="\n")
    print("\n")

    # Drawing the grid
    #   pygame.draw.line(window, background_color, starting point, ending point, line_width)
    for i in range(SIZE + 1):
        line_width = 1
        if i % BASE == 0:
            line_width = 4
        # Vertical lines
        pygame.draw.line(window, (0, 0, 0), (50 + 50 * i, 50), (50 + 50 * i, 50 + 50 * SIZE), line_width)
        # Horizontal lines
        pygame.draw.line(window, (0, 0, 0), (50, 50 + 50 * i), (50 + 50 * SIZE, 50 + 50 * i), line_width)
    for i in range(SIZE):
        for j in range(SIZE):
            number_not_hover(window, (i, j))


    # Return to choose another level Button
    for i in range(2):
        x = 5 + 30 * i
        y = 5 + 20 * i
        pygame.draw.line(window, (0, 0, 0), (x, 5), (x, 25), 1)
        pygame.draw.line(window, (0, 0, 0), (5, y), (35, y), 1)
    turn_back_button_not_hover(window)


    # Clear all answers Button
    for i in range(2):
        x = 430 + 70 * i
        y = 20 + 20 * i
        pygame.draw.line(window, (0, 0, 0), (x, 20), (x, 40), 1)
        pygame.draw.line(window, (0, 0, 0), (430, y), (500, y), 1)
    clear_button_not_hover(window)

    
    # Submit button
    #   Draw borders
    for i in range(2):
        pygame.draw.line(window, (0, 0, 0), (200 + 150 * i, 520), (200 + 150 * i, 550), 2)
        pygame.draw.line(window, (0, 0, 0), (200, 520 + 30 * i), (350, 520 + 30 * i), 2)
    submit_button_not_hover(window)

    while True:
        game_board_interaction(window)



def game_board_interaction(window):
    for event in pygame.event.get():
        # Stores the (x,y) coordinates of the cursor
        mouse_position = pygame.mouse.get_pos()
        x, y = mouse_position[0], mouse_position[1]

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # When mouse hovers on SUDOKU board
        if 50 <= x <= 500 and 50 <= y <= 500:
            for i in range(SIZE):
                for j in range(SIZE):
                    # When mouse hovers on current position
                    if ((y - (y % 50)) // 50 - 1, (x - (x % 50)) // 50 - 1) == (i, j):
                        number_hover(window, (i, j))

                        # Press Enter, left, right, up, down
                        if event.type == pygame.KEYDOWN:
                            # Enter
                            if event.key == pygame.K_RETURN:
                                fill_missing_number(window, (i, j))
                            # Left
                            if event.key == pygame.K_LEFT:
                                if j > 0:
                                    pygame.mouse.set_pos(x - 50, y)
                            # Right
                            if event.key == pygame.K_RIGHT:
                                if j < SIZE - 1:
                                    pygame.mouse.set_pos(x + 50, y)
                            # Up
                            if event.key == pygame.K_UP:
                                if i > 0:
                                    pygame.mouse.set_pos(x, y - 50)
                            # Down
                            if event.key == pygame.K_DOWN:
                                if i < SIZE - 1:
                                    pygame.mouse.set_pos(x, y + 50)

                        # Click on current position
                        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                            fill_missing_number(window, (i, j))
                    else:
                        number_not_hover(window, (i, j))

        # When mouse hovers outside of SUDOKU board
        else:
            # When mouse hovers on turn back button
            if 5 <= x <= 35 and 5 <= y <= 25:
                turn_back_button_hover(window)
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        start(window)
            else:
                # When mouse hovers on clear button
                if 430 <= x <= 500 and 20 <= y <= 40:
                    clear_button_hover(window)
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        clear_all_answers(window)
                else:
                    # When mouse hovers on submit button
                    if 200 <= x <= 350 and 520 <= y <= 550:
                        submit_button_hover(window)
                        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                            submit(window)
                    else:
                        turn_back_button_not_hover(window)
                        clear_button_not_hover(window)
                        submit_button_not_hover(window)
                        # Interact with SUDOKU board by keyboard
                        keyboard_control(window)

    pygame.display.update()
    return



# Interact with SUDOKU board by keyboard
def keyboard_control(window):
    global CURRENT_INDEX

    number_hover(window, CURRENT_INDEX)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    fill_missing_number(window, CURRENT_INDEX)

                if event.key == pygame.K_LEFT:
                    if CURRENT_INDEX[1] > 0:
                        number_not_hover(window, CURRENT_INDEX)
                        number_hover(window, (CURRENT_INDEX[0], CURRENT_INDEX[1] - 1))

                if event.key == pygame.K_RIGHT:
                    if CURRENT_INDEX[1] < SIZE - 1:
                        number_not_hover(window, CURRENT_INDEX)
                        number_hover(window, (CURRENT_INDEX[0], CURRENT_INDEX[1] + 1))

                if event.key == pygame.K_UP:
                    if CURRENT_INDEX[0] > 0:
                        number_not_hover(window, CURRENT_INDEX)
                        number_hover(window, (CURRENT_INDEX[0] - 1, CURRENT_INDEX[1]))

                if event.key == pygame.K_DOWN:
                    if CURRENT_INDEX[0] < SIZE - 1:
                        number_not_hover(window, CURRENT_INDEX)
                        number_hover(window, (CURRENT_INDEX[0] + 1, CURRENT_INDEX[1]))

            # When mouse hovers on SUDOKU board, or Submit button, or Clear button, or Turn back button:  Quit function
            mouse_postion = pygame.mouse.get_pos()
            if 50 <= mouse_postion[0] <= 500 and 50 <= mouse_postion[1] <= 500:
                return
            if 200 <= mouse_postion[0] <= 350 and 520 <= mouse_postion[1] <= 550:
                return
            if 430 <= mouse_postion[0] <= 500 and 20 <= mouse_postion[1] <= 40:
                return
            if 5 <= mouse_postion[0] <= 35 and 5 <= mouse_postion[1] <= 25:
                return



def fill_missing_number(window, number_index):
    global CURRENT_INDEX
    CURRENT_INDEX = number_index

    i, j = number_index[0], number_index[1]

    number_font = pygame.font.SysFont('Comic Sans MS', 35)

    if (i, j) in BLANK:
        # Change background color
        pygame.draw.rect(window, (176, 196, 222), ((j + 1) * 50 + 5, (i + 1) * 50 + 5, 40, 40))

        # If position has already filled, keep the value of that position on the screen
        if GAME_BOARD[i][j] != 0:
            value = number_font.render(str(GAME_BOARD[i][j]), True, changeable_grid_element_color)  
            window.blit(value, ((j + 1) * 50 + 15, (i + 1) * 50))

        pygame.display.update()

        while True:
            for sub_event in pygame.event.get():
                if sub_event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if sub_event.type == pygame.KEYDOWN:
                    # Type the value of that postion
                    if sub_event.unicode.isnumeric() and int(sub_event.unicode) != 0:
                        # Clear old value
                        pygame.draw.rect(window, (176, 196, 222), ((j + 1) * 50 + 5, (i + 1) * 50 + 5, 40, 40))
                        # Fill new value
                        value = number_font.render(str(sub_event.unicode), True, changeable_grid_element_color)                
                        window.blit(value, ((j + 1) * 50 + 15, (i + 1) * 50))
                        # Update game board
                        GAME_BOARD[i][j] = int(sub_event.unicode)
                        pygame.display.update()

                    if sub_event.key == pygame.K_BACKSPACE:
                        # Update game board
                        GAME_BOARD[i][j] = 0
                        # Clear current value
                        pygame.draw.rect(window, (176, 196, 222), ((j + 1) * 50 + 5, (i + 1) * 50 + 5, 40, 40))
                        pygame.display.update()

                    # Submit the number in that position by ENTER or ESC
                    if sub_event.key in [pygame.K_RETURN, pygame.K_ESCAPE]:
                        number_hover(window, (i, j))
                        return

                # Submit the number in that position by clicking
                if sub_event.type == pygame.MOUSEBUTTONUP and sub_event.button == 1:
                    number_hover(window, (i, j))
                    return           
    else:
        return



# A position on SUDOKU board is hovered on
def number_hover(window, number_index):
    i, j = number_index[0], number_index[1]

    global CURRENT_INDEX
    CURRENT_INDEX = (i, j)

    number_font = pygame.font.SysFont('Comic Sans MS', 35)

    # Change background color
    pygame.draw.rect(window, marker_color, ((j + 1) * 50 + 5, (i + 1) * 50 + 5, 40, 40))

    # If position has already filled, keep the value of that position on the screen
    if GAME_BOARD[i][j] != 0:
        value = number_font.render(str(GAME_BOARD[i][j]), True, original_grid_element_color) 
        if (i, j) in BLANK:
            value = number_font.render(str(GAME_BOARD[i][j]), True, changeable_grid_element_color)  
        window.blit(value, ((j + 1) * 50 + 15, (i + 1) * 50))

    pygame.display.update()
    return



def number_not_hover(window, number_index):
    i, j = number_index[0], number_index[1]

    number_font = pygame.font.SysFont('Comic Sans MS', 35)

    # Change background color
    pygame.draw.rect(window, background_color, ((j + 1) * 50 + 5, (i + 1) * 50 + 5, 40, 40))

    # If position has already filled, keep the value of that position on the screen
    if GAME_BOARD[i][j] != 0:
        value = number_font.render(str(GAME_BOARD[i][j]), True, original_grid_element_color)    
        if (i, j) in BLANK:
            value = number_font.render(str(GAME_BOARD[i][j]), True, changeable_grid_element_color) 
        window.blit(value, ((j + 1) * 50 + 15, (i + 1) * 50))

    pygame.display.update()
    return



def turn_back_button_not_hover(window):
    pygame.draw.rect(window, wrong_number_color, (6, 6, 29, 19))
    # Arrow
    pygame.draw.line(window, "white", (11, 15), (19, 8), 2)
    pygame.draw.line(window, "white", (11, 15), (19, 22), 2)
    pygame.draw.line(window, "white", (12, 15), (28, 15), 2)
    pygame.display.update()
    return



def turn_back_button_hover(window):
    pygame.draw.rect(window, "red", (6, 6, 29, 19))
    # Arrow
    pygame.draw.line(window, "white", (11, 15), (19, 8), 2)
    pygame.draw.line(window, "white", (11, 15), (19, 22), 2)
    pygame.draw.line(window, "white", (12, 15), (28, 15), 2)
    pygame.display.update()
    return



def clear_button_not_hover(window):
    small_string_font = pygame.font.SysFont('Comic Sans MS', 15)
    pygame.draw.rect(window, marker_color, (431, 21, 69, 19))
    value = small_string_font.render("Clear", True,(0, 0, 0))
    window.blit(value, (447, 20))
    pygame.display.update()
    return



def clear_button_hover(window):
    small_string_font = pygame.font.SysFont('Comic Sans MS', 15)
    pygame.draw.rect(window, wrong_number_color, (431, 21, 69, 19))
    value = small_string_font.render("Clear", True,(0, 0, 0))
    window.blit(value, (447, 20))
    pygame.display.update()
    return



def clear_all_answers(window):
    for i in range(SIZE):
        for j in range(SIZE):
            if (i, j) in BLANK and GAME_BOARD[i][j] != 0:
                GAME_BOARD[i][j] = 0
                pygame.draw.rect(window, background_color, ((j + 1) * 50 + 5, (i + 1) * 50 + 5, 40, 40))
    pygame.display.update()
    return


# Submit button is hovered on
def submit_button_hover(window):
    string_font = pygame.font.SysFont('Comic Sans MS', 20)
    pygame.draw.rect(window, light_color, (202, 522, 148, 28))
    value = string_font.render("Submit", True, (255, 255, 255))            
    window.blit(value, (245, 520))
    pygame.display.update()
    return



def submit_button_not_hover(window):
    string_font = pygame.font.SysFont('Comic Sans MS', 20)
    pygame.draw.rect(window, dark_color, (202, 522, 148, 28))
    value = string_font.render("Submit", True, (255, 255, 255))            
    window.blit(value, (245, 520))
    pygame.display.update()
    return



# Highlight invalid number on SUDOKU board
def wrong_answer(window, number_index):
    row, col = number_index[0], number_index[1]

    number_font = pygame.font.SysFont('Comic Sans MS', 35)

    pygame.draw.rect(window, wrong_number_color, ((col + 1) * 50 + 5, (row + 1) * 50 + 5, 40, 40))
    if GAME_BOARD[row][col] != 0:
        value = number_font.render(str(GAME_BOARD[row][col]), True, original_grid_element_color)
        if (row, col) in BLANK:
            value = number_font.render(str(GAME_BOARD[row][col]), True, "white")
        window.blit(value, ((col + 1) * 50 + 15, (row + 1) * 50))
    
    pygame.display.update()
    return



# Highlight valid number on SUDOKU board
def right_answer(window, number_index):
    row, col = number_index[0], number_index[1]

    number_font = pygame.font.SysFont('Comic Sans MS', 35)

    if (row, col) not in INVALID_INDEXES:
        pygame.draw.rect(window, marker_color, ((col + 1) * 50 + 5, (row + 1) * 50 + 5, 40, 40))
        if GAME_BOARD[row][col] != 0:
            value = number_font.render(str(GAME_BOARD[row][col]), True, original_grid_element_color)
            if (row, col) in BLANK:
                value = number_font.render(str(GAME_BOARD[row][col]), True, "blue")
            window.blit(value, ((col + 1) * 50 + 15, (row + 1) * 50))
    
    pygame.display.update()
    return



# Submit answer
def submit(window):
    global INVALID_INDEXES
    INVALID_INDEXES = []
    if is_valid_sudoku(GAME_BOARD) == True:
        for i in range(SIZE):
            for j in range(SIZE):
                if (i, j) in BLANK:
                    right_answer(window, (i, j))
        congratulate(window)

    else:
        # If check columns fails
        if len(list(check_columns(GAME_BOARD))) != 0:
            for value in check_columns(GAME_BOARD):
                col = value["col"]
                for row in range(SIZE):
                    if GAME_BOARD[row][col] in value["dup_list"]:
                        if (row, col) not in INVALID_INDEXES:
                            INVALID_INDEXES.append((row, col))
                        wrong_answer(window, (row, col))
                    else:
                        right_answer(window, (row, col))
        
        # If check rows fails
        if len(list(check_rows(GAME_BOARD))) != 0:
            for value in check_rows(GAME_BOARD):
                row = value["row"]
                for col in range(SIZE):
                    if GAME_BOARD[row][col] in value["dup_list"]:
                        if (row, col) not in INVALID_INDEXES:
                            INVALID_INDEXES.append((row, col))
                        wrong_answer(window, (row, col))
                    else:
                        right_answer(window, (row, col))

        # If check squares fails
        if len(list(check_squares(GAME_BOARD))) != 0:
            for value in check_squares(GAME_BOARD):
                r, c = value["squr"][0], value["squr"][1]
                for row in range(r * BASE, r * BASE + BASE):
                    for col in range(c * BASE, c * BASE + BASE):
                        if GAME_BOARD[row][col] in value["dup_list"]:
                            if (row, col) not in INVALID_INDEXES:
                                INVALID_INDEXES.append((row, col))
                            wrong_answer(window, (row, col))
                        else:
                            right_answer(window, (row, col))

        # If columns, rows, squares are OK, highlight empty positions
        if len(list(check_columns(GAME_BOARD))) + len(list(check_rows(GAME_BOARD))) + len(list(check_squares(GAME_BOARD))) == 0:
            for row in range(SIZE):
                for col in range(SIZE):
                    if GAME_BOARD[row][col] == 0:
                        wrong_answer(window, (row, col))
    return



def congratulate(window):
    window.fill(background_color)

    string_font = pygame.font.SysFont('Comic Sans MS', 20)
    number_font = pygame.font.SysFont('Comic Sans MS', 35)

    value = number_font.render("Well done!", True, (0, 0, 0))
    window.blit(value, (190, 30))

    # Try again, Other Levels
    for i in range(4):
        x = 100 + 150 * i
        if i > 1:
            x = 150 * i
        pygame.draw.line(window, (0, 0, 0), (x, 170), (x, 210), 2)
    
        if i == 0 or i == 2:
            pygame.draw.line(window, (0, 0, 0), (x, 170), (x + 150, 170), 2)
            pygame.draw.line(window, (0, 0, 0), (x, 210), (x + 150, 210), 2)

    # Quit
    for i in range(2):
        x = 200 + 150 * i
        y = 250 + 40 * i
        pygame.draw.line(window, (0, 0, 0), (x, 250), (x, 290), 2)
        pygame.draw.line(window, (0, 0, 0), (200, y), (350, y), 2)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            mouse_position = pygame.mouse.get_pos()

            # Try again, Other LEVEL
            for i in range(2):
                x = 100 + 200 * i + 2
                pygame.draw.rect(window, light_color, (x, 172, 148, 38))

                if x <= mouse_position[0] <= x + 150 and 170 <= mouse_position[1] <= 210:
                    pygame.draw.rect(window, dark_color, (x, 172, 148, 38))
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        if i == 0:
                            game_on(window)
                        if i == 1:
                            start(window)
            
            value = string_font.render("Play again", True, (255, 255, 255)) 
            window.blit(value, (134, 176))

            value = string_font.render("Other levels", True, (255, 255, 255)) 
            window.blit(value, (317, 176))

            # Quit button
            pygame.draw.rect(window, wrong_number_color, (202, 252, 148, 38))
            if 200 <= mouse_position[0] <= 350 and 250 <= mouse_position[1] <= 290:
                pygame.draw.rect(window, "red", (202, 252, 148, 38))
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pygame.quit()
                    sys.exit()

            value = string_font.render("Quit", True, (255, 255, 255)) 
            window.blit(value, (252, 256))

            pygame.display.update()



# The first screen
def start(window):
    window.fill(background_color)

    global LEVEL

    number_font = pygame.font.SysFont('Comic Sans MS', 35)
    string_font = pygame.font.SysFont('Comic Sans MS', 20)

    # Levels
    value = number_font.render("Choose a level", True, (0, 0, 0))            
    window.blit(value, (160, 80))

    # Borders of buttons
    for i in range(4):
        x = 100 + 150 * i
        y = 210 + 40 * i
        if i > 1:
            x = 150 * i
            y = 200 + 40 * i
        # Vertical borders
        pygame.draw.line(window, (0, 0, 0), (x, 210), (x, 250), 2)
        pygame.draw.line(window, (0, 0, 0), (x, 280), (x, 320), 2)
        # Horizontal borders
        pygame.draw.line(window, (0, 0, 0), (100, y), (250, y), 2)
        pygame.draw.line(window, (0, 0, 0), (300, y), (450, y), 2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            mouse_position = pygame.mouse.get_pos()

            # When mouse 40 on a button, change it's background color
            for i in range(2):
                for j in range(2):
                    x = 100 + 200 * i
                    y = 210 + 70 * j

                    if (i, j) == (0, 0):
                        LEVEL = "easy"
                    elif (i, j) == (0, 1):
                        LEVEL = "hard"
                    elif (i, j) == (1, 0):
                        LEVEL = "intermediate"
                    else:
                        LEVEL = "pro"

                    pygame.draw.rect(window, dark_color, (x + 2, y + 2, 148, 38))
                    if x <= mouse_position[0] <= x + 150 and y <= mouse_position[1] <= y + 30:
                        pygame.draw.rect(window, light_color, (x + 2, y + 2, 148, 38))
                        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                            game_on(window)

            # Buttons' names
            value = string_font.render("Easy", True, (255, 255, 255)) 
            window.blit(value, (150, 216))

            value = string_font.render("Intermediate", True, (255, 255, 255)) 
            window.blit(value, (315, 216))
    
            value = string_font.render("Hard", True, (255, 255, 255)) 
            window.blit(value, (150, 286))

            value = string_font.render("Pro", True, (255, 255, 255)) 
            window.blit(value, (360, 286))

            pygame.display.update()



def main():
    # Set up screen
    pygame.init()
    pygame.display.set_caption("Sudoku")
    pygame.font.init()
    # number_font = pygame.font.SysFont('Comic Sans MS', 35)
    # string_font = pygame.font.SysFont('Comic Sans MS', 20)
    # small_string_font = pygame.font.SysFont('Comic Sans MS', 15)
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    window.fill(background_color)
    start(window)



if __name__ == "__main__":
    main()

            