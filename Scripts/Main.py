import pygame
from GameManager import GameManager


def main():

    pygame.init()
    game_manager = GameManager()

    while True:
        game_manager.update()
        pygame.display.flip()


if __name__ == "__main__":
    main()
