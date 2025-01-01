import pygame
from enum import Enum


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


class TearSettings:
    tearWidth = 30
    tearHeight = 30
    tearSpeed = 5


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


class ImportedImages:
    icon = "Src/icons/64x64.ico"

    # Player
    playerImage = "Src/Textures/Play/Issac_Loot.png"
    tearImage = "Src/Textures/Play/Tear.png"

    # Rooms
    class RoomImages(Enum):
        START_ROOM = "Src/Textures/Play/start_000.png"
        COMMON_ROOM = "Src/Textures/Play/room_001.png"

    class DoorImages(Enum):
        OPEN_DOOR = "Src/Textures/Play/OpenDoor.png"

    class ShitImages(Enum):
        TYPE_0 = "Src/Textures/Play/poops/poops (1).png"
        TYPE_1 = "Src/Textures/Play/poops/poops (2).png"
        TYPE_2 = "Src/Textures/Play/poops/poops (3).png"
        TYPE_3 = "Src/Textures/Play/poops/poops (4).png"
        TYPE_4 = "Src/Textures/Play/poops/poops (5).png"  # images not found

    # MainMenu
    BackGround = "Src/Textures/Title/Title1.png"
    StartButton = "Src/Textures/Title/Draw2.png"  # Not found
    Options = "Src/Textures/Title/Options.png"
    Continues = "Src/Textures/Title/Continue.png"
    Bomb = "Src/Textures/Play/pickup_016_bomb.png"
    Draw = "Src/Textures/Title/Draw1.png"

    # Enemies
    # Fly = "data/textures/enemies/fly_ok.png"
    # Fly_die = "data/textures/enemies/fly_rip.png"

    # Friendly_NPCs
    NPCImage = "Src/Textures/Play/Issac_Loot.png"  # test
    chatboxImage = "Src/Textures/Play/Issac_Loot.png"


class ImportedBGM:
    bgmpath = ["Src/sounds/main_theme.mp3", "Src/sounds/isaac_hurt1.mp3"]
