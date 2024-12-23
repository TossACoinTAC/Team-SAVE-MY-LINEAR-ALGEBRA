import pygame
from GameManager import GameManager
from player import player

isaac = player()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Some Title")

icon = pygame.image.load("assets/icons/64x64.ico").convert_alpha()
pygame.display.set_icon(icon)

start_page_title_surface = pygame.image.load(
    "assets/images/start_page_title.png"
).convert_alpha()

# start_text_font = pygame.font.Font("assets/fonts/IsaacGame.ttf", 50)
# start_text_surface = start_text_font.render(
#     "Press any key to start", True, "cyan"
# ).convert_alpha()
# start_text_pos = start_text_surface.get_rect(center=(400, 300))


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()
    # update the screen
    screen.fill("Black")
    screen.blit(start_page_title_surface, (0, 0))
    # screen.blit(start_text_surface, start_text_pos)
    screen.blit(isaac.image, isaac.rect)

    isaac.move()
    GameManager.update()
pygame.quit()
