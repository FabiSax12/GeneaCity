from os import name
import pygame
from clases.tree import FamilyTree
from visuals.sprite import Sprite
from characters.person import Person
from interfaces.screen_manager import ScreenManagerInterface
from ui.residents_display import ResidentsOverlay

class Player(Person):
    def __init__(self, person_info: dict, screen_manager: ScreenManagerInterface):
        super().__init__(person_info)
        self.__screen_manager = screen_manager
        self.__score = 0
        self.__position = pygame.Vector2(person_info["position"]["x"], person_info["position"]["y"])
        self.__sprite = Sprite(self.__position, self.info["gender"], self.info["id"])

        person_info["score"] = self.__score
        self.__screen_manager.game_data.data = person_info
        self.__screen_manager.game_data.save()
        self.__family_tree = FamilyTree(self.__screen_manager.game_data.data)

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
        elif self.__position.x + dx > 100000:
            self.__position.x = 100000
        else:
            self.__position.x += dx
            self.__sprite.update()

        if self.__position.y + dy < 0:
            self.__position.y = 0
        elif self.__position.y + dy > 100000:
            self.__position.y = 100000
        else:
            self.__position.y += dy
            self.__sprite.update()

        self.__save_position()

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

    def interact(self, houses: list):
        """Interact with houses if player is near.

        Args:
            houses (list): List of house objects to interact with
        """
        for house in houses:
            if self.__position.distance_to((house.position[0], house.position[1])) < 50:
                residents = self.__screen_manager.api.get_house_residents(house.id)
                residents_display = ResidentsOverlay(residents, self.__screen_manager)
                self.__screen_manager.overlay_screen = residents_display

                for resident in residents:
                    character, level = self.__family_tree.get_node(resident["id"])

                    if character is None:
                        if resident["father"] == self.father and resident["mother"] == self.mother:
                            self.__family_tree.add_member(resident, "sibling", self.__family_tree.root.id, self.__screen_manager.game_data)
                            self.score += 5 * (level + 1)

                        elif resident["father"] == self.id or resident["mother"] == self.id:
                            self.__family_tree.add_member(resident, "child", self.__family_tree.root.id, self.__screen_manager.game_data)
                            self.score += 5 * (level + 1)
                        
                        continue

                    # If the character's father is known and not already in the tree, add it
                    if resident["father"] is not None and not character.father:
                        father_info = self.__screen_manager.api.get_inhabitant_information(resident["father"])
                        self.__family_tree.add_member(father_info, "father", resident["id"], self.__screen_manager.game_data)
                        self.score += 5 * (level + 1)
                    
                    # If the character's mother is known and not already in the tree, add it
                    if resident["mother"] is not None and not character.mother:
                        mother_info = self.__screen_manager.api.get_inhabitant_information(resident["mother"])
                        self.__family_tree.add_member(mother_info, "mother", resident["id"], self.__screen_manager.game_data)
                        self.score += 5 * (level + 1)

    def __save_position(self):
        """Save the player's position to the game data."""
        self.__screen_manager.game_data.data["position"] = {
            "x": int(self.__position.x),
            "y": int(self.__position.y)
        }
        self.__screen_manager.game_data.save()

    def find_id_in_family_tree(self, target_id) -> dict:
        """Find an ID in the family tree."""
        return self.__family_tree.get_node(target_id)
    
    def _update_family_tree(self):
        """Update the family tree in the game data."""
        self.__family_tree._update_game_data(self.__screen_manager.game_data.data)

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
