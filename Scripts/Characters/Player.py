from pygame import *
from Statics import *
from TmpTools.tools import *
from GameManagers.BGMPlayer import BGMPlayer
import pygame.event as ev


class Player(pygame.sprite.Sprite):
    def __init__(self, spawn_pos: Vector2):  # spawn_pos: for transportation
        super().__init__()
        self.set_animation()
        self.attack = 1
        

        self.rect = self.image.get_rect(center=spawn_pos)

        self.speed = PlayerSettings.playerSpeed
        self.movement = Vector2(0, 0)

        self.tear_ready = pygame.sprite.GroupSingle()
        self._tears = pygame.sprite.Group()

        self.shoot_timer = 0
        self.shoot_delay = 200

        self.bgm_player = BGMPlayer()
        self.move_sound_timer = 0
        self.move_sound_delay = 600
        self.move_sound_played = False

        # resource system : HP
        # self.heart = pygame.sprite.GroupSingle()
        # self.heart.add(Heart())

        # planting bomb
        self.bomb_group = pygame.sprite.GroupSingle()
        self.explosion_group = pygame.sprite.GroupSingle()

    def set_animation(self):

        self.timer = 0
        self.frame_index = 0
        m = PlayerSettings.MULTI
        sheet = pygame.image.load(ImportedImages.playerImage)


        #set_head_animation
        self.head_frames = []
        self.head_frames_rects = PlayerSettings.head_frame_rects
        for i in range(len(PlayerSettings.head_frame_rects)):
            self.head_frames.append(StaticMethods.get_images(sheet, *self.head_frames_rects[i], (0, 0, 0), m))
        
        #set_body_animation
        self.body_right_frames = []
        self.body_right_frames_rects = PlayerSettings.body_right_frame_rects
        for i in range(len(PlayerSettings.body_right_frame_rects)):
            self.body_right_frames.append(StaticMethods.get_images(sheet, *self.body_right_frames_rects[i], (0, 0, 0), m))
        
        self.body_left_frames = []
        self.body_left_frames_rects = PlayerSettings.body_left_frame_rects
        for i in range(len(PlayerSettings.body_left_frame_rects)):
            self.body_left_frames.append(StaticMethods.get_images(sheet, *self.body_left_frames_rects[i], (0, 0, 0), m))
        
        self.body_up_frames = []
        self.body_up_frames_rects = PlayerSettings.body_up_frame_rects
        for i in range(len(PlayerSettings.body_up_frame_rects)):
            self.body_up_frames.append(StaticMethods.get_images(sheet, *self.body_up_frames_rects[i], (0, 0, 0), m))
        
        self.body_down_frames = []
        self.body_down_frames_rects = PlayerSettings.body_down_frame_rects
        for i in range(len(PlayerSettings.body_down_frame_rects)):
            self.body_down_frames.append(StaticMethods.get_images(sheet, *self.body_down_frames_rects[i], (0, 0, 0), m))

        m = PlayerSettings.MULTI
        head_height = self.head_frames_rects[0][3] * m
        dx = (self.head_frames_rects[0][2] - self.body_down_frames_rects[0][2]) * m // 2
        complete_width = self.head_frames_rects[0][2] * m
        complete_height = (self.head_frames_rects[0][3] + self.body_down_frames_rects[0][3]) * m
        complete_image = Surface((complete_width, complete_height), SRCALPHA) 
        complete_image.blit(self.body_down_frames[self.frame_index], (dx, head_height - 10))
        complete_image.blit(self.head_frames[0], (0, 0))
        self.image = complete_image


    def update_animation(self, keys):


        m = PlayerSettings.MULTI
        head_height = self.head_frames_rects[0][3] * m
        dx = (self.head_frames_rects[0][2] - self.body_down_frames_rects[0][2]) * m // 2
        complete_width = self.head_frames_rects[0][2] * m
        complete_height = (self.head_frames_rects[0][3] + self.body_down_frames_rects[0][3]) * m
        
        current_time = time.get_ticks()
        if self.timer == 0:
            self.timer = current_time
        elif current_time - self.timer > 125:
            self.timer = current_time
            self.frame_index += 1
            self.frame_index %= 10


        if keys[K_s]:
            complete_image = Surface((complete_width, complete_height), SRCALPHA) 
            complete_image.blit(self.body_down_frames[self.frame_index], (dx, head_height - 10))
            complete_image.blit(self.head_frames[0], (0, 0))
            self.image = complete_image
            
        if keys[K_d]:
            complete_image = Surface((complete_width, complete_height), SRCALPHA) 
            complete_image.blit(self.body_right_frames[self.frame_index], (dx, head_height - 10))
            complete_image.blit(self.head_frames[1], (0, 0))
            self.image = complete_image
         
        if keys[K_a]:
            complete_image = Surface((complete_width, complete_height), SRCALPHA) 
            complete_image.blit(self.body_left_frames[self.frame_index], (dx, head_height - 10))
            complete_image.blit(self.head_frames[2], (0, 0))
            self.image = complete_image
           
        if keys[K_w]:
            complete_image = Surface((complete_width, complete_height), SRCALPHA) 
            complete_image.blit(self.body_up_frames[self.frame_index], (dx, head_height - 10))
            complete_image.blit(self.head_frames[3], (0, 0))
            self.image = complete_image

    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    @property
    def tears(self):
        return self._tears

    @tears.setter
    def tears(self, value):
        pass  # don't need a setter

    def move(self, keys):

        if keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]:
            # move
            try:
                self.movement = (
                    self.speed
                    * (keys[pygame.K_LSHIFT] + 1)  # press left shift to dash
                    * Vector2(
                        keys[pygame.K_d] - keys[pygame.K_a],
                        keys[pygame.K_s] - keys[pygame.K_w],
                    ).normalize()
                )
            except ValueError:
                self.movement = Vector2(0, 0)
            self.rect.move_ip(self.movement)

            # deal with sound
            if not self.move_sound_played:
                #self.bgm_player.play("ISAAC_WALK", 0)
                self.move_sound_timer = pygame.time.get_ticks()
                self.move_sound_played = True
            if pygame.time.get_ticks() - self.move_sound_timer > self.move_sound_delay:
                self.move_sound_played = False

    def shoot(self, keys):
        if (
            (
                keys[pygame.K_UP]
                or keys[pygame.K_DOWN]
                or keys[pygame.K_LEFT]
                or keys[pygame.K_RIGHT]
            )
            # group's sprite list is empty
            and not self.tear_ready.sprites()
        ):
            # shoot
            shooted_tear = Tear(self.rect.center)
            try:
                shooted_tear.direction = Vector2(
                    keys[pygame.K_RIGHT] - keys[pygame.K_LEFT],
                    keys[pygame.K_DOWN] - keys[pygame.K_UP],
                ).normalize()
                #self.bgm_player.play("ISAAC_SHOOT", 0)
            except ValueError:
                shooted_tear.direction = Vector2(0, 0)

            self.tear_ready.add(shooted_tear)
            self._tears.add(shooted_tear)

            self.shoot_timer = pygame.time.get_ticks()
        if pygame.time.get_ticks() - self.shoot_timer > self.shoot_delay:
            self.tear_ready.empty()

    def triple_shoot(self, keys):
        if (
            keys[pygame.K_UP]
            or keys[pygame.K_DOWN]
            or keys[pygame.K_LEFT]
            or keys[pygame.K_RIGHT]
        ) and not self.tear_ready.sprites():
            directions = []
            if keys[pygame.K_UP]:
                directions = [Vector2(0, -1), Vector2(-1, -1), Vector2(1, -1)]
            elif keys[pygame.K_DOWN]:
                directions = [Vector2(0, 1), Vector2(-1, 1), Vector2(1, 1)]
            elif keys[pygame.K_LEFT]:
                directions = [Vector2(-1, 0), Vector2(-1, -1), Vector2(-1, 1)]
            elif keys[pygame.K_RIGHT]:
                directions = [Vector2(1, 0), Vector2(1, -1), Vector2(1, 1)]

            for direction in directions:
                shooted_tear = Tear(self.rect.center)
                try:
                    shooted_tear.direction = direction.normalize()
                except ValueError:
                    shooted_tear.direction = Vector2(0, 0)
                self.tear_ready.add(shooted_tear)
                self._tears.add(shooted_tear)

            self.shoot_timer = pygame.time.get_ticks()
        if pygame.time.get_ticks() - self.shoot_timer > self.shoot_delay:
            self.tear_ready.empty()

    def planting(self, keys):  # plant the bomb
        if keys[pygame.K_e] and not self.bomb_group.sprites():
            new_bomb = Bomb(self.rect.center)
            self.bomb_group.add(new_bomb)
            new_explosion = Explosion(self.rect.center)
            self.explosion_group.add(new_explosion)

    def update(self, keys):
        self.move(keys)
        self.triple_shoot(keys)
        self.planting(keys)
        self._tears.update()

        self.bomb_group.update()
        self.explosion_group.update()
        self.update_animation(keys)


# class Heart(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()
#         self.frame = []
#         self.frame_index = 0
#         self.frame_rects = PlayerSettings.heart_frame_rects
#         self.sheet = pygame.image.load(ImportedImages.heartImage)
#         for i in range(len(self.frame_rects)):
#             tmp_image = get_images(self.sheet, *self.frame_rects[i], (0, 0, 0), 3.0)
#             self.frame.append(
#                 pygame.transform.scale(
#                     tmp_image, (PlayerSettings.heartWidth, PlayerSettings.heartHeight)
#                 )
#             )
#         self.image = self.frame[0]
#         self.rect = self.image.get_rect()
#         self.rect.x = ScreenSettings.marginWidth
#         self.rect.y = ScreenSettings.marginHeight
#         self.HP = PlayerSettings.PlayerHP
#         self.timer = 0

#     def update(self):
#         current_time = pygame.time.get_ticks()
#         if current_time - self.timer > 1000:
#             self.HP -= 1
#             self.timer = current_time

#         if self.HP == 0:

#             event.post(event.Event(Events.GAME_OVER))
#             # 触发事件游戏结束
#         self.image = self.frame[6 - self.HP]


class Tear(pygame.sprite.Sprite):
    def __init__(self, spawn_pos: Vector2, Bloody=False):
        super().__init__()
        self.set_die_animation(Bloody)
        self.image = self.frame[0]
        self.image = pygame.transform.scale(
            self.image, (TearSettings.tearWidth, TearSettings.tearHeight)
        )
        self.rect = self.image.get_rect(center=spawn_pos)
        self.speed = TearSettings.tearSpeed
        self._direction = Vector2(0, 0)

    def set_die_animation(self, Type: bool):
        self.timer = 0
        self.state = "live"
        self.frame = []
        self.frame_index = 0
        self.frame_rects = TearSettings.tear_frame_rects
        self.sheet = pygame.image.load(ImportedImages.tear_pop_Image)
        for i in range(15):
            tmp_image = get_images(
                self.sheet, *self.frame_rects[i + Type * 15], (0, 0, 0), 3.0
            )
            self.frame.append(
                pygame.transform.scale(
                    tmp_image, (TearSettings.tearWidth, TearSettings.tearHeight)
                )
            )

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value: Vector2):
        self._direction = value

    def update(self):
        self.rect.move_ip(self.direction * self.speed)
        if self._direction == Vector2(0, 0):
            self.kill()
        if self.state == "die":
            self.speed = 0
            self.update_animation()

    def update_animation(self):

        self.image = self.frame[self.frame_index]

        current_time = pygame.time.get_ticks()
        if current_time - self.timer > 125:
            self.timer = current_time
            self.frame_index += 1

        if self.frame_index >= 14:
            self.kill()


class Bloody_Tear(Tear):
    def __init__(self):
        super().__init__(ImportedImages.BldtearImage)


class Bomb(pygame.sprite.Sprite):
    def __init__(self, spawn_pos: Vector2):
        super().__init__()
        self.frame_rects = BombSettings.bomb_frame_rects
        self.sheet = pygame.image.load(ImportedImages.BombImage)
        self.frame = []
        for i in range(3):
            tmp_image = get_images(self.sheet, *self.frame_rects[i], (0, 0, 0), 3.0)
            self.frame.append(
                pygame.transform.scale(
                    tmp_image, (BombSettings.bombWidth, BombSettings.bombHeight)
                )
            )
        self.image = self.frame[0]
        self.rect = self.image.get_rect(center=spawn_pos)
        self.bgm_player = BGMPlayer()
        
        self.radius = BombSettings.affect_radius  # 伤害半径
        self.power = BombSettings.power  # 伤害值

        self.timer = 0
        self.frame_index = 0
        self.flicker_timer = 0

    def explode_animation(self):
        self.image = self.frame[self.frame_index]
        current_time = pygame.time.get_ticks()
        if current_time - self.timer > 100:
            self.timer = current_time
            self.frame_index = (self.frame_index + 1) % 3
            self.flicker_timer += 1

        if self.flicker_timer >= 9:
            self.bgm_player.play("BOMB_EXPLODE", 0)
            ev.post(
                ev.Event(
                    Events.BOMB_EXPLOSION,
                    {
                        "pos": self.rect.center,
                        "radius": self.radius,
                        "power": self.power,
                    },
                )
            )
            self.kill()

    def update(self):
        self.explode_animation()


class Explosion(pygame.sprite.Sprite):  # just act as an animation
    def __init__(self, spawn_pos: Vector2):
        super().__init__()
        self.frame_rects = ExplosionSettings.explosion_frame_rects
        self.sheet = pygame.image.load(ImportedImages.ExplosionImage)
        self.frame = []
        for i in range(16):
            tmp_image = get_images(self.sheet, *self.frame_rects[i], (0, 0, 0), 3.0)
            self.frame.append(
                pygame.transform.scale(
                    tmp_image,
                    (
                        ExplosionSettings.explosionWidth,
                        ExplosionSettings.explosionHeight,
                    ),
                )
            )
        self.image = self.frame[8]
        self.rect = self.image.get_rect(center=spawn_pos)

        self.timer = 0
        self.frame_index = 8

    def explode_animation(self):
        self.image = self.frame[self.frame_index]
        current_time = pygame.time.get_ticks()
        if current_time - self.timer > 200:
            self.timer = current_time
            self.frame_index = (self.frame_index + 1) % 16

        if self.frame_index == 7:
            self.kill()

    def update(self):
        self.explode_animation()
