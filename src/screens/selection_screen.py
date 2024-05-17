import sys
import pygame
from ui.card import Card
from ui.colors import Colors
from typing import Literal, List, Dict
from screens.game_screen import GameScreen

class SelectionScreen:
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager
        self.font = pygame.font.SysFont("Arial", 25)
        self.title_text = self.font.render("Personajes disponibles", True, Colors.BLACK.value)
        self.cards: List[Card] = []
        self.characters = []
        self.selected_card_index = 0
        self.cards_scroll = 0
        self.load_characters()
        self.selected_character = None

    def load_characters(self):
        self.screen_manager.api.get_available_inhabitants((10000, 10000), self.update_cards)

    def update_cards(self, characters: List[Dict]):
        self.characters = characters
        card_width = 150
        card_height = 100

        self.cards = [
            Card(
                self.screen_manager.window,
                card_width,
                card_height,
                85 + card_width * (i % 4) + 10 * (i % 4),
                100 + card_height * (i // 4) + 10 * (i // 4),
                character
            ) for i, character in enumerate(characters)
        ]

        if self.cards:
            self.cards[0].select()

    def select_character(self):
        character_id = self.cards[self.selected_card_index].character['id']

        if self.cards:
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
        if key == pygame.K_RETURN:
            self.cards[self.selected_card_index].select()
            self.select_character()
            self.screen_manager.current_screen = GameScreen(self.screen_manager, self.selected_character)
        elif key == pygame.K_w:
            self.move_selection_vertical(-4)
        elif key == pygame.K_s:
            self.move_selection_vertical(4)
        elif key == pygame.K_a:
            self.move_selection_horizontal(-1)
        elif key == pygame.K_d:
            self.move_selection_horizontal(1)

    def move_selection_vertical(self, offset: int):
        new_index = self.selected_card_index + offset
        if 0 <= new_index < len(self.cards):
            self.selected_card_index = new_index
            if offset > 0 and self.selected_card_index // 4 > self.cards_scroll + 3:
                self.scroll("down")
            elif offset < 0 and self.selected_card_index // 4 < self.cards_scroll:
                self.scroll("up")
            self.update_card_selection()

    def move_selection_horizontal(self, offset: int):
        new_index = self.selected_card_index + offset
        if 0 <= new_index < len(self.cards) and (self.selected_card_index // 4) == (new_index // 4):
            self.selected_card_index = new_index
            self.update_card_selection()

    def update_card_selection(self):
        for i, card in enumerate(self.cards):
            if i == self.selected_card_index:
                card.select()
            else:
                card.deselect()

    def update(self):
        pass

    def draw(self):
        self.screen_manager.window.fill(Colors.WHITE.value)
        self.screen_manager.window.blit(self.title_text, (self.screen_manager.window.get_width() // 2 - self.title_text.get_width() // 2, 50))
        start_index = self.cards_scroll * 4
        end_index = start_index + 4 * 6
        for card in self.cards[start_index:end_index]:
            card.draw()

    def scroll(self, direction: Literal["up", "down"]):
        if direction == "down" and self.cards_scroll < (len(self.cards) - 1) // 4:
            self.cards_scroll += 1
        elif direction == "up" and self.cards_scroll > 0:
            self.cards_scroll -= 1

        dy = 110 if direction == "down" else -110
        for card in self.cards:
            card.position = (card.position[0], card.position[1] - dy)
