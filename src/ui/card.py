import random
import pygame
from .colors import Colors

class Card:
    def __init__(self, window: pygame.Surface, width: int, height: int, x, y, character: dict):
        self.__window = window
        self.__character = character
        self.__width = width
        self.__height = height

        self.__selected = False
        self.__image = pygame.image.load(f"src/assets/spritesheet{character["gender"]}{random.randint(1, 3)}.png")
        self.__image.set_clip(pygame.Rect(0, 0, self.__image.get_width() / 4, self.__image.get_height() / 4))
        self.__image = self.__image.subsurface(self.__image.get_clip())
        self.__image = pygame.transform.scale(self.__image, (self.__image.get_width() * 1.5, self.__image.get_height() * 1.5))

        self.__rect = pygame.Rect(x, y, self.__width, self.__height)

    def draw(self):
        color = Colors.LIGHT_GRAY.value if not self.__selected else Colors.LIGHT_BLUE.value
        pygame.draw.rect(self.__window, color, self.__rect, border_radius=15)

        name = pygame.font.SysFont(None, 25).render(self.__character['name'], True, Colors.BLACK.value)
        gender = pygame.font.SysFont(None, 20).render(self.__character["gender"], True, Colors.BLACK.value)
        age = pygame.font.SysFont(None, 20).render(f"{self.__character["age"]} años", True, Colors.BLACK.value)


        self.__window.blit(name, (self.__rect.x + 10, self.__rect.y + 10))
        self.__window.blit(gender, (self.__rect.x + 10, self.__rect.y + 40))
        self.__window.blit(age, (self.__rect.x + 10, self.__rect.y + 70))
        self.__window.blit(self.__image, (self.rect.x + self.__width // 4 * 3 - self.__image.get_width() // 2, self.rect.y + self.__height // 2 - self.__image.get_height() // 2))
    
    def select(self):
        self.__selected = True

    def deselect(self):
        self.__selected = False

    @property
    def rect(self):
        return self.__rect
    
    @property
    def position(self):
        return self.__rect.topleft
    
    @position.setter
    def position(self, value: tuple[int, int]):
        self.__rect.topleft = value
    
    @property
    def character(self):
        return self.__character
