import sys
import pygame
from screens.history_screen import HistoryScreen
from ui.button import Button
from ui.colors import Colors
from screens.screen import Screen
from screens.game_screen import GameScreen
from screens.screen_manager import ScreenManager
from screens.selection_screen import SelectionScreen
from ui.image import ImageHandler
from ui.text import TextRenderer

class WelcomeScreen(Screen):
    """Welcome screen class."""
    
    NEW_GAME_OPTION = "new_game"
    CONTINUE_OPTION = "continue"

    def __init__(self, screen_manager: ScreenManager):
        super().__init__(screen_manager)
        self.selected_option = WelcomeScreen.NEW_GAME_OPTION

        self.text_renderer = TextRenderer("src/assets/fonts/PressStart2P-Regular.ttf")
        self.image_handler = ImageHandler()

        self.title_text, self.title_rect = self.text_renderer.render_text_with_outline("GeneaCity", "title", ("center", (screen_manager.window.get_width() // 2, 150)))
        self.subtitle_text, self.subtitle_rect = self.text_renderer.render_text_with_outline("El juego de la vida", "subtitle", ("center", (screen_manager.window.get_width() // 2, 150 + self.title_text.get_height())))

        self.image, self.image_rect = self.image_handler.load_and_scale_image("src/assets/images/GeneaCity.png", 75, 75, 20 + screen_manager.window.get_width() // 2 + self.title_text.get_width() // 2, 150)

        self.background_image, self.background_image_rect = self.image_handler.load_and_prepare_background("src/assets/images/welcome_screen_bg.webp", screen_manager.window.get_width(), screen_manager.window.get_height())

        self.new_game_button = Button(
            text="Nueva Partida",
            position=(screen_manager.window.get_width() // 2 - 100, screen_manager.window.get_height() // 2),
            on_click=self.start_new_game,
            bg_color=(0, 122, 204),
            text_color=(255, 255, 255),
            hover_bg_color=(0, 162, 255),
        )

        self.continue_button = Button(
            text="Continuar Partida",
            position=(screen_manager.window.get_width() // 2 - 100, screen_manager.window.get_height() // 2 + 60),
            on_click=self.continue_game,
            bg_color=(0, 122, 204),
            text_color=(255, 255, 255),
            hover_bg_color=(0, 162, 255),
        )

        self.history_button = Button(
            text="Historial",
            position=(screen_manager.window.get_width() // 2 - 100, screen_manager.window.get_height() // 2 + 120),
            on_click=self.show_history,
            bg_color=(0, 122, 204),
            text_color=(255, 255, 255),
            hover_bg_color=(0, 162, 255),
        )

    def handle_events(self, events: list[pygame.event.Event]):
        """Handle pygame events."""
        for event in events:
            if event.type == pygame.QUIT:
                self.quit_game()
            self.new_game_button.handle_event(event)
            self.continue_button.handle_event(event)
            self.history_button.handle_event(event)

    def start_new_game(self):
        """Start a new game."""
        self.screen_manager.game_mode = WelcomeScreen.NEW_GAME_OPTION
        self.screen_manager.current_screen = SelectionScreen(self.screen_manager)

    def continue_game(self):
        """Continue the game."""
        game_data = self.screen_manager.game_data.load_last_game()

        if game_data is None: return

        response = self.screen_manager.api.get_inhabitant_information(game_data["id"])

        response["position"] = {
            "x": game_data["position"]["x"],
            "y": game_data["position"]["y"]
        }

        self.screen_manager.game_data.data = response
        self.screen_manager.current_screen = GameScreen(self.screen_manager, response)

    def show_history(self):
        """Show the history screen."""
        self.screen_manager.current_screen = HistoryScreen(self.screen_manager)

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
        self.draw_image()
        self.draw_texts()
        self.new_game_button.draw(self.screen_manager.window)
        self.continue_button.draw(self.screen_manager.window)
        self.history_button.draw(self.screen_manager.window)

    def draw_texts(self):
        """Draw the texts on the screen."""
        self.screen_manager.window.blit(self.title_text, self.title_rect)
        self.screen_manager.window.blit(self.subtitle_text, self.subtitle_rect)

    def draw_image(self):
        """Draw the image on the screen."""
        self.screen_manager.window.blit(self.background_image, self.background_image_rect)
        self.screen_manager.window.blit(self.image, self.image_rect)
        
