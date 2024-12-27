import pygame
from Statics import *

# BGM settings
class BgmPlayer():
    def __init__(self):
        pygame.mixer.init()
        self.main_theme_BGM = pygame.mixer.Sound(ImportedBGM.bgmpath[0]) 
        self.isaac_walk_BGM = pygame.mixer.Sound(ImportedBGM.bgmpath[1]) 
        self.channel = None

    def play(self, SOUND_NAME, loop):   #loop = 0 is once loop = -1 is forever
        if SOUND_NAME == "MAIN_THEME":
            self.channel = self.main_theme_BGM.play(loops=loop)
        if SOUND_NAME == "ISAAC_WALK":
            self.channel = self.isaac_walk_BGM.play(loops=loop)
        
    def stop(self):
        if self.channel:
            self.channel.stop() 

    def update(self, SOUND_NAME, MODE):
        #UPDATE CURRENT STATUS AND PLAY NEW BGM
        self.play(SOUND_NAME, MODE)
