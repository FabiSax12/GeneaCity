import pygame
from ui.button import Button
from ui.card import ResidentCard
from screens.screen import Screen
from ui.child_overlay import ChildOverlay
from ui.grid_layout import GridLayout
from interfaces.screen_manager import ScreenManagerInterface
from ui.marry_overlay import MarryOverlay

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
            screen_manager,
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
        if resident["id"] == self.screen_manager.game_data.data["partner"]:
            resident_card.action = self.__show_children_creation
        else:
            resident_card.action = self.__show_marry_house_selection

        return resident_card
    
    def __delete_overlay(self):
        """Delete the overlay screen."""
        del self.screen_manager.overlay_screen

    def __show_marry_house_selection(self, resident):
        """Show the house selection screen."""
        self.__delete_overlay()
        self.screen_manager.overlay_screen = MarryOverlay(self.screen_manager, resident, self.__marry)

    def __show_children_creation(self, resident):
        """Show the children creation screen."""
        self.__delete_overlay()
        self.screen_manager.overlay_screen = ChildOverlay(self.screen_manager, self.__create_child)

    def __marry(self, resident_id: int, x: int, y: int, on_error_callback=None):
        """Marry the resident."""
        try:
            response = self.screen_manager.api.marry_inhabitants(
                self.screen_manager.game_data.data["id"],
                resident_id,
                x,
                y
            )

            self.screen_manager.game_data.data["partner"] = resident_id
            self.screen_manager.game_data.data["marital_status"] = "Married"
            # self.screen_manager.game_data.data["house"] = response["houseId"]
            self.screen_manager.game_data.save()

            return response
        
        except ValueError as e:
            print("Error:", e)
            on_error_callback(e)
            
    def __create_child(self, name: str, gender, age):
        """Create a child."""
        try:
            response = self.screen_manager.api.create_children(
                name,
                self.screen_manager.game_data.data["id"],
                gender,
                age
            )

            if response["childId"]:
                print(self.screen_manager.game_data.data)
                self.screen_manager.show_toast("Hijo creado exitosamente.", 3)
                self.screen_manager.game_data.data["family_tree"]["children"].append({"id": response["childId"], "name": name})
                self.screen_manager.game_data.save()
                del self.screen_manager.overlay_screen

        except ValueError as e:
            print("Error:", e)
            self.screen_manager.show_toast("Error al crear hijo.", 3)