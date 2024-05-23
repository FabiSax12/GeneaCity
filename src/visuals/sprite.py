import pygame
from typing import Literal

class Sprite(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int], gender: Literal["Male", "Female"], id: int):
        super().__init__()
        self.__sheet = pygame.image.load(f"src/assets/spritesheet{gender}{id % 4 + 1}.png")
        self.__sprite_width = self.__sheet.get_width() // 4
        self.__sprite_height = self.__sheet.get_height() // 4

        self.__sheet.set_clip(pygame.Rect(0, 0, self.__sprite_width, self.__sprite_height))

        self.__image = self.__sheet.subsurface(self.__sheet.get_clip())
        self.__image = pygame.transform.scale(self.__image, (self.__sprite_width, self.__sprite_height))

        self.__rect = self.__image.get_rect()
        self.__rect.topleft = position

        self.__frame = 0
        self.__direction = "down"
        self.__animation = {
            "down": [
                (0, 0), 
                (self.__sprite_width, 0), 
                (self.__sprite_width * 2, 0), 
                (self.__sprite_width * 3, 0)
            ],
            "left": [
                (0, self.__sprite_height),
                (self.__sprite_width, self.__sprite_height),
                (self.__sprite_width * 2, self.__sprite_height),
                (self.__sprite_width * 3, self.__sprite_height)
            ],
            "right": [
                (0, self.__sprite_height * 2),
                (self.__sprite_width, self.__sprite_height * 2),
                (self.__sprite_width * 2, self.__sprite_height * 2),
                (self.__sprite_width * 3, self.__sprite_height * 2)
            ],
            "up": [
                (0, self.__sprite_height * 3),
                (self.__sprite_width, self.__sprite_height * 3),
                (self.__sprite_width * 2, self.__sprite_height * 3),
                (self.__sprite_width * 3, self.__sprite_height * 3)
            ]
        }

    def _get_frame(self, frame_set):
        self.__frame += 0.04
        if int(self.__frame) > (len(frame_set) - 1):
            self.__frame = 0
        return frame_set[int(self.__frame)]
    
    def _clip(self):
        frame_coords = self._get_frame(self.__animation[self.__direction])
        self.__sheet.set_clip(pygame.Rect(*frame_coords, self.__sprite_width, self.__sprite_height))

    def update(self):
        self._clip()
        self.__image = self.__sheet.subsurface(self.__sheet.get_clip())
        self.__image = pygame.transform.scale(self.__image, (self.__sprite_width, self.__sprite_height))

    # Properties

    @property
    def image(self) -> pygame.Surface:
        return self.__image
    
    @property
    def rect(self) -> pygame.Rect:
        return self.__rect

    @property
    def direction(self) -> str:
        return self.__direction
    
    @direction.setter
    def direction(self, value: str):
        if value in self.__animation.keys() and value != self.__direction:
            self.__direction = value