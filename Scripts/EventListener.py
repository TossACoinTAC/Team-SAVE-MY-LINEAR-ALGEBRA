import pygame
from Statics import Events, Scenes
from GameManager import GameManager


class EventListener(GameManager):
    def __init__(self):
        super().__init__()
        self.active_scene = Scenes.MAIN_MENU

    def listen(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    exit()
                case Events.MAIN_TO_STARTROOM:
                    self.active_scene = Scenes.START_ROOM
                case Events.WALL_COLLIDE:
                    colliders = event.dict["collider"]  # collider sprite group

    def change_scene(self):
        return self.active_scene
