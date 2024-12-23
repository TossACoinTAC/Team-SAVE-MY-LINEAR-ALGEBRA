import pygame
import numpy as np
from GameManager import GameManager


class player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/images/isaac.png")
        self.rect = self.image.get_rect(bottomright=(200, 520))
        self.velocity = 200

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]:
            movement = (
                self.velocity
                * (keys[pygame.K_LSHIFT] + 1)  # press left shift to dash
                * GameManager.get_deltatime()
                * np.array(
                    [
                        keys[pygame.K_d] - keys[pygame.K_a],
                        keys[pygame.K_s] - keys[pygame.K_w],
                    ]
                )
            )
            self.rect.move_ip(movement)
