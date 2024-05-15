import pygame
from visuals.tile import Tile

class Map:
    def __init__(self, width, height, screen: pygame.Surface):
        self.width = width
        self.height = height
        self.screen = screen

        self.x = 0
        self.y = 0

        self.tile_size = 100
        self.tile_image = pygame.image.load("src/assets/tile.png")
        self.tile_image = pygame.transform.scale(self.tile_image, (self.tile_size, self.tile_size))

        self.tile_x_amount = self.screen.get_width() // self.tile_size + 2
        self.tile_y_amount = self.screen.get_height() // self.tile_size + 2

        self.tiles = [[Tile(self.tile_image) for _ in range(self.tile_x_amount)] for _ in range(self.tile_y_amount)]

    def move(self, dx, dy):
        """Move the map.

        Args:
            dx (_type_): difference in x-axis
            dy (_type_): difference in y-axis
        """
        if self.x + dx < -100:
            self.x = 0
        elif self.x + dx > 0:
            self.x = -100
        else:
            self.x += dx

        if self.y + dy < -100:
            self.y = 0
        elif self.y + dy > 0:
            self.y = -100
        else:
            self.y += dy

        self.draw()

    def draw(self):
        """Draw the map."""
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                tile_x = x * self.tile_size + self.x
                tile_y = y * self.tile_size + self.y
                self.screen.blit(tile.image, (tile_x, tile_y))
