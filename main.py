import queue

import pygame
import random
pygame.init()

WIDTH, HEIGHT = 700, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
NUM_FONT = pygame.font.SysFont('comicsans', 20)
NUM_COLORS = {1: 'black', 2: 'green', 3: 'red', 4: 'orange',
              5: 'yellow', 6: 'purple', 7: 'blue', 8: 'pink'}
RECT_COLOR = (200, 200, 200)
CLICKED_RECT_COLOR = (140, 140, 140)
pygame.display.set_caption('minesweeper')
BG_COLOR = "white"
ROWS, COLS = 15, 15
MINES = 30
FLAG_RECT_COLOR = 'red'



def find_place(row, col, rows, cols):
    places = []

    if row > 0:
        places.append((row - 1, col))
    if row < rows - 1:
        places.append((row + 1, col))
    if row > 0:
        places.append((row, col - 1))
    if row < cols - 1:
        places.append((row, col + 1))

    if row > 0 and col > 0:
        places.append((row - 1, col - 1))
    if row < rows - 1 and col < cols - 1:
        places.append((row + 1, col + 1))
    if row < rows - 1 and col > 1:
        places.append((row + 1, col - 1))
    if row > 0 and col < cols - 1:
        places.append((row - 1, col + 1))

    return places


def grid(rows, cols, mines):
    field = [[0 for _ in range(cols)] for _ in range(rows)]
    mine_positions = set()

    while len(mine_positions) < mines:
        row = random.randrange(0, rows)
        col = random.randrange(0, cols)
        pos = row, col

        if pos in mine_positions:
            continue

        mine_positions.add(pos)
        field[row][col] = -1

    for mine in mine_positions:
        places = find_place(*mine, rows, cols)
        for r, c in places:
            field[r][c] += 1

    return field


def draw(win, field, cover_field):
    win.fill(BG_COLOR)
    size = WIDTH / ROWS

    for i, row in enumerate(field):
        y = size * i
        for j, value in enumerate(row):
            x = size * j

            is_covered = cover_field[i][j] == 0
            is_flag = cover_field[i][j] == -2

            if is_flag:
                pygame.draw.rect(win, FLAG_RECT_COLOR,(x,y,size,size))
                pygame.draw.rect(win,'black',(x,y,size,size),2)
                continue

            if is_covered:
                pygame.draw.rect(win, RECT_COLOR, (x, y, size, size))
                pygame.draw.rect(win, 'black', (x, y, size, size), 2)
                continue
            else:
                pygame.draw.rect(win, CLICKED_RECT_COLOR, (x, y, size, size))
                pygame.draw.rect(win, 'black', (x, y, size, size), 2)

            if value > 0:
                text = NUM_FONT.render(str(value), 1, NUM_COLORS[value])
                win.blit(text, (x + (size/2 - text.get_width()/2),
                                y + (size/2 - text.get_height()/2)))

    pygame.display.update()


def get_grid_pos(mouse_pos):
    mx, my = mouse_pos
    row = int(my // (WIDTH / ROWS))
    col = int(mx // (WIDTH / ROWS))

    return row, col

def uncover_from_pos(row, col, cover_field, field):
    q = queue.Queue()
    q.put((row, col))
    visited = set()

    while not q.empty():
        current = q.get()

        places = find_place(*current, ROWS, COLS)
        for r, c in places:
            if (r, c) in visited:
                continue

            value = field[r][c]
            if value == 0 and cover_field[r][c] != -2:
                q.put((r, c))

            cover_field[r][c] = 1
            visited.add((r, c))


def main():
    run = True
    field = grid(ROWS, COLS, MINES)
    cover_field = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    flags = MINES
    clicks = 0


    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                row,col = get_grid_pos(pygame.mouse.get_pos())
                if row >= ROWS or col >= COLS:
                    continue
                mouse_pressed = pygame.mouse.get_pressed()
                if mouse_pressed[0]:
                    cover_field[row][col] = 1
                    if clicks == 0 or field[row][col] == 0:
                        uncover_from_pos(row,col,cover_field,field)
                elif mouse_pressed[2]:
                    if cover_field[row][col] == -2:
                        cover_field[row][col] = 0
                        flags += 1
                    else:
                        flags -= 1
                        cover_field[row][col] = -2

        draw(win, field, cover_field)



    pygame.quit()

if __name__ == "__main__":
    main()