import pygame
from abc import ABC
from typing import Literal, Tuple

class TextRenderStrategy(ABC):
    """Base class for text render strategies."""
    def render(self, text: str, font: pygame.font.Font, text_color: Tuple[int, int, int], pos: Tuple[Literal["topleft", "center", "topright", "bottomleft", "bottomright"], Tuple[int, int]]) -> Tuple[pygame.Surface, pygame.Rect]:
        raise NotImplementedError

class SimpleTextRenderStrategy(TextRenderStrategy):
    """Class for simple text rendering."""
    def render(self, text: str, font: pygame.font.Font, text_color: Tuple[int, int, int], pos: Tuple[Literal["topleft", "center", "topright", "bottomleft", "bottomright"], Tuple[int, int]]) -> Tuple[pygame.Surface, pygame.Rect]:
        text_surface = font.render(text, True, text_color)
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

class OutlinedTextRenderStrategy(TextRenderStrategy):
    """Class for text rendering with outline."""
    def render(self, text: str, font: pygame.font.Font, outline_color: Tuple[int, int, int], text_color: Tuple[int, int, int], pos: Tuple[Literal["topleft", "center", "topright", "bottomleft", "bottomright"], Tuple[int, int]]) -> Tuple[pygame.Surface, pygame.Rect]:
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

class TextRenderer:
    """Class to handle text rendering with various strategies."""

    def __init__(self, font: str):
        pygame.font.init()
        self.fonts = {
            "title": pygame.font.Font(f"src/assets/fonts/{font}", 55),
            "subtitle": pygame.font.Font(f"src/assets/fonts/{font}", 25),
            "default": pygame.font.Font(f"src/assets/fonts/{font}", 12)
        }
        self.simple_strategy = SimpleTextRenderStrategy()
        self.outline_strategy = OutlinedTextRenderStrategy()

    def render_text(self, text: str, font_key: str, pos: Tuple[int, int], text_color=(255, 255, 255)) -> Tuple[pygame.Surface, pygame.Rect]:
        font = self.fonts.get(font_key, self.fonts["default"])
        return self.simple_strategy.render(text, font, text_color, ("topleft", pos))

    def render_text_with_outline(self, text: str, font_key: str, pos: Tuple[Literal["topleft", "center", "topright", "bottomleft", "bottomright"], Tuple[int, int]], outline_color=(0, 0, 0), text_color=(255, 255, 255)) -> Tuple[pygame.Surface, pygame.Rect]:
        font = self.fonts.get(font_key, self.fonts["default"])
        return self.outline_strategy.render(text, font, outline_color, text_color, pos)
