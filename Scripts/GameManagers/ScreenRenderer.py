from pygame import *
from Statics import *
from GameManagers.GameManager import GameManager


class ScreenRenderer(GameManager):
    # Awake()
    def __init__(self):
        super().__init__()
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
    def render_screen(self, active_scene: Scenes):
        self.update_clock()
        self.update_scene(active_scene)
        pygame.display.flip()

    def update_clock(self):
        self.clock = pygame.time.Clock()
        self.clock.tick(ScreenSettings.fps)

    def update_sprite(self, sprite: sprite.GroupSingle, keys=None):
        sprite.update(keys)
        sprite.draw(self.screen)

    def update_scene(self, active_scene: Scenes):
        match active_scene:
            case Scenes.MAIN_MENU:
                self.main_menu.update()
                self.main_menu.draw(self.screen)

            case Scenes.START_ROOM:
                self.update_sprite(self.room_group)
                self.update_sprite(self.isaac_group, self.get_keys())
                self.isaac.tears.draw(self.screen)
