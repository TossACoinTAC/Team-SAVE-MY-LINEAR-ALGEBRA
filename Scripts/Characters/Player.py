from pygame import *
from Statics import *
from TmpTools.tools import *
from GameManagers.BGMPlayer import BGMPlayer


class Player(pygame.sprite.Sprite):
    def __init__(self, spawn_pos: Vector2):  # spawn_pos: for transportation
        super().__init__()
        self.image = pygame.image.load(ImportedImages.playerImage)
        self.image = pygame.transform.scale(
            self.image, (PlayerSettings.playerWidth, PlayerSettings.playerHeight)
        )
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
        self.heart = pygame.sprite.GroupSingle()
        self.heart.add(Heart())

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
                self.bgm_player.play("ISAAC_WALK", 0)
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
                self.bgm_player.play("ISAAC_SHOOT", 0)
            except ValueError:
                shooted_tear.direction = Vector2(0, 0)

            self.tear_ready.add(shooted_tear)
            self._tears.add(shooted_tear)

            self.shoot_timer = pygame.time.get_ticks()
        if pygame.time.get_ticks() - self.shoot_timer > self.shoot_delay:
            self.tear_ready.empty()

    def pooping(self):
        pass

    def update(self, keys):
        self.move(keys)
        self.shoot(keys)
        self._tears.update()


class Heart(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frame = []
        self.frame_index = 0
        self.frame_rects = PlayerSettings.heart_frame_rects
        self.sheet = pygame.image.load(ImportedImages.heartImage)
        for i in range(len(self.frame_rects)):
            tmp_image = get_images(self.sheet, *self.frame_rects[i], (0, 0, 0), 3.0)
            self.frame.append(
                pygame.transform.scale(
                    tmp_image, (PlayerSettings.heartWidth, PlayerSettings.heartHeight)
                )
            )
        self.image = self.frame[0]
        self.rect = self.image.get_rect()
        self.rect.x = ScreenSettings.marginWidth
        self.rect.y = ScreenSettings.marginHeight
        self.HP = PlayerSettings.PlayerHP
        self.timer = 0

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.timer > 1000:
            self.HP -= 1
            self.timer = current_time

        if self.HP == 0:

            event.post(event.Event(Events.GAME_OVER))
            # 触发事件游戏结束
        self.image = self.frame[6 - self.HP]


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
                self.sheet, *self.frame_rects[i + 1 * 15], (0, 0, 0), 3.0
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
