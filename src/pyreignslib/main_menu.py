import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UILabel, UIProgressBar

from pyreignslib.core import CHANGE_MODE_EVENT, GameContext, GameMode
from pyreignslib.prototype_mode import PrototypeMode


class MainMenuMode(GameMode):
    """Presents the user with the main menu"""

    def __init__(self, ctx: GameContext) -> None:
        super().__init__(ctx)
        self.options = ["Play", "Quit"]
        ctx.background.fill((224, 197, 123))

        UIButton(
            pygame.Rect(
                60, ctx.window.get_rect().centery, ctx.window.get_width() - 120, 64
            ),
            "Play",
            ctx.ui_manager,
            object_id="#play_btn",
        )

        UIButton(
            pygame.Rect(
                60, ctx.window.get_rect().centery + 76, ctx.window.get_width() - 120, 64
            ),
            "Exit",
            ctx.ui_manager,
            object_id="#exit_game_btn",
        )

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle PyGame events while active"""

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_object_id == "#play_btn":
                    pygame.event.post(
                        pygame.event.Event(CHANGE_MODE_EVENT, mode=GeneratingTownMode)
                    )

                if event.ui_object_id == "#exit_game_btn":
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

    def update(self, elapsed_time: float) -> None:
        """Update the state of the mode"""
        pass

    def draw(self) -> None:
        """Draw to the screen while active"""
        pass


class GeneratingTownMode(GameMode):
    def __init__(self, ctx: GameContext) -> None:
        super().__init__(ctx)
        self._generation_time: float = 0

        ctx.background.fill((74, 99, 99))

        self.label = UILabel(
            pygame.Rect(
                0, ctx.window.get_rect().centery - 32, ctx.window.get_width(), 32
            ),
            "Generating Town...",
            ctx.ui_manager,
            object_id="#label",
        )

        self.progress_bar = UIProgressBar(
            pygame.Rect(
                20, ctx.window.get_rect().centery, ctx.window.get_width() - 40, 32
            ),
            ctx.ui_manager,
            object_id="#progress-bar",
        )

        self.progress_bar.set_current_progress(0)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle PyGame events while active"""
        pass

    def update(self, elapsed_time: float) -> None:
        """Update the state of the mode"""
        self._generation_time += elapsed_time
        self.progress_bar.set_current_progress(100 * (self._generation_time / 10))

        if self._generation_time >= 10:
            pygame.event.post(pygame.event.Event(CHANGE_MODE_EVENT, mode=PrototypeMode))

    def draw(self) -> None:
        """Draw to the screen while active"""
        pass
