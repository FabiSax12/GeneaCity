import pygame
from ui.colors import Colors
from screens.screen_manager import ScreenManager


class GameCard:
    def __init__(self, screen_manager: ScreenManager, game: dict, pos: tuple[int, int]):
        self.__screen_manager = screen_manager
        self.__game = game
        self.__width = screen_manager.window.get_width() // 2
        self.__height = 100

        self.__card = pygame.Rect(pos[0], pos[1], self.__width, self.__height)

        self.__name_text, self.__name_rect = screen_manager.text_renderer.render_text(
            game["name"], 
            "normal", 
            (pos[0] + 10, pos[1] + 20),
            Colors.BLACK.value
        )
        self.__points_text, self.__points_rect = screen_manager.text_renderer.render_text(
            f"Puntos: {game['points']}",
            "normal",
            (pos[0] + self.__name_rect.x, pos[1] + 20),
            Colors.BLACK.value
        )

    def draw(self):
        print("Rendering", self.__name_rect, self.__points_rect)
        pygame.draw.rect(self.__screen_manager.window, Colors.WHITE.value, self.__card)
        self.__screen_manager.window.blit(self.__name_text, self.__name_rect)
        self.__screen_manager.window.blit(self.__points_text, self.__points_rect)







