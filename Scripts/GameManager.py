from pygame import *
from Statics import *
from Player import Player
from Rooms import *
from Attack import Bullet
from BGMPlayer import *

isaac = pygame.sprite.GroupSingle()
isaac.add(
    Player(
        spawn_pos=0.5 * Vector2(ScreenSettings.screenWidth, ScreenSettings.screenHeight)
    )
)

tears = pygame.sprite.Group()
def tears_add(player: Player):
    new_tear = Bullet(
        spawn_pos=Vector2(player.rect.x, player.rect.y)
    )
    new_tear.first_update(get_keys())
    tears.add(
        new_tear
    )


rooms = pygame.sprite.Group()
start_room = StartRoom()  # final:rooms=Rooms.gen_rooms()
rooms.add(start_room)  # final:rooms.add(rooms)


def get_keys():
    return pygame.key.get_pressed()


class ScreenRenderer:

    # Awake()
    def __init__(self):
        self.set_screen()
        self.set_icon()
        self.bgm = BgmPlayer()
        self.playbgm = True

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
        if self.playbgm:
            self.bgm.update("MAIN_THEME", -1)
            self.playbgm = False
        self.update_sprite(rooms)
        self.update_sprite(isaac, get_keys())
        tears_add(isaac.sprite)
        tears.update()
        tears.draw(self.screen)
        pygame.display.flip()

    def update_clock(self):
        self.clock = pygame.time.Clock()
        self.clock.tick(ScreenSettings.fps)

    def update_sprite(self, sprite: sprite.Group, keys=None):
        sprite.update(keys)
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
