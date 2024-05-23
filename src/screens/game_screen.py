import sys
import pygame
from clases.map import Map
from ui.colors import Colors
from clases.house import House
from ui.text import TextRenderer
from screens.screen import Screen
from characters.player import Player
from screens.pause_screen import PauseScreen
from screens.screen_manager import ScreenManager

class GameScreen(Screen):
    """Game screen class."""

    def __init__(self, screen_manager: ScreenManager, player_data: dict):
        super().__init__(screen_manager)
        self.__map = Map((100000, 100000), self.screen_manager.window)
        self.__player = Player(player_data, screen_manager)
        self.__dx_counter = 0
        self.__dy_counter = 0
        self.__houses = []
        self.text_renderer = TextRenderer("src/assets/fonts/PressStart2P-Regular.ttf")
        self.update_houses()

    def handle_events(self, events: list[pygame.event.Event]):
        """Handle pygame events."""
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
            self.move_player(horizontal_movement * 300 * self.screen_manager.dt, 0)
            
        elif horizontal_movement != 0:
            self.move_player(horizontal_movement * 300 * self.screen_manager.dt, 0)

        elif vertical_movement != 0:
            self.move_player(0, vertical_movement * 300 * self.screen_manager.dt)

        self.check_map_update()

        if keys[pygame.K_e]:
            self.__player.interact(self.__houses)

        if keys[pygame.K_ESCAPE]:
            self.screen_manager.current_screen = PauseScreen(self.screen_manager)

    def move_player(self, horizontal_movement: float, vertical_movement: float):
        """Move the player and the map."""
        self.__player.move(horizontal_movement, vertical_movement)
        self.__dx_counter += horizontal_movement
        self.__dy_counter += vertical_movement

        if self.__player.pos[0] > 0 or self.__player.pos[1] > 0:
            self.__map.move(-horizontal_movement, -vertical_movement)
            for house in self.__houses:
                house.move(-horizontal_movement, -vertical_movement)

    def check_map_update(self):
        """Check if the map needs to be updated with new houses."""
        if abs(self.__dx_counter) >= self.screen_manager.window.get_height() // 2 or abs(self.__dy_counter) >= self.screen_manager.window.get_height() // 2:
            self.update_houses()
            self.__dx_counter = 0
            self.__dy_counter = 0

    def update(self):
        """Update screen state."""
        self.handle_input()

    def draw(self):
        """Draw screen."""
        self.__map.draw()
        for house in self.__houses:
            house.draw()

        pos_text, pos_rect = self.text_renderer.render_text_with_outline(f"Posición: {int(self.__player.pos[0])}, {int(self.__player.pos[1])}", "default", ("topleft", (10, 10)))
        name_text, name_rect = self.text_renderer.render_text_with_outline(f"Nombre: {self.__player.name}", "default", ("topleft", (10, 40)))
        age_text, age_rect = self.text_renderer.render_text_with_outline(f"Edad: {self.__player.age}", "default", ("topleft", (10, 70)))
        score_text, score_rect = self.text_renderer.render_text_with_outline(f"Puntuación: {self.__player.score}", "default", ("topleft", (10, 100)))

        self.screen_manager.window.blit(pos_text, pos_rect)
        self.screen_manager.window.blit(name_text, name_rect)
        self.screen_manager.window.blit(age_text, age_rect)
        self.screen_manager.window.blit(score_text, score_rect)

        self.__player.draw(self.screen_manager.window)

    def update_houses(self):
        """Update houses around the player's position."""
        self.screen_manager.api.get_houses(self.__player.pos, self.create_houses)

    def create_houses(self, houses_data: list[dict]):
        """Create house objects from data."""
        self.__houses = [House(house_info, self.screen_manager.window, self.__player.pos) for house_info in houses_data]
