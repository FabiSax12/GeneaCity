import pygame
from typing import Tuple

class ImageHandler:
    """Class to handle image scaling and cropping."""

    @staticmethod
    def load_and_scale_image(path: str, width: int, height: int, x: int, y: int) -> Tuple[pygame.Surface, pygame.Rect]:
        image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.scale(image, (width, height))
        image_rect = image.get_rect(x=x, centery=y)
        return image, image_rect

    @staticmethod
    def load_and_prepare_background(path: str, target_width: int, target_height: int) -> Tuple[pygame.Surface, pygame.Rect]:
        image = pygame.image.load(path).convert_alpha()
        image = ImageHandler.scale_image(image, (target_width, target_height))
        image = ImageHandler.crop_center(image, target_width, target_height)
        image_rect = image.get_rect()
        return image, image_rect

    @staticmethod
    def scale_image(image: pygame.Surface, target_size: Tuple[int, int]) -> pygame.Surface:
        original_width, original_height = image.get_size()
        target_width, target_height = target_size

        width_scale = target_width / original_width
        height_scale = target_height / original_height

        scale_factor = max(width_scale, height_scale)

        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)

        return pygame.transform.scale(image, (new_width, new_height))
    
    @staticmethod
    def crop_center(image: pygame.Surface, target_width: int, target_height: int) -> pygame.Surface:
        image_rect = image.get_rect()
        center_x, center_y = image_rect.center

        left = max(0, center_x - target_width // 2)
        top = max(0, center_y - target_height // 2)
        right = min(image_rect.width, center_x + target_width // 2)
        bottom = min(image_rect.height, center_y + target_height // 2)

        return image.subsurface(pygame.Rect(left, top, right - left, bottom - top))
