import os.path
import random
import pygame
from FlappyBird import Bird


pipe_img = pygame.transform.scale2x(pygame.image.load(
    os.path.join('../../', 'images/pipe.png')
))


class Pipe:
    """
    Represents a pipe object
    """
    GAP = 200
    VEL = 5

    def __init__(self, x: int):
        """
        Initialize pipe object
        :param x: int
        :return: None
        """
        self.x = x
        self.height = 0

        # Where the top and bottom of the pipe is
        self.top = 0
        self.bottom = 0

        self.PIPE_TOP = pygame.transform.flip(pipe_img, False, True)
        self.PIPE_BOTTOM = pipe_img

        self.passed = False

        self.set_height()

    def set_height(self):
        """
        set the height of the pipe, from the top of the screen
        :return: None
        """
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        """
        Move pipe based on vel
        :return: None
        """
        self.x -= self.VEL

    def draw(self, window: pygame.Surface):
        """
        Draw both the top and bottom of the pipe
        :param window: Pygame window/surface
        :return: None
        """
        # Draw top
        window.blit(self.PIPE_TOP, (self.x, self.top))
        # Draw bottom
        window.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird: Bird, window: pygame.Surface):
        """
        Returns if a point is colliding with the pipe
        :param bird: Bird object
        :param window: Pygame window/surface
        :return:
        """
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        bottom_point = bird_mask.overlap(bottom_mask, bottom_offset)
        top_point = bird_mask.overlap(top_mask, top_offset)

        if bottom_point or top_point:
            return True

        return False
