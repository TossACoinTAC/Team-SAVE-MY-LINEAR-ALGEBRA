import pygame
from Statics import Events, Scenes


class EventListener:
    def __init__(self):
        self.active_scene = Scenes.MAIN_MENU

    def listen(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    exit()
                case Events.MAIN_TO_STARTROOM:
                    self.active_scene = Scenes.START_ROOM

    def change_scene(self):
        return self.active_scene
