import pygame
from typing import Optional, Tuple
from clases.person import Person

class Sprite(pygame.sprite.Sprite):
    def __init__(self, position: Tuple[int, int]):
        self._sheet = pygame.image.load("src/assets/spritesheet.png")
        self._sheet.set_clip(pygame.Rect(0, 0, 88, 105))
        self._image = self._sheet.subsurface(self._sheet.get_clip())
        self._image = pygame.transform.scale(self._image, (44, 52.5))
        self._rect = self._image.get_rect()
        self._rect.topleft = position
        self._frame = 0
        self._animation = {
            "down": [(0, 0), (88, 0), (176, 0), (264, 0)],
            "up": [(0, 105), (88, 105), (176, 105), (264, 105)],
            "left": [(0, 210), (88, 210), (176, 210), (264, 210)],
            "right": [(0, 315), (88, 315), (176, 315), (264, 315)]
        }
        self._direction = "down"
    
    def set_direction(self, direction: str):
        self._direction = direction

    def _get_frame(self, frame_set):
        self._frame += 1
        if self._frame > (len(frame_set) - 1):
            self._frame = 0
        return frame_set[self._frame]

    def _clip(self):
        frame_coords = self._get_frame(self._animation[self._direction])
        self._sheet.set_clip(pygame.Rect(*frame_coords, 88, 105))
    
    def update(self):
        self._clip()
        self._image = self._sheet.subsurface(self._sheet.get_clip())
        self._image = pygame.transform.scale(self._image, (44, 52.5))

    def event_listener(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                self._frame = 0
            else:
                self._frame = 4
            self.update()

class Player(Person):
    def __init__(self, person_info: dict, screen: pygame.Surface):
        super().__init__(person_info)
        self.screen = screen
        self._score = 0
        self.position = pygame.Vector2(person_info["house"]["x"], person_info["house"]["y"])
        self.sprite = Sprite(self.position)

    def __str__(self):
        return f"{self.name} is {self.age} years old and has a score of {self._score}."

    def increase_score(self, amount: int):
        self._score += amount

    def decrease_score(self, amount: int):
        self._score -= amount

    def spawn(self, pos: Optional[Tuple[int, int]] = None):
        if pos:
            self.position.update(pos)
        self.screen.blit(self.sprite._image, self.position)

    def move(self, dx: int, dy: int):
        direction = "right" if dx > 0 else "left" if dx < 0 else "down" if dy > 0 else "up" if dy < 0 else self.sprite._direction
        self.position.x += dx
        self.position.y += dy
        self.sprite.set_direction(direction)
        self.sprite.update()

    def get_pos(self) -> Tuple[int, int]:
        return self.position.x, self.position.y

    def get_score(self) -> int:
        return self._score

    def set_score(self, score: int):
        self._score = score

    # Evitar sombrear el método get_info de la clase base
    def get_player_info(self) -> dict:
        return {"id": self.id, "name": self.name, "age": self.age, "score": self._score, "x": self.position.x, "y": self.position.y}
