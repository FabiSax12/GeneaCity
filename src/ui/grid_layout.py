import pygame
from ui.card import Card, SelectableCard, ActionableCard
from typing import Dict, List, Literal

class GridLayout:
    def __init__(self, screen_manager, card_width, card_height, columns, card_factory, margin_x=10, margin_y=10, position=(0, 0), scroll_trigger=0):
        self.screen_manager = screen_manager
        self.card_width = card_width
        self.card_height = card_height
        self.columns = columns
        self.margin_x = margin_x
        self.margin_y = margin_y
        self.position = position
        self.scroll_trigger = scroll_trigger
        self.card_factory = card_factory
        self.cards: List[Card] = []
        self.card_type = None
        self.selected_card_index = 0
        self.cards_scroll = 0

    def update_cards(self, window, data: List[Dict]):
        try:
            length = len(self.cards)
            print(length)
            for i, item in enumerate(data):
                i += length

                self.cards.append(
                    self.card_factory(
                        window,
                        self.card_width,
                        self.card_height,
                        self.position[0] + self.card_width * (i % self.columns) + self.margin_x * (i % self.columns),
                        self.position[1] + self.card_height * (i // self.columns) + self.margin_y * (i // self.columns),
                        item
                    )
                )

            self.card_type = type(self.cards[0])

            if self.cards and issubclass(self.card_type, SelectableCard):
                self.cards[0].select()

            print(len(self.cards))
        except IndexError:
            pass

    def handle_events(self, event):
        if self.card_type:
            if issubclass(self.card_type, ActionableCard):
                for card in self.cards:
                    card.handle_event(event)

    def handle_keydown(self, key: int):
        if key == pygame.K_w:
            self.move_selection_vertical(-1)
        elif key == pygame.K_s:
            self.move_selection_vertical(1)
        elif key == pygame.K_a:
            self.move_selection_horizontal(-1)
        elif key == pygame.K_d:
            self.move_selection_horizontal(1)

    def move_selection_vertical(self, offset: int):
        new_index = self.selected_card_index + (offset * self.columns)
        
        if 0 <= new_index < len(self.cards):
            self.selected_card_index = new_index
            if offset > 0 and self.selected_card_index // self.columns > self.cards_scroll - 1 + self.scroll_trigger:
                self.scroll("down")
            elif offset < 0 and self.selected_card_index // self.columns < self.cards_scroll:
                self.scroll("up")
            
            if issubclass(self.card_type, SelectableCard):
                self.update_card_selection()

    def move_selection_horizontal(self, offset: int):
        new_index = self.selected_card_index + offset
        if 0 <= new_index < len(self.cards) and (self.selected_card_index // self.columns) == (new_index // self.columns):
            self.selected_card_index = new_index

            if issubclass(self.card_type, SelectableCard):
                self.update_card_selection()

    def update_card_selection(self):
        for i, card in enumerate(self.cards):
            if i == self.selected_card_index:
                card.select()
            else:
                card.deselect()

    def scroll(self, direction: Literal["up", "down"]):
        if direction == "down" and self.cards_scroll < (len(self.cards) - 1) // self.columns:
            self.cards_scroll += 1
        elif direction == "up" and self.cards_scroll > 0:
            self.cards_scroll -= 1

        dy = 110 if direction == "down" else -110
        for card in self.cards:
            card.position = (card.position[0], card.position[1] - dy)
            if issubclass(self.card_type, ActionableCard):
                card._action_button.position = (card._action_button.position[0], card._action_button.position[1] - dy)

    def draw(self, window):
        start_index = self.cards_scroll * self.columns
        end_index = start_index + self.columns * 4

        if self.cards == []:
            if not self.cards:
                text = "No hay elementos para mostrar"
                font = pygame.font.Font(None, 36)
                text_surface = font.render(text, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(window.get_width() // 2, window.get_height() // 2))
                window.blit(text_surface, text_rect)
        else:
            for card in self.cards[start_index:end_index]:
                card.draw()
