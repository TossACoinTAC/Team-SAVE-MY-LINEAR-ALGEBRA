import pygame
from Statics import Events, Scenes
from GameManagers.GameManager import GameManager


class EventListener(GameManager):
    def __init__(self):
        super().__init__()
        self.active_scene = Scenes.MAIN_MENU
        self.bgm_player.play("MAIN_THEME", -1)

    def listen(self):
        self.detect_collision(self.isaac)
        self.detect_collision(self.isaac.tears)
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    exit()
                case Events.MAIN_TO_STARTROOM:
                    self.active_scene = Scenes.START_ROOM
                    self.bgm_player.stop()
                    # self.bgm_player.play("STARTROOM", -1)    # need bgm here , can be a common bgm for all rooms

                case Events.WALL_COLLIDE:
                    event.dict["collider"].hit_wall = True

    def get_active_scene(self):
        return self.active_scene

    def detect_collision(self, other):
        for wall in self.room.walls:
            wall.detect_collision(other, Events.WALL_COLLIDE)
        for frame in self.room.frame:
            frame.detect_collision(other, Events.WALL_COLLIDE)
        for door in self.room.doors:
            door.detect_collision(other, Events.WALL_COLLIDE)
