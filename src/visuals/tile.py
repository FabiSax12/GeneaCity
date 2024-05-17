import pygame

class TileRenderer:
    """Class responsible for rendering the tile using Pygame."""
    
    def __init__(self, image: pygame.Surface):
        self.__image = image
        self.__rect = self.__image.get_rect()

    def move(self, dx, dy):
        """Move the tile."""
        self.__rect.x += dx
        self.__rect.y += dy

    def draw(self, screen, x, y):
        """Draw the tile."""
        screen.blit(self.__image, (x, y))

    @property
    def rect(self):
        """Get the rectangle."""
        return self.__rect
    
    @property
    def image(self):
        """Get the image."""
        return self.__image

    @property
    def pos(self):
        """Get the position."""
        return self.__rect.topleft

    @property
    def perimeter(self):
        """Get the perimeter."""
        return self.__rect.topleft, self.__rect.bottomright
    
class Tile:
    """Class representing a tile."""

    def __init__(self, image: pygame.Surface):
        self.__renderer = TileRenderer(image)

    def move(self, dx, dy):
        """Move the tile."""
        self.__renderer.move(dx, dy)

    def draw(self, screen, x, y):
        """Draw the tile."""
        self.__renderer.draw(screen, x, y)

    @property
    def rect(self):
        """Get the rectangle."""
        return self.__renderer.rect
    
    @property
    def image(self):
        """Get the image."""
        return self.__renderer.image