import pygame
from Statics import *

class StaticState(pygame.sprite.Sprite):
    def __init__(self, importImage, x, y, MULTI, ALPHA):
        super().__init__()
        self.image = pygame.image.load(importImage)
        self.image.set_alpha(ALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image = pygame.transform.scale(self.image, (int(self.rect.width * MULTI), int(self.rect.height * MULTI)))
    def update(self):
        pass

class coin(StaticState):
    def __init__(self):
        super().__init__(
            ImportedImages.UI.coin,
            UISettings.coin.x,
            UISettings.coin.y,
            UISettings.coin.MULTI,
            UISettings.coin.ALPHA)
        self.coin_num = 0
    def update(self, screen):
        fonts = pygame.font.Font('Src/fonts/IsaacGame.ttf', 48) #"Src/fonts/prices.psd"
        coin_text = fonts.render(f"{self.coin_num}", True, (225, 225, 225))
        screen.blit(coin_text, (UISettings.coin.x + 45, UISettings.coin.y + 10))


class attack(StaticState):
    def __init__(self):
        super().__init__(
            ImportedImages.UI.attack,
            UISettings.attack.x,
            UISettings.attack.y,
            UISettings.attack.MULTI,
            UISettings.attack.ALPHA)
        self.attack_num = 1
    def update(self, screen):
        fonts = pygame.font.Font('Src/fonts/IsaacGame.ttf', 48) #"Src/fonts/prices.psd"
        attack_text = fonts.render(f"{self.attack_num}", True, (225, 225, 225))
        screen.blit(attack_text, (UISettings.attack.x + 55, UISettings.attack.y + 10))
