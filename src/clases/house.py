import pygame

class House:
    def __init__(self, house_info: dict):
        self.id = int(house_info["id"])
        self.x = int(house_info["x"])
        self.y = int(house_info["y"])
        self.occupants = house_info["occupants"]

        self.image = pygame.image.load("src/assets/house_1.jpeg")
        self.image = pygame.transform.scale(self.image, (55, 55))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect.topleft)