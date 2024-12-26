from pygame import *
from Statics import *
from Player import Player

isaac = pygame.sprite.GroupSingle()
isaac.add(
    Player(0.5 * Vector2(ScreenSettings.screenWidth, ScreenSettings.screenHeight))
)


def get_keys():
    return pygame.key.get_pressed()


class ScreenRenderer:

    # Awake()
    def __init__(self):
        self.set_screen()
        self.set_icon()

    def set_screen(self):
        self.screen = pygame.display.set_mode(
            (ScreenSettings.screenWidth, ScreenSettings.screenHeight)
        )
        pygame.display.set_caption(ScreenSettings.caption)

    def set_icon(self):
        icon = pygame.image.load(ImportedImages.icon).convert_alpha()
        pygame.display.set_icon(icon)

    # Update()
    def update(self):
        self.update_clock()
        self.update_sprite(isaac, get_keys())
        self.draw_sprite(isaac)
        pygame.display.flip()

    def update_clock(self):
        self.clock = pygame.time.Clock()
        self.clock.tick(ScreenSettings.fps)

    def update_sprite(self, sprite, keys):
        sprite.update(keys)

    def draw_sprite(self, sprite):
        sprite.draw(self.screen)


class EventListener:
    @staticmethod
    def listen():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


class GameManager:
    def __init__(self):
        self.screen_renderer = ScreenRenderer()

    def update(self):
        self.screen_renderer.update()
        EventListener.listen()
