import pygame


class ImageObject:
    def __init__(self, screen, x_pos, y_pos, width, height, img_path):
        self._screen = screen
        self._x_pos = x_pos
        self._y_pos = y_pos
        self._width = width
        self._height = height
        self._img_path = img_path

    def display_image_to_screen(self):
        """
        Add the image of the given size to the screen in the desired location.
        :return: None
        """
        # Add the image to the screen
        img = pygame.image.load(self._img_path)
        img = pygame.transform.scale(img, (self._width, self._height))
        self._screen.blit(img, (self._x_pos, self._y_pos))

        # Update the screen
        # pygame.display.flip()

    def is_object_on_image(self, obj_location, obj_size):
        if (obj_location['x'] < self._x_pos + self._width and
                obj_location['x'] + obj_size['width'] > self._x_pos and
                obj_location['y'] < self._y_pos + self._height and
                obj_size['height'] + obj_location['y'] > self._y_pos):
            return True
        else:
            return False

    @property
    def x_pos(self):
        return self._x_pos

    @property
    def y_pos(self):
        return self._y_pos

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height
