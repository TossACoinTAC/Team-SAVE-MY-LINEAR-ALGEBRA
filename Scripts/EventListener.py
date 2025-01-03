import pygame
from Statics import Events, Scenes
from GameManager import GameManager


class EventListener(GameManager):
    def __init__(self):
        super().__init__()
        self.active_scene = Scenes.MAIN_MENU
        self.bgm_player.play("MAIN_THEME", -1)

    def listen(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    exit()
                case Events.MAIN_TO_STARTROOM:
                    self.active_scene = Scenes.START_ROOM
                    self.bgm_player.stop()
                    # self.bgm_player.play("STARTROOM", -1)     need bgm here

                case Events.WALL_COLLIDE:
                    colliders = event.dict["collider"]  # collider sprite group

    def get_active_scene(self):
        return self.active_scene
