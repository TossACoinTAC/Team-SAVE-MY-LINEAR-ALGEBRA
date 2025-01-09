from pygame import *
from Statics import *
from Characters.Player import Player
from Characters.LLM import *
import pygame.event as ev 


class NPC(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(
            ImportedImages.NPCImage
        )  # 随便选的图片，可以换成其它的
        self.image = pygame.transform.scale(
            self.image, (PlayerSettings.playerWidth, PlayerSettings.playerHeight)
        )
        self.rect = self.image.get_rect()
        self.rect.center = (500, 500)  # 随便设的地方，有商店了可以让他再商店里生成
        self.HP = 0x3f3f3f3f  # 无敌

    def gen_chatbox(self, keys):
        if keys[pygame.K_q]:
            ev.post(ev.Event(Events.TO_CHATBOX))


    def update(self, keys = None):
        pass


# 创建 ChatBox
class ChatBox(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # 加载并调整图像大小
        self.image = pygame.image.load(ImportedImages.chatboxImage)
        self.image = pygame.transform.scale(
            self.image, (ScreenSettings.screenWidth, ScreenSettings.screenHeight)
        )
        self.rect = self.image.get_rect()

        # 初始化变量
        self.chat_log = []
        self.current_step = 0
        self.input_text = ""
        self.allow_input = True
        self.messages = NPC_Original_messages.npc_message[1]    #两个npc

        # 定义字体和颜色
        pygame.font.init()
        self.FONT = pygame.font.Font(None, 36)
        self.BG_COLOR = (30, 30, 30)  # 背景色
        self.INPUT_COLOR = (50, 50, 50)  # 输入框颜色

        # 游戏文本内容
        self.GAME_TEXTS = [
            "Welcome, brave adventurer! I sense that you are seeking a challenge worthy of your mettle. As the guardian of this fortress, it is my duty to test your wits and abilities. Type 'exit' or 'quit' to end the chat.",
        ]
        self.chat_log.append(self.GAME_TEXTS[0])

        self.linenumber = 2
        self.y_offset = 20

    def render_text(self, text, x, y, color=(255, 255, 255)):
        text_surface = self.FONT.render(text, True, color)
        self.image.blit(text_surface, (x, y))

    def update(self, keys):
        # 显示聊天日志
        self.image.fill(self.BG_COLOR)
        self.y_offset = 20
        for line in self.chat_log[-2:]:  # 显示最后 2 条记录
            self.render_wrapped_text(line, 20, self.y_offset)
            self.y_offset += 25

        # 显示输入框
        pygame.draw.rect(
            self.image,
            self.INPUT_COLOR,
            (20, ScreenSettings.screenHeight - 60, ScreenSettings.screenWidth - 40, 40),
        )
        
        self.handle_input(keys)
        self.render_wrapped_text(self.input_text, 30, ScreenSettings.screenHeight - 50)

    def handle_input(self, keys):
        inputed = False
        if keys[pygame.K_RETURN]:
            if self.input_text.strip() and self.allow_input:
                # 添加玩家输入到聊天日志
                self.chat_log.append(f"You: {self.input_text.strip()}")

                # 调用 LLM_chat 函数获取回复
                response = LLM_chat(self.input_text.strip(), self.messages)
                #print(response)
                self.chat_log.append(f"NPC: {response}")

                if "quit" in self.input_text.strip() or "exit" in self.input_text.strip():
                    for sprite in self.groups():
                        if isinstance(sprite, ChatBox):
                            sprite.kill()
                    ev.post(ev.Event(Events.EXIT_CHATBOX))
                    #self.kill()
                
                self.input_text = ""
            inputed = True


        elif keys[pygame.K_BACKSPACE]:
            if self.input_text and self.allow_input:
                self.input_text = self.input_text[:-1]
            inputed = True

        elif keys[pygame.K_SPACE]:
            if self.input_text and self.allow_input:
                self.input_text += " "
            inputed = True

        else:
            for key in range(len(keys)):
                if keys[key]:
                    if self.allow_input:
                        self.input_text += pygame.key.name(key)
                    inputed = True
                    break

        self.allow_input = not inputed


    def render_wrapped_text(self, text, x, y, color=(255, 255, 255)):
        words = text.split(" ")
        space_width, _ = self.FONT.size(" ")
        max_width = ScreenSettings.screenWidth - 40
        current_line = []
        current_width = 0
        for word in words:
            word_width, word_height = self.FONT.size(word)
            if current_width + word_width + space_width > max_width:
                self.render_text(" ".join(current_line), x, y, color)
                y += word_height
                current_line = [word]
                current_width = word_width
                self.linenumber += 1
            else:
                current_line.append(word)
                current_width += word_width + space_width

        if current_line:
            self.render_text(" ".join(current_line), x, y, color)


'''
pygame.init()
screen = pygame.display.set_mode((ScreenSettings.screenWidth, ScreenSettings.screenHeight))
pygame.display.set_caption("ChatBox Game")

chatbox = ChatBox()
all_sprites = pygame.sprite.Group(chatbox)

# 主游戏循环
run_game = True
while run_game:
    screen.fill((30,30,30))
    # 更新并渲染聊天框
    all_sprites.update()
    all_sprites.draw(screen)
    # 事件处理
    for event in pygame.event.get():
        if event.type == QUIT:
            run_game = False
        chatbox.handle_input(event)


    # 更新显示
    pygame.display.flip()

# 退出游戏
pygame.quit()


# 初始化 Pygame
pygame.init()

# 设置窗口
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ChatBox Game")

# 定义字体和颜色
FONT = pygame.font.Font(None, 36)
BG_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)
INPUT_COLOR = (50, 50, 50)

# 游戏文本内容
GAME_TEXTS = [
    "Welcome, adventurer! You find yourself in a dark forest. What will you do?",
    "You hear a rustling noise behind you. It's getting closer. What is your next move?",
    "A mysterious figure steps out of the shadows. They speak to you: 'Who are you?'"
]

# 初始化变量
chat_log = []
current_step = 0
input_text = ""
run_game = True

# 定义渲染文本函数
def render_text(text, x, y, color=TEXT_COLOR):
    text_surface = FONT.render(text, True, color)
    screen.blit(text_surface, (x, y))

# 主游戏循环
while run_game:
    screen.fill(BG_COLOR)

    # 显示聊天日志
    y_offset = 20
    for line in chat_log[-10:]:  # 显示最后 10 条记录
        render_text(line, 20, y_offset)
        y_offset += 40

    # 显示输入框
    pygame.draw.rect(screen, INPUT_COLOR, (20, HEIGHT - 60, WIDTH - 40, 40))
    render_text(input_text, 30, HEIGHT - 50)

    # 事件处理
    for event in pygame.event.get():
        if event.type == QUIT:
            run_game = False

        elif event.type == KEYDOWN:
            if event.key == K_RETURN:
                if input_text.strip():
                    # 添加玩家输入到聊天日志
                    chat_log.append(f"You: {input_text.strip()}")

                    # 添加游戏生成内容
                    if current_step < len(GAME_TEXTS):
                        chat_log.append(GAME_TEXTS[current_step])
                        current_step += 1
                    else:
                        chat_log.append("The game has ended. Thank you for playing!")

                    input_text = ""

            elif event.key == K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode

    # 更新显示
    pygame.display.flip()

# 退出游戏
pygame.quit()
'''