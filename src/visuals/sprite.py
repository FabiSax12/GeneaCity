import pygame

class Sprite(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int]):
        super().__init__()
        self.__sheet = pygame.image.load("src/assets/spritesheet.png")
        self.__sheet.set_clip(pygame.Rect(0, 0, 88, 105))
        self.__image = self.__sheet.subsurface(self.__sheet.get_clip())
        self.__image = pygame.transform.scale(self.__image, (44, 52.5))
        self.__rect = self.__image.get_rect()
        self.__rect.topleft = position
        self.__frame = 0
        self.__direction = "down"
        self.__animation = {
            "down": [(0, 0), (88, 0), (176, 0), (264, 0)],
            "up": [(0, 105), (88, 105), (176, 105), (264, 105)],
            "left": [(0, 210), (88, 210), (176, 210), (264, 210)],
            "right": [(0, 315), (88, 315), (176, 315), (264, 315)]
        }

    def _get_frame(self, frame_set):
        self.__frame += 0.05
        if int(self.__frame) > (len(frame_set) - 1):
            self.__frame = 0
        return frame_set[int(self.__frame)]
    
    def _clip(self):
        frame_coords = self._get_frame(self.__animation[self.__direction])
        self.__sheet.set_clip(pygame.Rect(*frame_coords, 88, 105))

    def update(self):
        self._clip()
        self.__image = self.__sheet.subsurface(self.__sheet.get_clip())
        self.__image = pygame.transform.scale(self.__image, (44, 52.5))

    # Properties

    @property
    def image(self) -> pygame.Surface:
        return self.__image

    @property
    def direction(self) -> str:
        return self.__direction
    
    @direction.setter
    def direction(self, value: str):
        if value in self.__animation.keys() and value != self.__direction:
            self.__direction = value