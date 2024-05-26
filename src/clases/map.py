import pygame
from typing import Tuple
from visuals.tile import Tile

class MapRenderer:
    """Class responsible for rendering the map using Pygame."""

    def __init__(self, window: pygame.Surface, tile_size: int, tile_image):
        self.__window = window
        self.__tile_size = tile_size
        self.__tile_image = pygame.transform.scale(tile_image, (self.__tile_size, self.__tile_size))

        self.__x = 0
        self.__y = 0

        self.__tile_x_amount = self.__window.get_width() // self.__tile_size + 2
        self.__tile_y_amount = self.__window.get_height() // self.__tile_size + 2

        self.__tiles = [[Tile(self.__tile_image) for _ in range(self.__tile_x_amount)] for _ in range(self.__tile_y_amount)]

    def move(self, dx, dy):
        """Move the map.

        Args:
            dx (_type_): difference in x-axis
            dy (_type_): difference in y-axis
        """
        if self.__x + dx < -self.__tile_size:
            self.__x = 0
        elif self.__x + dx > 0:
            self.__x = -self.__tile_size
        else:
            self.__x += dx

        if self.__y + dy < -self.__tile_size:
            self.__y = 0
        elif self.__y + dy > 0:
            self.__y = -self.__tile_size
        else:
            self.__y += dy

    def draw(self):
        """Draw the map."""
        for y, row in enumerate(self.__tiles):
            for x, tile in enumerate(row):
                tile_x = x * self.__tile_size + self.__x
                tile_y = y * self.__tile_size + self.__y
                self.__window.blit(tile.image, (tile_x, tile_y))

class Map:
    """Class representing a map."""

    def __init__(self, size: Tuple[int, int], window: pygame.Surface):
        self.__width = size[0]
        self.__height = size[1]
        self.__renderer = MapRenderer(window, 100, pygame.image.load("src/assets/images/tile.png"))

    def move(self, dx, dy):
        """Move the map.

        Args:
            dx (_type_): difference in x-axis
            dy (_type_): difference in y-axis
        """
        self.__renderer.move(dx, dy)

    def draw(self):
        """Draw the map."""
        self.__renderer.draw()

    @property
    def width(self):
        return self.__width
    
    @property
    def height(self):
        return self.__height
    
