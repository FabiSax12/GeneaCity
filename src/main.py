import pygame
from clases.api import Api
from clases.game_data import GameDataManager
from screens.screen_manager import ScreenManager
from screens.welcome_screen import WelcomeScreen
from ui.image import ImageHandler
from ui.text import TextRenderer

class GameLoop:
    """Class to handle the game loop."""

    def __init__(self, screen_manager: ScreenManager):
        self.screen_manager = screen_manager

    def run(self):
        """Run the main game loop."""
        while self.screen_manager.current_screen is not None:
            self.screen_manager.update()
            # self.screen_manager.handle_events(pygame.event.get())
            pygame.display.flip()

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
        game_data_manager = GameDataManager()
        api = Api("https://geneacity.life/API")
        text_renderer = TextRenderer("PressStart2P-Regular.ttf")
        image_handler = ImageHandler()
        self.screen_manager = ScreenManager(api, game_data_manager, text_renderer, image_handler, WelcomeScreen)
        self.game_loop = GameLoop(self.screen_manager)

    def start(self):
        """Start the game."""
        self.game_loop.run()

    def close(self):
        """Close the game."""
        pygame.quit()

if __name__ == "__main__":
    game = GameManager.get_instance()
    game.start()
