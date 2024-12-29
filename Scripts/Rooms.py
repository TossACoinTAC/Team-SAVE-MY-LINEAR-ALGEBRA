from pygame import *
from Statics import *
import random


def gen_rooms():
    pass


class Door(pygame.sprite.Sprite):
    # randomly select a door image if not specified
    random_image = random.choice(list(ImportedImages.DoorImages)).value

    def __init__(self, doorImage=random_image):
        super().__init__()
        self.image = pygame.image.load(doorImage)
        self.image = pygame.transform.scale(
            self.image,
            (PlayerSettings.playerWidth * 1.5, PlayerSettings.playerHeight * 1.5),
        )
        self.rect = self.image.get_rect()


class SingleRoom(pygame.sprite.Sprite):

    def gen_doors(self):
        # generate four random doors
        self.doors = pygame.sprite.Group()
        door_locations = [
            (self.rect.width / 2, ScreenSettings.marginHeight),  # top
            (ScreenSettings.marginWidth-20, self.rect.height / 2),  # left
            (self.rect.width / 2, ScreenSettings.roomHeight),  # bottom
            (ScreenSettings.roomWidth, self.rect.height / 2),  # right
        ]
        for i in range(4):
            door = Door()
            door.image = pygame.transform.rotate(door.image,90*i)
            door.rect.center = door_locations[i]
            # need to add rotations here
            self.doors.add(door)
        self.doors.draw(self.image)  # draw on the Room's frame
        

    # randomly select a room image if not specified
    random_image = random.choice(list(ImportedImages.RoomImages)).value

    def __init__(self, roomImage=random_image):
        super().__init__()
        self.image = pygame.image.load(roomImage)
        self.image = pygame.transform.scale(
            self.image, (ScreenSettings.screenWidth, ScreenSettings.screenHeight)
        )
        self.rect = self.image.get_rect()
        self.gen_doors()


class StartRoom(SingleRoom):
    def __init__(self):
        super().__init__(ImportedImages.RoomImages.START_ROOM.value)
