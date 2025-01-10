import asyncio
from pygame import *
from GameManagers.BGMPlayer import BGMPlayer
from Characters.Player import *
from Characters.NPC import *
from Characters.Enemies import *
from Scenes.Rooms import *
from Scenes.MainMenu import MainMenu
from Scenes.MainMenu import bossHealthBarIcon
from Scenes.GameWin import GameWin
from Scenes.Heart import *
from Scenes.bosshp import bossheart
from Scenes.shop import *
from Scenes.UI import *


class GameManager:
    # just an alias
    def get_keys(self):
        return pygame.key.get_pressed()

    # Awake()
    def __init__(self):
        self.set_screen()
        self.set_icon()
        self.set_room()
        self.set_issac()
        self.set_npc()
        self.set_spawn_enemies()
        self.set_bgm()
        self.set_scenes()
        self.set_clock()
        self.set_heart()
        self.set_chatbox()
        self.set_boss()
        self.set_shop()
        self.set_UI()

    # SET
    def set_UI(self):
        self.UI = pygame.sprite.Group()
        self.coinsystem = coin()
        self.attacksystem = attack()
        self.bombsystem = Bomb()
        self.UI.add(self.coinsystem, self.attacksystem, self.bombsystem)

    def set_shop(self):
        self.lucky = pygame.sprite.Group()
        self._lucky = lucky()
        self._price = price()
        self.lucky.add(self._lucky, self._price)

    def set_boss(self):
        self.bossBody = BossBody()
        self.bossAttack = BossAttack()
        self.bloodyTears = pygame.sprite.Group()
        self.bosshpicon = pygame.sprite.Group()
        self.bosshpicon.add(bossHealthBarIcon())

    def set_spawn_enemies(self):
        self.enemy_group = pygame.sprite.Group()
        self.update_enemies_normal_state = "True"
        self.update_enemies_boss_state = "True"

    def set_heart(self):
        self.heart = pygame.sprite.GroupSingle()
        self._heart = Heart()
        self.heart.add(self._heart)

    def set_scenes(self):
        self.active_scene = Scenes.MAIN_MENU
        self.main_menu: pygame.sprite.Group = MainMenu()
        self.game_win: pygame.sprite.Group = GameWin()

    def set_clock(self):
        self.clock = pygame.time.Clock()

    def set_bgm(self):
        self.bgm_player = BGMPlayer()
        self.bgm_player.play("MAIN_THEME", -1)

    def set_issac(
        self,
        spawn_pos=(ScreenSettings.screenWidth / 2, ScreenSettings.screenHeight / 2),
    ):
        self.isaac_group = pygame.sprite.GroupSingle()
        self.isaac = Player(spawn_pos)
        self.isaac_group.add(self.isaac)

    def set_npc(self):
        self.npc_group = pygame.sprite.Group()
        self.npc1 = NPC()
        self.npc_group.add(self.npc1)

    def set_room(self):
        self.room_group = pygame.sprite.Group()
        self.room = StartRoom()
        self.room_group.add(self.room)
        self.new_room = None
        self.new_room_rect: pygame.Rect = None
        self.room_transitioning = False
        self.transition_speed_horizontal = 15
        self.transition_speed_vertical = 10

    def set_chatbox(self):
        self.Chatboxes = pygame.sprite.GroupSingle()
        chatbox = ChatBox()
        self.Chatboxes.add(chatbox)

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
        self.clock.tick(ScreenSettings.fps)
        asyncio.run(self.async_update())
        self.deal_events()
        self.update_scene(self.active_scene)
        pygame.display.flip()

    def update_sprites(self, sprites: sprite.Group, keys=None):
        sprites.update(keys)
        sprites.draw(self.screen)

    def update_enemies_normal(self):
        if self.update_enemies_normal_state == "True":
            for i in range(UpdateEnemiesSettings.flyNumber):
                self.enemy_group.add(Fly())
        self.update_enemies_normal_state = "False"

    def update_enemies_boss(self):
        if self.update_enemies_boss_state == "True":
            for i in range(UpdateEnemiesSettings.bossNumber):
                self.enemy_group.add(self.bossBody, self.bossAttack)
        self.update_enemies_boss_state = "False"

    def update_boss_spawn_fly(self):
        if self.bossAttack.if_spwan_fly == "True":
            self.bossAttack.if_spwan_fly = "False"
            for i in range(random.randint(1, 3)):
                self.enemy_group.add(
                    Fly_blood(self.bossAttack.rect.x, self.bossAttack.rect.y)
                )

    def update_boss_shoot(self):
        if self.bossAttack.if_shoot == "True":
            self.bossAttack.if_shoot = "False"
            vector_list1 = [
                (-1.732 / 2, -1 / 2),
                (-2 / 2, 0),
                (-1.732 / 2, 1 / 2),
                (-1 / 2, 1.732 / 2),
                (0, 2 / 2),
            ]
            vector_list2 = [
                (-1.732 / 2, 1 / 2),
                (-1 / 2, 1.732 / 2),
                (0, 2 / 2),
                (1 / 2, 1.732 / 2),
                (1.732 / 2, 1 / 2),
            ]
            vector_list3 = [
                (0, 2 / 2),
                (1 / 2, 1.732 / 2),
                (1.732 / 2, 1 / 2),
                (2 / 2, 0),
                (1.732 / 2, -1 / 2),
                (1 / 2, -1.732 / 2),
            ]
            if self.isaac.rect.x <= 462:
                vector_list = vector_list1
            elif self.isaac.rect.x >= 1280 - 462:
                vector_list = vector_list3
            else:
                vector_list = vector_list2
            for direction_x, direction_y in vector_list:
                self.bloodyTears.add(
                    BloodyTear(
                        self.bossAttack.rect.x,
                        self.bossAttack.rect.y,
                        direction_x,
                        direction_y,
                    )
                )

    def update_scene(self, active_scene: Scenes):
        match active_scene:

            case Scenes.MAIN_MENU:
                self.main_menu.update()
                self.main_menu.draw(self.screen)

            case Scenes.GAMEWIN:
                self.screen.fill((0, 0, 0))
                self.game_win.update()
                self.game_win.draw(self.screen)

            case Scenes.START_ROOM:
                # 制作每一关的刷怪时,注意调整图层关系(update顺序,让小怪在boss上面显示)
                self.update_enemies_boss()
                self.update_enemies_normal()
                self.update_boss_spawn_fly()
                self.update_boss_shoot()

                self.room_group.draw(self.screen)
                self.update_sprites(self.isaac_group, self.get_keys())
                self.update_sprites(self.npc_group, self.get_keys())

                self.lucky.update()
                self.lucky.draw(self.screen)

                self.enemy_group.update()
                self.enemy_group.draw(self.screen)
                self.isaac.tears.draw(self.screen)
                self.isaac.explosion_group.draw(self.screen)
                self.isaac.bomb_group.draw(self.screen)
                self.room.get_walls().draw(self.screen)
                self.heart.update()
                self.heart.draw(self.screen)

                self.bloodyTears.update()
                self.bloodyTears.draw(self.screen)

                # temp code
                bossheart.update(
                    self.screen,
                    BossSettings.health_bar.x,
                    BossSettings.health_bar.y,
                    BossSettings.health_bar.width,
                    BossSettings.health_bar.height,
                    self.bossBody.HP,
                    BossSettings.health_bar.max,
                )
                self.bosshpicon.update()
                self.bosshpicon.draw(self.screen)

                self.UI.update(self.screen)
                self.UI.draw(self.screen)

            case Scenes.CHAT_BOX:
                self.update_sprites(self.Chatboxes, self.get_keys())

    def deal_events(self):
        self.detect_collision()
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    exit()
                case Events.GAME_OVER:
                    pygame.quit()
                    exit()
                case Events.GAME_WIN:
                    self.active_scene = Scenes.GAMEWIN
                case Events.TO_MAIN:
                    self.bossBody.HP = 10
                    self.active_scene = Scenes.MAIN_MENU
                case Events.ROOM_CLEAR:
                    for door in self.room.get_doors():
                        door: Door
                        door.is_open = True
                case Events.MAIN_TO_STARTROOM:
                    self.active_scene = Scenes.START_ROOM
                    self.bgm_player.stop()
                    # self.bgm_player.play("STARTROOM", -1)    # need bgm here , can be a common bgm for all rooms
                case Events.TO_CHATBOX:
                    self.active_scene = Scenes.CHAT_BOX
                case Events.EXIT_CHATBOX:
                    self.active_scene = Scenes.START_ROOM
                case Events.BOMB_EXPLOSION:
                    self.bombsystem.bomb_num -= 1
                    pos = event.pos
                    radius = event.radius
                    for group in [
                        self.enemy_group,
                        self.npc_group,
                        self.room.get_walls(),
                    ]:
                        for entity in group:
                            if Vector2(entity.rect.center).distance_to(pos) <= radius:
                                entity.HP -= 3
                                if isinstance(entity, Wall):
                                    entity.destroyed()
                                else:
                                    entity.update()
                    for entity in self.isaac_group:
                        if Vector2(entity.rect.center).distance_to(pos) <= radius:
                            ev.post(ev.Event(Events.SLICE_ISAAC))
                case Events.SLICE_ISAAC:
                    self.Isaac_Body = Body(spawn_pos=self.isaac.rect.center)
                    self.Isaac_Head = Head(spawn_pos=self.isaac.rect.center)
                    self.isaac_group.empty()
                    self.isaac = self.Isaac_Body
                    self.isaac_group.add(self.isaac)
                    self.isaac_group.add(self.Isaac_Head)

    def detect_collision(self):
        self.detect_collision_isaac_and_walls()
        self.detect_collision_tears_and_walls()
        self.detect_collision_tears_and_enemies()
        self.detect_collision_isaac_and_npc()
        self.detect_collision_isaac_and_enemies()
        self.detect_collision_bloodytear_and_frames()
        self.detect_collision_bloodytear_and_isaac()
        self.detect_collision_lucky_and_isaac()
        self.detect_collision_boss_and_isaac()

    def detect_collision_boss_and_isaac(self):
        collided_boss_and_isaac = StaticMethods.mask_spritecollide(
            self.bossBody, self.isaac_group, False
        )
        if collided_boss_and_isaac:
            self.isaac.rect.move_ip(-self.isaac.movement)

    def detect_collision_lucky_and_isaac(self):
        collided_lucky_and_isaac = StaticMethods.mask_spritecollide(
            self.isaac, self.lucky, False
        )

        if self._lucky.state == "destroy":
            mode = random.choice(["heart", "attack", "coin"])
            if mode == "heart":
                if self._heart.HP < 4:
                    self._heart.HP += 2
                else:
                    self._heart.HP = PlayerSettings.PlayerHP
            if mode == "attack":
                self.isaac.attack += 1
                self.attacksystem.attack_num += 1
            if mode == "coin":
                self.coinsystem.coin_num += 3
            self._lucky.state = "normal"

        keys = pygame.key.get_pressed()
        if (
            self.coinsystem.coin_num >= 5
            and self._lucky.state == "normal"
            and keys[pygame.K_q]
            and pygame.sprite.spritecollide(self.isaac, self.lucky, False)
        ):
            self._lucky.state = "open"
            self.coinsystem.coin_num -= 5
        if StaticMethods.mask_spritecollide(self.isaac, self.lucky, False):
            self.isaac.rect.move_ip(-self.isaac.movement)

    def detect_collision_bloodytear_and_frames(self):
        collided_bloodytear_and_frames = pygame.sprite.groupcollide(
            self.bloodyTears, self.room.get_frame(), False, False
        )
        for bloodytear, frame in collided_bloodytear_and_frames.items():
            bloodytear.state = "die"

    def detect_collision_isaac_and_enemies(self):
        collided_isaac_and_enemies = StaticMethods.mask_spritecollide(
            self.isaac, self.enemy_group, False
        )
        if collided_isaac_and_enemies:
            for heart in self.heart:
                heart.state = "reduce"

    def detect_collision_bloodytear_and_isaac(self):
        collided_isaac_and_bloodytear = StaticMethods.mask_spritecollide(
            self.isaac, self.bloodyTears, False
        )

        for bloodytear in collided_isaac_and_bloodytear:

            if bloodytear.state == "live":
                for heart in self.heart:
                    heart.state = "reduce"
                bloodytear.state = "die"

    def detect_collision_tears_and_enemies(self):
        collided_tears_and_monsters = StaticMethods.mask_groupcollide(
            self.isaac.tears, self.enemy_group, False, False
        )
        for tear, enemies in collided_tears_and_monsters.items():
            for enemy in enemies:
                self.bgm_player.play("TEAR_HIT", 0)
                if tear.state == "live":
                    if enemy.HP > 0:
                        tear.state = "die"
                    enemy.HP -= self.isaac.attack
                    if enemy.state == "live" and enemy.HP <= 0:
                        self.coinsystem.coin_num += 1

    def detect_collision_tears_and_walls(self):
        collided_tears_and_walls = StaticMethods.mask_groupcollide(
            self.isaac.tears, self.room.get_walls(), False, False
        )
        for tear, walls in collided_tears_and_walls.items():
            tear: Tear  # once for all below, sweet
            for wall in walls:
                if tear.state == "live" and isinstance(wall, Shit):
                    wall.HP -= 1
                    self.bgm_player.play("TEAR_HIT", 0)
                    wall.destroyed()
            tear.state = "die"

        collided_tears_and_frames = pygame.sprite.groupcollide(
            self.isaac.tears, self.room.get_frame(), False, False
        )
        for tear, frame in collided_tears_and_frames.items():
            tear.state = "die"

    def detect_collision_isaac_and_walls(self):
        if (
            StaticMethods.mask_spritecollide(self.isaac, self.room.get_walls(), False)
        ) or pygame.sprite.spritecollide(self.isaac, self.room.get_frame(), False):
            self.isaac.rect.move_ip(-self.isaac.movement)

    def detect_collision_isaac_and_npc(self):
        if (
            abs(self.npc1.rect.x - self.isaac.rect.x) <= 20
            and abs(self.npc1.rect.x - self.isaac.rect.y) <= 20
        ):
            self.npc1.gen_chatbox(self.get_keys())

    async def detect_collision_isaac_and_doors(self):
        collided_isaac_and_doors = StaticMethods.mask_spritecollide(
            self.isaac, self.room.get_doors(), False
        )
        door_location_tag = None
        for door in collided_isaac_and_doors:
            door: Door

            door_location_tag = door.location_tag
            # door.is_open = True  # in event later
            if door.is_open:

                await self.gen_new_room(door.location_tag)
                await self.clear_old_room()
                self.room_transitioning = True
                door.is_open = False

        if self.room_transitioning:
            await self.room_transit(door_location_tag)

    async def clear_old_room(self):
        self.room.get_walls().empty()
        self.isaac_group.empty()
        self.npc_group.empty()
        self.enemy_group.empty()

    async def gen_new_room(self, door_location_tag: str):
        match door_location_tag:
            case "top":
                self.new_room_rect = pygame.Rect(
                    0,
                    -ScreenSettings.screenHeight,
                    ScreenSettings.screenWidth,
                    ScreenSettings.screenHeight,
                )
            case "bottom":
                self.new_room_rect = pygame.Rect(
                    0,
                    ScreenSettings.screenHeight,
                    ScreenSettings.screenWidth,
                    ScreenSettings.screenHeight,
                )
            case "left":
                self.new_room_rect = pygame.Rect(
                    -ScreenSettings.screenWidth,
                    0,
                    ScreenSettings.screenWidth,
                    ScreenSettings.screenHeight,
                )
            case "right":
                self.new_room_rect = pygame.Rect(
                    ScreenSettings.screenWidth,
                    0,
                    ScreenSettings.screenWidth,
                    ScreenSettings.screenHeight,
                )
        self.new_room = SingleRoom(rect=self.new_room_rect)
        self.room_group.add(self.new_room)

    async def room_transit(self, door_location_tag: str):

        self.screen.fill((0, 0, 0))  # clear screen

        match door_location_tag:
            case "top":
                self.room.rect.move_ip(0, self.transition_speed_vertical)
                self.new_room.rect.move_ip(0, self.transition_speed_vertical)
                if self.new_room_rect.top >= 0:
                    self.new_room_rect.top = 0
                    isaac_spawn_pos = (
                        ScreenSettings.screenWidth / 2,
                        ScreenSettings.screenHeight - 150,
                    )
                    await self.stop_transition(isaac_spawn_pos)

            case "bottom":
                self.room.rect.move_ip(0, -self.transition_speed_vertical)
                self.new_room.rect.move_ip(0, -self.transition_speed_vertical)
                if self.new_room_rect.top <= 0:
                    self.new_room_rect.top = 0
                    isaac_spawn_pos = (ScreenSettings.screenWidth / 2, 150)
                    await self.stop_transition(isaac_spawn_pos)

            case "left":
                self.room.rect.move_ip(self.transition_speed_horizontal, 0)
                self.new_room.rect.move_ip(self.transition_speed_horizontal, 0)
                if self.new_room_rect.left >= 0:
                    self.new_room_rect.left = 0
                    isaac_spawn_pos = (
                        ScreenSettings.screenWidth - 300,
                        ScreenSettings.screenHeight / 2,
                    )
                    await self.stop_transition(isaac_spawn_pos)

            case "right":
                self.room.rect.move_ip(-self.transition_speed_horizontal, 0)
                self.new_room.rect.move_ip(-self.transition_speed_horizontal, 0)
                if self.new_room_rect.left <= 0:
                    self.new_room_rect.left = 0
                    isaac_spawn_pos = (300, ScreenSettings.screenHeight / 2)
                    await self.stop_transition(isaac_spawn_pos)

    async def stop_transition(self, isaac_spawn_pos):
        self.room_transitioning = False
        self.room_group.remove(self.room)
        self.room_group.remove(self.new_room)
        self.room = self.new_room
        self.room_group.add(self.room)
        self.set_issac(isaac_spawn_pos)
        self.set_npc()
        self.set_spawn_enemies()

    # Coroutines
    async def async_update(self):
        await self.detect_collision_isaac_and_doors()
