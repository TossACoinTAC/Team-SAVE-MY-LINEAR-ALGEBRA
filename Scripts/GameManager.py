from pygame import *
from Statics import *
from Player import Player
from Rooms import *
from Attack import Bullet
from BGMPlayer import *
from main_menu import *

isaac = pygame.sprite.GroupSingle()
isaac.add(
    Player(
        spawn_pos=0.5 * Vector2(ScreenSettings.screenWidth, ScreenSettings.screenHeight)
    )
)

tears = pygame.sprite.Group()
def tears_add(player: Player):
    if not get_keys()[pygame.K_UP] and not get_keys()[pygame.K_DOWN] and not get_keys()[pygame.K_LEFT] and not get_keys()[pygame.K_RIGHT]:
        return
    new_tear = Bullet(
        spawn_pos=Vector2(player.rect.x+PlayerSettings.playerWidth * 0.5, player.rect.y+PlayerSettings.playerHeight * 0.5)
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

         # szd : update main_menu
        main_menu_all.update()
        main_menu_all.draw(self.screen)

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


# szd : main_menu
main_menu_all = pygame.sprite.Group()
main_menu_all.add(
    BackGround(),
    StartButton(),
    Static_state(
        ImportedImages.MainMenuImages.Options,
        MainMenuSettings.Options.x,
        MainMenuSettings.Options.y,
        MainMenuSettings.Options.MULTI,
        MainMenuSettings.Options.ALPHA,
    ),
    Static_state(
        ImportedImages.MainMenuImages.Continues,
        MainMenuSettings.Continue.x,
        MainMenuSettings.Continue.y,
        MainMenuSettings.Continue.MULTI,
        MainMenuSettings.Continue.ALPHA,
    ),
    Dynamic_state(
        ImportedImages.MainMenuImages.Draw,
        MainMenuSettings.Draw.frame_rects,
        MainMenuSettings.Draw.x,
        MainMenuSettings.Draw.y,
        MainMenuSettings.Draw.MULTI,
        MainMenuSettings.Draw.frames_duration,
    ),
    Dynamic_state(
        ImportedImages.MainMenuImages.Bomb,
        MainMenuSettings.Bomb.frame_rects,
        MainMenuSettings.Bomb.x,
        MainMenuSettings.Bomb.y,
        MainMenuSettings.Bomb.MULTI,
        MainMenuSettings.Bomb.frames_duration,
    ),
)
