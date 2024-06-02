import sys
import pygame
from ui.colors import Colors
from screens.screen import Screen
from interfaces.screen_manager import ScreenManagerInterface

class InstructionsScreen(Screen):
    def __init__(self, screen_manager: ScreenManagerInterface):
        super().__init__(screen_manager)
        self.font = "src/assets/fonts/PressStart2P-Regular.ttf"
        self.title_text = pygame.font.Font(self.font, 16).render("Instrucciones", True, Colors.BLACK.value)
        self.instructions = [
            "1. Muevete con las teclas de direccion 'W', 'A', 'S', 'D'",
            "2. Interactua con las casas con la tecla 'E'",
            "3. Abre el arbol genealogico con la tecla 'TAB'",
            "4. Pausar el juego con la tecla 'ESC'",
        ]

        self.continue_text = pygame.font.Font(self.font, 7).render("Presiona 'ENTER' para continuar", True, Colors.BLACK.value)

    def update(self, *args, **kwargs):
        if "event" in kwargs:
            event = kwargs["event"]

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    del self._screen_manager.overlay_screen

    def draw(self):
        window_width = self.screen_manager.window.get_width()
        window_height = self.screen_manager.window.get_height()

        background_rect = pygame.Rect( window_width // 6, window_height // 4, window_width // 1.5, window_height // 2)
        pygame.draw.rect(self.screen_manager.window, Colors.WHITE.value, background_rect, border_radius=10)
        self.screen_manager.window.blit(self.title_text, (window_width // 2 - self.title_text.get_width() // 2, window_height // 4 + 50))

        for i, instruction in enumerate(self.instructions):
            text = pygame.font.Font(self.font, 9).render(instruction, True, Colors.BLACK.value)
            self.screen_manager.window.blit(text, (window_width // 2 - text.get_width() // 2, window_height // 4 + 100 + i * 30))

        self.screen_manager.window.blit(self.continue_text, (window_width // 2 - self.continue_text.get_width() // 2, window_height // 4 + 300))