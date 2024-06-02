import pygame
from .colors import Colors
from .button import Button
from abc import ABC, abstractmethod

class Card(ABC):
    def __init__(self, window: pygame.Surface, width: int, height: int, x, y):
        self.__window = window
        self.__width = width
        self.__height = height
        self.__rect = pygame.Rect(x, y, self.__width, self.__height)

    @abstractmethod
    def draw(self):
        pygame.draw.rect(self.window, Colors.LIGHT_GRAY.value, self.__rect, border_radius=15)

    @property
    def window(self):
        return self.__window

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
    def width(self):
        return self.__width
    
    @property
    def height(self):
        return self.__height

class SelectableCard(Card, ABC):
    def __init__(self, window: pygame.Surface, width: int, height: int, x: int, y: int):
        super().__init__(window, width, height, x, y)
        self.__selected = False

    def select(self):
        self.__selected = True

    def deselect(self):
        self.__selected = False

    @property
    def selected(self):
        return self.__selected

class ActionableCard(Card, ABC):
    def __init__(self, window: pygame.Surface, width: int, height: int, x: int, y: int):
        super().__init__(window, width, height, x, y)
        self._action = None
        self._action_button = None

    @abstractmethod
    def _create_action_button(self) -> Button:
        pass

    @property
    def action(self):
        return self._action
    
    @action.setter
    def action(self, value):
        self._action = value
        self._action_button = self._create_action_button()

class CharacterCard(SelectableCard):
    def __init__(self, window: pygame.Surface, width: int, height: int, x: int, y: int, character: dict):
        super().__init__(window, width, height, x, y)
        self.__character = character
        self.__selected = False
        self.__image = self.__load_image(character["gender"], character["id"])

    def __load_image(self, gender: str, character_id: int) -> pygame.Surface:
        image_path = f"src/assets/images/spritesheet{gender}{character_id % 4 + 1}.png"
        image = pygame.image.load(image_path)
        image.set_clip(pygame.Rect(0, 0, image.get_width() // 4, image.get_height() // 4))
        image = image.subsurface(image.get_clip())
        return pygame.transform.scale(image, (image.get_width() * 1.5, image.get_height() * 1.5))

    def draw(self):
        color = Colors.LIGHT_GRAY.value if not self.__selected else Colors.LIGHT_BLUE.value
        pygame.draw.rect(self.window, color, self.rect, border_radius=15)

        font = pygame.font.SysFont(None, 25)
        name = font.render(self.__character['name'], True, Colors.BLACK.value)
        gender = font.render(self.__character["gender"], True, Colors.BLACK.value)
        age = font.render(f"{self.__character['age']} años", True, Colors.BLACK.value)

        self.window.blit(name, (self.rect.x + 10, self.rect.y + 10))
        self.window.blit(gender, (self.rect.x + 10, self.rect.y + 40))
        self.window.blit(age, (self.rect.x + 10, self.rect.y + 70))
        self.window.blit(self.__image, (self.rect.x + self.width // 4 * 3 - self.__image.get_width() // 2, self.rect.y + self.height // 2 - self.__image.get_height() // 2))
    
    def select(self):
        self.__selected = True

    def deselect(self):
        self.__selected = False
    
    @property
    def character(self):
        return self.__character

class GameCard(Card):
    def __init__(self, window: pygame.Surface, width: int, height: int, x: int, y: int, game: dict):
        super().__init__(window, width, height, x, y)
        self.__game = game
        self.__selected = False
        self.__name = pygame.font.Font("src/assets/fonts/PressStart2P-Regular.ttf", 10).render(game["name"], True, Colors.BLACK.value)
        self.__points = pygame.font.Font("src/assets/fonts/PressStart2P-Regular.ttf", 10).render(f"Puntos: {game['score']}", True, Colors.BLACK.value)

    def draw(self):
        pygame.draw.rect(self.window, Colors.WHITE.value, self.rect, border_radius=15)
        self.window.blit(self.__name, (self.position[0] + 10, self.position[1] + 10))
        self.window.blit(self.__points, (self.position[0] + 10, self.position[1] + 40))
    
    def select(self):
        self.__selected = True

    def deselect(self):
        self.__selected = False
    
    @property
    def game(self):
        return self.__game

class ResidentCard(ActionableCard):
    def __init__(self, window: pygame.Surface, width: int, height: int, x: int, y: int, resident: dict, player: dict):
        super().__init__(window, width, height, x, y)
        self.__resident = resident
        self.__player = player
        self.__name = pygame.font.Font("src/assets/fonts/PressStart2P-Regular.ttf", 10).render(resident["name"], True, Colors.BLACK.value)
        self.__marital_status = pygame.font.Font("src/assets/fonts/PressStart2P-Regular.ttf", 7).render(f"Estado civil: {resident['marital_status']}", True, Colors.BLACK.value)
        self.__gender = pygame.font.Font("src/assets/fonts/PressStart2P-Regular.ttf", 7).render(f"Género: {resident["gender"]}", True, Colors.BLACK.value)
        self.__image = self.__load_image(resident["gender"], resident["id"])

    def __load_image(self, gender: str, character_id: int) -> pygame.Surface:
        image_path = f"src/assets/images/spritesheet{gender}{character_id % 4 + 1}.png"
        image = pygame.image.load(image_path)
        image.set_clip(pygame.Rect(0, 0, image.get_width() // 4, image.get_height() // 4))
        image = image.subsurface(image.get_clip())
        return pygame.transform.scale(image, (image.get_width() * 1.5, image.get_height() * 1.5))

    def handle_event(self, event: pygame.event.Event):
        if (self._action_button and
            self.__resident["marital_status"] == "Single" and
            self.__player["marital_status"] == "Single" and
            self.__resident["age"] >= 18 and
            self.__resident["age"] <= 45 and
            self.__resident["gender"] != self.__player["gender"]):

            self._action_button.handle_event(event)

        if self._action_button and self.__player["partner"] == self.__resident["id"]:
            self._action_button.handle_event(event)    

    def draw(self):
        pygame.draw.rect(self.window, Colors.WHITE.value, self.rect, border_radius=15)
        self.window.blit(self.__name, (self.position[0] + 10, self.position[1] + 10))
        self.window.blit(self.__marital_status, (self.position[0] + 10, self.position[1] + 25))
        self.window.blit(self.__gender, (self.position[0] + 10, self.position[1] + 40))
        self.window.blit(self.__image, (self.position[0] + self.width // 4 * 3 - self.__image.get_width() // 2, self.position[1] + self.height // 2 - self.__image.get_height() // 2))

        if (self._action_button and
            self.__resident["marital_status"] == "Single" and
            self.__player["marital_status"] == "Single" and
            self.__resident["age"] >= 18 and
            self.__resident["age"] <= 45 and
            self.__resident["gender"] != self.__player["gender"]):

            self._action_button.draw(self.window)

        if self._action_button and self.__player["partner"] == self.__resident["id"]:
            self._action_button.draw(self.window)

    def _create_action_button(self) -> Button:
        if self.__player["partner"] == self.__resident["id"]:
            print("Es tu pareja")
            return Button(
                text="Tener hijo",
                position=(self.position[0] + self.width // 12, self.height // 4 * 3 - 10 + self.position[1]),
                on_click=lambda: self.action(self.__resident),
                size=(self.width // 3, 20),
                font_size=25,
                bg_color=Colors.RED.value,
                hover_bg_color=Colors.DARK_PINK.value,
                border_radius=5
            )
            
        return Button(
            text="Casarse",
            position=(self.position[0] + self.width // 12, self.height // 4 * 3 - 10 + self.position[1]),
            on_click=lambda: self.action(self.__resident),
            size=(self.width // 3, 20),
            font_size=25,
            bg_color=Colors.RED.value,
            hover_bg_color=Colors.DARK_PINK.value,
            border_radius=5
        )
