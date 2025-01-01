import pygame
import pygame.event as ev
from Statics import *
from tools import *


class Static_state(pygame.sprite.Sprite):
    def __init__(self, importImage, x, y, MULTI, ALPHA):
        super().__init__()
        self.image = pygame.image.load(importImage)
        self.image.set_alpha(ALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image = pygame.transform.scale(
            self.image, (int(self.rect.width * MULTI), int(self.rect.height * MULTI))
        )

    def update(self):
        pass


class Dynamic_state(pygame.sprite.Sprite):
    def __init__(self, importImage, frame_rects, x, y, MULTI, frame_duration):
        super().__init__()

        self.frames = []
        self.frames_index = 0
        self.frame_rects = frame_rects
        self.load_frames(self.frame_rects, importImage, MULTI)
        self.image = self.frames[self.frames_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.timer = 0
        self.frame_durations = frame_duration
        self.MULTI = MULTI

    def load_frames(self, frame_rects, importImage, MULTI):
        sheet = pygame.image.load(importImage)
        for frame_rect in frame_rects:
            self.frames.append(get_images(sheet, *frame_rect, (0, 0, 0), MULTI))

    def update(self):
        pass

    def update(self):
        self.current_time = pygame.time.get_ticks()

        if self.timer == 0:
            self.timer = self.current_time
        elif self.current_time - self.timer > self.frame_durations:
            self.frames_index += 1
            self.frames_index %= len(self.frame_rects)
            self.timer = self.current_time
        self.image = self.frames[self.frames_index]


class BackGround(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(ImportedImages.BackGround)
        self.image = pygame.transform.scale(
            self.image, (ScreenSettings.screenWidth, ScreenSettings.screenHeight)
        )
        self.rect = self.image.get_rect()

    def update(self):
        pass


class StartButton(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(ImportedImages.StartButton)
        self.image.set_alpha(MainMenuSettings.StartButton.ALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = MainMenuSettings.StartButton.x
        self.rect.y = MainMenuSettings.StartButton.y
        self.multi = MainMenuSettings.StartButton.MULTI

    def update(self):
        self.image = pygame.transform.scale(
            self.image,
            (int(self.rect.width * self.multi), int(self.rect.height * self.multi)),
        )
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.multi = 1.2 * MainMenuSettings.StartButton.MULTI
            if pygame.mouse.get_pressed()[0]:
                pygame.event.post(ev.Event(Events.MAIN_TO_STARTROOM))
        else:
            self.multi = MainMenuSettings.StartButton.MULTI
        # if MainMenuSettings.StartButton.x <= mouse_x and mouse_x <= MainMenuSettings.StartButton.x + 150 and MainMenuSettings.StartButton.y <= mouse_y and mouse_y <= MainMenuSettings.StartButton.y + 150:
        #     self.multi = 1.2 * MainMenuSettings.StartButton.MULTI
        # else:
        #     self.multi = MainMenuSettings.StartButton.MULTI
