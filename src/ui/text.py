import pygame
from typing import Literal, Tuple

class TextRenderer:
    """Class to handle text rendering with outline."""
    
    def __init__(self, font_path: str):
        pygame.font.init()
        self.fonts = {
            "title": pygame.font.Font(font_path, 55),
            "subtitle": pygame.font.Font(font_path, 25),
            "default": pygame.font.Font(font_path, 12)
        }

    def render_text_with_outline(self, text: str, font_key: str, pos: Tuple[Literal["topleft", "center", "topright", "bottomleft", "bottomright"], Tuple[int, int]] = ("topleft", (0, 0)), outline_color=(0, 0, 0), text_color=(255, 255, 255)) -> Tuple[pygame.Surface, pygame.Rect]:
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
        
        text_rect = text_surface.get_rect()
        if pos[0] == "topleft":
            text_rect.topleft = pos[1]
        elif pos[0] == "center":
            text_rect.center = pos[1]
        elif pos[0] == "topright":
            text_rect.topright = pos[1]
        elif pos[0] == "bottomleft":
            text_rect.bottomleft = pos[1]
        elif pos[0] == "bottomright":
            text_rect.bottomright = pos[1]

        return text_surface, text_rect
