import pygame
from clases.api import Api
from ui.colors import Colors

class ScreenManager:
    """Class to manage game screens."""

    def __init__(self):
        pygame.init()
        self.__screen = pygame.display.set_mode((800, 800))
        self.__current_screen: pygame.Surface = None
        self.__clock = pygame.time.Clock()
        self.__dt = 0
        self.__api = Api("https://geneacity.life/API")
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
            # self.api.get_houses((0, 0))

        if self.__current_screen:
            self.__current_screen.update()
            self.__current_screen.draw()

    # Properties

    @property
    def current_screen(self):
        """Get the screen."""
        return self.__current_screen
    
    @current_screen.setter
    def current_screen(self, screen):
        """Set the screen."""
        self.__current_screen = screen

    @property
    def window(self):
        """Get the window."""
        return self.__screen
    
    @property
    def api(self):
        """Get the api."""
        return self.__api
    
    @property
    def dt(self):
        """Get the delta time."""
        return self.__dt