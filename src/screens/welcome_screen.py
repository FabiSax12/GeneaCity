import sys
import pygame
from ui.colors import Colors
from screens.screen import Screen
from screens.game_screen import GameScreen
from screens.screen_manager import ScreenManager
from screens.selection_screen import SelectionScreen

player_mock = {
    "id": "5",
    "name": "Cannon",
    "gender": "Male",
    "age": "27",
    "marital_status": "Single",
    "alive": "Alive",
    "father": "0",
    "mother": "1",
    "house": {"x": 250, "y": 250}
}

class WelcomeScreen(Screen):
    """Welcome screen class."""
    
    NEW_GAME_OPTION = "new_game"
    CONTINUE_OPTION = "continue"

    def __init__(self, screen_manager: ScreenManager):
        super().__init__(screen_manager)
        self.font = pygame.font.SysFont("Arial", 30)
        self.title_text = pygame.font.SysFont("Arial", 60).render("GeneaCity", True, Colors.BLACK.value)
        self.subtitle_text = pygame.font.SysFont("Arial", 28).render("El juego de la vida", True, Colors.BLACK.value)

        self.new_game_text = self.font.render("Nueva Partida", True, Colors.BLACK.value)
        self.continue_text = self.font.render("Continuar Partida", True, Colors.BLACK.value)

        self.title_rect = self.title_text.get_rect(center=(screen_manager.window.get_width() // 2, 50))
        self.subtitle_rect = self.subtitle_text.get_rect(center=(screen_manager.window.get_width() // 2, 50 + self.title_text.get_height()))
        self.new_game_rect = self.new_game_text.get_rect(center=(screen_manager.window.get_width() // 2, screen_manager.window.get_height() // 2))
        self.continue_rect = self.continue_text.get_rect(center=(screen_manager.window.get_width() // 2, screen_manager.window.get_height() // 2 + 50))

        self.image = pygame.image.load("src/assets/GeneaCity.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.image_rect = self.image.get_rect(x=20 + screen_manager.window.get_width() // 2 + self.title_text.get_width() // 2, centery=50)

        self.selected_option = WelcomeScreen.NEW_GAME_OPTION

    def handle_events(self, events: list[pygame.event.Event]):
        """Handle pygame events."""
        for event in events:
            if event.type == pygame.QUIT:
                self.quit_game()
                
            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)

    def handle_keydown(self, key: int):
        """Handle keydown events."""
        if key in (pygame.K_w, pygame.K_UP):
            self.selected_option = WelcomeScreen.NEW_GAME_OPTION
        elif key in (pygame.K_s, pygame.K_DOWN):
            self.selected_option = WelcomeScreen.CONTINUE_OPTION
        elif key == pygame.K_ESCAPE:
            self.quit_game()
        elif key == pygame.K_RETURN:
            self.select_option()

    def select_option(self):
        """Select the current option."""
        if self.selected_option == WelcomeScreen.NEW_GAME_OPTION:
            self.screen_manager.current_screen = SelectionScreen(self.screen_manager)
        elif self.selected_option == WelcomeScreen.CONTINUE_OPTION:
            self.screen_manager.current_screen = GameScreen(self.screen_manager, player_mock)

    def quit_game(self):
        """Quit the game."""
        pygame.quit()
        sys.exit()

    def update(self):
        """Update screen state."""
        pass

    def draw(self):
        """Draw screen."""
        self.screen_manager.window.fill(Colors.WHITE.value)
        self.draw_texts()
        self.draw_image()
        self.highlight_selected_option()

    def draw_texts(self):
        """Draw the texts on the screen."""
        self.screen_manager.window.blit(self.title_text, self.title_rect)
        self.screen_manager.window.blit(self.subtitle_text, self.subtitle_rect)
        self.screen_manager.window.blit(self.new_game_text, self.new_game_rect)
        self.screen_manager.window.blit(self.continue_text, self.continue_rect)

    def draw_image(self):
        """Draw the image on the screen."""
        self.screen_manager.window.blit(self.image, self.image_rect)

    def highlight_selected_option(self):
        """Highlight the selected option."""
        if self.selected_option == WelcomeScreen.NEW_GAME_OPTION:
            pygame.draw.rect(self.screen_manager.window, Colors.BLACK.value, self.new_game_rect, 2)
        elif self.selected_option == WelcomeScreen.CONTINUE_OPTION:
            pygame.draw.rect(self.screen_manager.window, Colors.BLACK.value, self.continue_rect, 2)
