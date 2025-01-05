import pygame
import pygame.event as ev
from Statics import *
from TmpTools.tools import *


class MainMenu(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.add(BackGround(), StartButton(), Options(), Continue(), Draw(), Bomb())


class StaticState(pygame.sprite.Sprite):
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


class DynamicState(pygame.sprite.Sprite):
    def __init__(self, importImage, frame_rects, x, y, MULTI, frame_duration):
        super().__init__()

        self.frames = []
        self.frames_index = 0
        self.frame_rects = frame_rects
        self.load_frames(self.frame_rects, importImage, MULTI)
        self.image: pygame.Surface = self.frames[self.frames_index]
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
        self.rect = self.image.get_rect()
        self.image.set_alpha(MainMenuSettings.StartButton.ALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = MainMenuSettings.StartButton.x
        self.rect.y = MainMenuSettings.StartButton.y
        self.multi = MainMenuSettings.StartButton.MULTI
        self.image = pygame.transform.smoothscale(
            self.image, (self.rect.width * self.multi, self.rect.height * self.multi)
        )
        self.scaled_images = {
            1: self.image,
            1.2: pygame.transform.smoothscale(
                self.image, (self.rect.width * 3.6, self.rect.height * 3.6)
            ),
        }

    def update(self):

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if (
            self.rect.left <= mouse_x <= self.rect.right * 1.5
            and self.rect.top <= mouse_y <= self.rect.bottom * 1.2
        ):
            self.image = self.scaled_images[1.2]
            center_x, center_y = self.scaled_images[1].get_rect().center
            # Get the new rect of the scaled image
            scaled_rect = self.image.get_rect()
            # Set the center of the new rect to the original image's center
            scaled_rect.center = (center_x, center_y)

            if pygame.mouse.get_pressed()[0]:
                ev.post(ev.Event(Events.MAIN_TO_STARTROOM))
        else:
            self.image = self.scaled_images[1]


class Options(StaticState):
    def __init__(self):
        super().__init__(
            ImportedImages.Options,
            MainMenuSettings.Options.x,
            MainMenuSettings.Options.y,
            MainMenuSettings.Options.MULTI,
            MainMenuSettings.Options.ALPHA,
        )


class Continue(StaticState):
    def __init__(self):
        super().__init__(
            ImportedImages.Continues,
            MainMenuSettings.Continue.x,
            MainMenuSettings.Continue.y,
            MainMenuSettings.Continue.MULTI,
            MainMenuSettings.Continue.ALPHA,
        )


class Draw(DynamicState):
    def __init__(self):
        super().__init__(
            ImportedImages.Draw,
            MainMenuSettings.Draw.frame_rects,
            MainMenuSettings.Draw.x,
            MainMenuSettings.Draw.y,
            MainMenuSettings.Draw.MULTI,
            MainMenuSettings.Draw.frames_duration,
        )


class Bomb(DynamicState):
    def __init__(self):
        super().__init__(
            ImportedImages.Bomb,
            MainMenuSettings.Bomb.frame_rects,
            MainMenuSettings.Bomb.x,
            MainMenuSettings.Bomb.y,
            MainMenuSettings.Bomb.MULTI,
            MainMenuSettings.Bomb.frames_duration,
        )
