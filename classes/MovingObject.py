import pygame
from classes.ImageObject import ImageObject
from constants import WINDOW_WIDTH


class MovingObject(ImageObject):
    def __init__(self, screen, x_pos, y_pos, width, height, img_path, speed):
        ImageObject.__init__(self, screen, x_pos, y_pos, width, height, img_path)
        self._speed = speed

    def move_object(self):
        self._x_pos -= self._speed

    def is_out_of_screen(self):
        return self._x_pos < 0
