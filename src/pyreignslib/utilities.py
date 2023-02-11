"""
Utility functions and classes for loading
resources such as images and fonts
"""
import pathlib
from typing import Optional, Union

import pygame
import pygame.color
import pygame.constants
import pygame.font
import pygame.image
import pygame.surface
import pygame.transform


def load_png(
    filepath: Union[str, pathlib.Path], scale: int = 1
) -> pygame.surface.Surface:
    """load an from the resources/images directory

    Parameters
    ----------
    filename : str
        The name of the .png file to load
    """

    try:
        image = pygame.image.load(filepath)

        size = image.get_size()
        size = (size[0] * scale, size[1] * scale)
        image = pygame.transform.scale(image, size)

        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()

    except FileNotFoundError:
        print(f"Cannot load image: {filepath}")
        raise SystemExit

    return image


def draw_text(
    surface: pygame.surface.Surface,
    text: str,
    color: pygame.color.Color,
    rect: pygame.rect.Rect,
    font: pygame.font.Font,
    antialias: bool = False,
    background: Optional[pygame.color.Color] = None,
) -> str:
    """Draws some text to an area of a Surface

    This function automatically wraps words and returns any text
    that did not get blitted to the surface
    """
    rect = pygame.rect.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if background:
            image = font.render(text[:i], True, color, background)
            image.set_colorkey(background)
        else:
            image = font.render(text[:i], antialias, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text
