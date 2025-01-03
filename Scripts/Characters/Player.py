from pygame import *
from Statics import *
from GameManagers.BGMPlayer import BGMPlayer


class CanHitWalls(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self._hit_wall = False

    @property
    def hit_wall(self):
        return self._hit_wall

    @hit_wall.setter
    def hit_wall(self, value: bool):
        self._hit_wall = value


class Player(CanHitWalls):
    def __init__(self, spawn_pos: Vector2):  # spawn_pos: for transportation
        super().__init__()
        self.image = pygame.image.load(ImportedImages.playerImage)
        self.image = pygame.transform.scale(
            self.image, (PlayerSettings.playerWidth, PlayerSettings.playerHeight)
        )
        self.rect = self.image.get_rect(center=spawn_pos)
        self._speed = PlayerSettings.playerSpeed
        self.tear_ready = pygame.sprite.GroupSingle()
        self._tears = pygame.sprite.Group()
        self.shoot_timer = 0
        self.move_sound_timer = 0
        self.move_sound_played = False
        self.delay = 200
        self.bgm = BGMPlayer()

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value: int):
        self._speed = value

    @property
    def tears(self):
        return self._tears

    @tears.setter
    def tears(self, value):
        pass  # don't need a setter

    def move(self, keys):

        # hit_wall detection
        self._speed = 0 if self._hit_wall else PlayerSettings.playerSpeed

        # move
        if keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]:
            try:
                movement = (
                    self._speed
                    * (keys[pygame.K_LSHIFT] + 1)  # press left shift to dash
                    * Vector2(
                        keys[pygame.K_d] - keys[pygame.K_a],
                        keys[pygame.K_s] - keys[pygame.K_w],
                    ).normalize()
                )
            except ValueError:
                movement = Vector2(0, 0)
            self.rect.move_ip(movement)

            # deal with sound
            if not self.move_sound_played:
                self.bgm.play("ISAAC_WALK", 0)
                self.move_sound_played = True
                self.move_sound_timer = pygame.time.get_ticks()
            if pygame.time.get_ticks() - self.move_sound_timer > self.delay * 3:
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
                self.bgm.play("ISAAC_SHOOT", 0)
            except ValueError:
                shooted_tear.direction = Vector2(0, 0)

            self.tear_ready.add(shooted_tear)
            self._tears.add(shooted_tear)

            self.shoot_timer = pygame.time.get_ticks()
        if pygame.time.get_ticks() - self.shoot_timer > self.delay:
            self.tear_ready.empty()

    def pooping(self):
        pass

    def update(self, keys):
        self.move(keys)
        self.shoot(keys)
        self._tears.update()


class Tear(CanHitWalls):
    def __init__(self, spawn_pos: Vector2):
        super().__init__()
        self.image = pygame.image.load(ImportedImages.tearImage)
        self.image = pygame.transform.scale(
            self.image, (TearSettings.tearWidth, TearSettings.tearHeight)
        )
        self.rect = self.image.get_rect(center=spawn_pos)
        self.speed = TearSettings.tearSpeed
        self._direction = Vector2(0, 0)

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value: Vector2):
        self._direction = value

    def update(self):
        self.rect.move_ip(self.direction * self.speed)
        if self._hit_wall or self._direction == Vector2(0, 0):
            print(("hitwall"))
            self.kill()
