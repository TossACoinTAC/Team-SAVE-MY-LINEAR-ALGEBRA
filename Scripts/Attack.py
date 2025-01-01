from pygame import *
from Statics import *
from BGMPlayer import BgmPlayer
import pygame
from pygame.math import Vector2

class Bullet(pygame.sprite.Sprite):
    def __init__(self, spawn_pos: Vector2):
        super().__init__()
        self.image = pygame.image.load(ImportedImages.tearImage)
        self.image = pygame.transform.scale(
            self.image, (TearSettings.tearWidth, TearSettings.tearHeight)
        )
        self.rect = self.image.get_rect(center=spawn_pos)
        self.speed = TearSettings.tearSpeed
        self.direction = Vector2(0, 0)  # 初始没有方向

    def update(self):
        # 移动子弹
        self.rect.move_ip(self.direction * self.speed)

        # 检测是否碰到墙壁或边界
        if not ScreenSettings.marginWidth <= self.rect.left <= ScreenSettings.roomWidth or \
           not ScreenSettings.marginHeight <= self.rect.top <= ScreenSettings.roomHeight:
            self.kill()
        else:
            pass
            # 检测与墙体碰撞
            #if pygame.sprite.spritecollideany(self, walls_group):
            #    self.kill()

    def first_update(self, keys):
        # 根据键盘输入设置方向
        if keys[pygame.K_UP]:
            self.direction = Vector2(0, -1)  # 向上
        elif keys[pygame.K_DOWN]:
            self.direction = Vector2(0, 1)  # 向下
        elif keys[pygame.K_LEFT]:
            self.direction = Vector2(-1, 0)  # 向左
        elif keys[pygame.K_RIGHT]:
            self.direction = Vector2(1, 0)  # 向右
        
        self.update()

    
'''
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 0, 0))  # 红色墙体
        self.rect = self.image.get_rect(topleft=(x, y))

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    # 创建子弹组和墙壁组
    bullets = pygame.sprite.Group()
    walls = pygame.sprite.Group()

    # 创建一些墙壁
    walls.add(Wall(300, 200, 100, 20), Wall(500, 400, 20, 100))

    running = True
    while running:
        keys = pygame.key.get_pressed()  # 检测按键状态

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # 发射子弹
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    bullets.add(Bullet(Vector2(400, 300)))

        # 更新子弹
        bullets.update(keys, walls)

        # 绘制屏幕
        screen.fill((0, 0, 0))
        bullets.draw(screen)
        walls.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
'''