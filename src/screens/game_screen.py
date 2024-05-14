import pygame
import sys
from clases.map import Map
from screens.screen import Screen
from screens.screen_manager import ScreenManager
from characters.player import Player
from clases.house import House
from clases.game import Renderer

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
        self.map = Map(500, 500)
        self.player = Player(player_mock, self.screen_manager.get_screen())
        # self.event_handler = EventHandler()
        # self.input_handler = InputHandler(self.player)

        houses_data = self.screen_manager.api.get_houses(self.player.get_pos())
        self.houses = [House(house_info) for house_info in houses_data]
        self.renderer = Renderer(self.screen_manager.screen, self.houses)

        self.running = False

    def handle_events(self, events: list[pygame.event.Event]):
        """Handle pygame events."""
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # if event.type == pygame.KEYDOWN:
            #     self.update_houses()

            # self.player.sprite.event_listener(event)

    def handle_input(self):
        """Handle user input."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: self.player.move(0, -300 * self.screen_manager.dt)
        if keys[pygame.K_s]: self.player.move(0, 300 * self.screen_manager.dt)
        if keys[pygame.K_a]: self.player.move(-300 * self.screen_manager.dt, 0)
        if keys[pygame.K_d]: self.player.move(300 * self.screen_manager.dt, 0)
        if keys[pygame.K_ESCAPE]: pygame.quit()

    def update(self):
        """Update screen state."""
        # self.running = not self.event_handler.handle_events()
        self.handle_input()
        self.renderer.render(self.player)

    def draw(self):
        """Draw screen."""
        # self.screen_manager.screen.fill(Colors.GRASS.value)
        for house in self.houses:
            house.draw(self.screen_manager.screen)
        self.player.draw(self.screen_manager.screen)
        self.map.draw(self.screen_manager.screen, self.player.get_pos())

    def update_houses(self):
        self.screen_manager.api.get_houses(self.player.get_pos())
