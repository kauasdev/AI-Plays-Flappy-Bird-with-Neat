import pygame
import pyautogui
import math
from Bird import Bird
from Pipe import Pipe
from Base import Base


pygame.font.init()  # Init font
pygame.display.set_caption("Flappy Bird")


class FlappyBird:

    def __init__(self):
        self.window = pygame.display.set_mode(self.get_window_w_h())

    @staticmethod
    def get_window_w_h() -> tuple[int, int]:
        """
        Returns the height and one-third of the width of the screen
        :return: (window_width:int, window_height:int)
        """
        window_width, window_height = pyautogui.size()
        window_width = math.ceil(window_width/3)

        return window_width, window_height



