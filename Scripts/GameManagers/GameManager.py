from pygame import *
from GameManagers.BGMPlayer import BGMPlayer
from Characters.Player import Player
from Characters.NPC import *
from Characters.Enemies import *
from Scenes.Rooms import *
from Scenes.MainMenu import MainMenu


class GameManager:
    def __init__(self):

        self.bgm_player = BGMPlayer()

        self.isaac_group = pygame.sprite.GroupSingle()
        self.isaac = Player(
            spawn_pos=0.5
            * Vector2(ScreenSettings.screenWidth, ScreenSettings.screenHeight)
        )
        self.isaac_group.add(self.isaac)

        self.main_menu: pygame.sprite.Group = MainMenu()

        self.room_group = pygame.sprite.GroupSingle()
        self.room = StartRoom()
        self.room_group.add(self.room)

        self.enemy_group = pygame.sprite.Group()
        self.npc_group = pygame.sprite.Group()

    # just an alias
    def get_keys(self):
        return pygame.key.get_pressed()
