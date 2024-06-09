from screens.screen import Screen

class LoadingScreen(Screen):
    """Loading screen class."""
    def __init__(self, screen_manager):
        """Constructor for the loading screen.

        Args:
            screen_manager (ScreenManager): Screen manager instance
        """
        super().__init__(screen_manager)
        self.__loading_text, self.__loading_text_rect = self.screen_manager.text_renderer.render_text_with_outline(
            "Obteniendo datos...",
            "subtitle",
            (
                "center", 
                (self.screen_manager.window.get_width() // 2, self.screen_manager.window.get_height() // 2)
            )
        )

    def draw(self):
        """Render the loading screen."""
        self.screen_manager.window.blit(self.__loading_text, self.__loading_text_rect)

    def update(self, *args, **kwargs):
        """Update the loading screen."""
        pass