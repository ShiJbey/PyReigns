import dataclasses
from typing import Dict, Tuple

import pygame.font
import pygame.surface
import pygame_gui


@dataclasses.dataclass
class GameSettings:
    window_size: Tuple[int, int]
    fps: int
    title: str
    icon_title: str
    show_debug: bool = False


@dataclasses.dataclass
class GameContext:
    is_running: bool
    window: pygame.surface.Surface
    background: pygame.surface.Surface
    settings: GameSettings
    default_font: pygame.font.Font
    ui_manager: pygame_gui.UIManager
    images: Dict[str, pygame.surface.Surface] = dataclasses.field(default_factory=dict)
