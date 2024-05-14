class Tile:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()

    def draw(self, screen, x, y):
        self.rect.topleft = (x, y)
        screen.blit(self.image, self.rect)