import sys
import pygame
from clases.map import Map
from ui.colors import Colors
from clases.house import House
from screens.screen import Screen
from characters.player import Player
from screens.screen_manager import ScreenManager

player_mock = {
    "id": "5",
    "name": "Cannon",
    "gender": "Male",
    "age": "27",
    "marital_status": "Single",
    "alive": "Alive",
    "father": "0",
    "mother": "1",
    "house": {"x": 250, "y": 250}
}

class GameScreen(Screen):
    """Game screen class."""
    
    def __init__(self, screen_manager: ScreenManager):
        super().__init__(screen_manager)
        self.__map = Map(900, 900, self.screen_manager.window)
        self.__player = Player(player_mock)
        self.__dx_counter = 0
        self.__dy_counter = 0
        self.__houses = []
        self.update_houses()

    def handle_events(self, events: list[pygame.event.Event]):
        """Handle pygame events.
        Args:
            events (list[pygame.event.Event]): list of pygame events
        """
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def handle_input(self):
        """Handle input events."""
        keys = pygame.key.get_pressed()
        horizontal_movement = 0
        vertical_movement = 0

        if keys[pygame.K_w]:
            vertical_movement -= 1
        if keys[pygame.K_s]:
            vertical_movement += 1
        if keys[pygame.K_a]:
            horizontal_movement -= 1
        if keys[pygame.K_d]:
            horizontal_movement += 1

        if horizontal_movement != 0 and vertical_movement != 0:
            self.__player.move(horizontal_movement * 300 * self.screen_manager.dt, 0)

            self.__dx_counter += horizontal_movement * 300 * self.screen_manager.dt

            if self.__player.pos[0] > 0:
                self.__map.move(-horizontal_movement * 300 * self.screen_manager.dt, 0)
                for house in self.__houses:
                    house.move(-horizontal_movement * 300 * self.screen_manager.dt, 0)
            
        elif horizontal_movement != 0:
            self.__player.move(horizontal_movement * 300 * self.screen_manager.dt, 0)
            self.__dx_counter += horizontal_movement * 300 * self.screen_manager.dt

            if self.__player.pos[0] > 0:
                self.__map.move(-horizontal_movement * 300 * self.screen_manager.dt, 0)
                for house in self.__houses:
                    house.move(-horizontal_movement * 300 * self.screen_manager.dt, 0)

        elif vertical_movement != 0:
            self.__player.move(0, vertical_movement * 300 * self.screen_manager.dt)
            self.__dy_counter += vertical_movement * 300 * self.screen_manager.dt
            
            if self.__player.pos[1] > 0:
                self.__map.move(0, -vertical_movement * 300 * self.screen_manager.dt)
                for house in self.__houses:
                    house.move(0, -vertical_movement * 300 * self.screen_manager.dt)

        if abs(self.__dx_counter) >= self.screen_manager.window.get_height() // 2 or abs(self.__dy_counter) >= self.screen_manager.window.get_height() // 2:
            self.update_houses()
            self.__dx_counter = 0
            self.__dy_counter = 0

        if keys[pygame.K_ESCAPE]:
            pygame.quit()

    def update(self):
        """Update screen state."""
        self.handle_input()

    def draw(self):
        """Draw screen."""
        self.__map.draw()

        for house in self.__houses:
            house.draw()

        pos_text = pygame.font.Font(None, 30).render(f"Posición: {int(self.__player.pos[0])}, {int(self.__player.pos[1])}", True, Colors.WHITE.value)
        self.screen_manager.window.blit(pos_text, (10, 10))

        self.__player.draw(self.screen_manager.window)

    def update_houses(self):
        self.screen_manager.api.get_houses(self.__player.pos, self.create_houses)

    def create_houses(self, houses_data: list[dict]):
        self.__houses = [ House(house_info, self.screen_manager.window, self.__player.pos) for house_info in houses_data ]
        print("Created houses: ", [house.id for house in self.__houses])