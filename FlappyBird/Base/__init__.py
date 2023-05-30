import pygame
import os


base_img = pygame.transform.scale2x(pygame.image.load(
    os.path.join('../../', 'images/base.png')
))


class Base:
    """
    Represents the moving floor of the game
    """
    VEL = 5
    WIDTH = base_img.get_width()
    IMG = base_img

    def __init__(self, y: int):
        """
        Initialize the object
        :param y: int
        :return: None
        """
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        """
        Move floor so it looks like scrolling
        :return: None
        """
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, window: pygame.Surface):
        """
        Draw the floor. This is two images that move together.
        :param window: Pygame window/surface
        :return: None
        """
        window.blit(self.IMG, (self.x1, self.y))
        window.blit(self.IMG, (self.x2, self.y))
