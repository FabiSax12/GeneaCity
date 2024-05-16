from abc import ABC, abstractmethod
from screens.screen_manager import ScreenManager


class Screen(ABC):
    def __init__(self, screen_manager: ScreenManager):
        self.__screen_manager = screen_manager

    @property
    def screen_manager(self):
        return self.__screen_manager

    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def draw(self):
        pass