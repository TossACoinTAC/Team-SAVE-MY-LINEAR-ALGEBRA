from pygame import *
from GameManagers.BGMPlayer import BGMPlayer
from Characters.Player import *
from Characters.NPC import *
from Characters.Enemies import *
from Scenes.Rooms import *
from Scenes.MainMenu import MainMenu


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
        self.set_spawn_monster()
        self.set_bgm()
        self.set_scenes()
        self.set_clock()

    # SET
    def set_scenes(self):
        self.active_scene = Scenes.MAIN_MENU
        self.main_menu: pygame.sprite.Group = MainMenu()

    def set_clock(self):
        self.clock = pygame.time.Clock()

    def set_bgm(self):
        self.bgm_player = BGMPlayer()
        self.bgm_player.play("MAIN_THEME", -1)

    def set_issac(self):
        self.isaac_group = pygame.sprite.GroupSingle()
        self.isaac = Player(
            spawn_pos=0.5
            * Vector2(ScreenSettings.screenWidth, ScreenSettings.screenHeight)
        )
        self.isaac_group.add(self.isaac)

    def set_npc(self):
        self.npc_group = pygame.sprite.Group()
        npc1 = NPC()
        self.npc_group.add(npc1)

    def set_room(self):
        self.room_group = pygame.sprite.Group()
        self.room = StartRoom()
        self.room_group.add(self.room)
        self.new_room = None

    def set_spawn_monster(self):
        self.enemy_group = pygame.sprite.Group()

        self.npc_group = pygame.sprite.GroupSingle()
        self.npc1 = NPC()
        self.npc_group.add(self.npc1)

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
    def render_screen(self):
        self.clock.tick(ScreenSettings.fps)
        self.update_scene(self.active_scene)
        pygame.display.flip()

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
                self.update_sprite(self.npc_group, self.get_keys())
                self.isaac.tears.draw(self.screen)
                self.isaac.explosion_group.draw(self.screen)
                self.isaac.bomb_group.draw(self.screen)
                self.room.get_walls().draw(self.screen)

            case Scenes.CHAT_BOX:
                self.update_sprite(self.Chatboxes, self.get_keys())

    def deal_events(self):
        self.detect_collision()
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    exit()
                case Events.GAME_OVER:
                    pass
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
                case Events.BOMB_EXPLOSION:
                    pos = event.pos
                    radius = event.radius
                    for group in [
                        self.enemy_group,
                        self.npc_group,
                        self.room.get_walls(),
                        self.isaac_group,
                    ]:
                        for entity in group:
                            if Vector2(entity.rect.center).distance_to(pos) <= radius:
                                entity.kill()

    def detect_collision(self):
        self.detect_collision_issac_and_walls()
        self.detect_collision_tears_and_walls()
        self.detect_collision_tears_and_monsters()

    def detect_collision_tears_and_monsters(self):
        collided_tears_and_monsters = StaticMethods.mask_groupcollide(
            self.isaac.tears, self.enemy_group, False, False
        )
        for tear, enemies in collided_tears_and_monsters.items():
            for enemy in enemies:
                if tear.state == "live":
                    enemy.HP -= 1
            tear.state = "die"

    def detect_collision_tears_and_walls(self):
        # detect tears-walls collision
        collided_tears_and_walls = StaticMethods.mask_groupcollide(
            self.isaac.tears, self.room.get_walls(), False, False
        )
        for tear, walls in collided_tears_and_walls.items():
            tear: Tear  # once for all below, sweet
            for wall in walls:
                if tear.state == "live" and isinstance(wall, Shit):
                    wall.destroyed()
            tear.state = "die"

        collided_tears_and_frames = pygame.sprite.groupcollide(
            self.isaac.tears, self.room.get_frame(), False, False
        )
        for tear, frame in collided_tears_and_frames.items():
            tear.state = "die"

    def detect_collision_issac_and_walls(self):
        if (
            StaticMethods.mask_spritecollide(self.isaac, self.room.get_walls(), False)
        ) or pygame.sprite.spritecollide(self.isaac, self.room.get_frame(), False):
            self.isaac.rect.move_ip(-self.isaac.movement)

        collided_isaac_and_doors = StaticMethods.mask_spritecollide(
            self.isaac, self.room.get_doors(), False
        )
        for door in collided_isaac_and_doors:
            door: Door
            if door.is_open:
                pass
            print(door.location_tag)

        # detect tears-walls collision
        collided_tears_and_walls = StaticMethods.mask_groupcollide(
            self.isaac.tears, self.room.get_walls(), False, False
        )
        for tear, walls in collided_tears_and_walls.items():
            tear: Tear  # once for all below, sweet
            tear.state = "die"
            for wall in walls:
                if isinstance(wall, Shit):
                    wall.destroyed()

        collided_tears_and_frames = pygame.sprite.groupcollide(
            self.isaac.tears, self.room.get_frame(), False, False
        )
        for tear, frame in collided_tears_and_frames.items():
            tear.state = "die"

        # detect isaac-npc collision
        if (
            abs(self.npc1.rect.x - self.isaac.rect.x) <= 10
            and abs(self.npc1.rect.x - self.isaac.rect.y) <= 10
        ):
            self.npc1.gen_chatbox()
