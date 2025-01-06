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
        self.clock = pygame.time.Clock()
        self.bgm_player = BGMPlayer()
        self.bgm_player.play("MAIN_THEME", -1)

        self.active_scene = Scenes.MAIN_MENU

        self.isaac_group = pygame.sprite.GroupSingle()
        self.isaac = Player(
            spawn_pos=0.5
            * Vector2(ScreenSettings.screenWidth, ScreenSettings.screenHeight)
        )
        self.isaac_group.add(self.isaac)

        self.main_menu: pygame.sprite.Group = MainMenu()

        self.room_group = pygame.sprite.GroupSingle()
        self.room = StartRoom()
        self.room_group.add(self.room)

        self.enemy_group = pygame.sprite.Group()

        self.npc_group = pygame.sprite.Group()
        npc1 = NPC()
        self.npc_group.add(npc1)

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
                self.room.get_walls().draw(self.screen)

    def deal_events(self):
        self.detect_collision()
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    exit()
                case Events.MAIN_TO_STARTROOM:
                    self.active_scene = Scenes.START_ROOM
                    self.bgm_player.stop()
                    # self.bgm_player.play("STARTROOM", -1)    # need bgm here , can be a common bgm for all rooms

    def detect_collision(self):
        # detect isaac-walls collision
        collided_isaac_and_doors = pygame.sprite.spritecollide(
            self.isaac, self.room.get_doors(), False
        )
        if (
            pygame.sprite.spritecollide(self.isaac, self.room.get_walls(), False)
            or pygame.sprite.spritecollide(self.isaac, self.room.get_frame(), False)
            or collided_isaac_and_doors
        ):
            self.isaac.rect.move_ip(-self.isaac.movement)
        for door in collided_isaac_and_doors:
            door: Door
            print(door.location_tag)

        # detect tears-walls collision
        collided_tears_and_walls = pygame.sprite.groupcollide(
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
        collided_tears_and_doors = pygame.sprite.groupcollide(
            self.isaac.tears, self.room.get_doors(), False, False
        )
        for tear, doors in collided_tears_and_doors.items():
            tear.state = "die"
