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
        self.gen_walls()
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
    
    def gen_walls(self):
        self.walls = pygame.sprite.Group()
        wall_number = random.randint(1,8)
        for _ in range(wall_number):
            wall = Shit(1)    # can be changed to other types of walls
            randx = random.randint(ScreenSettings.marginWidth,ScreenSettings.roomWidth)
            randy = random.randint(ScreenSettings.marginHeight,ScreenSettings.roomHeight)
            wall_location = (randx,randy)
            wall.rect.center = wall_location
            self.walls.add(wall)
        self.walls.draw(self.image)  # draw on the Room's frame
        
        


class StartRoom(SingleRoom):
    def __init__(self):
        super().__init__(ImportedImages.RoomImages.START_ROOM.value)


class Wall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
    


class Shit(Wall):
    def __init__(self, type):
        super().__init__()
        self.image = pygame.image.load(ImportedImages.ShitImages.shit[0])
        self.image = pygame.transform.scale(
            self.image, (PlayerSettings.playerWidth, PlayerSettings.playerHeight)
        )
        self.rect = self.image.get_rect()

