import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Define room colors for demo purposes
ROOM_COLORS = [(200, 200, 200), (100, 100, 255)]  # Cleared room, new room

# Initial positions
current_room_y = 0
new_room_y = -SCREEN_HEIGHT

# Transition flag
transitioning = False

# Speed of transition
transition_speed = 10


def draw_room(color, y_position):
    """Draws a room on the screen at a specified Y-coordinate."""
    pygame.draw.rect(screen, color, (0, y_position, SCREEN_WIDTH, SCREEN_HEIGHT))


# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Start transition on pressing the up arrow
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            transitioning = True

    # Update positions during transition
    if transitioning:
        current_room_y += transition_speed
        new_room_y += transition_speed

        # Stop transition when the new room occupies the screen
        if current_room_y >= SCREEN_HEIGHT:
            transitioning = False

        # Drawing
        screen.fill((0, 0, 0))  # Clear screen with black
        draw_room(ROOM_COLORS[1], new_room_y)  # Draw new room
        draw_room(ROOM_COLORS[0], current_room_y)  # Draw current room
    pygame.display.flip()

    # Frame rate
    clock.tick(60)
