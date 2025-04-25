import arcade

import GameView


def main():
    """
    Main entry point for the Twisted Towers game.

    Creates a window and begins the arcade event loop.
    """
    window = GameView.GameView()
    window.setup()

    arcade.run()


if __name__ == "__main__":
    main()
