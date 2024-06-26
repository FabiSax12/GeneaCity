import pygame
from clases.map import Map
from clases.tree import FamilyTree
from screens.tree_screen import FamilyTreeScreen
from ui.colors import Colors
from clases.house import House
from screens.screen import Screen
from characters.player import Player
from screens.pause_screen import PauseScreen
from interfaces.screen_manager import ScreenManagerInterface

class GameScreen(Screen):
    """Game screen class."""

    def __init__(self, screen_manager: ScreenManagerInterface, player_data: dict):
        super().__init__(screen_manager)
        self.__map = Map((100000, 100000), self.screen_manager.window)
        self.__player = Player(player_data, screen_manager)
        self.__dx_counter = 0
        self.__dy_counter = 0
        self.__houses = []
        self.text_renderer = screen_manager.text_renderer
        self.update_houses()

    def handle_input(self):
        """Handle input events."""
        keys = pygame.key.get_pressed()
        horizontal_movement = 0
        vertical_movement = 0

        if keys[pygame.K_w] and self.__player.pos[1] > 0:
            vertical_movement -= 1
        if keys[pygame.K_s] and self.__player.pos[1] < self.__map.height:
            vertical_movement += 1
        if keys[pygame.K_a] and self.__player.pos[0] > 0:
            horizontal_movement -= 1
        if keys[pygame.K_d] and self.__player.pos[0] < self.__map.width:
            horizontal_movement += 1

        if horizontal_movement != 0 and vertical_movement != 0:
            self.move_player(horizontal_movement * 300 * self.screen_manager.dt, 0)
            
        elif horizontal_movement != 0:
            self.move_player(horizontal_movement * 300 * self.screen_manager.dt, 0)

        elif vertical_movement != 0:
            self.move_player(0, vertical_movement * 300 * self.screen_manager.dt)

        self.check_map_update()

    def move_player(self, horizontal_movement: float, vertical_movement: float):
        """Move the player and the map."""
        self.__player.move(horizontal_movement, vertical_movement)
        self.__dx_counter += horizontal_movement
        self.__dy_counter += vertical_movement

        if self.__player.pos[0] > 0 and self.__player.pos[0] < 100000 or self.__player.pos[1] > 0 and self.__player.pos[1] < 100000:
            self.__map.move(-horizontal_movement, -vertical_movement)
            for house in self.__houses:
                house.move(-horizontal_movement, -vertical_movement)
        

    def check_map_update(self):
        """Check if the map needs to be updated with new houses."""
        if abs(self.__dx_counter) >= self.screen_manager.window.get_height() // 4 or abs(self.__dy_counter) >= self.screen_manager.window.get_height() // 4:
            self.update_houses()
            self.__dx_counter = 0
            self.__dy_counter = 0

    def update(self, *args, **kwargs):
        """Update screen state."""
        if "event" in kwargs:
            event = kwargs["event"]
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.screen_manager.overlay_screen = PauseScreen(self.screen_manager)
            
                if event.key == pygame.K_e:
                    self.__player.interact(self.__houses)

                if event.key == pygame.K_TAB:
                    self.screen_manager.overlay_screen = FamilyTreeScreen(self.screen_manager, self.__player.id)
                    
    def draw(self):
        """Draw screen."""
        pygame.Surface.fill(self.screen_manager.window, Colors.GRASS.value)
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
