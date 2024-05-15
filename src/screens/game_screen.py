import sys
import pygame
from clases.map import Map
from ui.colors import Colors
from clases.house import House
from screens.screen import Screen
from characters.player import Player
from screens.screen_manager import ScreenManager

player_mock = {
    "id": 1, 
    "name": "John", 
    "age": 25, 
    "house": {"x": 250, "y": 250}
}

class GameScreen(Screen):
    """Game screen class."""
    
    def __init__(self, screen_manager: ScreenManager):
        super().__init__(screen_manager)
        self.map = Map(900, 900, self.screen_manager.screen)
        self.player = Player(player_mock, self.screen_manager.screen)
        self.screen_manager.screen.fill(Colors.GRASS.value)

        houses_data = self.screen_manager.api.get_houses(self.player.get_pos())
        self.houses = [ House(house_info) for house_info in houses_data ]

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
            self.player.move(horizontal_movement * 300 * self.screen_manager.dt, 0)

            if self.player.get_pos()[0] > 0:
                self.map.move(-horizontal_movement * 300 * self.screen_manager.dt, 0)
            
        elif horizontal_movement != 0:
            self.player.move(horizontal_movement * 300 * self.screen_manager.dt, 0)

            if self.player.get_pos()[0] > 0:
                self.map.move(-horizontal_movement * 300 * self.screen_manager.dt, 0)

        elif vertical_movement != 0:
            self.player.move(0, vertical_movement * 300 * self.screen_manager.dt)
            
            if self.player.get_pos()[1] > 0:
                self.map.move(0, -vertical_movement * 300 * self.screen_manager.dt)

        if keys[pygame.K_ESCAPE]:
            pygame.quit()

    def update(self):
        """Update screen state."""
        self.handle_input()

    def draw(self):
        """Draw screen."""
        self.map.draw()

        # for house in self.houses:
        #     house.draw(self.screen_manager.screen, self.player.get_pos())

        pos_text = pygame.font.Font(None, 30).render(f"Posición: {int(self.player.get_pos()[0])}, {int(self.player.get_pos()[1])}", True, Colors.WHITE.value)
        self.screen_manager.screen.blit(pos_text, (10, 10))

        self.player.draw(self.screen_manager.screen)

    def update_houses(self):
        self.screen_manager.api.get_houses(self.player.get_pos())
