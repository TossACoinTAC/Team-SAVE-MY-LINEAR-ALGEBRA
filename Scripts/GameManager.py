from pygame import *
from BGMPlayer import *
from ScreenRenderer import ScreenRenderer
from EventListener import EventListener


class GameManager:
    def __init__(self):
        self.bgm_player = BgmPlayer()
        self.playbgm = True
        self.event_listener = EventListener()
        self.screen_renderer = ScreenRenderer()
        self.active_scene = self.event_listener.change_scene()  # Scenes.MAIN_MENU

    def update(self):
        self.event_listener.listen()
        self.active_scene = self.event_listener.change_scene()
        self.screen_renderer.render_screen(self.active_scene)
        self.update_bgm()

    def update_bgm(self):
        if self.playbgm:
            self.bgm_player.update("MAIN_THEME", -1)
            self.playbgm = False
