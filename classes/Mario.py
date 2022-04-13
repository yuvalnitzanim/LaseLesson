from classes.MovingObject import MovingObject
from constants import *


class Mario(MovingObject):
    def __init__(self, screen, x_pos, y_pos, width, height, img_path):
        MovingObject.__init__(self, screen, x_pos, y_pos, width, height, img_path, 7)
        self.__can_move = True
        self.__jump_direction = ""

    def move_right(self):
        if (self._x_pos + self._width) + self._speed < WINDOW_WIDTH and self.__can_move:
            self._x_pos += self._speed

    def move_left(self):
        if self._x_pos - self._speed > 0 and self.__can_move:
            self._x_pos -= self._speed

    def jump(self):
        self.__can_move = False
        self._img_path = SUPER_MARIO_JUMP_IMG_PATH
        if self.__jump_direction == "":
            self.__jump_direction = "up"
            return "up"
        elif self.__jump_direction == "up":
            if self._y_pos < LIMIT_FOR_JUMP:
                self.__jump_direction = "down"
                return "down"
            else:
                self._y_pos -= JUMP_SPEED
                self._x_pos += X_MOVE_DISTANCE_IN_JUMP_AND_BEND
                return "up"
        elif self.__jump_direction == "down":
            if self._y_pos > SUPER_MARIO_START_Y_POS:
                self.__jump_direction = ""
                self.__can_move = True
                self._y_pos = SUPER_MARIO_START_Y_POS
                self._img_path = SUPER_MARIO_IMG_PATH
                return "done"
            else:
                self._y_pos += JUMP_SPEED
                self._x_pos += X_MOVE_DISTANCE_IN_JUMP_AND_BEND
                return "down"

    def bend(self):
        self.__can_move = False
        self._img_path = SUPER_MARIO_BEND_IMG_PATH
        if self.__jump_direction == "":
            self.__jump_direction = "down"
            return "down"
        elif self.__jump_direction == "down":
            # if self._y_pos > LIMIT_FOR_BEND:
            if self._height < LIMIT_FOR_BEND:
                self.__jump_direction = "up"
                return "up"
            else:
                self._y_pos += BEND_SPEED
                self._height -= BEND_HEIGHT_CHANGE
                self._width -= BEND_WIDTH_CHANGE
                self._x_pos += X_MOVE_DISTANCE_IN_JUMP_AND_BEND
                return "down"
        elif self.__jump_direction == "up":
            if self._y_pos < SUPER_MARIO_START_Y_POS:
                self.__jump_direction = ""
                self.__can_move = True
                self._y_pos = SUPER_MARIO_START_Y_POS
                self._img_path = SUPER_MARIO_IMG_PATH
                return "done"
            else:
                self._y_pos -= BEND_SPEED
                self._height += BEND_HEIGHT_CHANGE
                self._width += BEND_WIDTH_CHANGE
                self._x_pos += X_MOVE_DISTANCE_IN_JUMP_AND_BEND
                return "up"
