from ui.button import Button
from screens.screen import Screen

class DeathScreen(Screen):
    """Death screen class."""

    def __init__(self, screen_manager):
        super().__init__(screen_manager)

        self.text_renderer = screen_manager.text_renderer
        self.image_handler = screen_manager.image_handler

        self.title_text, self.title_rect = self.text_renderer.render_text_with_outline("Has muerto", "title", ("center", (screen_manager.window.get_width() // 2, 150)))
        self.subtitle_text, self.subtitle_rect = self.text_renderer.render_text_with_outline("Tu legado no ha sido suficiente", "subtitle", ("center", (screen_manager.window.get_width() // 2, 150 + self.title_text.get_height())))

        # self.image, self.image_rect = self.image_handler.load_and_scale_image("src/assets/images/death.png", 75, 75, 20 + screen_manager.window.get_width() // 2 + self.title_text.get_width() // 2, 150)

        self.background_image, self.background_image_rect = self.image_handler.load_and_prepare_background("src/assets/images/game_over_background.webp", screen_manager.window.get_width(), screen_manager.window.get_height(), alpha=130)

        self.new_game_button = Button(
            text="Volver",
            position=(screen_manager.window.get_width() // 2 - 100, screen_manager.window.get_height() // 2),
            on_click=self.screen_manager.back,
            bg_color=(0, 122, 204),
            text_color=(255, 255, 255),
            hover_bg_color=(0, 162, 255),
        )

    def draw(self):
        self.screen_manager.window.blit(self.background_image, self.background_image_rect)

        self.screen_manager.window.blit(self.title_text, self.title_rect)
        self.screen_manager.window.blit(self.subtitle_text, self.subtitle_rect)

        self.new_game_button.draw(self.screen_manager.window)

    def update(self, *args, **kwargs):
        if "event" in kwargs:
            event = kwargs["event"]

            self.new_game_button.handle_event(event)
