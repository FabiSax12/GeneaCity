import sys
import pygame
from ui.button import Button
from ui.text import TextRenderer
from ui.image import ImageHandler
from screens.screen import Screen
from screens.screen_manager import ScreenManager
from ui.game_card import GameCard

class HistoryScreen(Screen):
    """History screen class."""
    
    def __init__(self, screen_manager: ScreenManager):
        super().__init__(screen_manager)

        self.text_renderer = TextRenderer("src/assets/fonts/PressStart2P-Regular.ttf")
        self.image_handler = ImageHandler()

        self.title_text, self.title_rect = self.text_renderer.render_text_with_outline("Historial", "title", ("center", (screen_manager.window.get_width() // 2, 150)))
        self.background_image, self.background_image_rect = self.image_handler.load_and_prepare_background("src/assets/images/welcome_screen_bg.webp", screen_manager.window.get_width(), screen_manager.window.get_height())

        self.back_button = Button(
            text="Volver",
            position=(screen_manager.window.get_width() // 2 - 100, screen_manager.window.get_height() // 2 + 120),
            on_click=self.go_back,
            bg_color=(0, 122, 204),
            text_color=(255, 255, 255),
            hover_bg_color=(0, 162, 255),
        )

        self.history_data = screen_manager.game_data.load()

        self.__cards = [
            GameCard(
                screen_manager,
                data,
                (
                    screen_manager.window.get_width() // 2 - 200,
                    200 + i * 110
                )
            ) 
            for i, data in enumerate(self.history_data)
        ]
            
    def handle_events(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            self.back_button.handle_event(event)

    def update(self):
        pass

    def draw(self):
        self.screen_manager.window.blit(self.background_image, self.background_image_rect)
        self.screen_manager.window.blit(self.title_text, self.title_rect)
        self.back_button.draw(self.screen_manager.window)

        for card in self.__cards:
            card.draw()

    def go_back(self):
        self.screen_manager.current_screen = self.screen_manager.previous_screen