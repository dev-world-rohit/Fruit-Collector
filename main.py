import pygame
from pygame.locals import *
import random
from data.scripts.text import font
from data.scripts.game_break import Break

pygame.init()

screen_size = [550, 550]
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Fruit Collector")


# generating the breaks numbers as well as the mines
def breaks(level, game_rule):
    number_mines = game_rule[level][0]
    rows = columns = game_rule[level][1]
    game_grid = [[0 for _ in range(columns)] for _ in range(rows)]

    i = 0
    while i < number_mines:
        row, col = random.randint(0, rows - 1), random.randint(0, columns - 1)
        if game_grid[row][col] == 'm':
            continue
        game_grid[row][col] = 'm'
        i += 1
    
    return game_grid


# finding the number around the mines
def finding_numbers(break_grid):
    rows = cols = len(break_grid)
    for i in range(rows):
        for j in range(cols):
            if break_grid[i][j] == 'm':
                continue
            mines = 0
            if 0 <= i - 1 < rows and 0 <= j - 1 < cols and break_grid[i - 1][j - 1] == 'm':
                mines += 1
            if 0 <= i < rows and 0 <= j - 1 < cols and break_grid[i][j - 1] == 'm':
                mines += 1
            if 0 <= i + 1 < rows and 0 <= j - 1 < cols and break_grid[i + 1][j - 1] == 'm':
                mines += 1
            if 0 <= i - 1 < rows and 0 <= j < cols and break_grid[i - 1][j] == 'm':
                mines += 1
            if 0 <= i - 1 < rows and 0 <= j + 1 < cols and break_grid[i - 1][j + 1] == 'm':
                mines += 1
            if 0 <= i < rows and 0 <= j + 1 < cols and break_grid[i][j + 1] == 'm':
                mines += 1
            if 0 <= i + 1 < rows and 0 <= j + 1 < cols and break_grid[i + 1][j + 1] == 'm':
                mines += 1
            if 0 <= i + 1 < rows and 0 <= j < cols and break_grid[i + 1][j] == 'm':
                mines += 1
            break_grid[i][j] = mines
    return break_grid


# generating the board assigning the values [x, y, color, size, name]. name can be 1, 2, 3, 4, 5, m, or nothing
def generate_board(level, game_rule):
    break_grid = breaks(level, game_rule)
    game_board = finding_numbers(break_grid)


# variables--------------------------------------------------------------#
clock = pygame.time.Clock()
fps = 30

game_rule = {"Easy": [10, 10],  # [rows/columns, number of mines]
             "Medium": [18, 40],
             "Hard": [25, 99]}

score_area = [0, 0, screen_size[0], 50]

level = "Easy"
generate_board(level, game_rule)

score_board_color = (74, 117, 44)
light_green_breaks = (191, 225, 125)
dark_green_breaks = (185, 221, 119)
break_back_light = (229, 194, 159)
break_back_dark = (178, 150, 123)

black_text = font('large_font.png', (255, 255, 255), 1)
text_1 = font('large_font.png', (0, 255, 0), 1)
text_2 = font('large_font.png', (0, 0, 255), 1)
text_3 = font('large_font.png', (255, 0, 0), 1)
text_4 = font('large_font.png', (255, 0, 255), 1)
text_5 = font('large_font.png', (255, 255, 0), 1)

# main game loop-----------------------------------------------------------------#
game = True
while game:
    screen.fill((255, 255, 255))
    
    pygame.draw.rect(screen, score_board_color, score_area)
    black_text.display_fonts(screen, str(level), [30, 18])

    # binding the keys------------------------------------------------#
    for event in pygame.event.get():
        if event.type == QUIT:
            game = False

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
