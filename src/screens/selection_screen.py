import sys
import pygame
from ui.colors import Colors
from typing import List, Dict
from ui.card import CharacterCard
from ui.grid_layout import GridLayout
from screens.game_screen import GameScreen
from screens.screen_manager import ScreenManager

class SelectionScreen:
    def __init__(self, screen_manager: ScreenManager):
        self.screen_manager = screen_manager
        self.font = pygame.font.SysFont("Arial", 25)
        self.title_text = self.font.render("Personajes disponibles", True, Colors.BLACK.value)
        self.characters = []
        self.grid_layout = GridLayout(150, 100, 4, self.create_character_card, position=(85, 100), scroll_trigger=3)
        self.load_characters()
        self.selected_character = None

    def create_character_card(self, window, width, height, x, y, character):
        return CharacterCard(window, width, height, x, y, character)

    def load_characters(self):
        self.screen_manager.api.get_available_inhabitants((10000, 10000), self.update_cards)

    def update_cards(self, characters: List[Dict]):
        self.characters = characters
        self.grid_layout.update_cards(self.screen_manager.window, characters)

    def select_character(self):
        character_id = self.grid_layout.cards[self.grid_layout.selected_card_index].character['id']

        if self.grid_layout.cards:
            response = self.screen_manager.api.select_available_inhabitant(character_id)
            
            if response["status"]:
                self.selected_character = self.screen_manager.api.get_inhabitant_information(character_id)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)

    def handle_keydown(self, key: int):
        self.grid_layout.handle_keydown(key)
        if key == pygame.K_RETURN:
            self.grid_layout.cards[self.grid_layout.selected_card_index].select()
            self.select_character()
            self.screen_manager.current_screen = GameScreen(self.screen_manager, self.selected_character)

    def update(self):
        pass

    def draw(self):
        self.screen_manager.window.fill(Colors.WHITE.value)
        self.screen_manager.window.blit(self.title_text, (self.screen_manager.window.get_width() // 2 - self.title_text.get_width() // 2, 50))
        self.grid_layout.draw(self.screen_manager.window)