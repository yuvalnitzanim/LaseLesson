import pygame
import random
from constants import *
from classes.MovingObject import MovingObject
from classes.Obstacle import Obstacle
from classes.Booster import Booster
from classes.ImageObject import ImageObject
from classes.Mario import Mario
import time


class Game:
    def __init__(self, screen):
        self.__screen = screen
        self.__object_list = []
        self.__mario = None
        self.add_initial_objects()
        self.__can_move = True
        self.__is_game_over = False
        self.__points = 0
        self.__count_before_add_point = 0

    def show_points_text(self):
        self.__count_before_add_point += 1
        if self.__count_before_add_point == TICKS_BEFORE_POINT_IS_ADDED:
            self.__count_before_add_point = 0
            self.__points += 1
        font = pygame.font.SysFont('Arial', POINTS_TEXT_SIZE)
        self.__screen.blit(font.render("Points: " + str(self.__points), True, BLACK), (POINTS_TEXT_X, POINTS_TEXT_Y))

    def is_game_over(self):
        self.check_if_game_over()
        self.show_points_text()
        return self.__is_game_over

    def add_initial_objects(self):
        background = ImageObject(self.__screen, 0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, 'Images/background.png')
        self.__object_list.append(background)

        self.__mario = Mario(self.__screen, SUPER_MARIO_START_X_POS, SUPER_MARIO_START_Y_POS,
                             SUPER_MARIO_WIDTH, SUPER_MARIO_HEIGHT, SUPER_MARIO_IMG_PATH)

        for i in range(3):
            self.__create_new_obstacle(i)

        for i in range(7):
            self.__create_new_background_object(i)

        self.__create_new_booster(15)

    def __create_new_obstacle(self, space_between_obj=1):
        rand_height = random.randint(0, 1)
        if rand_height == 1:
            # The moving object is on the ground
            rand_moving_object = random.randint(1, len(GROUND_OBSTACLE_IMAGES))
            moving_objects_image = GROUND_OBSTACLE_IMAGES[rand_moving_object - 1]
        else:
            # The moving object is on the sky
            rand_moving_object = random.randint(1, len(SKY_OBSTACLE_IMAGES))
            moving_objects_image = SKY_OBSTACLE_IMAGES[rand_moving_object - 1]

        y_pos = TOP_Y_YOS + rand_height * SPACE_BETWEEN_MOVING_OBJECTS_Y
        obstacle = Obstacle(self.__screen,
                            WINDOW_WIDTH - ENEMY_SIZE + SPACE_BETWEEN_MOVING_OBJECTS_X * space_between_obj,
                            y_pos, ENEMY_SIZE, ENEMY_SIZE, moving_objects_image, SPEED)

        self.__object_list.append(obstacle)

    def __create_new_background_object(self, space_between_obj=1):
        rand_height = random.randint(0, 3)

        rand_moving_object = random.randint(1, len(SKY_BACKGROUND_OBJECTS_IMAGES))
        moving_objects_image = SKY_BACKGROUND_OBJECTS_IMAGES[rand_moving_object - 1]
        width = SKY_BACKGROUND_WIDTH[rand_moving_object - 1]
        height = SKY_BACKGROUND_HEIGHT[rand_moving_object - 1]
        y_pos = TOP_Y_YOS_FOR_BACKGROUND_OBJECTS + rand_height * SPACE_BETWEEN_MOVING_OBJECTS_Y
        bg_object = MovingObject(self.__screen,
                                 WINDOW_WIDTH - ENEMY_SIZE + SPACE_BETWEEN_BACKGROUND_OBJECTS_X * space_between_obj,
                                 y_pos, width, height, moving_objects_image, BACKGROUND_OBJECTS_SPEED)

        self.__object_list.append(bg_object)

    def __create_new_booster(self, space_between_obj=1):
        rand_height = random.randint(0, 1)

        rand_moving_object = random.randint(1, len(BOOSTER_IMAGES))
        moving_objects_image = BOOSTER_IMAGES[rand_moving_object - 1]
        boosters_points = BOOSTER_POINTS[rand_moving_object - 1]

        y_pos = TOP_Y_YOS + rand_height * SPACE_BETWEEN_MOVING_OBJECTS_Y
        bg_object = Booster(self.__screen,
                            WINDOW_WIDTH - ENEMY_SIZE + SPACE_BETWEEN_BACKGROUND_OBJECTS_X * space_between_obj,
                            y_pos, BOOSTERS_SIZE, BOOSTERS_SIZE, moving_objects_image, BOOSTERS_SPEED,
                            boosters_points)

        self.__object_list.append(bg_object)

    def move_objects(self):
        for value in self.__object_list:
            if isinstance(value, MovingObject):
                value.move_object()

                if value.is_out_of_screen():
                    self.__object_list.remove(value)
                    if isinstance(value, Obstacle):
                        self.__create_new_obstacle()
                    elif isinstance(value, Booster):
                        self.__create_new_booster()
                    else:
                        self.__create_new_background_object()

    def display_objects_to_screen(self):
        """
        The function goes over any object that is on the screen (using the dictionary that contains objects)
        and displays the objects on the screen.
        :return: None
        """
        for value in self.__object_list:
            value.display_image_to_screen()

        self.__mario.display_image_to_screen()


    def on_click(self, mouse_pos):
        """
        Tests on the click of a button and checks which button was pressed using the 'Current Screen' variable.
        :param mouse_pos: The position of the mouse click.
        :return: None
        """
        print("click")

    def move_mario(self, direction):
        if not self.__can_move:
            return
        if direction == "left":
            self.__mario.move_left()
        elif direction == "right":
            self.__mario.move_right()
        elif direction == "jump":
            self.make_mario_jump_or_bend("jump")
        elif direction == "bend":
            self.make_mario_jump_or_bend("bend")

    def make_mario_jump_or_bend(self, action):
        if not self.__can_move:
            return

        self.__can_move = False
        self.display_objects_to_screen()

        if action == "jump":
            ans = self.__mario.jump()
        else:
            ans = self.__mario.bend()

        while not self.is_game_over() and ans != "done":
            self.move_objects()
            self.show_points_text()
            self.display_objects_to_screen()
            pygame.display.flip()
            if action == "jump":
                ans = self.__mario.jump()
            else:
                ans = self.__mario.bend()

        self.__can_move = True

    def check_if_game_over(self):
        for obj in self.__object_list:
            obj_location = {'x': obj.x_pos, 'y': obj.y_pos}
            obj_size = {'width': obj.width, 'height': obj.height}

            if self.__mario.is_object_on_image(obj_location, obj_size):
                if isinstance(obj, Obstacle):
                    self.__is_game_over = True
                    break
                elif isinstance(obj, Booster):
                    # print("add extra ", obj.get_extra_points(), " points!")
                    self.__points += obj.get_extra_points()
                    self.__object_list.remove(obj)
                    self.__create_new_booster()
