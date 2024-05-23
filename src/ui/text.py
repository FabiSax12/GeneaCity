import pygame
from typing import Tuple

class TextRenderer:
    """Class to handle text rendering with outline."""
    
    def __init__(self, font_path: str):
        self.fonts = {
            "title": pygame.font.Font(font_path, 55),
            "subtitle": pygame.font.Font(font_path, 25),
            "default": pygame.font.Font(font_path, 30)
        }

    def render_text_with_outline(self, text: str, font_key: str, center_x: int, center_y: int, outline_color=(0, 0, 0), text_color=(255, 255, 255)) -> Tuple[pygame.Surface, pygame.Rect]:
        font = self.fonts.get(font_key, self.fonts["default"])
        base = font.render(text, True, text_color)
        outline = font.render(text, True, outline_color)

        size = (outline.get_width() + 2, outline.get_height() + 2)
        text_surface = pygame.Surface(size, pygame.SRCALPHA)
        
        text_surface.blit(outline, (1, 0))
        text_surface.blit(outline, (0, 1))
        text_surface.blit(outline, (2, 1))
        text_surface.blit(outline, (1, 2))
        
        text_surface.blit(base, (1, 1))
        
        text_rect = text_surface.get_rect(center=(center_x, center_y))
        
        return text_surface, text_rect
