from pygame import *
from Statics import *
from Player import Player


isaac = pygame.sprite.GroupSingle()
isaac.add(
    Player(0.5 * Vector2(ScreenSettings.screenWidth, ScreenSettings.screenHeight))
)


def run():

    pygame.init()

    # Set up the screen
    screen = pygame.display.set_mode(
        (ScreenSettings.screenWidth, ScreenSettings.screenHeight)
    )
    pygame.display.set_caption(ScreenSettings.caption)

    # Set icon
    icon = pygame.image.load(ImportedImages.icon).convert_alpha()
    pygame.display.set_icon(icon)

    # Set up the player
    isaac = pygame.sprite.GroupSingle()
    isaac.add(
        Player(0.5 * Vector2(ScreenSettings.screenWidth, ScreenSettings.screenHeight))
    )

    # Main loop
    while True:
        pygame.time.Clock().tick(ScreenSettings.fps)
        screen.fill("Black")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        keys = pygame.key.get_pressed()
        isaac.draw(screen)
        isaac.update(keys)
        pygame.display.flip()


if __name__ == "__main__":
    run()
