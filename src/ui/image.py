import pygame
from typing import Tuple

class ImageHandler:
    """Class to handle image loading, scaling, and cropping."""

    @staticmethod
    def load_image(path: str) -> pygame.Surface:
        """Load an image from a file path."""
        return pygame.image.load(path).convert_alpha()

    @staticmethod
    def scale_image(image: pygame.Surface, width: int, height: int) -> pygame.Surface:
        """Scale an image to the specified width and height."""
        return pygame.transform.scale(image, (width, height))

    @staticmethod
    def get_image_rect(image: pygame.Surface, x: int, y: int) -> pygame.Rect:
        """Get the rectangle of an image centered at (x, y)."""
        return image.get_rect(x=x, centery=y)

    @staticmethod
    def crop_center(image: pygame.Surface, target_width: int, target_height: int) -> pygame.Surface:
        """Crop the center of the image to the specified target width and height."""
        image_rect = image.get_rect()
        center_x, center_y = image_rect.center

        left = max(0, center_x - target_width // 2)
        top = max(0, center_y - target_height // 2)
        right = min(image_rect.width, center_x + target_width // 2)
        bottom = min(image_rect.height, center_y + target_height // 2)

        return image.subsurface(pygame.Rect(left, top, right - left, bottom - top))

    @staticmethod
    def load_and_scale_image(path: str, width: int, height: int, x: int, y: int) -> Tuple[pygame.Surface, pygame.Rect]:
        """Load an image from a file, scale it, and get its rectangle centered at (x, y)."""
        image = ImageHandler.load_image(path)
        image = ImageHandler.scale_image(image, width, height)
        image_rect = ImageHandler.get_image_rect(image, x, y)
        return image, image_rect

    @staticmethod
    def load_and_prepare_background(path: str, target_width: int, target_height: int) -> Tuple[pygame.Surface, pygame.Rect]:
        """Load an image from a file, scale and crop it to the target size, and get its rectangle."""
        image = ImageHandler.load_image(path)
        image = ImageHandler.scale_image(image, target_width, target_height)
        image = ImageHandler.crop_center(image, target_width, target_height)
        image_rect = image.get_rect()
        return image, image_rect
