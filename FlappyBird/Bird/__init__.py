import pygame
import os


bird_imgs = [
    pygame.transform.scale2x(pygame.image.load(
        os.path.join('../../', f'images/bird{x}.png'))
    ) for x in range(1, 4)
]


def blit_rotate_center(surf, image, top_left, angle):
    """
    Rotate a surface and blit it to the window
    :param surf: the surface to blit to
    :param image: the image surface to rotate
    :param top_left: the top left position of the image
    :param angle: a float value for angle
    :return: None
    """
    rotated_img = pygame.transform.rotate(image, angle)
    new_rect = rotated_img.get_rect(
        center=image.get_rect(topleft=top_left).center
    )
    surf.blit(rotated_img, new_rect)


class Bird:
    MAX_ROTATION = 25
    IMGS = bird_imgs
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        """
        Initialize the object
        :param x: starting x pos (int)
        :param y: starting y pos (int)
        :return: None
        """
        self.x = x
        self.y = y
        self.tilt = 0  # degrees to tilt
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        """
        Make the bird jump
        :return: None
        """
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        """
        Make the bird move
        :return: None
        """
        self.tick_count += 1

        # For downward acceleration
        displacement = self.vel * self.tick_count + .5 * 3 * self.tick_count ** 2
        # Calculate displacement

        # Terminal velocity
        if displacement >= 16:
            displacement = (displacement/abs(displacement)) * 16

        if displacement < 0:
            displacement -= 2

        self.y = self.y + displacement

        if displacement < 0 or self.y < self.height + 50:  # tilt up
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:  # tilt down
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, window):
        """
        Draw the bird
        :param window: Pygame window or surface
        :return: None
        """
        self.img_count += 1

        # For animation of bird, loop through three images
        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count <= self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count <= self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # So when bird is nose diving it isn't flapping
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        # Tilt the bird
        blit_rotate_center(window, self.img, (self.x, self.y), self.tilt)

    def get_mask(self) -> pygame.Mask:
        """
        Gets the mask for the current image of bird
        :return: Mask
        """
        return pygame.mask.from_surface(self.img)
