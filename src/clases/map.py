import pygame
from visuals.tile import Tile

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.tile_size = 100
        self.tile_image = pygame.image.load("src/assets/tile.png")
        self.tile_image = pygame.transform.scale(self.tile_image, (self.tile_size, self.tile_size))

        self.tiles = [[Tile(self.tile_image) for _ in range(width)] for _ in range(height)]
        print(len(self.tiles), len(self.tiles[0]))

    def draw(self, screen, player_pos: tuple[int, int]):
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                tile.draw(screen, x * self.tile_size, y * self.tile_size)
