import pygame

class Sprite(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int]):
        super().__init__()
        self._sheet = pygame.image.load("src/assets/spritesheet.png")
        self._sheet.set_clip(pygame.Rect(0, 0, 88, 105))
        self._image = self._sheet.subsurface(self._sheet.get_clip())
        self._image = pygame.transform.scale(self._image, (44, 52.5))
        self._rect = self._image.get_rect()
        self._rect.topleft = position
        self._frame = 0
        self._direction = "down"
        self._animation = {
            "down": [(0, 0), (88, 0), (176, 0), (264, 0)],
            "up": [(0, 105), (88, 105), (176, 105), (264, 105)],
            "left": [(0, 210), (88, 210), (176, 210), (264, 210)],
            "right": [(0, 315), (88, 315), (176, 315), (264, 315)]
        }

    def set_direction(self, direction: str):
        self._direction = direction

    def _get_frame(self, frame_set):
        self._frame += 0.05
        if int(self._frame) > (len(frame_set) - 1):
            self._frame = 0
        return frame_set[int(self._frame)]
    
    def _clip(self):
        frame_coords = self._get_frame(self._animation[self._direction])
        self._sheet.set_clip(pygame.Rect(*frame_coords, 88, 105))

    def update(self):
        self._clip()
        self._image = self._sheet.subsurface(self._sheet.get_clip())
        self._image = pygame.transform.scale(self._image, (44, 52.5))