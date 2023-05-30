import pygame
import pyautogui
import math


def get_window_w_h() -> tuple[int, int]:
    """
    Returns the height and one-third of the width of the screen
    :return: (window_width:int, window_height:int)
    """
    window_width, window_height = pyautogui.size()
    window_width = math.ceil(window_width/3)

    return window_width, window_height


pygame.font.init()  # Init font
pygame.display.set_caption("Flappy Bird")

WINDOW = pygame.display.set_mode((get_window_w_h()))
