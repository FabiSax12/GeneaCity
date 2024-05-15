import pygame

class Tile:
    def __init__(self, image: pygame.Surface):
        self.__image = image
        self.__rect = self.__image.get_rect()

    def move(self, dx, dy):
        """Move the tile.

        Args:
            dx (_type_): difference in x-axis
            dy (_type_): difference in y-axis
        """
        self.__rect.x += dx
        self.__rect.y += dy

    def draw(self, screen, x, y):
        """Draw the tile."""
        screen.blit(self.__image, (x, y))

    # Properties

    @property
    def image(self):
        return self.__image
    
    @property
    def rect(self):
        return self.__rect
    
    @property
    def pos(self):
        return self.__rect.topleft
    
    @property
    def perimeter(self):
        return self.__rect.topleft, self.__rect.bottomright