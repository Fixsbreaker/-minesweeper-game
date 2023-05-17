import pygame
pygame.init()

WIDTH, HEIGHT = 700, 800

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('minesweeper')

def main():
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

    pygame.quit()

if __name__ == "__main__":
    main()