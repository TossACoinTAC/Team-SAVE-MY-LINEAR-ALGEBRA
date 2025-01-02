import pygame
from Statics import Events, Scenes


class EventListener:
    def __init__(self):
        self.active_scene = Scenes.MAIN_MENU

    def listen(self):
        quit = False
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    quit = True
                    break
                case Events.MAIN_TO_STARTROOM:
                    self.active_scene = Scenes.START_ROOM
        if quit:
            pygame.quit()
            exit()

    def change_scene(self):
        return self.active_scene
