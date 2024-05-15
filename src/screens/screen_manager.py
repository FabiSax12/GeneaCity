import pygame
from clases.api import Api
from ui.colors import Colors

class ScreenManager:
    """Class to manage game screens."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        self.current_screen = None
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.api = Api("https://geneacity.life/API")
        self.req_timer = 0
    
    def set_screen(self, screen):
        """Set the current screen.

        Args:
            screen (_type_): screen to set
        """
        pygame.display.flip()
        self.screen.fill(Colors.GRASS.value)
        self.current_screen = screen
    
    def get_screen(self):
        """Get the current screen."""
        return self.current_screen
    
    def handle_events(self, events: list[pygame.event.Event]):
        """Handle pygame events.
        
        Args:
            events (list[pygame.event.Event]): list of pygame events
        """
        if self.current_screen:
            self.current_screen.handle_events(events)

    def update(self):
        """Update the screen manager."""
        self.dt = self.clock.tick(100) / 1000.0
        self.req_timer += 0.005
        self.screen.fill(Colors.GRASS.value)

        if self.req_timer >= 1:
            self.req_timer = 0
            # self.api.get_houses((0, 0))
            print("new req")

        if self.current_screen:
            self.current_screen.update()
            self.current_screen.draw()
