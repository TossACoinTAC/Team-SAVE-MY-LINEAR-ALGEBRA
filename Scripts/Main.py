import pygame
from GameManagers.GameManager import GameManager


def main():

    pygame.init()
    game_manager: GameManager = GameManager()

    while True:
        game_manager.deal_events()
        game_manager.render_screen()


if __name__ == "__main__":
    main()
