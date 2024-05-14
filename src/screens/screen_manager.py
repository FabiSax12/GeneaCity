import pygame
from clases.api import Api

class ScreenManager:
    """Class to manage game screens."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        self.clock = pygame.time.Clock()
        self.current_screen = None
        self.dt = 0
        self.api = Api("https://geneacity.life/API")
    
    def set_screen(self, screen):
        """Set the current screen."""
        self.current_screen = screen
    
    def get_screen(self):
        """Get the current screen."""
        return self.current_screen
    
    def handle_events(self, events: list[pygame.event.Event]):
        """Handle pygame events."""
        if self.current_screen:
            self.current_screen.handle_events(events)

    def update(self):
        """Update the screen manager."""
        self.dt = self.clock.tick(60) / 1000.0
        
        if self.current_screen:
            self.current_screen.update()
            self.current_screen.draw()
