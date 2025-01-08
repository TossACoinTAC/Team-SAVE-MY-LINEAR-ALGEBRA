from pygame import *
from TmpTools.tools import *
import random
from Statics import *
from math import *

class Monster(pygame.sprite.Sprite):
    def __init__(
        self,
        importImage,
        importImage_die,
        frame_rects,
        frame_rects_die,
        x,
        y,
        MULTI,
        frame_duration,
        HP,
        speed,

    ):
        super().__init__()
        # setup_live_animation
        self.frames = []
        self.frames_index = 0
        self.frame_rects = frame_rects
        self.load_frames(self.frame_rects, importImage, MULTI, self.frames)
        self.image = self.frames[self.frames_index]
        self.frame_durations = frame_duration

        # die_animation
        self.frames_die = []
        self.frames_index_die = 0
        self.frame_rects_die = frame_rects_die
        self.load_frames(self.frame_rects_die, importImage_die, MULTI, self.frames_die)
        self.image_die = self.frames[self.frames_index_die]

        # update_position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.speed_x = random.choice(self.speed)
        self.speed_y = random.choice(self.speed)

        self.move_mode = random.choice(["straight"])  # random_turn 没写完

        self.turn_interval = random.randint(500, 1000)
        self.turn_countdown = self.turn_interval

        # not important

        self.HP = HP
        self.state = "live"
        self.timer = 0
        self.MULTI = MULTI

    def load_frames(self, frame_rects, importImage, MULTI, frame):
        sheet = pygame.image.load(importImage)
        for frame_rect in frame_rects:
            frame.append(get_images(sheet, *frame_rect, (0, 0, 0), MULTI))

    def update(self):

        self.update_animation()
        self.update_position()
        self.check_die()
    
    def check_die(self):
        if self.HP <= 0:
            self.state = 'die'
    
    def detect_collision(self):
        if self.rect.left <= ScreenSettings.marginWidth or self.rect.right >= (
            ScreenSettings.screenWidth - ScreenSettings.marginWidth):
            self.speed_x = -self.speed_x
        if self.rect.top <= ScreenSettings.marginHeight or self.rect.bottom >= (
            ScreenSettings.screenHeight - ScreenSettings.marginHeight):
            self.speed_y = -self.speed_y

    def update_position(self):


        if self.move_mode == "straight":
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.detect_collision()

        if self.move_mode == "radnom_turn":
            self.turn_countdown -= 1
            if self.turn_countdown <= 0:
                self.speed_x = random.choice(self.speed)
                self.speed_y = random.choice(self.speed)
                self.turn_countdown = self.turn_interval
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.detect_collision()

    def update_animation(self):

        if self.state == "live":
            self.current_time = pygame.time.get_ticks()
            if self.timer == 0:
                self.timer = self.current_time
            elif self.current_time - self.timer > self.frame_durations:
                self.frames_index += 1
                self.frames_index %= len(self.frame_rects)
                self.timer = self.current_time
            self.image = self.frames[self.frames_index]

        if self.state == "die":
            self.speed_x = 0
            self.speed_y = 0
            self.current_time = pygame.time.get_ticks()
            if self.timer == 0:
                self.timer = self.current_time
            elif self.current_time - self.timer > self.frame_durations:
                self.frames_index_die += 1

                self.timer = self.current_time
            if self.frames_index_die == 10:
                self.kill()

            self.image = self.frames_die[self.frames_index_die]



class Fly(Monster):
    def __init__(self):
        super().__init__(
            ImportedImages.Fly,
            ImportedImages.Fly_die,
            EnemiesSettings.Fly.frame_rects,
            EnemiesSettings.Fly.frame_rects_die,
            EnemiesSettings.Fly.x,
            EnemiesSettings.Fly.y,
            EnemiesSettings.Fly.MULTI,
            EnemiesSettings.Fly.frames_duration,
            EnemiesSettings.Fly.HP,
            EnemiesSettings.Fly.speed,)

class Fly_blood(Monster):
    def __init__(self, x, y):
        super().__init__(
            ImportedImages.Fly_blood,
            ImportedImages.Fly_die,
            EnemiesSettings.Fly.frame_rects_blood,
            EnemiesSettings.Fly.frame_rects_die,
            x,y,
            EnemiesSettings.Fly.MULTI,
            EnemiesSettings.Fly.frames_duration,
            EnemiesSettings.Fly.HP,
            EnemiesSettings.Fly.speed,)

class BossBody(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.set_body_animation()

        self.set_clock()
        self.set_position()
        self.set_HP()
        self.if_beattacked = 'False'


    
    def set_HP(self):
        self.HP = BossSettings.health_bar.max

    def set_position(self):
        self.rect.centerx = 0.5 * ScreenSettings.screenWidth
        self.rect.centery = 0.3 * ScreenSettings.screenHeight

    def set_clock(self):
        self.animation_timer = 0
        self.beattacked_timer = 0

    def set_body_animation(self):
        self.frames = []
        self.frame_index = 0
        self.frame_rects = BossSettings.Body.frame_rects
        
        sheet = pygame.image.load(ImportedImages.Boss)
        for frame_rect in self.frame_rects:
            self.frames.append(pygame.transform.scale(
                get_images(sheet, *frame_rect, (0, 0, 0), 1.0),
                (int(140 * 2.2), int(120 * 2.2))))

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()

    def update(self):

        if self.if_beattacked == 'False':
            current_time = pygame.time.get_ticks()
            if self.animation_timer == 0:
                self.animation_timer = current_time
            elif current_time - self.animation_timer > 500:
                self.frame_index += 1
                self.frame_index %= len(self.frame_rects)
                self.animation_timer = current_time
            self.image = self.frames[self.frame_index]

class BossAttack(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.HP = 10000000
        self.set_Attack_animation()
        self.set_clock()
        self.set_position()
        self.state = 'sleep'
        self.if_shoot = 'False'
        self.if_spwan_fly = 'False'

    def set_position(self):
        self.rect.centerx = 0.5 * ScreenSettings.screenWidth
        self.rect.centery = 0.22 * ScreenSettings.screenHeight

    def set_clock(self):
        self.timer = 0

    def set_Attack_animation(self):

        self.frames = []
        self.frame_index = 0
        self.frame_rects = BossSettings.attack.frame_rects
        
        sheet = pygame.image.load(ImportedImages.Boss)
        for frame_rect in self.frame_rects:
            self.frames.append(pygame.transform.scale(
                get_images(sheet, *frame_rect, (0, 0, 0), 1.0),
                (int(frame_rect[2] * 2.2), int(frame_rect[3] * 2.2))))

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()

    def update(self):
        if self.state == 'awake':
            duration = [125, 125, 125, 400, 400, 400, 125, 125]
            self.current_time = pygame.time.get_ticks()
            if self.timer == 0:
                self.timer = self.current_time
            elif self.current_time - self.timer > duration[self.frame_index]:
                self.frame_index += 1
                self.timer = self.current_time
                if self.frame_index == 4:
                    self.if_shoot = 'True'
                if self.frame_index == 5:
                    self.if_spwan_fly = 'True'
            self.image = self.frames[self.frame_index]
            if self.frame_index == len(self.frame_rects) - 1:
                self.state = 'sleep'
                self.frame_index = 0
        if self.state == 'sleep':
            self.current_time = pygame.time.get_ticks()
            if self.current_time - self.timer > random.randint(1000, 3000):
                self.state = 'awake'
        
        

class BloodyTear(pygame.sprite.Sprite):
    def __init__(self, x, y, direction_x, direction_y):
        super().__init__()
        self.set_animation()

        self.image = self.frame[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = TearSettings.tearSpeed
        self.timer = 0
        self.direction = Vector2(direction_x, direction_y)

    def set_animation(self):

        self.state = "live"
        self.frame = []
        self.frame_index = 0
        self.frame_rects = TearSettings.tear_frame_rects
        self.sheet = pygame.image.load(ImportedImages.tear_pop_Image)
        for i in range(len(self.frame_rects)//2):
            self.frame.append(pygame.transform.scale(
                get_images(self.sheet, *self.frame_rects[i + 15], (0, 0, 0), 1.0),
                (TearSettings.tearWidth, TearSettings.tearHeight)))


    def update(self):
        self.rect.move_ip(self.direction * self.speed)


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


