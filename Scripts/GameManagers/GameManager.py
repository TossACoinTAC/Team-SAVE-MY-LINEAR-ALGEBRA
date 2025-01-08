from pygame import *
from GameManagers.BGMPlayer import BGMPlayer
from Characters.Player import *
from Characters.NPC import *
from Characters.Enemies import *
from Scenes.Rooms import *
from Scenes.MainMenu import MainMenu
from Scenes.MainMenu import bossHealthBarIcon
from Scenes.Heart import *
from Scenes.bosshp import bossheart

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

    # SET
    def set_boss(self):
        self.bossBody = BossBody()
        self.bossAttack = BossAttack()
        self.bloodyTears = pygame.sprite.Group()
        self.bosshpicon = pygame.sprite.Group()
        self.bosshpicon.add(bossHealthBarIcon())


    def set_spawn_enemies(self):
        self.enemy_group = pygame.sprite.Group()
        self.update_enemies_normal_state = 'True'
        self.update_enemies_boss_state = 'True'

    def set_heart(self):
        self.heart = pygame.sprite.GroupSingle()
        self._heart = Heart() 
        self.heart.add(self._heart)
    
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
        self.isaac = Player(spawn_pos = (640, 600))
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
    def render_screen(self):
        self.clock.tick(ScreenSettings.fps)
        self.update_scene(self.active_scene)
        pygame.display.flip()

    def update_sprite(self, sprite: sprite.GroupSingle, keys=None):
        sprite.update(keys)
        sprite.draw(self.screen)
    
    def update_enemies_normal(self):
        if self.update_enemies_normal_state == 'True':
            for i in range(UpdateEnemiesSettings.flyNumber):
                self.enemy_group.add(Fly())
        self.update_enemies_normal_state = 'False'

    def update_enemies_boss(self):
        if self.update_enemies_boss_state == 'True':
            for i in range(UpdateEnemiesSettings.bossNumber):
                self.enemy_group.add(self.bossBody, self.bossAttack)
        self.update_enemies_boss_state = 'False'

    def update_boss_spawn_fly(self):
        if self.bossAttack.if_spwan_fly == 'True':
            self.bossAttack.if_spwan_fly = 'False'
            for i in range(random.randint(3, 5)):
                self.enemy_group.add(Fly_blood(self.bossAttack.rect.x, self.bossAttack.rect.y))

    def update_boss_shoot(self):
        if self.bossAttack.if_shoot == 'True':
            self.bossAttack.if_shoot = 'False'
            vector_list1 = [(-1.732/2, -1/2), (-2/2, 0), (-1.732/2, 1/2), (-1/2, 1.732/2), (0, 2/2)]
            vector_list2 = [(-1.732/2, 1/2), (-1/2, 1.732/2), (0, 2/2), (1/2, 1.732/2),(1.732/2, 1/2)]
            vector_list3 = [(0, 2/2), (1/2, 1.732/2),(1.732/2, 1/2),(2/2, 0), (1.732/2, -1/2),(1/2, -1.732/2)]
            if self.isaac.rect.x <= 462:
                vector_list = vector_list1
            elif self.isaac.rect.x >= 1280 - 462:
                vector_list = vector_list3
            else:
                vector_list = vector_list2
            for (direction_x, direction_y) in vector_list:
                self.bloodyTears.add(BloodyTear(self.bossAttack.rect.x, self.bossAttack.rect.y, direction_x, direction_y))
            
    def update_scene(self, active_scene: Scenes):
        match active_scene:

            case Scenes.MAIN_MENU:
                self.main_menu.update()
                self.main_menu.draw(self.screen)

            case Scenes.START_ROOM:
                #制作每一关的刷怪时,注意调整图层关系(update顺序,让小怪在boss上面显示)
                self.update_enemies_boss()
                self.update_enemies_normal()
                self.update_boss_spawn_fly()
                self.update_boss_shoot()

                self.update_sprite(self.room_group)
                self.update_sprite(self.isaac_group, self.get_keys())
                self.update_sprite(self.npc_group, self.get_keys())
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

                #temp code
                bossheart.update(self.screen, BossSettings.health_bar.x, BossSettings.health_bar.y, BossSettings.health_bar.width, BossSettings.health_bar.height, self.bossBody.HP, BossSettings.health_bar.max)
                self.bosshpicon.update()
                self.bosshpicon.draw(self.screen)

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
                case Events.EXIT_CHATBOX:
                    self.active_scene = Scenes.START_ROOM
                case Events.BOMB_EXPLOSION:
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
                            for heart in self.heart:
                                heart.state = 'reduce'

    def detect_collision(self):
        self.detect_collision_isaac_and_walls()
        self.detect_collision_tears_and_walls()
        self.detect_collision_tears_and_enemies()
        self.detect_collision_isaac_and_npc()
        self.detect_collision_isaac_and_enemies()
        self.detect_collision_bloodytear_and_frames()
        self.detect_collision_bloodytear_and_isaac()

    def detect_collision_bloodytear_and_frames(self):
        collided_bloodytear_and_frames = pygame.sprite.groupcollide(
            self.bloodyTears, self.room.get_frame(), False, False)
        for bloodytear, frame in collided_bloodytear_and_frames.items():
            bloodytear.state = "die"
    
    def detect_collision_isaac_and_enemies(self):
        collided_isaac_and_enemies = StaticMethods.mask_spritecollide(
            self.isaac, self.enemy_group, False)
        if collided_isaac_and_enemies:
            for heart in self.heart:
                heart.state = 'reduce'

    def detect_collision_bloodytear_and_isaac(self):
        collided_isaac_and_bloodytear = StaticMethods.mask_spritecollide(
            self.isaac, self.bloodyTears, False)

        for bloodytear in collided_isaac_and_bloodytear:

            if bloodytear.state == 'live':
                for heart in self.heart:
                    heart.state = 'reduce'
                bloodytear.state = 'die'

    def detect_collision_tears_and_enemies(self):
        collided_tears_and_monsters = StaticMethods.mask_groupcollide(
            self.isaac.tears, self.enemy_group, False, False
        )
        for tear, enemies in collided_tears_and_monsters.items():
            for enemy in enemies:
                if tear.state == "live":
                    if enemy.HP > 0:
                        tear.state = "die"
                    enemy.HP -= 1


    def detect_collision_tears_and_walls(self):
 
        collided_tears_and_walls = StaticMethods.mask_groupcollide(
            self.isaac.tears, self.room.get_walls(), False, False
        )
        for tear, walls in collided_tears_and_walls.items():
            tear: Tear  # once for all below, sweet
            for wall in walls:
                if tear.state == "live" and isinstance(wall, Shit):
                    wall.HP -= 1
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

        collided_isaac_and_doors = StaticMethods.mask_spritecollide(
            self.isaac, self.room.get_doors(), False
        )
        for door in collided_isaac_and_doors:
            door: Door
            if door.is_open:
                pass


    def detect_collision_isaac_and_npc(self):
        if (
            abs(self.npc1.rect.x - self.isaac.rect.x) <= 20
            and abs(self.npc1.rect.x - self.isaac.rect.y) <= 20
        ):
            self.npc1.gen_chatbox(self.get_keys())
