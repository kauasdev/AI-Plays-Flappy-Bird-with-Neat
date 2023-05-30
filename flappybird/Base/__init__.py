import pygame


class Base:
    """
    Represents the moving floor of the game
    """
    VEL = 5

    def __init__(self, y: int, base_img: pygame.Surface):
        """
        Initialize the object
        :param y: int
        :return: None
        """
        self.BASE_IMG = base_img
        self.WIDTH = self.BASE_IMG.get_width()
        self.IMG = self.BASE_IMG
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
