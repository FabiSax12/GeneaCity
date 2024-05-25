import sys
import pygame
from typing import Literal, Type
from ui.colors import Colors
from ui.text import TextRenderer
from ui.image import ImageHandler
from clases.game_data import GameDataManager
from interfaces.api_interface import ApiInterface

class ScreenManager:
    """Class to manage game screens."""

    def __init__(self, api: ApiInterface, game_data_manager: GameDataManager, text_renderer: TextRenderer, image_handler: ImageHandler, initial_screen_cls: Type[pygame.Surface], window_size: tuple[int, int] = (800, 800)):
        pygame.init()
        pygame.display.set_caption("GeneaCity")
        pygame.display.set_icon(pygame.image.load("src/assets/images/GeneaCity.png"))
        self.__screen = pygame.display.set_mode(window_size)
        self.__initial_screen_cls = initial_screen_cls
        self.__current_screen: pygame.Surface = self.__initial_screen_cls(self)
        self.__previous_screen: pygame.Surface = None
        self.__overlay_screen: pygame.Surface = None
        self.__clock = pygame.time.Clock()
        self.__dt = 0
        self.__api = api
        self.__game_data_manager = game_data_manager
        self.__text_renderer = text_renderer
        self.__image_handler = image_handler
        self.__req_timer = 0
        self.__game_mode: Literal["new_game", "continue"] = None

    def handle_events(self, events: list[pygame.event.Event]):
        """Handle pygame events."""
        if self.__overlay_screen:
            self.__overlay_screen.handle_events(events)
        elif self.__current_screen:
            self.__current_screen.handle_events(events)

    def update(self):
        """Update the screen manager."""
        self.__dt = self.__clock.tick(100) / 1000.0
        self.__req_timer += 0.005
        self.__screen.fill(Colors.GRASS.value)

        if self.__req_timer >= 1:
            self.__req_timer = 0
            # Use callback to handle asynchronous API response
            self.__api.get_houses((0, 0), self.handle_houses_response)

        if self.__current_screen:
            if self.__overlay_screen is None:
                self.__current_screen.update()
            self.__current_screen.draw()

        if self.__overlay_screen:
            shadow = pygame.Surface(self.__screen.get_size(), pygame.SRCALPHA)
            shadow.fill(Colors.BLACK.value)
            shadow.set_alpha(128)
            self.__screen.blit(shadow, (0, 0))
            self.__overlay_screen.update()
            self.__overlay_screen.draw()

    def handle_houses_response(self, houses):
        """Handle the response from the get_houses API call."""
        pass

    # Properties

    @property
    def current_screen(self):
        """Get the current screen."""
        return self.__current_screen
    
    @current_screen.setter
    def current_screen(self, screen):
        """Set the current screen."""
        self.__previous_screen = self.__current_screen
        self.__current_screen = screen

    @property
    def previous_screen(self):
        """Get the previous screen."""
        return self.__previous_screen
    
    @property
    def overlay_screen(self):
        """Get the overlay screen."""
        return self.__overlay_screen
    
    @overlay_screen.setter
    def overlay_screen(self, screen):
        """Set the overlay screen."""
        self.__overlay_screen = screen

    @overlay_screen.deleter
    def overlay_screen(self):
        """Delete the overlay screen."""
        self.__overlay_screen = None

    @property
    def window(self):
        """Get the window."""
        return self.__screen
    
    @property
    def api(self):
        """Get the API."""
        return self.__api
    
    @property
    def game_data(self):
        """Get the game data."""
        return self.__game_data_manager
    
    @property
    def dt(self):
        """Get the delta time."""
        return self.__dt

    @property
    def text_renderer(self):
        """Get the text renderer."""
        return self.__text_renderer

    @property
    def image_handler(self):
        """Get the image handler."""
        return self.__image_handler
    
    @property
    def game_mode(self):
        """Get the game mode."""
        return self.__game_mode
    
    @game_mode.setter
    def game_mode(self, mode: Literal["new", "old"]):
        """Set the game mode."""
        self.__game_mode = mode
