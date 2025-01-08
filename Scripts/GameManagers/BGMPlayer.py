import pygame
from Statics import *


# BGM settings
class BGMPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.main_theme_BGM = pygame.mixer.Sound(ImportedBGM.main_theme)
        self.isaac_walk_BGM = pygame.mixer.Sound(ImportedBGM.walk)
        self.isaac_shoot_BGM = pygame.mixer.Sound(ImportedBGM.shoot)
        self.isaac_hurt_BGM = pygame.mixer.Sound(ImportedBGM.hurt)
        self.bomb_explode_BGM = pygame.mixer.Sound(ImportedBGM.explosion)
        self.tear_hit_BGM = pygame.mixer.Sound(ImportedBGM.tear_impact)
        self.channel = None
        self.sounds_to_play = []

    def play(self, sound, loop):  # loop = 0 is once loop = -1 is forever
        self.sounds_to_play.append(sound)  # use a loop to avoid clashes
        for sound in self.sounds_to_play:
            if sound == "MAIN_THEME":
                self.channel = self.main_theme_BGM.play(loops=loop)
            if sound == "ISAAC_WALK":
                self.channel = self.isaac_walk_BGM.play(loops=loop)
            if sound == "ISAAC_SHOOT":
                self.channel = self.isaac_shoot_BGM.play(loops=loop)
            if sound == "ISAAC_HURT":
                self.channel = self.isaac_hurt_BGM.play(loops=loop)
            if sound == "BOMB_EXPLODE":
                self.channel = self.bomb_explode_BGM.play(loops=loop)
            if sound == "TEAR_HIT":
                self.channel = self.tear_hit_BGM.play(loops=loop)
        self.sounds_to_play.clear()

    def stop(self):
        if self.channel:
            self.channel.stop()
