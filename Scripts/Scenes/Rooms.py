from pygame import *
from Statics import *
import random


class SingleRoom(pygame.sprite.Sprite):
    def __init__(self, roomImage=None):
        super().__init__()
        # randomly select a room image if not specified
        if not roomImage:
            roomImage = random.choice(list(ImportedImages.RoomImages)).value
        self.image = pygame.image.load(roomImage)
        self.image = pygame.transform.scale(
            self.image, (ScreenSettings.screenWidth, ScreenSettings.screenHeight)
        )
        self.rect = self.image.get_rect()

        self._frame = pygame.sprite.Group()
        self.set_frame()
        self._walls = pygame.sprite.Group()
        self.gen_walls()
        self._doors = pygame.sprite.Group()
        self.gen_doors()

        self.roomImage = random.choice(
            list(ImportedImages.RoomImages)
        ).value  # random again for next initialization

    # property without setter
    def get_frame(self):
        return self._frame

    def get_walls(self):
        return self._walls

    def get_doors(self):
        return self._doors

    def set_frame(self):
        edge_thickness = 10
        self.top_edge = pygame.Rect(
            self.rect.left,
            self.rect.top + ScreenSettings.marginHeight,
            self.rect.width,
            edge_thickness,
        )
        self.bottom_edge = pygame.Rect(
            self.rect.left,
            self.rect.bottom - ScreenSettings.marginHeight,
            self.rect.width,
            edge_thickness,
        )
        self.left_edge = pygame.Rect(
            self.rect.left + ScreenSettings.marginWidth,
            self.rect.top,
            edge_thickness,
            self.rect.height,
        )
        self.right_edge = pygame.Rect(
            self.rect.right - ScreenSettings.marginWidth,
            self.rect.top,
            edge_thickness,
            self.rect.height,
        )
        edges = [self.top_edge, self.bottom_edge, self.left_edge, self.right_edge]
        for i in range(4):
            self._frame.add(Frame(edges[i]))

    def gen_doors(self):
        # generate four random doors
        door_locations = [
            (self.rect.width / 2, ScreenSettings.marginHeight + 10),  # top
            (ScreenSettings.marginWidth - 25, self.rect.height / 2),  # left
            (self.rect.width / 2, ScreenSettings.roomHeight - 10),  # bottom
            (ScreenSettings.roomWidth + 10, self.rect.height / 2),  # right
        ]
        door_location_tags = ["top", "left", "bottom", "right"]

        for i in range(4):
            door = Door(door_location_tags[i])
            door.image = pygame.transform.rotate(door.image, 90 * i)
            door.rect.center = door_locations[i]
            self._doors.add(door)
        self._doors.draw(self.image)  # draw on the Room's frame

    def gen_walls(self):
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
                ):
                    wall = Shit()
                    if (
                        y > ScreenSettings.marginHeight + Shit().image.get_height()
                        and y < ScreenSettings.roomHeight - Shit().image.get_height()
                    ):
                        wall.rect.center = (x, y)
                        self._walls.add(wall)

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
                self._walls.add(wall)

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
                    self._walls.add(wall)

        num_rocks = random.randint(1, 5)
        for _ in range(num_rocks):
            while True:
                x = random.randint(
                    ScreenSettings.marginWidth,
                    ScreenSettings.roomWidth - ScreenSettings.marginWidth,
                )
                y = random.randint(
                    ScreenSettings.marginHeight,
                    ScreenSettings.roomHeight - ScreenSettings.marginHeight,
                )
                rock = Rock()
                rock.rect.center = (x, y)

                if not any(wall.rect.colliderect(rock.rect) for wall in self._walls):
                    self._walls.add(rock)
                    break


class Door(pygame.sprite.Sprite):
    def __init__(self, location_tag: str, doorImage=None):
        super().__init__()
        # randomly select a door image if not specified
        if not doorImage:
            doorImage = random.choice(list(ImportedImages.ClosedDoorImages)).value
        self.image = pygame.image.load(doorImage)
        self.image = pygame.transform.scale(
            self.image,
            (PlayerSettings.playerWidth * 1.5, PlayerSettings.playerHeight * 1.3),
        )
        self.rect = self.image.get_rect()
        self.location_tag = location_tag
        self._is_open = True
        match doorImage:
            case ImportedImages.ClosedDoorImages.CLOSED_WOOD_DOOR.value:
                self.type_tag = "Wood"
            case ImportedImages.ClosedDoorImages.CLOSED_SHOP_DOOR.value:
                self.type_tag = "Shop"
            case ImportedImages.ClosedDoorImages.CLOSED_TREASURE_DOOR.value:
                self.type_tag = "Treasure"
            case ImportedImages.ClosedDoorImages.CLOSED_SECRET_DOOR.value:
                self.type_tag = "Secret"
            case ImportedImages.ClosedDoorImages.CLOSED_BLUEWOMB_DOOR.value:
                self.type_tag = "BlueWomb"
            case ImportedImages.ClosedDoorImages.CLOSED_CATACOMB_DOOR.value:
                self.type_tag = "Catacomb"

    @property
    def is_open(self):
        return self._is_open

    @is_open.setter
    def is_open(self, value: bool):
        self._is_open = value


class Frame(pygame.sprite.Sprite):
    def __init__(self, rect: pygame.Rect):
        super().__init__()
        self.rect = rect


class Wall(pygame.sprite.Sprite):
    def __init__(self, wall_image):
        super().__init__()
        self.image = wall_image
        self.image = pygame.transform.scale(
            self.image,
            (PlayerSettings.playerWidth * 0.8, PlayerSettings.playerHeight * 0.8),
        )
        self.rect = self.image.get_rect()


class Shit(Wall):
    def __init__(self):
        shit_image = pygame.image.load(ImportedImages.ShitImages["TYPE_0"].value)
        self.HP = 50
        super().__init__(shit_image)

    def destroyed(self):
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


class Block(Wall):
    def __init__(self, block_image):
        super().__init__(block_image)


def divide_image(img):
    image_width, image_height = img.get_size()
    part_width = image_width // 3
    elements = []
    for i in range(3):
        rect = pygame.Rect(i * part_width, 0, part_width, image_height)
        part = img.subsurface(rect).copy()
        elements.append(part)
    return elements


class Rock(Block):
    def __init__(self):
        self.image = divide_image(
            pygame.image.load(ImportedImages.BlockImage.Rock.value)
        )[0]
        super().__init__(self.image)


class Black_Treasure_Box(Block):
    def __init__(self):
        self.image = divide_image(
            pygame.image.load(ImportedImages.BlockImage.Rock.value)
        )[1]
        super().__init__(self.image)


class Gold_Treasure_Box(Block):
    def __init__(self):
        self.image = divide_image(
            pygame.image.load(ImportedImages.BlockImage.Rock.value)
        )[2]
        super().__init__(self.image)


class StartRoom(SingleRoom):
    def __init__(self):
        super().__init__(ImportedImages.RoomImages.START_ROOM.value)


class Shop(SingleRoom):
    def __init__(self):
        super().__init__(ImportedImages.RoomImages.SHOP.value)


class TreasureRoom(SingleRoom):
    def __init__(self):
        super().__init__(ImportedImages.RoomImages.TREASURE.value)


class SecretRoom(SingleRoom):
    def __init__(self):
        super().__init__(ImportedImages.RoomImages.SECRET.value)


class BlueWomb(SingleRoom):
    def __init__(self):
        super().__init__(ImportedImages.RoomImages.BLUEWOMB.value)


class BossRoom(SingleRoom):
    def __init__(self):
        super().__init__(ImportedImages.RoomImages.CATACOMB.value)
