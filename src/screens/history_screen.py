import sys
from turtle import pos
import pygame
from ui.button import Button
from ui.card import GameCard
from ui.text import TextRenderer
from ui.image import ImageHandler
from screens.screen import Screen
from ui.grid_layout import GridLayout
from screens.screen_manager import ScreenManager

class HistoryScreen(Screen):
    """History screen class."""
    
    def __init__(self, screen_manager: ScreenManager):
        super().__init__(screen_manager)

        self.text_renderer = TextRenderer("PressStart2P-Regular.ttf")
        self.image_handler = ImageHandler()

        self.title_text, self.title_rect = self.text_renderer.render_text_with_outline("Historial", "title", ("center", (screen_manager.window.get_width() // 2, 150)))
        self.background_image, self.background_image_rect = self.image_handler.load_and_prepare_background("src/assets/images/welcome_screen_bg.webp", screen_manager.window.get_width(), screen_manager.window.get_height())

        self.back_button = Button(
            text="Volver",
            position=(screen_manager.window.get_width() // 2 - 100, screen_manager.window.get_height() * (4/5)),
            on_click=self.go_back,
            bg_color=(0, 122, 204),
            text_color=(255, 255, 255),
            hover_bg_color=(0, 162, 255),
        )

        self.history_data = screen_manager.game_data.load()

        if self.history_data == []:
            return

        self.grid_layout = GridLayout(
            card_width=400, 
            card_height=100, 
            columns=1, 
            card_factory=self.create_game_card,
            position=(screen_manager.window.get_width() // 2 - 200, 200)
        )
        self.grid_layout.update_cards(self.screen_manager.window, self.history_data)

    def create_game_card(self, window, width, height, x, y, game):
        return GameCard(window, width, height, x, y, game)

    def handle_events(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.grid_layout.handle_keydown(event.key)
            self.back_button.handle_event(event)

    def update(self):
        pass

    def draw(self):
        self.screen_manager.window.blit(self.background_image, self.background_image_rect)
        self.screen_manager.window.blit(self.title_text, self.title_rect)
        self.back_button.draw(self.screen_manager.window)

        if self.history_data:
            self.grid_layout.draw(self.screen_manager.window)
        else:
            text, rect = self.text_renderer.render_text_with_outline("No hay historial de partidas", "normal", ("center", (self.screen_manager.window.get_width() // 2, 300)))
            self.screen_manager.window.blit(text, rect)

    def go_back(self):
        self.screen_manager.current_screen = self.screen_manager.previous_screen
