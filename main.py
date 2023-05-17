import pygame
import random
pygame.init()

WIDTH, HEIGHT = 700, 800

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('minesweeper')
BG_COLOR = "green"
ROWS, CALLS = 30, 30


def draw(win):
    win.fill(BG_COLOR)
    pygame.display.update()


def find_place(row, col, rows, cols):
    places = []

    if row > 0:
        places.append(row - 1, col)
    if row < len(rows) - 1:
        places.append(row + 1, col)
    if row > 0:
        places.append(row, col - 1)
    if row < len(cols) - 1:
        places.append(row, col + 1)

    if row > 0 and col > 0:
        places.append(row - 1, col - 1)
    if row < len(rows) - 1 and col < len(cols) - 1:
        places.append(row + 1, col + 1)
    if row < len(rows) - 1 and col > 1:
        places.append(row + 1, col - 1)
    if row > 0 and col < len(cols) - 1:
        places.append(row - 1, col + 1)

    return places


def grid(rows, cols, mines):
    field = [[0 for _ in range(cols)] for _ in range(rows)]
    mines_place = set()
    mines_created = 0

    while mines_created < mines:
        row = random.randrange(0, rows)
        col = random.randrange(0, cols)
        pos = row, col
        if pos in mines_place:
            continue
        mines_place.add(pos)
        field[row][col] = -1



def main():
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        draw(win)

    pygame.quit()

if __name__ == "__main__":
    main()