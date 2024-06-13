#!/usr/bin/env python3
"""RockPaperScissors class which contains the game logic and GUI."""

import os
import sys
from random import choice

import pygame

WIDTH = 1000
HEIGHT = 800

BUTTON_COLOUR = (153, 204, 255)
WHITE = (255, 255, 255)
TEXT_COLOUR = (0, 0, 0)

FONT = "Calibri"
FONT_SIZE_TEXT = 24

RESOURCE_DIR = os.path.join(os.path.abspath(os.getcwd()), 'resources', 'images')

ROCK_IMG = pygame.image.load(os.path.join(RESOURCE_DIR, 'rock.png'))
PAPER_IMG = pygame.image.load(os.path.join(RESOURCE_DIR, 'paper.png'))
SCISSORS_IMG = pygame.image.load(os.path.join(RESOURCE_DIR, 'scissors.png'))
IMG = [ROCK_IMG, PAPER_IMG, SCISSORS_IMG]

ROCK = "Rock"
PAPER = "Paper"
SCISSORS = "Scissors"
CHOICES = [ROCK, PAPER, SCISSORS]


class RockPaperScissors:
    """Rock, Paper and Scissors game and GUI class."""

    def __init__(self):
        """Constructor."""
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Rock Paper Scissors')
        self.clock = pygame.time.Clock()

        self.player_score = 0
        self.computer_score = 0
        self.game_started = False
        self.computer_choice = ""
        self.player_choice = ""
        self.game_result = 0

        self.rock_rect = self._create_rect(50, 600, 80, 40)
        self.paper_rect = self._create_rect(150, 600, 80, 40)
        self.scissors_rect = self._create_rect(250, 600, 90, 40)

    def play(self):
        """Start the game."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.game_started = True
                    self._handle_mouse_click(event.pos)

            self._draw()

        pygame.quit()
        sys.exit()

    def _handle_mouse_click(self, pos):
        """Handle mouse click events."""
        if self.rock_rect.collidepoint(pos):
            self.player_choice = ROCK
        elif self.paper_rect.collidepoint(pos):
            self.player_choice = PAPER
        elif self.scissors_rect.collidepoint(pos):
            self.player_choice = SCISSORS
        else:
            return

        self.computer_choice = choice(CHOICES)
        self.game_result = self._compute(self.computer_choice, self.player_choice)

        if self.game_result == 1:
            self.player_score += 1
        elif self.game_result == 2:
            self.computer_score += 1

    def _draw(self):
        """Create elements and draw the game."""
        self.screen.fill(WHITE)

        self._draw_title('Rock Paper Scissors')
        self._draw_button(self.rock_rect, 'Rock')
        self._draw_button(self.paper_rect, 'Paper')
        self._draw_button(self.scissors_rect, 'Scissors')

        if self.game_started:
            self._display_choices()
            self._display_result()

        self._display_scores()

        pygame.display.flip()
        self.clock.tick(60)

    def _display_choices(self):
        """Display the choices made by player and computer."""
        player_img = IMG[CHOICES.index(self.player_choice)]
        computer_img = IMG[CHOICES.index(self.computer_choice)]
        self.screen.blit(self._scale_image(player_img, 300, 300), (45, 200))
        self.screen.blit(self._scale_image(computer_img, 300, 300), (650, 200))

    def _display_result(self):
        """Display the result of the game."""
        if self.game_result == 1:
            result_text = 'Player wins'
        elif self.game_result == 2:
            result_text = 'Computer wins'
        else:
            result_text = "It's a draw"

        self._set_text(result_text, WIDTH // 2, HEIGHT // 2 - 50)

    def _display_scores(self):
        """Display the scores of player and computer."""
        self._set_text(f"Player score: {self.player_score}", WIDTH // 4, HEIGHT - 125)
        self._set_text(
            f"Computer score: {self.computer_score}", 3 * WIDTH // 4, HEIGHT - 125
        )
        self._set_text(
            f"Computer chose: {self.computer_choice}", WIDTH // 2, HEIGHT // 2 + 50
        )

    def _compute(self, computer_choice: str, player_choice: str) -> int:
        """Compute who wins the round and update scores."""
        if (
            player_choice == ROCK
            and computer_choice == SCISSORS
            or player_choice == PAPER
            and computer_choice == ROCK
            or player_choice == SCISSORS
            and computer_choice == PAPER
        ):
            return 1
        elif (
            computer_choice == ROCK
            and player_choice == SCISSORS
            or computer_choice == PAPER
            and player_choice == ROCK
            or computer_choice == SCISSORS
            and player_choice == PAPER
        ):
            return 2
        return 0

    def _create_rect(self, x: int, y: int, width: int, height: int) -> pygame.Rect:
        """Create rectangle with width and height on x and y coordinate."""
        return pygame.Rect(x, y, width, height)

    def _set_font(
        self, text: str, font: str, size: int, colour: tuple[int, int, int]
    ) -> tuple[pygame.Surface, pygame.Rect]:
        """Set font for text."""
        _font = pygame.font.SysFont(font, size)
        _text = _font.render(text, True, colour)
        return _text, _text.get_rect()

    def _set_text(self, text: str, x: int, y: int):
        """Set text to screen."""
        _text, _text_rect = self._set_font(text, FONT, FONT_SIZE_TEXT, TEXT_COLOUR)
        _text_rect.center = (x, y)
        self.screen.blit(_text, _text_rect)

    def _scale_image(
        self, image: pygame.Surface, width: int, height: int
    ) -> pygame.Surface:
        """Return scaled image of size width, height."""
        return pygame.transform.smoothscale(image, (width, height))

    def _draw_button(self, rect: pygame.Rect, text: str):
        """Draw button with text."""
        pygame.draw.rect(self.screen, BUTTON_COLOUR, rect)
        self._set_text(text, *rect.center)

    def _draw_title(self, text: str):
        """Draw title on screen."""
        _text, _text_rect = self._set_font(text, FONT, 40, TEXT_COLOUR)
        _text_rect.center = (WIDTH // 2, HEIGHT // 10)
        self.screen.blit(_text, _text_rect)


if __name__ == '__main__':
    pass
