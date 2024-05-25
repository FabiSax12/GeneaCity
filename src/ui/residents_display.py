import pygame
from requests import delete
from ui.button import Button
from pygame.event import Event
from screens.screen import Screen
from screens.screen_manager import ScreenManager

class ResidentsOverlay(Screen):
    """Display residents in a house."""

    def __init__(self, residents: list[dict], screen_manager: ScreenManager):
        """Initialize the residents display.

        Args:
            screen_manager (ScreenManager): Screen manager object
            residents (list[dict]): List of residents
        """
        self.__screen_manager = screen_manager
        self.__residents = residents
        self.__close_button = Button(
            "Cerrar", 
            (self.__screen_manager.window.get_width() // 2 - 100, self.__screen_manager.window.get_height() - 50),
            self.__delete_overlay
        )

    def draw_residents(self):
        """Display residents in a house.

        Args:
            house_id (int): House ID
        """
        rect_height = len(self.__residents) * 100
        rect_width = 300
        rect_x = self.__screen_manager.window.get_width() // 2 - rect_width // 2
        rect_y = self.__screen_manager.window.get_height() // 2 - rect_height // 2

        pygame.draw.rect(self.__screen_manager.window, (255, 255, 255), (rect_x, rect_y, rect_width, rect_height))

        for i, resident in enumerate(self.__residents):
            name_text, name_rect = self.__screen_manager.text_renderer.render_text_with_outline(resident["name"], "default", ("topleft", (rect_x + 10, rect_y + 10 + i * 100)))

            self.__screen_manager.window.blit(name_text, name_rect)

    def print_residents(self):
        """Print residents in a house."""
        for resident in self.__residents:
            print("ID: ", resident["id"])
            print("Name: ", resident["name"])
            print("Gender: ", resident["gender"])
            print("Marital status: ", resident["marital_status"])
            print("Father: ", resident["father"])
            print("Mother: ", resident["mother"])

    def draw(self):
        """Draw the screen."""

        def delete_overlay():
            del self.__screen_manager.overlay_screen

        
        self.__close_button.draw(self.__screen_manager.window)
        self.draw_residents()

    def update(self):
        pass

    def handle_events(self, events: list[Event]):
        for event in events:
            self.__close_button.handle_event(event)
            
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    del self.__screen_manager.overlay_screen
                    break

    def __delete_overlay(self):
        """Delete the overlay screen."""
        del self.__screen_manager.overlay_screen