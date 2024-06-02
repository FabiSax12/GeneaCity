import pygame
from ui.button import Button
from ui.colors import Colors
from screens.screen import Screen
from interfaces.screen_manager import ScreenManagerInterface

class PauseScreen(Screen):
    def __init__(self, screen_manager: ScreenManagerInterface):
        super().__init__(screen_manager)
        self.__screen_manager = screen_manager
        self.__buttons = [
            Button("Continuar", (300, 300), self._resume),
            Button("Guardar y salir", (300, 400), self._save_and_quit)
        ]

    def _resume(self):
        del self.__screen_manager.overlay_screen

    def _save_and_quit(self):
        self.__screen_manager.game_data.save()

        from screens.welcome_screen import WelcomeScreen
        
        del self.__screen_manager.overlay_screen
        self.__screen_manager.current_screen = WelcomeScreen(self.__screen_manager)

    def update(self, *args, **kwargs):
        if "event" in kwargs:
            event = kwargs["event"]

            for button in self.__buttons:
                button.handle_event(event)

    def draw(self):
        window = self.__screen_manager.window
        white_rect = pygame.Rect(150, 150, 500, 500)
        pygame.draw.rect(window, Colors.WHITE.value, white_rect)
        
        for button in self.__buttons:
            button.draw(window)
