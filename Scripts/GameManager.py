from pygame import *
from BGMPlayer import BGMPlayer
from Player import Player
from Rooms import *


class GameManager:
    def __init__(self):
        self.bgm_player = BGMPlayer()
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
