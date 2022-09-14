#!/usr/bin/env python3

from game import RockPaperScissor


def main() -> None:
    """Main method were we start the game"""
    # Start game
    game = RockPaperScissor()
    game.play()


if __name__ == "__main__":
    main()
