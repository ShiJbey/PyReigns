from typing import Tuple

import pygame
import pygame.constants
import pygame.event
import pygame.sprite

from .card import Card, CardSpriteGroup
from .core.context import GameContext
from .core.mode import GameMode
from .utilities import draw_text

LEFT_MOUSE_BTN = 1
SHOW_DEBUG = False


class PrototypeMode(GameMode):
    __slots__ = (
        "all_cards",
        "card",
        "last_drag_pos",
        "right_threshold",
        "left_threshold",
        "is_hovering_left",
        "is_hovering_right",
    )

    THRESHOLD_WIDTH: int = 125

    def __init__(self, context: GameContext) -> None:
        super().__init__(context)
        self.card: Card = Card(
            self.context.images["card-bg"],
            self.context.window.get_size(),
            prompt_text="Will you help me eliminate the enemy? Or will you die at my feet?",
        )
        self.all_cards: CardSpriteGroup = CardSpriteGroup([self.card])
        self.last_drag_pos: Tuple[int, int] = (0, 0)
        self.right_threshold: int = (
            self.context.window.get_width() - self.THRESHOLD_WIDTH
        )
        self.left_threshold: int = self.THRESHOLD_WIDTH
        self.is_hovering_left: bool = False
        self.is_hovering_right: bool = False

    def update(self, elapsed_time: float) -> None:
        self.all_cards.update(elapsed_time=elapsed_time)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.constants.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if event.button == LEFT_MOUSE_BTN:
                if self.card.rect.collidepoint(mouse_pos):
                    self.card.dragged = True
                    self.last_drag_pos = mouse_pos

        if event.type == pygame.constants.MOUSEMOTION:
            if self.card.dragged:
                mouse_pos = pygame.mouse.get_pos()
                dx = mouse_pos[0] - self.last_drag_pos[0]
                dy = mouse_pos[1] - self.last_drag_pos[1]
                self.last_drag_pos = mouse_pos
                self.card.rect.x += dx
                self.card.rect.y += dy

                # Show or hide option prompts
                self.is_hovering_right = self.card.rect.centerx > self.right_threshold
                self.is_hovering_left = self.card.rect.centerx < self.left_threshold

        if event.type == pygame.constants.MOUSEBUTTONUP:
            self.card.dragged = False
            self.is_hovering_left = False
            self.is_hovering_right = False
            if self.card.rect.centerx > self.right_threshold:
                self.card.on_accept()
            elif self.card.rect.centerx < self.left_threshold:
                self.card.on_reject()

    def draw(self) -> None:
        self.context.background.fill((224, 197, 123))

        # Draw top and bottom bars
        pygame.draw.rect(
            self.context.window,
            (54, 26, 19),
            pygame.rect.Rect(0, 0, self.context.window.get_width(), 120),
        )

        pygame.draw.rect(
            self.context.window,
            (54, 26, 19),
            pygame.rect.Rect(
                0,
                self.context.window.get_height() - 100,
                self.context.window.get_width(),
                100,
            ),
        )

        draw_text(
            self.context.window,
            "Character Name (Age: #)",
            color=pygame.Color(255, 255, 255),
            rect=pygame.rect.Rect(
                10,
                self.context.window.get_height() - 90,
                self.context.window.get_width() - 10,
                32,
            ),
            font=self.context.default_font,
        )

        draw_text(
            self.context.window,
            "February 10, 2023",
            color=pygame.Color(255, 255, 255),
            rect=pygame.rect.Rect(
                10,
                self.context.window.get_height() - 58,
                self.context.window.get_width() - 10,
                32,
            ),
            font=self.context.default_font,
        )

        if SHOW_DEBUG:
            # Draw swipe thresholds
            pygame.draw.rect(
                self.context.window,
                (0, 255, 0, 20),
                pygame.rect.Rect(
                    0, 0, self.THRESHOLD_WIDTH, self.context.window.get_height()
                ),
            )

            pygame.draw.rect(
                self.context.window,
                (0, 255, 0, 20),
                pygame.rect.Rect(
                    self.context.window.get_width() - self.THRESHOLD_WIDTH,
                    0,
                    self.THRESHOLD_WIDTH,
                    self.context.window.get_height(),
                ),
            )

        textRect = pygame.rect.Rect(0, 0, self.context.window.get_width() - 40, 64)
        textRect.center = (self.context.window.get_width() // 2, textRect.centery)
        textRect.y = 130

        draw_text(
            self.context.window,
            self.card.prompt_text,
            pygame.Color(0, 0, 0),
            textRect,
            self.context.default_font,
        )

        # Draw card sprites
        self.all_cards.draw(self.context.window)

        if self.is_hovering_right:
            pygame.draw.rect(
                self.context.window,
                (0, 0, 0, 20),
                pygame.rect.Rect(
                    self.context.window.get_width()
                    - self.context.window.get_width() // 4,
                    200,
                    self.context.window.get_width() // 4,
                    32,
                ),
            )

            draw_text(
                self.context.window,
                self.card.accept_text,
                pygame.Color(255, 255, 255),
                pygame.rect.Rect(
                    self.context.window.get_width()
                    - self.context.window.get_width() // 4,
                    200,
                    self.context.window.get_width() // 4,
                    32,
                ),
                self.context.default_font,
            )

        if self.is_hovering_left:
            pygame.draw.rect(
                self.context.window,
                (0, 0, 0, 20),
                pygame.rect.Rect(0, 200, self.context.window.get_width() // 4, 32),
            )

            draw_text(
                self.context.window,
                self.card.reject_text,
                pygame.Color(255, 255, 255),
                pygame.rect.Rect(0, 200, self.context.window.get_width() // 4, 32),
                self.context.default_font,
            )

    def _get_next_card(self) -> None:
        """Get the next decision card for the player"""
        raise NotImplementedError()
