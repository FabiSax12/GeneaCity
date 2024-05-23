import sys
import pygame

class Button:
    """Class to represent a Button component."""
    
    def __init__(self, text, position, on_click, size=(200, 50), font_size=24, bg_color=(100, 100, 100), text_color=(255, 255, 255), hover_bg_color=(150, 150, 150), border_radius=10):
        """
        Initialize the button component.
        
        Args:
            text (str): The text to display on the button.
            position (tuple): The (x, y) position of the button on the screen.
            size (tuple): The (width, height) size of the button.
            on_click (function): The function to call when the button is clicked.
            font_size (int, optional): The font size of the button text. Defaults to 24.
            bg_color (tuple, optional): The background color of the button. Defaults to (100, 100, 100).
            text_color (tuple, optional): The color of the text. Defaults to (255, 255, 255).
            hover_bg_color (tuple, optional): The background color when the button is hovered. Defaults to (150, 150, 150).
            border_radius (int, optional): The radius of the button's border corners. Defaults to 10.
        """
        self.text = text
        self.position = position
        self.size = size
        self.on_click = on_click
        self.bg_color = bg_color
        self.text_color = text_color
        self.hover_bg_color = hover_bg_color
        self.border_radius = border_radius
        self.hovered = False
        
        self.font = pygame.font.Font(None, font_size)
        self.rect = pygame.Rect(position, size)
        self.text_surface = self.font.render(text, True, text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
    
    def handle_event(self, event):
        """
        Handle an event.
        
        Args:
            event (pygame.event.Event): The event to handle.
        """
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            self.on_click()

    def draw(self, screen):
        """
        Draw the button on the screen.
        
        Args:
            screen (pygame.Surface): The screen to draw the button on.
        """
        bg_color = self.hovered and self.hover_bg_color or self.bg_color
        pygame.draw.rect(screen, bg_color, self.rect, border_radius=self.border_radius)
        
        # Optional: Add a shadow effect
        shadow_color = (0, 0, 0, 100)
        shadow_offset = 5
        shadow_rect = self.rect.move(shadow_offset, shadow_offset)
        shadow_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        shadow_surface.fill(shadow_color)
        screen.blit(shadow_surface, shadow_rect.topleft)
        
        screen.blit(self.text_surface, self.text_rect)
    
    def update(self):
        """Update the button state if necessary."""
        pass