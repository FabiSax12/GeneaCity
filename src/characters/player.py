import pygame
from characters.person import Person
from visuals.sprite import Sprite

class Player(Person):
    def __init__(self, person_info: dict, screen: pygame.Surface):
        super().__init__(person_info)
        self.screen = screen
        self._score = 0
        self.position = pygame.Vector2(person_info["house"]["x"] - 88, person_info["house"]["y"] - 105)
        self.sprite = Sprite(self.position)
        print(self.screen)

    def draw(self, map_surface: pygame.Surface):
        # self.screen.fill((0, 0, 0))
        center = map_surface.get_rect().center
        map_surface.blit(self.sprite._image, (center[0] - 22, center[1] - 26.25))
        print(self.position.x, self.position.y)

    def move(self, dx: int, dy: int):
        direction = "right" if dx > 0 else "left" if dx < 0 else "down" if dy > 0 else "up" if dy < 0 else self.sprite._direction
        self.sprite.set_direction(direction)
        self.sprite.update()

    def get_pos(self) -> tuple[int, int]:
        return self.position.x, self.position.y

    def get_score(self) -> int:
        return self._score

    def set_score(self, score: int):
        self._score = score
        
    def get_player_info(self) -> dict:
        return {"id": self.id, "name": self.name, "age": self.age, "score": self._score, "x": self.position.x, "y": self.position.y}
