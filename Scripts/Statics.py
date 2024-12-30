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


class ImportedImages:
    playerImage = "Src/Textures/Play/Issac_Loot.png"
    icon = "Src/icons/64x64.ico"

    class RoomImages(Enum):
        START_ROOM = "Src/Textures/Play/start_000.png"
        COMMON_ROOM = "Src/Textures/Play/room_001.png"

    class DoorImages(Enum):
        OPEN_DOOR = "Src/Textures/Play/OpenDoor.png"

    class MainMenuImages:
        BackGround = "Src/Textures/Title/Title1.png"
        StartButton = "Src/Textures/Title/Draw2.png"
        Options = "Src/Textures/Title/Options.png"
        Continues = "Src/Textures/Title/Continue.png"
        Bomb = "Src/Textures/Play/pickup_016_bomb.png"
        Draw = "Src/Textures/Title/Draw1.png"


class ImportedBGM:
    bgmpath = ["Src/sounds/main_theme.mp3", "Src/sounds/isaac_hurt1.mp3"]
