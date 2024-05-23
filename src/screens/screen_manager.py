import pygame
from ui.colors import Colors
from interfaces.api_interface import ApiInterface
from clases.game_data import GameData

class ScreenManager:
    """Class to manage game screens."""

    def __init__(self, api: ApiInterface, game_data_manager: GameData):
        pygame.init()
        pygame.display.set_caption("GeneaCity")
        pygame.display.set_icon(pygame.image.load("src/assets/images/GeneaCity.png"))
        self.__screen = pygame.display.set_mode((800, 800))
        self.__current_screen: pygame.Surface = None
        self.__previous_screen: pygame.Surface = None
        self.__clock = pygame.time.Clock()
        self.__dt = 0
        self.__api = api
        self.__game_data_manager = game_data_manager
        self.__req_timer = 0
    
    def handle_events(self, events: list[pygame.event.Event]):
        """Handle pygame events.
        
        Args:
            events (list[pygame.event.Event]): list of pygame events
        """
        if self.__current_screen:
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
            self.__current_screen.update()
            self.__current_screen.draw()

    def handle_houses_response(self, houses):
        """Handle the response from the get_houses API call."""
        pass

    # Properties

    @property
    def current_screen(self):
        """Get the screen."""
        return self.__current_screen
    
    @current_screen.setter
    def current_screen(self, screen):
        """Set the screen."""
        self.__previous_screen = self.__current_screen
        self.__current_screen = screen

    @property
    def previous_screen(self):
        """Get the screen."""
        return self.__previous_screen

    @property
    def window(self):
        """Get the window."""
        return self.__screen
    
    @property
    def api(self):
        """Get the api."""
        return self.__api
    
    @property
    def game_data(self):
        """Get the game data."""
        return self.__game_data_manager
    
    @property
    def dt(self):
        """Get the delta time."""
        return self.__dt
