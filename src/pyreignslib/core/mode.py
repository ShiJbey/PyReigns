from abc import ABC, abstractmethod

import pygame.event

from .context import GameContext

CHANGE_MODE_EVENT = pygame.event.custom_type()


class GameMode(ABC):
    __slots__ = "context"

    def __init__(self, context: GameContext) -> None:
        super().__init__()
        self.context: GameContext = context

    @abstractmethod
    def update(self, elapsed_time: float) -> None:
        raise NotImplementedError

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        raise NotImplementedError

    @abstractmethod
    def draw(self) -> None:
        raise NotImplementedError
