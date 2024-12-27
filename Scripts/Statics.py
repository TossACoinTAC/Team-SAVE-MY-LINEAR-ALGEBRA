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


class ImportedImages:
    playerImage = "Src/Textures/Play/Issac_Loot.png"
    icon = "Src/icons/64x64.ico"

    class RoomImages(Enum):
        START_ROOM = "Src/Textures/Play/start_000.png"
        COMMON_ROOM = "Src/Textures/Play/room_001.png"

    class DoorImages(Enum):
        OPEN_DOOR = "Src/Textures/Play/OpenDoor.png"

class ImportedBGM:
    bgmpath = ["Src/sounds/main_theme.mp3","Src/sounds/isaac_hurt1.mp3"]