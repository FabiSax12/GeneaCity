import pygame
from visuals.tile import Tile

class Map:
    def __init__(self, width, height, screen: pygame.Surface):
        self.__width = width
        self.__height = height
        self.__screen = screen

        self.__x = 0
        self.__y = 0

        self.__tile_size = 100
        self.__tile_image = pygame.image.load("src/assets/tile.png")
        self.__tile_image = pygame.transform.scale(self.__tile_image, (self.__tile_size, self.__tile_size))

        self.__tile_x_amount = self.__screen.get_width() // self.__tile_size + 2
        self.__tile_y_amount = self.__screen.get_height() // self.__tile_size + 2

        self.__tiles = [[Tile(self.__tile_image) for _ in range(self.__tile_x_amount)] for _ in range(self.__tile_y_amount)]

    def move(self, dx, dy):
        """Move the map.

        Args:
            dx (_type_): difference in x-axis
            dy (_type_): difference in y-axis
        """
        if self.__x + dx < -100:
            self.__x = 0
        elif self.__x + dx > 0:
            self.__x = -100
        else:
            self.__x += dx

        if self.__y + dy < -100:
            self.__y = 0
        elif self.__y + dy > 0:
            self.__y = -100
        else:
            self.__y += dy

        self.draw()

    def draw(self):
        """Draw the map."""
        for y, row in enumerate(self.__tiles):
            for x, tile in enumerate(row):
                tile_x = x * self.__tile_size + self.__x
                tile_y = y * self.__tile_size + self.__y
                self.__screen.blit(tile.image, (tile_x, tile_y))
