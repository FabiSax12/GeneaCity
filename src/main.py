import pygame
from screens.screen_manager import ScreenManager
from screens.welcome_screen import WelcomeScreen

class GameManager:
    """Class to manage the game."""
    _instance = None

    @staticmethod
    def get_instance():
        """Get the instance of the GameManager class."""
        if GameManager._instance is None:
            GameManager()
        return GameManager._instance

    def __init__(self):
        """Create a new instance of the GameManager class."""
        if GameManager._instance is not None:
            raise Exception("Only one instance of GameManager is allowed")
        
        GameManager._instance = self
        self.screen_manager = ScreenManager()
        self.screen_manager.set_screen(WelcomeScreen(self.screen_manager))

    def start(self):
        """Start the game."""
        while self.screen_manager.get_screen() is not None:
            self.screen_manager.update()
            self.screen_manager.handle_events(pygame.event.get())
            pygame.display.flip()

    def close(self):
        """Close the game."""
        pygame.quit()

if __name__ == "__main__":
    game = GameManager.get_instance()
    game.start()
