import pygame
from pygame.locals import *
import random
from data.scripts.text import font
from data.scripts.game_break import Break

pygame.init()

screen_size = [500, 550]
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Fruit Collector")


# generating the breaks numbers as well as the mines
def breaks(level, game_rule):
    number_mines = game_rule[level][1]
    rows = columns = game_rule[level][0]
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
def generate_board(level, game_rule, score_area, colors, texts):
    break_grid = breaks(level, game_rule)
    game_board = finding_numbers(break_grid)
    rows = columns = game_rule[level][0]
    game_tiles = [[0 for _ in range(columns)] for _ in range(rows)]
    tile_size = screen_size[0] / game_rule[level][0]
    m = 0
    row = 0
    color = None
    back_color = None
    for i in range(len(game_board)):
        for j in range(len(game_board)):
            if j > 0:
                if m == 0:
                    color, back_color = "l_g_b", "b_b_d"
                    m = 1
                else:
                    color, back_color = "d_g_b", "b_b_l"
                    m = 0
            else:
                if i % 2 == 0:
                    color, back_color = "l_g_b", "b_b_d"
                    m = 1
                elif i % 2 != 0:
                    color, back_color = "d_g_b", "b_b_l"
                    m = 0

            tile = Break(i * tile_size, score_area[3] + j * tile_size, str(game_board[i][j]), tile_size, colors[color],
                   colors[back_color], texts[str(game_board[i][j])], level)
            game_tiles[i][j] = tile

    return game_tiles


# variables--------------------------------------------------------------#
clock = pygame.time.Clock()
fps = 30

level = "Hard"
game_rule = {"Easy": [10, 10, 2],  # [rows/columns, number of mines]
             "Medium": [20, 40, 1],
             "Hard": [25, 99, 1]}

score_area = [0, 0, screen_size[0], 50]

score_board_color = (74, 117, 44)
light_green_breaks = (191, 225, 125)
dark_green_breaks = (143, 190, 100)
break_back_light = (249, 194, 159)
break_back_dark = (208, 150, 123)
colors = {
    "l_g_b": light_green_breaks,
    "d_g_b": dark_green_breaks,
    "b_b_l": break_back_light,
    "b_b_d": break_back_dark,
}

black_text = font('large_font.png', (255, 255, 255), 1)
text_1 = font('large_font.png', (0, 255, 0), game_rule[level][2])
text_2 = font('large_font.png', (0, 0, 255), game_rule[level][2])
text_3 = font('large_font.png', (255, 0, 0), game_rule[level][2])
text_4 = font('large_font.png', (255, 0, 255), game_rule[level][2])
text_5 = font('large_font.png', (255, 255, 0), game_rule[level][2])
texts = {
    "0": text_5,
    "1": text_1,
    "2": text_2,
    "3": text_3,
    "4": text_4,
    "5": text_5,
    "6": text_1,
    "7": text_2,
    "8": text_3,
    "m": text_4
}

game_tiles = generate_board(level, game_rule, score_area,colors, texts)

# main game loop-----------------------------------------------------------------#
game = True
while game:
    screen.fill((255, 255, 255))
    
    pygame.draw.rect(screen, score_board_color, score_area)
    black_text.display_fonts(screen, str(level), [30, 18])

    for tiles in game_tiles:
        for tile in tiles:
            tile.display_tile(screen)

    # binding the keys------------------------------------------------#
    for event in pygame.event.get():
        if event.type == QUIT:
            game = False

        if event.type == MOUSEBUTTONDOWN:
            mouse_button = pygame.mouse.get_pressed()
            location = pygame.mouse.get_pos()
            tile_size = screen_size[0] / game_rule[level][0]
            x, y = int(location[0] // tile_size), int((location[1] - 50) // tile_size)
            if mouse_button[0]:
                game_tiles[x][y].clicked()
            if mouse_button[2]:
                print("right")

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
