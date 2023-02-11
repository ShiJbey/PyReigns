#!/usr/bin/env python3

from __future__ import annotations

import pathlib

import pygame

from pyreignslib.core.context import GameSettings
from pyreignslib.core.game import Game
from pyreignslib.main_menu import MainMenuMode
from pyreignslib.utilities import load_png

TITLE = "PyReigns"
ICON_TITLE = "PyReigns"
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 720
FPS = 60
ASSETS_DIR = pathlib.Path("./assets")
IMAGES_DIR = ASSETS_DIR / "images"
IMAGE_NAMES = {
    "card-bg": IMAGES_DIR / "card-background.png",
    "app-icon": IMAGES_DIR / "card-background.png",
}


def load_images(game: Game) -> None:
    for name, filepath in IMAGE_NAMES.items():
        game.context.images[name] = load_png(filepath)


def main():
    pygame.init()

    game = Game(
        GameSettings(
            window_size=(WINDOW_WIDTH, WINDOW_HEIGHT),
            fps=FPS,
            title=TITLE,
            icon_title=ICON_TITLE,
        ),
        initial_mode=MainMenuMode,
    )

    load_images(game)

    pygame.display.set_icon(game.context.images["app-icon"])

    game.start()


if __name__ == "__main__":
    main()
