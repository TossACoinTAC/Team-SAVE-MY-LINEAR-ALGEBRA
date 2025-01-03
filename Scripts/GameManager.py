from pygame import *
from BGMPlayer import *
from Player import Player
from Rooms import *


class GameManager:
    def __init__(self):
        self.bgm_player = BGMPlayer()
        self.playbgm = True
        self.isaac = pygame.sprite.GroupSingle()
        self.isaac.add(
            Player(
                spawn_pos=0.5
                * Vector2(ScreenSettings.screenWidth, ScreenSettings.screenHeight)
            )
        )

        self.rooms = pygame.sprite.Group()
        start_room = StartRoom()  # final:rooms=Rooms.gen_rooms()
        self.rooms.add(start_room)  # final:rooms.add(rooms)

    def update(self):
        # self.event_listener.listen()
        # self.active_scene = self.event_listener.change_scene()
        # self.screen_renderer.render_screen(self.active_scene)
        self.update_bgm()

    def update_bgm(self):
        if self.playbgm:
            self.bgm_player.play("MAIN_THEME", -1)
            self.playbgm = False
