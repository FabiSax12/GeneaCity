import pygame

class Tile:
    def __init__(self, image: pygame.Surface):
        self.image = image
        self.rect = self.image.get_rect()

    def move(self, dx, dy):
        """Move the tile.

        Args:
            dx (_type_): difference in x-axis
            dy (_type_): difference in y-axis
        """
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, screen, x, y):
        """Draw the tile."""
        screen.blit(self.image, (x, y))

    def get_pos(self):
        """Get the position of the tile.

        Returns:
            tuple: position of the tile
        """
        return self.rect.topleft
    
    def get_perimeter(self):
        """Get the perimeter of the tile."""
        return self.rect.topleft, self.rect.bottomright
    
    def get_rect(self) -> pygame.Rect:
        """Get the rect of the tile.

        Returns:
            pygame.Rect: rect of the tile
        """
        return self.rect