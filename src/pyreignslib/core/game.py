from typing import Type

import pygame
import pygame.surface
import pygame.time
import pygame_gui

from .context import GameContext, GameSettings
from .mode import CHANGE_MODE_EVENT, GameMode


class Game:
    __slots__ = "context", "clock", "mode"

    def __init__(self, settings: GameSettings, initial_mode: Type[GameMode]) -> None:
        self.context: GameContext = GameContext(
            is_running=False,
            window=self.initialize_window(settings),
            background=self.initialize_background(),
            default_font=self.initialize_default_font(),
            settings=settings,
            ui_manager=pygame_gui.UIManager(settings.window_size),
        )
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.mode: GameMode = initial_mode(self.context)
        self.context.ui_manager.set_visual_debug_mode(settings.show_debug)

    @staticmethod
    def initialize_window(settings: GameSettings) -> pygame.surface.Surface:
        window = pygame.display.set_mode(settings.window_size, pygame.constants.SCALED)
        pygame.display.set_caption(settings.title, settings.icon_title)
        return window

    @staticmethod
    def initialize_background() -> pygame.surface.Surface:
        background = pygame.Surface(pygame.display.get_surface().get_size())
        background = background.convert()
        background.fill((250, 250, 250))
        return background

    @staticmethod
    def initialize_default_font() -> pygame.font.Font:
        return pygame.font.Font(None, 36)

    def start(self) -> None:
        self.context.is_running = True

        try:
            while self.context.is_running:
                elapsed_time = self.clock.tick(self.context.settings.fps) / 1000.0
                self.draw()
                self.update(elapsed_time)
                self.handle_events()
        except SystemExit:
            pass
        except KeyboardInterrupt:
            pass

        self.quit()

    def update(self, elapsed_time: float) -> None:
        self.context.ui_manager.update(elapsed_time)
        self.mode.update(elapsed_time)

    def handle_events(self) -> None:
        for event in pygame.event.get():
            self.mode.handle_event(event)
            self.context.ui_manager.process_events(event)

            if event.type == pygame.constants.QUIT:
                self.context.is_running = False

            if event.type == CHANGE_MODE_EVENT:
                self.set_mode(event.mode)
        pygame.event.pump()

    def draw(self) -> None:
        self.context.window.blit(self.context.background, (0, 0))
        self.mode.draw()
        self.context.ui_manager.draw_ui(self.context.window)
        pygame.display.flip()

    def quit(self) -> None:
        pygame.quit()

    def set_mode(self, mode: Type[GameMode]) -> None:
        self.context.ui_manager.clear_and_reset()
        self.mode = mode(self.context)
