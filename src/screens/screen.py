import pygame
from abc import ABC, abstractmethod
from interfaces.observer_interface import IObserver
from interfaces.screen_manager import ScreenManagerInterface

class Screen(IObserver, ABC):
    def __init__(self, screen_manager: ScreenManagerInterface):
        self._screen_manager = screen_manager
    
    @abstractmethod
    def draw(self):
        """Draw the screen content."""
        pass

    @property
    def screen_manager(self):
        return self._screen_manager
