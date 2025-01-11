import asyncio
from pygame import *
from GameManagers.BGMPlayer import BGMPlayer
from Characters.Player import *
from Characters.Trainer import *
from Characters.Enemies import *
from Scenes.Rooms import *
from Scenes.shop import *
from Scenes.MainMenu import MainMenu
from Scenes.MainMenu import bossHealthBarIcon
from Scenes.GameWin import GameWin
from Scenes.GameOver import GameOver
from UI.UI import *
from UI.Heart import *
from UI.bosshp import bossheart


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
        self.set_trainer()
        self.set_bgm()
        self.set_scenes()
        self.set_clock()
        self.set_heart()
        self.set_chatbox()
        self.set_boss()
        self.set_UI()
        self.set_bloods()
        self.lucky = pygame.sprite.Group()
        self._lucky = lucky()
        self.enemy_group = pygame.sprite.Group()
        self.bugs = pygame.sprite.Group()
        self.boss_group = pygame.sprite.Group()
        self.room_clear_posted = False

    # SET
    def set_bloods(self):
        self.bloods = pygame.sprite.Group()

    def set_UI(self):
        self.UI = pygame.sprite.Group()
        self.coinsystem = coin()
        self.attacksystem = attack()
        self.bombsystem = Bomb()
        self.Room_hint_system = Room_hint(BossRoom_location, 1)
        self.UI.add(
            self.coinsystem, self.attacksystem, self.bombsystem, self.Room_hint_system
        )

    def set_shop(self):
        self._lucky = lucky()
        self._price = price()
        self.lucky.add(self._lucky, self._price)

    def set_boss(self):
        self.bossBody = BossBody()
        self.bossAttack = BossAttack()
        self.bloodyTears = pygame.sprite.Group()
        self.bosshpicon = pygame.sprite.Group()
        self.bosshpicon.add(bossHealthBarIcon())

    def set_heart(self):
        self.heart = pygame.sprite.GroupSingle()
        self._heart = Heart()
        self.heart.add(self._heart)

    def set_scenes(self):
        self.active_scene = Scenes.MAIN_MENU
        self.main_menu: pygame.sprite.Group = MainMenu()
        self.game_win: pygame.sprite.Group = GameWin()
        self.game_over: pygame.sprite.Group = GameOver()

    def set_clock(self):
        self.clock = pygame.time.Clock()

    def set_bgm(self):
        self.bgm_player = BGMPlayer()
        self.bgm_player.switch_BGM("MAIN_THEME")

    def set_issac(
        self,
        spawn_pos=(ScreenSettings.screenWidth / 2, ScreenSettings.screenHeight / 2),
    ):
        self.isaac_group = pygame.sprite.Group()  # Isaac may be sliced
        self.isaac = Player(spawn_pos)
        self.isaac_group.add(self.isaac)

    def set_trainer(self):
        self.trainer_group = pygame.sprite.Group()
        self.trainer = Trainer()
        self.trainer_group.add(self.trainer)

    def set_room(self):
        self.room_group = pygame.sprite.Group()
        self.room = StartRoom(RoomID=1)
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

    def spawn_enemies(self):
        self.bug1 = bug()
        self.bug2 = bug()
        self.enemy_group.add(self.bug1, self.bug2)
        self.bugs.add(self.bug1, self.bug2)
        for i in range(UpdateEnemiesSettings.flyNumber):
            self.enemy_group.add(Fly())

    def spawn_boss(self):
        for i in range(UpdateEnemiesSettings.bossNumber):
            self.boss_group.add(self.bossBody, self.bossAttack)
        for i in range(random.randint(1, 3)):
            self.boss_group.add(
                Fly_blood(self.bossAttack.rect.x, self.bossAttack.rect.y)
            )

    # Update()
    def update(self):
        self.clock.tick(ScreenSettings.fps)
        asyncio.run(self.async_update())
        self.deal_events()
        self.update_scene(self.active_scene)
        pygame.display.flip()

    def update_sprites(self, sprites: sprite.Group, keys=None):
        if not keys:
            sprites.update()
        else:
            sprites.update(keys)
        sprites.draw(self.screen)

    def common_scene_updates(self):
        self.update_sprites(self.room_group)
        self.update_sprites(self.bloods)
        self.update_sprites(self.room.get_walls())
        self.update_sprites(self.isaac_group, self.get_keys())
        self.update_sprites(self.isaac.explosion_group)
        self.update_sprites(self.isaac.bomb_group)
        self.update_sprites(self.isaac.tears)

        # UI
        self.heart.update()
        self.heart.draw(self.screen)
        self.UI.update(self.screen)
        self.UI.draw(self.screen)

    def update_scene(self, active_scene: Scenes):
        match active_scene:

            case Scenes.MAIN_MENU:
                self.main_menu.update()
                self.main_menu.draw(self.screen)

            case Scenes.GAMEOVER:
                self.screen.fill((0, 0, 0))
                self.game_over.update()
                self.game_over.draw(self.screen)

            case Scenes.GAMEWIN:
                self.screen.fill((0, 0, 0))
                self.game_win.update()
                self.game_win.draw(self.screen)

            # 制作每一关的刷怪时,注意调整图层关系(update顺序,让小怪在boss上面显示)
            case Scenes.START_ROOM:
                self.common_scene_updates()
                if not self.room_clear_posted:
                    ev.post(ev.Event(Events.ROOM_CLEAR))

            case Scenes.COMMON_ROOM | Scenes.BLUEWOMB | Scenes.SECRET:

                self.common_scene_updates()
                self.update_sprites(self.enemy_group)

                if len(self.enemy_group) == 0 and not self.room_clear_posted:
                    ev.post(ev.Event(Events.ROOM_CLEAR))

            case Scenes.TREASURE:
                self.common_scene_updates()
                self.update_sprites(self.trainer_group, self.get_keys())
                if not self.room_clear_posted:
                    ev.post(ev.Event(Events.ROOM_CLEAR))

            case Scenes.SHOP:
                self.common_scene_updates()
                self.update_sprites(self.lucky)
                if not self.room_clear_posted:
                    ev.post(ev.Event(Events.ROOM_CLEAR))

            # BossRoom
            case Scenes.CATACOMB:
                self.common_scene_updates()
                self.update_sprites(self.boss_group)
                self.update_boss_shoot()
                self.update_sprites(self.bloodyTears)
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

            case Scenes.CHAT_BOX:
                self.update_sprites(self.Chatboxes, self.get_keys())

    def update_boss_shoot(self):
        if self.bossAttack.if_shoot == "True":
            self.enemy_group.add(Fly_blood(self.bossAttack.rect.x, self.bossAttack.rect.y))
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

    def deal_events(self):
        self.detect_collision()
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    exit()
                case Events.GAME_OVER:
                    self.active_scene = Scenes.GAMEOVER
                case Events.GAME_WIN:
                    self.active_scene = Scenes.GAMEWIN
                case Events.RESTART:
                    self.bgm_player.stop_BGM()
                    self.__init__()

                case Events.MAIN_TO_STARTROOM:
                    self.active_scene = Scenes.START_ROOM
                    self.bgm_player.switch_BGM("COMMON")

                case Events.ROOM_CLEAR:
                    self.room.open_doors()
                    self.bgm_player.play_sound_effect("DOOR_OPEN")
                    self.room_clear_posted = True

                case Events.TO_CHATBOX:
                    self.active_scene = Scenes.CHAT_BOX

                case Events.EXIT_CHATBOX:
                    self.active_scene = Scenes.TREASURE

                case Events.BOMB_EXPLOSION:
                    self.bombsystem.bomb_num -= 1
                    pos = event.pos
                    radius = event.radius
                    for group in [
                        self.enemy_group,
                        self.boss_group,
                        self.trainer_group,
                        self.room.get_walls(),
                    ]:
                        for entity in group:
                            if isinstance(entity, BossBody):
                                if (
                                    Vector2(entity.rect.center).distance_to(pos)
                                    <= radius * 2
                                ):
                                    entity.HP -= 10
                                    entity.update()
                            elif Vector2(entity.rect.center).distance_to(pos) <= radius:
                                entity.HP -= 3
                                if isinstance(entity, Wall):
                                    entity.destroyed()
                                else:
                                    entity.update()
                    for entity in self.isaac_group:
                        if Vector2(entity.rect.center).distance_to(pos) <= radius:
                            self._heart.HP -= 2
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
        match self.active_scene:
            case Scenes.COMMON_ROOM | Scenes.BLUEWOMB | Scenes.SECRET:
                self.detect_collision_isaac_and_enemies()
                self.detect_collision_tears_and_enemies()
                self.detect_collision_bug_and_wall()
            case Scenes.SHOP:
                self.detect_collision_lucky_and_isaac()
            case Scenes.TREASURE:
                self.detect_collision_isaac_and_trainer()
                self.detect_buff_acquirance()
            case Scenes.CATACOMB:
                self.detect_collision_bloodytear_and_frames()
                self.detect_collision_bloodytear_and_isaac()
                self.detect_collision_boss_and_isaac()
                self.detect_collision_tears_and_enemies()

    def detect_collision_bug_and_wall(self):
        collided_bug_and_wall = StaticMethods.mask_groupcollide(
            self.bugs, self.room.get_walls(), False, False
        )
        for bug, walls in collided_bug_and_wall.items():
            if bug.move_direction == "left":
                bug.move_direction = "right"
            elif bug.move_direction == "right":
                bug.move_direction = "left"
            elif bug.move_direction == "up":
                bug.move_direction = "down"
            elif bug.move_direction == "down":
                bug.move_direction = "up"

    def detect_collision_boss_and_isaac(self):
        collided_boss_and_isaac = StaticMethods.mask_spritecollide(
            self.isaac, self.boss_group, False
        )
        if collided_boss_and_isaac:
            self.isaac.rect.move_ip(-self.isaac.movement)

    def detect_collision_lucky_and_isaac(self):

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
            # and StaticMethods.mask_spritecollide(self.isaac, self.lucky, False)
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
        collided_isaac_and_boss = StaticMethods.mask_spritecollide(
            self.isaac, self.boss_group, False
        )
        for enemy in collided_isaac_and_enemies:

            if enemy.state == 'live':
                for heart in self.heart:
                    heart.state = "reduce"

        if self.bossBody.state == 'live' and collided_isaac_and_boss:
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
        collided_tears_and_monsters: dict = StaticMethods.mask_groupcollide(
            self.isaac.tears, self.enemy_group, False, False
        )
        collided_tears_and_monsters.update(
            StaticMethods.mask_groupcollide(
                self.isaac.tears, self.boss_group, False, False
            )
        )
        for tear, enemies in collided_tears_and_monsters.items():
            for enemy in enemies:
                enemy: Monster
                if tear.state == "live" and enemy.HP > 0:
                    tear.state = "die"
                    self.bgm_player.play_sound_effect("TEAR_HIT")
                    enemy.HP -= self.isaac.attack
                    if enemy.state == "live" and enemy.HP <= 0:
                        self.coinsystem.coin_num += 1
                        num = random.choice([0, 1, 2, 3, 4, 5])
                        self.bloods.add(blood(enemy.rect.x, enemy.rect.y, num))
                        enemy.state = "die"
                        print(enemy.HP)

    def detect_collision_tears_and_walls(self):
        collided_tears_and_walls = StaticMethods.mask_groupcollide(
            self.isaac.tears, self.room.get_walls(), False, False
        )
        for tear, walls in collided_tears_and_walls.items():
            tear: Tear  # once for all below, sweet
            if tear.state == "live":
                self.bgm_player.play_sound_effect("TEAR_HIT")
                tear.state = "die"
                for wall in walls:
                    if isinstance(wall, Shit):
                        wall.HP -= self.isaac.attack
                        wall.destroyed()

        collided_tears_and_frames = pygame.sprite.groupcollide(
            self.isaac.tears, self.room.get_frame(), False, False
        )
        for tear, frame in collided_tears_and_frames.items():
            if tear.state == "live":
                self.bgm_player.play_sound_effect("TEAR_HIT")
                tear.state = "die"

    def detect_collision_isaac_and_walls(self):
        if StaticMethods.mask_spritecollide(self.isaac, self.room.get_walls(), False):
            self.isaac.rect.move_ip(-self.isaac.movement)
        if (
            self.isaac.rect.left <= ScreenSettings.marginWidth + 10
            or self.isaac.rect.right
            >= ScreenSettings.screenWidth - ScreenSettings.marginWidth - 10
            or self.isaac.rect.top <= ScreenSettings.marginHeight + 10
            or self.isaac.rect.bottom
            >= ScreenSettings.screenHeight - ScreenSettings.marginHeight - 10
        ):
            self.isaac.rect.move_ip(-self.isaac.movement)

    def detect_collision_isaac_and_trainer(self):
        if StaticMethods.mask_spritecollide(self.isaac, self.trainer_group, False):
            self.isaac.rect.move_ip(-self.isaac.movement)
        if pygame.sprite.spritecollide(self.isaac, self.trainer_group, False):
            if self.get_keys()[pygame.K_q]:
                ev.post(ev.Event(Events.TO_CHATBOX))

    def detect_buff_acquirance(self):
        for chatbox in self.Chatboxes:
            if chatbox.buff == 1:
                if self._heart.HP < 4:
                    self._heart.HP += 2
                else:
                    self._heart.HP = PlayerSettings.PlayerHP
            if chatbox.buff == 2:
                self.isaac.shoot_mode = 1
            if chatbox.buff == 3:
                self._heart.HP -= 1
            chatbox.buff = 0

    async def detect_collision_isaac_and_doors(self):
        collided_isaac_and_doors = StaticMethods.mask_spritecollide(
            self.isaac, self.room.get_doors(), False
        )
        door_location_tag = None
        for door in collided_isaac_and_doors:
            door: Door

            door_location_tag = door.location_tag
            door_type = door.type_tag
            if door.is_open:
                await self.gen_new_room(self.room.RoomID, door.location_tag, door_type)
                await self.clear_old_room()
                self.room_transitioning = True
                door.is_open = False

        if self.room_transitioning:
            await self.room_transit(door_location_tag)

    async def clear_old_room(self):
        self.room.get_walls().empty()
        self.isaac_group.empty()
        self.trainer_group.empty()
        self.enemy_group.empty()
        self.boss_group.empty()
        self.lucky.empty()
        self.bloods.empty()

    async def gen_new_room(self, roomID: int, door_location_tag: str, door_type: str):
        match door_location_tag:
            case "top":
                self.new_room_rect = pygame.Rect(
                    0,
                    -ScreenSettings.screenHeight,
                    ScreenSettings.screenWidth,
                    ScreenSettings.screenHeight,
                )
                roomID = int(roomID / 2)
            case "bottom":
                self.new_room_rect = pygame.Rect(
                    0,
                    ScreenSettings.screenHeight,
                    ScreenSettings.screenWidth,
                    ScreenSettings.screenHeight,
                )
                roomID = roomID * 2
            case "left":
                self.new_room_rect = pygame.Rect(
                    -ScreenSettings.screenWidth,
                    0,
                    ScreenSettings.screenWidth,
                    ScreenSettings.screenHeight,
                )
                roomID = int((roomID - 1) / 2)
            case "right":
                self.new_room_rect = pygame.Rect(
                    ScreenSettings.screenWidth,
                    0,
                    ScreenSettings.screenWidth,
                    ScreenSettings.screenHeight,
                )
                roomID = roomID * 2 + 1

        self.Room_hint_system.current_room = roomID

        match door_type:
            case "Wood":
                if roomID == 1:
                    self.new_room = StartRoom(RoomID=roomID, rect=self.new_room_rect)
                    self.active_scene = Scenes.START_ROOM
                else:
                    self.new_room = CommonRoom(RoomID=roomID, rect=self.new_room_rect)
                    self.active_scene = Scenes.COMMON_ROOM
            case "BlueWomb":
                self.new_room = BlueWomb(RoomID=roomID, rect=self.new_room_rect)
                self.active_scene = Scenes.BLUEWOMB
            case "Shop":
                self.new_room = Shop(RoomID=roomID, rect=self.new_room_rect)
                self.active_scene = Scenes.SHOP
            case "Treasure":
                self.new_room = TreasureRoom(RoomID=roomID, rect=self.new_room_rect)
                self.active_scene = Scenes.TREASURE
            case "Secret":
                self.new_room = SecretRoom(RoomID=roomID, rect=self.new_room_rect)
                self.active_scene = Scenes.SECRET
            case "Catacomb":
                self.new_room = BossRoom(RoomID=roomID, rect=self.new_room_rect)
                self.active_scene = Scenes.CATACOMB
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
                        ScreenSettings.screenHeight - 150 - 10,
                    )
                    await self.stop_transition(isaac_spawn_pos)

            case "bottom":
                self.room.rect.move_ip(0, -self.transition_speed_vertical)
                self.new_room.rect.move_ip(0, -self.transition_speed_vertical)
                if self.new_room_rect.top <= 0:
                    self.new_room_rect.top = 0
                    isaac_spawn_pos = (ScreenSettings.screenWidth / 2, 150 + 10)
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
        match self.active_scene:
            case Scenes.COMMON_ROOM | Scenes.BLUEWOMB | Scenes.SECRET:
                self.spawn_enemies()
            case Scenes.CATACOMB:
                self.spawn_boss()
            case Scenes.SHOP:
                self.set_shop()
            case Scenes.TREASURE:
                self.set_trainer()
        self.room_clear_posted = False
        self.bgm_player.get_BGM_current_pos()
        self.bgm_player.play_BGM()

    # Coroutines
    async def async_update(self):
        await self.detect_collision_isaac_and_doors()
