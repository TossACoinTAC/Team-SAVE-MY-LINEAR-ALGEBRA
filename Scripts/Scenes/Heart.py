from pygame import *
from Statics import *
from TmpTools.tools import *
from GameManagers.BGMPlayer import BGMPlayer
class Heart(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frame = []
        self.frame_index = 0
        self.frame_rects = HeartSettings.heart_frame_rects
        self.sheet = pygame.image.load(ImportedImages.heartImage)
        for i in range(len(self.frame_rects)):
            tmp_image = get_images(self.sheet, *self.frame_rects[i], (0, 0, 0), 3.0)
            self.frame.append(
                pygame.transform.scale(
                    tmp_image, (HeartSettings.heartWidth, HeartSettings.heartHeight)
                )
            )
        self.image = self.frame[0]
        self.rect = self.image.get_rect()
        self.rect.x = ScreenSettings.marginWidth
        self.rect.y = ScreenSettings.marginHeight
        self.HP = PlayerSettings.PlayerHP
        self.state = 'normal'
        self.timer = 0
        self.bgm_player = BGMPlayer()

    def update(self):

        current_time = pygame.time.get_ticks()
        if self.state == 'reduce' and current_time - self.timer > 1000:
            self.HP -= 1
            self.timer = current_time
            self.state = 'normal'
            self.bgm_player.play("ISAAC_HURT", 0)
        if self.HP == 0:
            event.post(event.Event(Events.GAME_OVER))
            # 触发事件游戏结束
        self.image = self.frame[6 - self.HP]

