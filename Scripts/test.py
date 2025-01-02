import pygame
import time


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)
        self.bullets = pygame.sprite.Group()
        self.last_shot_time = 0
        self.attack_speed = 0.5  # 每秒发射2发子弹（攻击间隔为0.5秒）

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        current_time = time.time()
        if current_time - self.last_shot_time >= self.attack_speed:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            self.bullets.add(bullet)
            self.last_shot_time = current_time


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 5

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()


pygame.init()
screen = pygame.display.set_mode((800, 600))
player = Player()
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    player.update()
    player.bullets.update()
    screen.fill((0, 0, 0))
    screen.blit(player.image, player.rect)
    player.bullets.draw(screen)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()