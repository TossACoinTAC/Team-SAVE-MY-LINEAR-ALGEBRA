import pygame
from enum import Enum


class Events:
    # Scene Changes
    MAIN_TO_STARTROOM = pygame.USEREVENT + 1
    TO_COMMONROOM = pygame.USEREVENT + 3
    TO_SHOP = pygame.USEREVENT + 5
    TO_TREASURE = pygame.USEREVENT + 7
    TO_SECRET = pygame.USEREVENT + 9
    TO_BLUEWOMB = pygame.USEREVENT + 11
    TO_CATACOMB = pygame.USEREVENT + 13

    TO_CHATBOX = pygame.USEREVENT + 19
    EXIT_CHATBOX = pygame.USEREVENT + 20

    # States
    GAME_OVER = pygame.USEREVENT + 21
    ROOM_CLEAR = pygame.USEREVENT + 22
    BOMB_EXPLOSION = pygame.USEREVENT + 23


class Scenes(Enum):
    MAIN_MENU = 0
    START_ROOM = 1
    COMMON_ROOM = 2
    SHOP = 3
    TREASURE = 4
    SECRET = 5
    BLUEWOMB = 6
    CATACOMB = 7
    CHAT_BOX = 11


# Files
class ImportedImages:
    icon = "Src/icons/64x64.ico"

    # Player
    playerImage = "Src/Textures/Play/Issac_Loot.png"
    tearImage = "Src/Textures/Play/Tear.png"
    tear_pop_Image = "data/textures/tears/tears_pop.png"
    BldtearImage = "Src/Textures/Play/Tear_002.png"
    heartImage = "Src/Textures/Play/Heart.png"
    BombImage = "Src/Textures/Play/bomb.png"
    ExplosionImage = "Src/Textures/Play/effect_029_explosion.png"

    # Rooms
    class RoomImages(Enum):
        START_ROOM = "Src/Textures/Map/start_000.png"
        COMMON_ROOM = "Src/Textures/Map/room_000.png"
        SHOP = "Src/Textures/Map/shop.png"
        TREASURE = "Src/Textures/Map/treasure.png"
        SECRET = "Src/Textures/Map/secret.png"
        BLUEWOMB = "Src/Textures/Map/bluewomb.png"
        CATACOMB = "Src/Textures/Map/catacomb.png"  # For Boss Room ?

    class OpenDoorImages(Enum):
        OPEN_WOOD_DOOR = "Src/Textures/Map/OpenWoodDoor.png"
        OPEN_SHOP_DOOR = "Src/Textures/Map/OpenShopDoor.png"
        OPEN_TREASURE_DOOR = "Src/Textures/Map/OpenTreasureDoor.png"
        OPEN_SECRET_DOOR = "Src/Textures/Map/OpenStoneDoor.png"
        OPEN_BLUEWOMB_DOOR = "Src/Textures/Map/OpenBlueWombDoor.png"
        OPEN_CATACOMB_DOOR = "Src/Textures/Map/OpenDevilDoor.png"

    class ClosedDoorImages(Enum):
        CLOSED_WOOD_DOOR = "Src/Textures/Map/ClosedWoodDoor.png"  # to common room
        CLOSED_SHOP_DOOR = "Src/Textures/Map/ClosedShopDoor.png"
        CLOSED_TREASURE_DOOR = "Src/Textures/Map/ClosedTreasureDoor.png"
        CLOSED_SECRET_DOOR = "Src/Textures/Map/ClosedStoneDoor.png"
        CLOSED_BLUEWOMB_DOOR = "Src/Textures/Map/ClosedBlueWombDoor.png"
        CLOSED_CATACOMB_DOOR = "Src/Textures/Map/ClosedDevilDoor.png"

    class ShitImages(Enum):
        TYPE_0 = "Src/Textures/Play/poops/poops (1).png"
        TYPE_1 = "Src/Textures/Play/poops/poops (2).png"
        TYPE_2 = "Src/Textures/Play/poops/poops (3).png"
        TYPE_3 = "Src/Textures/Play/poops/poops (4).png"
        TYPE_4 = "Src/Textures/Play/poops/poops (5).png"

    class BlockImage(Enum):
        Rock = "Data/Textures/Room/altars.png"

    # MainMenu
    BackGround = "Src/Textures/Title/Title1.png"
    StartButton = "Src/Textures/Title/Draw2.png"
    Options = "Src/Textures/Title/Options.png"
    Continues = "Src/Textures/Title/Continue.png"
    Bomb = "Src/Textures/Play/pickup_016_bomb.png"
    Draw = "Src/Textures/Title/Draw1.png"

    # Enemies
    Fly = "data/textures/enemies/fly_ok.png"
    Fly_die = "data/textures/enemies/fly_rip.png"

    # Friendly_NPCs
    NPCImage = "Src/Textures/Play/Issac_Loot.png"  # test
    chatboxImage = "Src/Textures/Play/Issac_Loot.png"


class ImportedBGM:
    main_theme = "Src/sounds/main_theme.mp3"
    walk = "Src/sounds/isaac_hurt1.mp3"
    shoot = "Src/sounds/pop1.wav"


# Settings
class ScreenSettings:
    screenWidth = 1280
    screenHeight = 720

    # distance between screen frame and room frame
    marginWidth = 150
    marginHeight = 50

    roomWidth = screenWidth - marginWidth
    roomHeight = screenHeight - marginHeight

    caption = "The Binding of Issac"
    fps = 60


class PlayerSettings:
    playerWidth = 65
    playerHeight = 90
    playerSpeed = 3
    PlayerAttackSpeed = 0.5
    PlayerHP = 6
    PlayerBuff = 0


class TearSettings:
    tearWidth = 100
    tearHeight = 100
    tearSpeed = 6
    tear_frame_rects = [
        (0, 0, 64, 64),
        (64, 0, 64, 64),
        (128, 0, 64, 64),
        (192, 0, 64, 64),
        (256, 0, 64, 64),
        (320, 0, 64, 64),
        (384, 0, 64, 64),
        (448, 0, 64, 64),
        (512, 0, 64, 64),
        (576, 0, 64, 64),
        (640, 0, 64, 64),
        (704, 0, 64, 64),
        (768, 0, 64, 64),
        (832, 0, 64, 64),
        (896, 0, 64, 64),
        (0, 64, 64, 64),
        (64, 64, 64, 64),
        (128, 64, 64, 64),
        (192, 64, 64, 64),
        (256, 64, 64, 64),
        (320, 64, 64, 64),
        (384, 64, 64, 64),
        (448, 64, 64, 64),
        (512, 64, 64, 64),
        (576, 64, 64, 64),
        (640, 64, 64, 64),
        (704, 64, 64, 64),
        (768, 64, 64, 64),
        (832, 64, 64, 64),
        (896, 64, 64, 64),
    ]

class BombSettings:
    bombWidth = 40
    bombHeight = 42
    bomb_frame_rects = [
        (0, 0, 40, 42),
        (40, 0, 40, 42),
        (80, 0, 40, 42),
    ]
    affect_radius = 100
    power = 3

class ExplosionSettings:
    explosionWidth = 96
    explosionHeight = 96
    explosion_frame_rects = []
    for i in range(4):
        for j in range(4):
            explosion_frame_rects.append((96 * j, 96 * i, 96, 96))

class MainMenuSettings:
    class StartButton:
        MULTI = 3.0
        ALPHA = 200
        x = 450
        y = 400

    class Options:
        MULTI = 1.5
        ALPHA = 180
        x = 420
        y = 500

    class Continue:
        MULTI = 1.5
        ALPHA = 180
        x = 680
        y = 550

    class Bomb:
        MULTI = 3.0
        ALPHA = 100
        x = 900
        y = 200
        frames_duration = 125
        frame_rects = [
            (69, 127, 21, 30),
            (101, 127, 21, 30),
            (133, 127, 21, 30),
            (69, 63, 21, 30),
            (133, 0, 21, 30),
        ]

    class Draw:
        MULTI = 3.0
        ALPHA = 0
        x = 400
        y = 100
        frames_duration = 125
        frame_rects = [(0, 0, 165, 156), (160, 0, 154, 156)]


class EnemiesSettings:
    class Fly:
        MULTI = 1.0
        ALPHA = 256
        x = 400
        y = 400
        frames_duration = 125
        frame_rects = [
            (7, 8, 42, 33),
            (71, 8, 42, 33),
            (134, 8, 42, 33),
            (197, 8, 42, 33),
        ]
        HP = 1
        speed = [1, 1, 5, -1, -1, -5]
        frame_rects_die = [
            (0, 0, 64, 63),
            (64, 0, 64, 63),
            (128, 0, 64, 63),
            (192, 0, 64, 63),
            (0, 63, 64, 63),
            (64, 63, 64, 63),
            (128, 63, 64, 63),
            (192, 63, 64, 63),
            (0, 126, 64, 63),
            (64, 126, 64, 63),
            (128, 126, 64, 63),
        ]
