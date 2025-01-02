from pygame import *
from Statics import *
from BGMPlayer import BgmPlayer
from Rooms import *


class Player(pygame.sprite.Sprite):
    def __init__(self, spawn_pos: Vector2):  # spawn_pos: for transportation
        super().__init__()
        self.image = pygame.image.load(ImportedImages.playerImage)
        self.image = pygame.transform.scale(
            self.image, (PlayerSettings.playerWidth, PlayerSettings.playerHeight)
        )
        self.rect = self.image.get_rect(center=spawn_pos)
        self.speed = PlayerSettings.playerSpeed
        self.bgm = BgmPlayer()

    def hit_walls(self, rooms):
        # boundaries can be changed to walls later
        # separate x and y , if not , press w and a simultaneously can escape
        if self.rect.top < ScreenSettings.marginHeight:
            self.rect.top = ScreenSettings.marginHeight
        elif self.rect.bottom > ScreenSettings.roomHeight:
            self.rect.bottom = ScreenSettings.roomHeight
        if self.rect.left < ScreenSettings.marginWidth:
            self.rect.left = ScreenSettings.marginWidth
        elif self.rect.right > ScreenSettings.roomWidth:
            self.rect.right = ScreenSettings.roomWidth

        self.walls = pygame.sprite.Group()
        for room in rooms:  # get all walls
            self.walls = room.walls

        # Check collision with walls
        for wall in self.walls:
            if self.rect.colliderect(wall.rect):
                dx = self.rect.centerx - wall.rect.centerx
                dy = self.rect.centery - wall.rect.centery
                if abs(dx) > abs(dy):  # Horizontal collision
                    if dx > 0:
                        self.rect.left = wall.rect.right  # Hit wall on the right
                    else:
                        self.rect.right = wall.rect.left  # Hit wall on the left
                else:  # Vertical collision
                    if dy > 0:
                        self.rect.top = wall.rect.bottom  # Hit wall on the bottom
                    else:
                        self.rect.bottom = wall.rect.top  # Hit wall on the top
                break

    def move(self, keys):
        if keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]:
            self.bgm.update("ISAAC_WALK", 0)
            movement = (
                self.speed
                * (keys[pygame.K_LSHIFT] + 1)  # press left shift to dash
                * Vector2(
                    keys[pygame.K_d] - keys[pygame.K_a],
                    keys[pygame.K_s] - keys[pygame.K_w],
                )
            )
            self.rect.move_ip(movement)

    def pooping(self):
        pass

    def update(self, keys, rooms):
        self.move(keys)
        self.hit_walls(rooms)
