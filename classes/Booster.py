import pygame
from classes.MovingObject import MovingObject


class Booster(MovingObject):
    def __init__(self, screen, x_pos, y_pos, width, height, img_path, speed, extra_points):
        MovingObject.__init__(self, screen, x_pos, y_pos, width, height, img_path, speed)
        self.__extra_points = extra_points

    def get_extra_points(self):
        return self.__extra_points
