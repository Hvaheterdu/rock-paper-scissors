#!/usr/bin/env python3


import os
import sys
from random import Random

import pygame

WIDTH = 1000
HEIGHT = 800

BUTTON_COLOUR = (153, 204, 255)
WHITE = (255, 255, 255)
TEXT_COLOUR = (0, 0, 0)

FONT = "Calibri"
FONT_SIZE_TEXT = 24

PARENT_DIR = os.path.abspath(os.getcwd())

ROCK_IMG = pygame.image.load(
    os.path.join(PARENT_DIR, 'resources', 'images', 'rock.png')
)
PAPER_IMG = pygame.image.load(
    os.path.join(PARENT_DIR, 'resources', 'images', 'paper.png')
)
SCISSORS_IMG = pygame.image.load(
    os.path.join(PARENT_DIR, 'resources', 'images', 'scissors.png')
)
IMG = [ROCK_IMG, PAPER_IMG, SCISSORS_IMG]

ROCK = "Rock"
PAPER = "Paper"
SCISSORS = "Scissors"
COMPUTER_CHOICES = [ROCK, PAPER, SCISSORS]


class RockPaperScissors:
    """Rock, Paper and Scissors game class"""

    def __init__(self):
        """Constructor"""
        pygame.init()

    def play(self):
        """Start the game"""
        self.__draw()

    def __draw(self):
        """Create elements and draw the game"""
        computer_choice = 0
        computer_score = 0
        player_score = 0
        game_result = 0

        screen = self.__create_screen()
        screen.fill(WHITE)
        pygame.display.set_caption('Rock Paper Scissors')

        rock = self.__create_rect(50, 600, 80, 40)
        paper = self.__create_rect(150, 600, 80, 40)
        scissors = self.__create_rect(250, 600, 90, 40)

        # Rectangles to cover previous text to avoid overlay
        # cover_left is human score text, cover_middle is middle text and
        # cover_right is computer choice text
        cover_left = self.__create_rect(WIDTH - 920, HEIGHT - 140, 230, 58)
        cover_middle = self.__create_rect(WIDTH - 800, HEIGHT - 260, 555, 30)
        cover_right = self.__create_rect(WIDTH - 380, HEIGHT - 190, 320, 80)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    rand = Random().randint(0, 2)
                    if rock.collidepoint(mouse_pos):
                        computer_choice = COMPUTER_CHOICES[rand]
                        screen.blit(self.__scale_image(
                            ROCK_IMG, 300, 300), (45, 200))
                        screen.blit(self.__scale_image(
                            IMG[rand], 300, 300), (650, 200))
                        game_result = self.__compute(computer_choice, ROCK)
                    elif paper.collidepoint(mouse_pos):
                        computer_choice = COMPUTER_CHOICES[rand]
                        screen.blit(self.__scale_image(
                            PAPER_IMG, 300, 300), (45, 200))
                        screen.blit(self.__scale_image(
                            IMG[rand], 300, 300), (650, 200))
                        game_result = self.__compute(computer_choice, PAPER)
                    elif scissors.collidepoint(mouse_pos):
                        computer_choice = COMPUTER_CHOICES[rand]
                        screen.blit(
                            self.__scale_image(
                                SCISSORS_IMG, 300, 300), (45, 200)
                        )
                        screen.blit(self.__scale_image(
                            IMG[rand], 300, 300), (650, 200))
                        game_result = self.__compute(computer_choice, SCISSORS)
                    else:
                        continue

                    if game_result == 1:
                        player_score += 1
                    elif game_result == 2:
                        computer_score += 1

            self.__draw_title(screen, 'Rock Paper Scissors')
            self.__draw_rect(screen, BUTTON_COLOUR, rock)
            self.__add_rect_text(screen, 'Rock', rock)
            self.__draw_rect(screen, BUTTON_COLOUR, paper)
            self.__add_rect_text(screen, 'Paper', paper)
            self.__draw_rect(screen, BUTTON_COLOUR, scissors)
            self.__add_rect_text(screen, 'Scissors', scissors)

            x, y = self.__rect_pos(rock)
            self.__show_score(
                screen,
                f"Player score: {player_score}",
                WIDTH - 810,
                HEIGHT - 125,
            )
            self.__set_text(
                screen, f"Computer choose: {computer_choice}", x + 700, y)
            self.__show_score(
                screen,
                f"Computer score: {computer_score}",
                WIDTH - 210,
                HEIGHT - 125,
            )

            if player_score == 0 and computer_score == 0:
                self.__set_text(
                    screen,
                    'Let the game begin! Start by choosing an action',
                    WIDTH - 500,
                    HEIGHT - 250,
                )
            elif game_result == 1:
                self.__set_text(screen, 'Player wins',
                                WIDTH - 500, HEIGHT - 250)
            elif game_result == 2:
                self.__set_text(screen, 'Computer wins',
                                WIDTH - 500, HEIGHT - 250)
            else:
                self.__set_text(screen, "It's a draw",
                                WIDTH - 500, HEIGHT - 250)

            pygame.display.flip()

            self.__draw_rect(screen, WHITE, cover_left)
            self.__draw_rect(screen, WHITE, cover_middle)
            self.__draw_rect(screen, WHITE, cover_right)

        pygame.quit()
        sys.exit()

    def __compute(self, computer_choice: str, player_choice: str) -> int:
        """Compute who wins the round and update scores"""
        if (
            player_choice == ROCK
            and computer_choice == SCISSORS
            or player_choice == PAPER
            and computer_choice == ROCK
            or player_choice == SCISSORS
            and computer_choice == PAPER
        ):
            return 1
        if (
            computer_choice == ROCK
            and player_choice == SCISSORS
            or computer_choice == PAPER
            and player_choice == ROCK
            or computer_choice == SCISSORS
            and player_choice == PAPER
        ):
            return 2
        return 0

    def __set_font(
        self, inp: str, font: str, size: int, colour: tuple[int, int, int]
    ) -> tuple[pygame.Surface, pygame.Rect]:
        """Set font for text"""
        _font = pygame.font.SysFont(font, size)
        _text = _font.render(inp, True, colour)
        _text_rect = _text.get_rect()
        return _text, _text_rect

    def __rect_pos(self, rect_obj: pygame.Rect) -> tuple[int, int]:
        """Return x, y coordinate for center of rectangle"""
        return rect_obj.centerx, rect_obj.centery

    def __create_screen(self) -> pygame.Surface:
        """Create screen to draw on"""
        return pygame.display.set_mode((WIDTH, HEIGHT))

    def __create_rect(self, x: int, y: int, width: int, height: int) -> pygame.Rect:
        """Create rectangle with width and height on x and y coordinate"""
        return pygame.Rect(x, y, width, height)

    def __show_score(self, screen: pygame.Surface, inp: str, x: int, y: int):
        """Show score of each player in the game"""
        _text, _text_rect = self.__set_font(
            inp, FONT, FONT_SIZE_TEXT, TEXT_COLOUR)
        _text_rect.center = (x, y)
        screen.blit(_text, _text_rect)

    def __add_rect_text(self, screen: pygame.Surface, inp: str, rect_obj: pygame.Rect):
        """Add text to rectangle object"""
        _text, _text_rect = self.__set_font(
            inp, FONT, FONT_SIZE_TEXT, TEXT_COLOUR)
        x, y = self.__rect_pos(rect_obj)
        _text_rect.center = (x, y)
        screen.blit(_text, _text_rect)

    def __set_text(self, screen: pygame.Surface, inp: str, x: int, y: int):
        """Set text to screen"""
        _text, _text_rect = self.__set_font(
            inp, FONT, FONT_SIZE_TEXT, TEXT_COLOUR)
        _text_rect.center = (x, y)
        screen.blit(_text, _text_rect)

    def __scale_image(self, image: pygame.Surface, x: int, y: int) -> pygame.Surface:
        """Return scaled image of size x, y, which need to be in a tuple"""
        return pygame.transform.smoothscale(image, (x, y))

    def __draw_rect(
        self,
        screen: pygame.Surface,
        colour: tuple[int, int, int],
        rect_obj: pygame.Rect,
    ) -> pygame.Rect:
        """Draw rectangle on screen with given colour"""
        return pygame.draw.rect(screen, colour, rect_obj)

    def __draw_title(self, screen: pygame.Surface, inp: str):
        """Draw title on screen with input inp"""
        _text, _text_rect = self.__set_font(inp, FONT, 40, TEXT_COLOUR)
        _text_rect.center = ((WIDTH // 2), (HEIGHT // 10))
        screen.blit(_text, _text_rect)
