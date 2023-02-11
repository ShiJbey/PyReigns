from typing import Any, List, Sequence, Tuple, Union

import pygame
import pygame.color
import pygame.math
import pygame.rect
import pygame.sprite
import pygame.surface
import pygame.transform


def get_sign(value: int):
    if value > 0:
        return 1
    elif value < 0:
        return -1
    else:
        return 0


class Card(pygame.sprite.Sprite):
    """
    Cards are what get dragged left or right by
    the user when making decisions
    """

    reset_speed: float = 10.0
    MAX_TILT: float = 15

    def __init__(
        self,
        image: pygame.surface.Surface,
        window_size: Tuple[int, int],
        prompt_text: str,
        accept_text: str = "yes",
        reject_text: str = "no",
    ) -> None:
        super().__init__()
        self.background_color: pygame.color.Color = pygame.color.Color(173, 173, 173)
        self.image: pygame.surface.Surface = pygame.transform.scale(image, (380, 380))
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.reset_pos: Tuple[int, int] = window_size[0] // 2, window_size[1] // 2 + 50
        self.rect.center = self.reset_pos
        self.dragged: bool = False
        self.rotation: int = 0
        self.prompt_text: str = prompt_text
        self.accept_text: str = accept_text
        self.reject_text: str = reject_text

    def update(self, *args: Any, **kwargs: Any) -> None:
        elapsed_time: float = kwargs["elapsed_time"]

        toward_center = pygame.math.Vector2(self.reset_pos) - pygame.math.Vector2(
            self.rect.center
        )

        distance_from_center = toward_center.magnitude()

        x_pos_sign = get_sign(self.rect.centerx - self.reset_pos[0])

        # Have to multiply by negative one to get the right rotation direction
        rotation_multiplier = min(distance_from_center / 50.0, 1) * x_pos_sign * -1
        self.rotation = round(self.MAX_TILT * rotation_multiplier)

        if self.dragged is False:
            if distance_from_center <= 3:
                self.rect.center = self.reset_pos
                self.rotation = 0
            else:
                toward_center.normalize()

                new_position = (
                    pygame.math.Vector2(self.rect.center)
                    + toward_center * self.reset_speed * elapsed_time
                )

                self.rect.center = round(new_position[0]), round(new_position[1])

    def on_accept(self) -> None:
        """Perform an operation when the user accepts this choice"""
        print("YES SWIPE!")

    def on_reject(self) -> None:
        """Perform an operation when the user rejects this choice"""
        print("NO SWIPE!")


class CardSpriteGroup(pygame.sprite.Group):
    __slots__ = "cards"

    def __init__(self, *sprites: Union[Card, Sequence[Card]]) -> None:
        super().__init__(*sprites)
        self.cards: List[Card] = []

        if isinstance(sprites, Card):
            self.cards.append(sprites)
        else:
            self.cards = list(*sprites)

    def draw(self, surface: pygame.surface.Surface) -> List[pygame.rect.Rect]:
        drawn_rects: List[pygame.rect.Rect] = []
        for card in self.cards:
            if card.rotation == 0:
                drawn_rects.append(surface.blit(card.image, card.rect))
            else:
                rot_image = pygame.transform.rotate(card.image, card.rotation)
                rot_rect = rot_image.get_rect(center=card.rect.center)
                drawn_rects.append(surface.blit(rot_image, rot_rect))

        return drawn_rects
