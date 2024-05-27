import pygame
from abc import ABC, abstractmethod
from interfaces.screen_manager import ScreenManagerInterface

class Screen(ABC):
    def __init__(self, screen_manager: ScreenManagerInterface):
        self._screen_manager = screen_manager

    @property
    def screen_manager(self):
        return self._screen_manager

    @abstractmethod
    def update(self):
        """Update the screen state."""
        pass
    
    @abstractmethod
    def draw(self):
        """Draw the screen content."""
        pass

    @abstractmethod
    def handle_events(self, events: list[pygame.event.Event]):
        """Handle pygame events."""
        pass
