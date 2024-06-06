import pygame
from abc import ABC, abstractmethod
from clases.game_data import GameDataManager


class ScreenManagerInterface(ABC):
    """Class to manage game screens."""
    def handle_events(self, events: list[pygame.event.Event]):
        pass

    def update(self):
        pass

    def handle_houses_response(self, houses):
        pass

    @property
    @abstractmethod
    def current_screen(self):
        pass
    
    @current_screen.setter
    @abstractmethod
    def current_screen(self, screen):
        pass

    @property
    @abstractmethod
    def previous_screen(self):
        pass
    
    @property
    @abstractmethod
    def overlay_screen(self):
        pass
    
    @overlay_screen.setter
    @abstractmethod
    def overlay_screen(self, screen):
        pass

    @overlay_screen.deleter
    @abstractmethod
    def overlay_screen(self):
        pass

    @property
    @abstractmethod
    def window(self):
        pass
    
    @property
    @abstractmethod
    def api(self):
        pass
    
    @property
    @abstractmethod
    def game_data(self) -> GameDataManager:
        pass
    
    @property
    @abstractmethod
    def dt(self):
        pass

    @property
    @abstractmethod
    def text_renderer(self):
        pass

    @property
    @abstractmethod
    def image_handler(self):
        pass
    
    @property
    @abstractmethod
    def game_mode(self):
        pass
    
    @game_mode.setter
    @abstractmethod
    def game_mode(self, mode: str):
        pass
