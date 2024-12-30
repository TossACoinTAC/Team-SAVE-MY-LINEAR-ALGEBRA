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
        mode = random.choice([1, 2, 3])  # 随机选择生成模式

        if mode == 1:
            # 模式一：在整个房间生成一整列一整列的墙体
            columns = random.randint(3, 6)  # 随机生成列数
            spacing = (ScreenSettings.roomWidth - ScreenSettings.marginWidth * 2) // columns
            for i in range(columns):
                x = ScreenSettings.marginWidth + i * spacing + spacing // 2
                for y in range(ScreenSettings.marginHeight, ScreenSettings.roomHeight, Shit(1).image.get_height()):  # 每列随机生成5个墙体
                    wall = Shit(1)
                    if y > ScreenSettings.marginHeight + Shit(1).image.get_height() and y < ScreenSettings.roomHeight - Shit(1).image.get_height():
                        wall.rect.center = (x, y)
                        self.walls.add(wall)

        elif mode == 2:
            # 模式二：在房间的四角生成单独的墙体，不紧挨着边框
            corner_offsets = [
                (ScreenSettings.marginWidth + 100, ScreenSettings.marginHeight + 100),
                (ScreenSettings.roomWidth - 100, ScreenSettings.marginHeight + 100),
                (ScreenSettings.marginWidth + 100, ScreenSettings.roomHeight - 100),
                (ScreenSettings.roomWidth - 100, ScreenSettings.roomHeight - 100),
            ]
            for offset in corner_offsets:
                wall = Shit(1)
                wall.rect.center = offset
                self.walls.add(wall)

        elif mode == 3:
            # 模式三：在房间的中心生成 5% 的墙体
            center_x = (ScreenSettings.marginWidth + ScreenSettings.roomWidth) // 2
            center_y = (ScreenSettings.marginHeight + ScreenSettings.roomHeight) // 2
            area_width = (ScreenSettings.roomWidth - ScreenSettings.marginWidth) * 0.1
            area_height = (ScreenSettings.roomHeight - ScreenSettings.marginHeight) * 0.1

            num_walls = max(1, int(area_width * area_height * 0.05))  # 至少生成 1 个墙体
            for _ in range(num_walls):
                randx = random.randint(center_x - int(area_width // 2), center_x + int(area_width // 2))
                randy = random.randint(center_y - int(area_height // 2), center_y + int(area_height // 2))
                wall = Shit(1)
                wall.rect.center = (randx, randy)
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
            self.image, (PlayerSettings.playerWidth*0.8, PlayerSettings.playerHeight*0.8)
        )
        self.rect = self.image.get_rect()

