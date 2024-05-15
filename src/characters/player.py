import pygame
from characters.person import Person
from visuals.sprite import Sprite

class Player(Person):
    def __init__(self, person_info: dict, screen: pygame.Surface):
        super().__init__(person_info)
        self.screen = screen
        self._score = 0
        self.position = pygame.Vector2(person_info["house"]["x"], person_info["house"]["y"])
        self.sprite = Sprite(self.position)

    def draw(self, map_surface: pygame.Surface):
        """Draw the player on the map.

        Args:
            map_surface (pygame.Surface): map surface
        """
        map_surface.blit(
            self.sprite._image, 
            (
                map_surface.get_width() // 2 - self.sprite._image.get_width() // 2, 
                map_surface.get_height() // 2 - self.sprite._image.get_height() // 2
            )
        )

    def  move(self, dx: int, dy: int):
        """Move the player.

        Args:
            dx (int): difference in x-axis
            dy (int): difference in y-axis
        """
        direction = "right" if dx > 0 else "left" if dx < 0 else "down" if dy > 0 else "up" if dy < 0 else self.sprite._direction
        self.sprite.set_direction(direction)
        
        if self.position.x + dx < 0:
            self.position.x = 0
        elif self.position.x + dx > 100000 - self.sprite._image.get_width():
            self.position.x = 100000 - self.sprite._image.get_width()
        else:
            self.position.x += dx
            self.sprite.update()

        if self.position.y + dy < 0:
            self.position.y = 0
        elif self.position.y + dy > 100000 - self.sprite._image.get_height():
            self.position.y = 100000 - self.sprite._image.get_height()
        else:
            self.position.y += dy
            self.sprite.update()

    def get_pos(self) -> tuple[int, int]:
        """Get the position of the player.

        Returns:
            tuple[int, int]: Position of the player in the map surface (x, y)
        """
        return self.position.x, self.position.y

    def get_score(self) -> int:
        """Get the player's score.

        Returns:
            
        """
        return self._score

    def set_score(self, score: int):
        """Set the player's score.

        Args:
            score (int): player's score
        """
        self._score = score
        
    def get_player_info(self) -> dict:
        """Get the player's information.

        Returns:
            dict: player's information
        """
        return {"id": self.id, "name": self.name, "age": self.age, "score": self._score, "x": self.position.x, "y": self.position.y}
