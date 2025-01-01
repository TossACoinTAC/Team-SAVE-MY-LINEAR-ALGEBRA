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
                # Determine the direction of collision and adjust position
                if (
                    self.rect.right > wall.rect.left
                    and self.rect.centerx < wall.rect.centerx
                ):
                    self.rect.right = wall.rect.left  # Hit wall on the left
                elif (
                    self.rect.left < wall.rect.right
                    and self.rect.centerx > wall.rect.centerx
                ):
                    self.rect.left = wall.rect.right  # Hit wall on the right
                if (
                    self.rect.bottom > wall.rect.top
                    and self.rect.centery < wall.rect.centery
                ):
                    self.rect.bottom = wall.rect.top  # Hit wall on top
                elif (
                    self.rect.top < wall.rect.bottom
                    and self.rect.centery > wall.rect.centery
                ):
                    self.rect.top = wall.rect.bottom  # Hit wall on bottom

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
