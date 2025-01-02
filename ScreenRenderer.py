from pygame import *
from Statics import *
from Player import Player
from Rooms import *
from Attack import Bullet
from enemies import *
from NPC import *
from main_menu import *
import time


isaac = pygame.sprite.GroupSingle()
isaac.add(
    Player(
        spawn_pos=0.5 * Vector2(ScreenSettings.screenWidth, ScreenSettings.screenHeight)
    )
)

tears = pygame.sprite.Group()


def get_keys():
    return pygame.key.get_pressed()


last_shoot_time = 0
def tears_add(player: Player):
    global last_shoot_time 
    current_time = pygame.time.get_ticks()
    if current_time - last_shoot_time >= PlayerSettings.PlayerAttackSpeed * 1000:
        if (
            not get_keys()[pygame.K_UP]
            and not get_keys()[pygame.K_DOWN]
            and not get_keys()[pygame.K_LEFT]
            and not get_keys()[pygame.K_RIGHT]
        ):
            return
        new_tear = Bullet(
            spawn_pos=Vector2(
                player.rect.x + PlayerSettings.playerWidth * 0.5,
                player.rect.y + PlayerSettings.playerHeight * 0.5,
            )
        )
        new_tear.first_update(get_keys())
        tears.add(new_tear)
        last_shoot_time = current_time



NPCs = pygame.sprite.Group()
npc = NPC()
NPCs.add(npc)

ChatBoxes = pygame.sprite.Group()
chatbox = ChatBox()

rooms = pygame.sprite.Group()
start_room = StartRoom()  # final:rooms=Rooms.gen_rooms()
rooms.add(start_room)  # final:rooms.add(rooms)


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
    def render_screen(self, active_scene: Scenes):
        self.update_clock()
        self.update_scene(active_scene)
        pygame.display.flip()

    def update_clock(self):
        self.clock = pygame.time.Clock()
        self.clock.tick(ScreenSettings.fps)

    def update_sprite(self, sprite: sprite.Group, keys=None, rooms=None):
        sprite.update(keys, rooms)
        sprite.draw(self.screen)


    def update_scene(self, active_scene: Scenes):
        match active_scene:
            case Scenes.MAIN_MENU:
                main_menu_all.update()
                main_menu_all.draw(self.screen)
            case Scenes.START_ROOM:
                self.update_sprite(rooms)
                self.update_sprite(isaac, get_keys(), rooms)
                tears_add(isaac.sprite)
                tears.update()
                tears.draw(self.screen)
                enemies.update(tears)
                enemies.draw(self.screen)
                for room in rooms:
                    room.update_walls(tears)
                NPCs.draw(self.screen)
                for npc in NPCs:
                    if npc.hit_player(isaac.sprite):
                        npc.gen_chatbox(ChatBoxes, chatbox)
                    else:
                        ChatBoxes.empty()
                '''
                current_keys = get_keys()
                last_keys = [0] * 323  # 初始化 last_keys 为全 0 列表

                # 检测按键变化，模拟 KEYDOWN 和 KEYUP 事件
                for key in range(pygame.K_ESCAPE, pygame.K_z + 1):  # 检查从 ESC 到 Z 的键
                    if current_keys[key] and not last_keys[key]:  # 检测按下事件
                        pygame.event.post(pygame.event.Event(KEYDOWN, {'key': key}))
                    elif not current_keys[key] and last_keys[key]:  # 检测松开事件
                        pygame.event.post(pygame.event.Event(KEYUP, {'key': key}))

                # 更新 last_keys 为当前键盘状态
                last_keys = current_keys

                #print(pygame.event.get())
                ''' 
                # 获取当前键盘状态
                for event in pygame.event.get():
                    #print("AAA")
                    if ChatBoxes.has_internal(chatbox):
                        #print("BBB")
                        if event.type == QUIT:
                            chatbox.kill()
                        chatbox.handle_input(event)
                    else:
                        if event.type == QUIT:
                            pygame.quit()
                            exit()


# szd: enemies
enemies = pygame.sprite.Group()
for i in range(5):
    fly = Fly()
    enemies.add(fly)

# szd : main_menu
main_menu_all = pygame.sprite.Group()
main_menu_all.add(
    BackGround(),
    StartButton(),
    Static_state(
        ImportedImages.Options,
        MainMenuSettings.Options.x,
        MainMenuSettings.Options.y,
        MainMenuSettings.Options.MULTI,
        MainMenuSettings.Options.ALPHA,
    ),
    Static_state(
        ImportedImages.Continues,
        MainMenuSettings.Continue.x,
        MainMenuSettings.Continue.y,
        MainMenuSettings.Continue.MULTI,
        MainMenuSettings.Continue.ALPHA,
    ),
    Dynamic_state(
        ImportedImages.Draw,
        MainMenuSettings.Draw.frame_rects,
        MainMenuSettings.Draw.x,
        MainMenuSettings.Draw.y,
        MainMenuSettings.Draw.MULTI,
        MainMenuSettings.Draw.frames_duration,
    ),
    Dynamic_state(
        ImportedImages.Bomb,
        MainMenuSettings.Bomb.frame_rects,
        MainMenuSettings.Bomb.x,
        MainMenuSettings.Bomb.y,
        MainMenuSettings.Bomb.MULTI,
        MainMenuSettings.Bomb.frames_duration,
    ),
)