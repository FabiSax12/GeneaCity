import pygame
from ui.button import Button
from ui.card import ResidentCard
from screens.screen import Screen
from ui.grid_layout import GridLayout
from interfaces.screen_manager import ScreenManagerInterface

class ResidentsOverlay(Screen):
    """Display residents in a house."""

    def __init__(self, residents: list[dict], screen_manager: ScreenManagerInterface):
        """Initialize the residents display.

        Args:
            screen_manager (ScreenManager): Screen manager object
            residents (list[dict]): List of residents
        """
        super().__init__(screen_manager)
        self.__residents = residents
        self.__grid_layout = GridLayout(
            card_width=250, 
            card_height=100, 
            columns=2,
            card_factory=self.create_resident_card,
            position=(screen_manager.window.get_width() // 2 - 255, 150)
        )
        self.__grid_layout.update_cards(self.screen_manager.window, self.__residents)
        self.__close_button = Button(
            "Cerrar", 
            (self.screen_manager.window.get_width() // 2 - 100, self.screen_manager.window.get_height() - 150),
            self.__delete_overlay
        )

    def draw_residents(self):
        """Display residents in a house.

        Args:
            house_id (int): House ID
        """
        rect_height = len(self.__residents) * 100
        rect_width = 300
        rect_x = self.screen_manager.window.get_width() // 2 - rect_width // 2
        rect_y = self.screen_manager.window.get_height() // 2 - rect_height // 2

        pygame.draw.rect(self.screen_manager.window, (255, 255, 255), (rect_x, rect_y, rect_width, rect_height))

        for i, resident in enumerate(self.__residents):
            name_text, name_rect = self.screen_manager.text_renderer.render_text_with_outline(resident["name"], "default", ("topleft", (rect_x + 10, rect_y + 10 + i * 100)))

            self.screen_manager.window.blit(name_text, name_rect)

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
        self.__close_button.draw(self.screen_manager.window)
        self.__grid_layout.draw(self.screen_manager.window)

    def update(self, *args, **kwargs):
        """Update the screen."""
        if "event" in kwargs:
            event = kwargs["event"]

            self.__grid_layout.handle_events(event)
            self.__close_button.handle_event(event)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    del self.screen_manager.overlay_screen

    def create_resident_card(self, window, width, height, x, y, resident):
        """Create a resident card."""
        resident_card = ResidentCard(window, width, height, x, y, resident, self.screen_manager.game_data.data)
        resident_card.action = self.__marry

        return resident_card
    
    def __delete_overlay(self):
        """Delete the overlay screen."""
        del self.screen_manager.overlay_screen

    def __marry(self, resident_id: int):
        """Marry the resident."""
        response = self.screen_manager.api.marry_inhabitants(
            self.screen_manager.game_data.data["id"],
            resident_id,
            1000,
            1000
        )

        return response