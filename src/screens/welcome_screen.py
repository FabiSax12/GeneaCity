import sys
import pygame
from screens.screen import Screen
from screens.screen_manager import ScreenManager
from screens.game_screen import GameScreen
from ui.colors import Colors


class WelcomeScreen(Screen):
    """Welcome screen class."""
    
    def __init__(self, screen_manager: ScreenManager):
        super().__init__(screen_manager)
        self.font = pygame.font.SysFont("Arial", 30)
        self.title_text = pygame.font.SysFont("Arial", 60).render("GeneaCity", True, Colors.BLACK.value)
        self.subtitle_text = pygame.font.SysFont("Arial", 28).render("El juego de la vida", True, Colors.BLACK.value)

        self.new_game_text = self.font.render("Nueva Partida", True, Colors.BLACK.value)
        self.continue_text = self.font.render("Continuar Partida", True, Colors.BLACK.value)

        self.title_rect = self.title_text.get_rect(center=(screen_manager.screen.get_width() // 2, 50))
        self.subtitle_rect = self.subtitle_text.get_rect(center=(screen_manager.screen.get_width() // 2, 50 + self.title_text.get_height()))
        self.new_game_rect = self.new_game_text.get_rect(center=(screen_manager.screen.get_width() // 2, screen_manager.screen.get_height() // 2))
        self.continue_rect = self.continue_text.get_rect(center=(screen_manager.screen.get_width() // 2, screen_manager.screen.get_height() // 2 + 50))

        self.image = pygame.image.load("src/assets/GeneaCity.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.image_rect = self.image.get_rect(x=20 + screen_manager.screen.get_width() // 2 + self.title_text.get_width() // 2, centery=50)

        self.selected_option = "new_game"

    def handle_events(self, events: list[pygame.event.Event]):
        """Handle pygame events."""
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.selected_option = "new_game"
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.selected_option = "continue"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    if self.selected_option == "new_game":
                        self.screen_manager.set_screen(GameScreen(self.screen_manager))
                    elif self.selected_option == "continue":
                        self.screen_manager.set_screen(GameScreen(self.screen_manager))

    def update(self):
        """Update screen state."""
        pass

    def draw(self):
        """Draw screen."""
        self.screen_manager.screen.fill(Colors.WHITE.value)
        self.screen_manager.screen.blit(self.title_text, self.title_rect)
        self.screen_manager.screen.blit(self.subtitle_text, self.subtitle_rect)
        self.screen_manager.screen.blit(self.new_game_text, self.new_game_rect)
        self.screen_manager.screen.blit(self.continue_text, self.continue_rect)
        self.screen_manager.screen.blit(self.image, self.image_rect)
        if self.selected_option == "new_game":
            pygame.draw.rect(self.screen_manager.screen, Colors.BLACK.value, self.new_game_rect, 2)
        elif self.selected_option == "continue":
            pygame.draw.rect(self.screen_manager.screen, Colors.BLACK.value, self.continue_rect, 2)