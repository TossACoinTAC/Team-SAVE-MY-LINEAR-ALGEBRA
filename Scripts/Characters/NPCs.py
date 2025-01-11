from pygame import *
from Statics import *
from Characters.LLM import *
import pygame.event as ev


class NPC(pygame.sprite.Sprite):
    def __init__(self, image_path: str):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(
            self.image, (PlayerSettings.playerWidth, PlayerSettings.playerHeight)
        )
        self.rect = self.image.get_rect()
        self.HP = 0x3F3F3F3F  # 无敌


class Trainer(NPC):
    def __init__(self):
        super().__init__(ImportedImages.NPCImage)
        self.rect.center = (
            0.6 * ScreenSettings.screenWidth,
            0.5 * ScreenSettings.screenHeight,
        )


class Merchant(NPC):
    def __init__(self):
        super().__init__(ImportedImages.NPCImage)
        self.rect.center = (
            0.4 * ScreenSettings.screenWidth,
            0.5 * ScreenSettings.screenHeight,
        )


class ChatBox(pygame.sprite.Sprite):
    def __init__(self, npc_type: str):
        super().__init__()

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
        self.npc_type = npc_type
        if self.npc_type == "Trainer":
            self.messages = NPC_Original_messages.npc_message[0]
        elif self.npc_type == "Merchant":
            self.messages = NPC_Original_messages.npc_message[1]

        # 定义字体和颜色
        pygame.font.init()
        self.FONT = pygame.font.Font(None, 36)
        self.BG_COLOR = (30, 30, 30)  # 背景色
        self.INPUT_COLOR = (50, 50, 50)  # 输入框颜色

        # 初始文本内容
        if self.npc_type == "Trainer":
            self.INIT_TEXTS = (
                "Welcome, brave adventurer! I sense that you are seeking a challenge worthy of your mettle."
                "As the guardian of this fortress, it is my duty to test your wits and abilities."
                "Type 'exit' or 'quit' to end the chat."
            )
        elif self.npc_type == "Merchant":
            self.INIT_TEXTS = "Type 'exit' or 'quit' to end the chat."
        self.chat_log.append(self.INIT_TEXTS)

        self.linenumber = 2
        self.y_offset = 20

        self.buff = 0

    def render_text(self, text, x, y, color=(255, 255, 255)):
        text_surface = self.FONT.render(text, True, color)
        self.image.blit(text_surface, (x, y))

    def update(self, keys, player_state: dict):
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

        self.handle_input(keys, player_state)
        self.render_wrapped_text(self.input_text, 30, ScreenSettings.screenHeight - 50)

    def handle_input(self, keys, player_state: dict):
        inputed = False
        if keys[pygame.K_RETURN]:
            if self.input_text.strip() and self.allow_input:
                # 添加玩家输入到聊天日志
                self.chat_log.append(f"You: {self.input_text.strip()}")

                # 调用 LLM_chat 函数获取回复
                response = LLM_chat(self.input_text.strip(), self.messages)
                # print(response)
                self.chat_log.append(f"NPC: {response}")

                if (
                    "quit" in self.input_text.strip()
                    or "exit" in self.input_text.strip()
                ):
                    for sprite in self.groups():
                        if isinstance(sprite, ChatBox):
                            sprite.kill()
                    ev.post(ev.Event(Events.EXIT_CHATBOX))
                    # self.kill()

                if "EXTRA BLOOD" in response:
                    self.buff = 1
                if "MORE BULLETS" in response:
                    self.buff = 2
                if "PUNISHMENT" in response:
                    self.buff = 3

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
