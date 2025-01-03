import pygame
from GameManagers.EventListener import EventListener
from GameManagers.ScreenRenderer import ScreenRenderer


def main():

    pygame.init()
    event_listener = EventListener()
    screen_renderer = ScreenRenderer()

    while True:
        event_listener.listen()
        screen_renderer.render_screen(event_listener.get_active_scene())


if __name__ == "__main__":
    main()
