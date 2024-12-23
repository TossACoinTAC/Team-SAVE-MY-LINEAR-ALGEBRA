import pygame


clock = pygame.time.Clock()


class GameManager:

    @staticmethod
    def update():

        # Flip the back buffer to the front and Set the FPS of the game to 30
        pygame.display.flip()
        return clock.tick()

    @staticmethod
    def get_deltatime() -> float:
        # Return the time in seconds since the last frame,
        # so that we can use it to move objects at a constant speed,
        # which is actually the integral of the velocity in 1 sec.
        # In this way, the fps won't need a pre-specification.
        return clock.get_fps() ** (-1)
