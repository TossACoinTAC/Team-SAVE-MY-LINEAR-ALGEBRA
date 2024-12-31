import pygame
from tools import *
import GameManager
import random
from Statics import *

class Monster(pygame.sprite.Sprite):
    def __init__(self, importImage, importImage_die, frame_rects, frame_rects_die, x, y, MULTI, frame_duration, HP, speed):
        super().__init__()
        #setup_live_animation
        self.frames = []
        self.frames_index = 0
        self.frame_rects = frame_rects
        self.load_frames(self.frame_rects, importImage, MULTI, self.frames)
        self.image = self.frames[self.frames_index]
        self.frame_durations = frame_duration

        #die_animation
        self.frames_die = []
        self.frames_index_die = 0
        self.frame_rects_die = frame_rects_die
        self.load_frames(self.frame_rects_die, importImage_die, MULTI, self.frames_die)
        self.image_die = self.frames[self.frames_index_die]

        #update_position
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(400, 800)
        self.rect.y = random.randint(200, 500)
        self.speed = speed
        self.speed_x = random.choice(self.speed)
        self.speed_y = random.choice(self.speed)
        self.move_mode = random.choice(['straight']) #random_turn 没写完
        self.turn_interval = random.randint(500, 1000)
        self.turn_countdown = self.turn_interval

        # not important
        self.HP = HP
        self.state = 'live' 
        self.timer = 0
        self.MULTI = MULTI

    def load_frames(self, frame_rects, importImage, MULTI, frame):
        sheet = pygame.image.load(importImage)
        for frame_rect in frame_rects:
            frame.append(get_images(sheet, *frame_rect, (0, 0, 0), MULTI))

    def update(self):
        
        self.update_animation()
        self.check_collision_kill()
        self.update_position()

    def update_position(self):
        if self.move_mode == 'straight':
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            if self.rect.left <= ScreenSettings.marginWidth or self.rect.right >= (ScreenSettings.screenWidth - ScreenSettings.marginWidth):
                self.speed_x = -self.speed_x
            if self.rect.top <= ScreenSettings.marginHeight or self.rect.bottom >= (ScreenSettings.screenHeight - ScreenSettings.marginHeight):
                self.speed_y = -self.speed_y
        
        if self.move_mode == 'radnom_turn':
            self.turn_countdown -= 1
            if self.turn_countdown <= 0:
                self.speed_x = random.choice(self.speed)
                self.speed_y = random.choice(self.speed)
                self.turn_countdown = self.turn_interval
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            if self.rect.left <= ScreenSettings.marginWidth or self.rect.right >= (ScreenSettings.screenWidth - ScreenSettings.marginWidth):
                self.speed_x = -self.speed_x
            if self.rect.top <= ScreenSettings.marginHeight or self.rect.bottom >= (ScreenSettings.screenHeight - ScreenSettings.marginHeight):
                self.speed_y = -self.speed_y

    def update_animation(self):

        if self.state == 'live':
            self.current_time = pygame.time.get_ticks()
            if self.timer == 0:
                self.timer = self.current_time
            elif self.current_time - self.timer > self.frame_durations:
                self.frames_index += 1
                self.frames_index %= len(self.frame_rects)
                self.timer = self.current_time
            self.image = self.frames[self.frames_index]

        if self.state == 'die':
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



    def check_collision_kill(self):
        if pygame.sprite.spritecollide(self, GameManager.tears, False):
            self.HP -= 1
        if self.HP <= 0:
            self.state = 'die'


