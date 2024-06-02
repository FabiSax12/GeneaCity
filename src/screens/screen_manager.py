import pygame
from typing import Type
from screens.game_screen import GameScreen
from screens.screen import Screen
from interfaces.api_interface import ApiInterface
from clases.game_data import GameDataManager
from ui.text import TextRenderer
from ui.image import ImageHandler
from interfaces.screen_manager import ScreenManagerInterface
from clases.event_handler import EventHandler
from ui.toast import Toast

class ScreenManager(ScreenManagerInterface):
    """Class to manage game screens."""

    def __init__(self, api: ApiInterface, game_data_manager: GameDataManager, text_renderer: TextRenderer, image_handler: ImageHandler, initial_screen_cls: Type[Screen], window_size: tuple[int, int] = (800, 800)):
        pygame.init()
        pygame.display.set_caption("GeneaCity")
        pygame.display.set_icon(pygame.image.load("src/assets/images/GeneaCity.png"))
        self.__screen = pygame.display.set_mode(window_size)
        self.__text_renderer = text_renderer
        self.__image_handler = image_handler
        self.__initial_screen_cls = initial_screen_cls
        self.__current_screen: Screen = self.__initial_screen_cls(self)
        self.__previous_screen: Screen = None
        self.__overlay_screen: Screen = None
        self.__toast = None
        self.__event_handler = EventHandler()
        self.__event_handler.attach(self.__current_screen)
        self.__clock = pygame.time.Clock()
        self.__dt = 0
        self.__api = api
        self.__game_data_manager = game_data_manager
        self.__req_timer = 0
        self.__game_mode: str = None

    # def handle_events(self, events: list[pygame.event.Event]):
    #     """Handle pygame events."""
    #     if self.__overlay_screen:
    #         self.__overlay_screen.handle_events(events)
    #     elif self.__current_screen:
    #         self.__current_screen.handle_events(events)

    def update(self):
        """Update the screen manager."""
        self.__dt = self.__clock.tick(100) / 1000.0
        self.__req_timer += 0.005
        self.__screen.fill((0, 0, 0))  # Fill screen with black color

        if self.__req_timer >= 1:
            self.__req_timer = 0
            # Use callback to handle asynchronous API response
            self.__api.get_houses((0, 0), self.handle_houses_response)

        if self.__current_screen:

            if isinstance(self.__current_screen, GameScreen) and self.__overlay_screen is None:
                self.__current_screen.handle_input()

            self.__event_handler.handle_events()
            self.__current_screen.draw()

        if self.__overlay_screen:
            shadow = pygame.Surface(self.__screen.get_size(), pygame.SRCALPHA)
            shadow.fill((0, 0, 0, 128))  # Black shadow with transparency
            self.__screen.blit(shadow, (0, 0))
            self.__overlay_screen.update()
            self.__overlay_screen.draw()

        if self.__toast:
            self.__toast.update()
            self.__toast.draw(self.window)

    def handle_houses_response(self, houses):
        """Handle the response from the get_houses API call."""
        pass

    def show_toast(self, message: str, duration: int = 2):
        """Show a toast message."""
        print("toast")
        self.__toast = Toast(message, self.window.get_width() - 210, self.window.get_height() - 60, 200, 50, duration=duration)

    @property
    def current_screen(self):
        """Get the current screen."""
        return self.__current_screen
    
    @current_screen.setter
    def current_screen(self, screen: Screen):
        """Set the current screen."""
        self.__previous_screen = self.__current_screen
        self.__event_handler.dettach(self.__current_screen)
        self.__current_screen = screen
        self.__event_handler.attach(screen)

    @property
    def previous_screen(self):
        """Get the previous screen."""
        return self.__previous_screen
    
    @property
    def overlay_screen(self):
        """Get the overlay screen."""
        return self.__overlay_screen
    
    @overlay_screen.setter
    def overlay_screen(self, screen: Screen):
        """Set the overlay screen."""
        self.__overlay_screen = screen
        self.__event_handler.attach(screen)

    @overlay_screen.deleter
    def overlay_screen(self):
        """Delete the overlay screen."""
        self.__event_handler.dettach(self.__overlay_screen)
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
    def game_mode(self, mode: str):
        """Set the game mode."""
        self.__game_mode = mode
