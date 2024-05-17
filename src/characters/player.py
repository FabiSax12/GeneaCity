import pygame
from characters.person import Person
from visuals.sprite import Sprite

class Player(Person):
    def __init__(self, person_info: dict):
        super().__init__(person_info)
        self.__score = 0
        self.__position = pygame.Vector2(person_info["house"]["x"], person_info["house"]["y"])
        print(self.info)
        self.__sprite = Sprite(self.__position, self.info["gender"], self.info["id"])

    def draw(self, map_surface: pygame.Surface):
        """Draw the player on the map.

        Args:
            map_surface (pygame.Surface): map surface
        """
        map_surface.blit(
            self.__sprite.image, 
            (
                map_surface.get_width() // 2 - self.__sprite.image.get_width() // 2, 
                map_surface.get_height() // 2 - self.__sprite.image.get_height() // 2
            )
        )

    def move(self, dx: int, dy: int):
        """Move the player.

        Args:
            dx (int): difference in x-axis
            dy (int): difference in y-axis
        """
        direction = "right" if dx > 0 else "left" if dx < 0 else "down" if dy > 0 else "up" if dy < 0 else self.__sprite._direction
        self.__sprite.direction = direction
        
        if self.__position.x + dx < 0:
            self.__position.x = 0
        elif self.__position.x + dx > 100000 - self.__sprite.image.get_width():
            self.__position.x = 100000 - self.__sprite.image.get_width()
        else:
            self.__position.x += dx
            self.__sprite.update()

        if self.__position.y + dy < 0:
            self.__position.y = 0
        elif self.__position.y + dy > 100000 - self.__sprite.image.get_height():
            self.__position.y = 100000 - self.__sprite.image.get_height()
        else:
            self.__position.y += dy
            self.__sprite.update()

    def increase_score(self, points: int):
        """Increase the player's score.

        Args:
            points (int): points to increase
        """
        if points < 0:
            raise ValueError("Points must be a positive integer.")
        
        self.__score += points
    
    def decrease_score(self, points: int):
        """Decrease the player's score.

        Args:
            points (int): points to decrease
        """
        if points < 0:
            raise ValueError("Points must be a positive integer.")
        
        if self.__score - points < 0:
            self.__score = 0
        else:
            self.__score -= points

    # Properties
    @property
    def pos(self) -> tuple[float, float]:
        """Get the position of the player.

        Returns:
            tuple[int, int]: Position of the player in the map surface (x, y)
        """
        return self.__position.x, self.__position.y

    @property
    def score(self) -> int:
        """Get the player's score."""
        return self.__score

    @score.setter
    def score(self, score: int):
        """Set the player's score.

        Args:
            score (int): player's score
        """
        self.__score = score