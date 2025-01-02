from pygame import *
from Statics import *
import random


def gen_rooms():
    pass


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
            (ScreenSettings.marginWidth - 40, self.rect.height / 2),  # left
            (self.rect.width / 2, ScreenSettings.roomHeight),  # bottom
            (ScreenSettings.roomWidth, self.rect.height / 2),  # right
        ]
        for i in range(4):
            door = Door()
            door.image = pygame.transform.rotate(door.image, 90 * i)
            door.rect.center = door_locations[i]
            self.doors.add(door)
        self.doors.draw(self.image)  # draw on the Room's frame

    def gen_walls(self):
        self.walls = pygame.sprite.Group()
        mode = random.choice([1, 2, 3])  # 随机选择生成模式

        if mode == 1:
            # 模式一：在整个房间生成一整列一整列的墙体
            columns = random.randint(3, 6)  # 随机生成列数
            spacing = (
                ScreenSettings.roomWidth - ScreenSettings.marginWidth * 2
            ) // columns
            for i in range(columns):
                x = ScreenSettings.marginWidth + i * spacing + spacing // 2
                for y in range(
                    ScreenSettings.marginHeight,
                    ScreenSettings.roomHeight,
                    Shit().image.get_height(),
                ):  # 每列随机生成5个墙体
                    wall = Shit()
                    if (
                        y > ScreenSettings.marginHeight + Shit().image.get_height()
                        and y < ScreenSettings.roomHeight - Shit().image.get_height()
                    ):
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
                wall = Shit()
                wall.rect.center = offset
                self.walls.add(wall)

        elif mode == 3:
            # 模式三：在房间的中心生成 4x4 的墙体
            center_x = (ScreenSettings.marginWidth + ScreenSettings.roomWidth) // 2
            center_y = (ScreenSettings.marginHeight + ScreenSettings.roomHeight) // 2
            wall_width = Shit().image.get_width()
            wall_height = Shit().image.get_height()

            start_x = center_x - (wall_width * 2.5)
            start_y = center_y - (wall_height * 2.5)

            for i in range(4):
                for j in range(4):
                    wall = Shit()
                    wall.rect.center = (
                        start_x + i * wall_width,
                        start_y + j * wall_height,
                    )
                    self.walls.add(wall)
        self.walls.draw(self.image)  # draw on the Room's frame

    def update_walls(self, bullet):
        for wall in self.walls:
            if isinstance(wall, Shit):
                wall.destroyed(bullet, self.image)
        self.walls.draw(self.image)


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


class Wall(pygame.sprite.Sprite):
    def __init__(self, wall_image):
        super().__init__()
        self.image = pygame.image.load(wall_image)
        self.image = pygame.transform.scale(
            self.image,
            (PlayerSettings.playerWidth * 0.8, PlayerSettings.playerHeight * 0.8),
        )
        self.rect = self.image.get_rect()


class Shit(Wall):
    def __init__(self):
        shit_image = ImportedImages.ShitImages["TYPE_0"].value
        self.HP = 25
        super().__init__(shit_image)

    def destroyed(self, bullet, img):
        if pygame.sprite.spritecollide(self, bullet, True):
            self.HP -= 1
            if self.HP <= 0:
                self.kill()
            else:
                new_image_key = f"TYPE_{int((50 - self.HP)/10)}"
                # pygame.draw.rect(img, (0, 0, 0, 0), self.rect)  # 用黑色覆盖旧位置
                self.image = pygame.image.load(
                    ImportedImages.ShitImages[new_image_key].value
                )
                self.image = pygame.transform.scale(
                    self.image,
                    (
                        PlayerSettings.playerWidth * 0.8,
                        PlayerSettings.playerHeight * 0.8,
                    ),
                )
                self.rect = self.image.get_rect(center=self.rect.center)


class StartRoom(SingleRoom):
    def __init__(self):
        super().__init__(ImportedImages.RoomImages.START_ROOM.value)


class Shop(SingleRoom):
    def __init__(self):
        super().__init__(ImportedImages.RoomImages.SHOP.value)
