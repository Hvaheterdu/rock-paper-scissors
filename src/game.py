#!/usr/bin/env python3


import os
import sys
from random import Random

import pygame

# Colour and screen size
WIDTH = 1000
HEIGHT = 800
BUTTON_COLOUR = (153, 204, 255)
WHITE = (255, 255, 255)
TEXT_COLOUR = (0, 0, 0)

# Current directory for this file
PARENT_DIR = os.path.abspath(os.getcwd())

# Images used
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

# Player actions
ROCK = "Rock"
PAPER = "Paper"
SCISSORS = "Scissors"
CHOICES = [ROCK, PAPER, SCISSORS]


class RockPaperScissors:
    """Rock, Paper and Scissors game class"""

    def __init__(self) -> None:
        """Constructor"""
        pygame.init()

    def play(self) -> None:
        """Start the game"""
        self.__draw()

    def __draw(self) -> None:
        """Create elements and draw the game"""
        computer_choice = 0
        computer_score = 0
        player_score = 0
        ret = 0

        # Create screen, fill background and add window title
        self.__screen = self.__create_screen()
        self.__screen.fill(WHITE)
        pygame.display.set_caption('Rock Paper Scissors')

        # Create rectangles that will become buttons
        rock = self.__create_rect(50, 600, 80, 40)
        paper = self.__create_rect(150, 600, 80, 40)
        scissors = self.__create_rect(250, 600, 90, 40)

        # Rectangles to cover previous text to avoid overlay
        # cover_left is human score text, cover_middle is middle text and
        # cover_right is computer choice text
        cover_left = self.__create_rect(WIDTH - 920, HEIGHT - 140, 230, 58)
        cover_middle = self.__create_rect(WIDTH - 800, HEIGHT - 260, 555, 30)
        cover_right = self.__create_rect(WIDTH - 380, HEIGHT - 190, 320, 80)

        # Draw on screen
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    rand = Random().randint(0, 2)

                    if rock.collidepoint(mouse_pos):
                        computer_choice = CHOICES[rand]
                        self.__screen.blit(
                            self.__scale_image(ROCK_IMG, 300, 300), (45, 200)
                        )
                        self.__screen.blit(
                            self.__scale_image(IMG[rand], 300, 300), (650, 200)
                        )
                        ret = self.__compute(computer_choice, ROCK)
                    elif paper.collidepoint(mouse_pos):
                        computer_choice = CHOICES[rand]
                        self.__screen.blit(
                            self.__scale_image(PAPER_IMG, 300, 300), (45, 200)
                        )
                        self.__screen.blit(
                            self.__scale_image(IMG[rand], 300, 300), (650, 200)
                        )
                        ret = self.__compute(computer_choice, PAPER)
                    elif scissors.collidepoint(mouse_pos):
                        computer_choice = CHOICES[rand]
                        self.__screen.blit(
                            self.__scale_image(SCISSORS_IMG, 300, 300), (45, 200)
                        )
                        self.__screen.blit(
                            self.__scale_image(IMG[rand], 300, 300), (650, 200)
                        )
                        ret = self.__compute(computer_choice, SCISSORS)
                    else:
                        continue

                    if ret == 1:
                        player_score += 1
                    elif ret == 2:
                        computer_score += 1

            self.__draw_title(self.__screen, 'Rock Paper Scissors')
            self.__draw_rect(self.__screen, BUTTON_COLOUR, rock)
            self.__add_rect_text(self.__screen, 'Rock', rock)
            self.__draw_rect(self.__screen, BUTTON_COLOUR, paper)
            self.__add_rect_text(self.__screen, 'Paper', paper)
            self.__draw_rect(self.__screen, BUTTON_COLOUR, scissors)
            self.__add_rect_text(self.__screen, 'Scissors', scissors)

            x, y = self.__rect_pos(rock)
            self.__show_score(
                self.__screen,
                f"Player score: {player_score}",
                WIDTH - 810,
                HEIGHT - 125,
            )
            self.__set_text(
                self.__screen, f"Computer choose: {computer_choice}", x + 700, y
            )
            self.__show_score(
                self.__screen,
                f"Computer score: {computer_score}",
                WIDTH - 210,
                HEIGHT - 125,
            )

            if player_score == 0 and computer_score == 0:
                self.__set_text(
                    self.__screen,
                    "Let the game begin! Start by choosing an action",
                    WIDTH - 500,
                    HEIGHT - 250,
                )
            elif ret == 1:
                self.__set_text(self.__screen, "Player wins", WIDTH - 500, HEIGHT - 250)
            elif ret == 2:
                self.__set_text(
                    self.__screen, "Computer wins", WIDTH - 500, HEIGHT - 250
                )
            else:
                self.__set_text(self.__screen, "It's a draw", WIDTH - 500, HEIGHT - 250)

            pygame.display.flip()

            self.__draw_rect(self.__screen, WHITE, cover_left)
            self.__draw_rect(self.__screen, WHITE, cover_middle)
            self.__draw_rect(self.__screen, WHITE, cover_right)

        pygame.quit()
        sys.exit()

    def __compute(self, computer_choice, player_choice) -> int:
        """Compute who wins the round and update scores

        :param str computer_choice: computer's action
        :param str player_choice: player's action
        :returns: 1 -> player wins, 2 -> computer wins
        """
        # Compute winner
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

    def __set_font(self, inp, font, size, colour) -> tuple:
        """Set font for text

        :param str inp: text to input
        :param str font: font type
        :param int size: text size
        :param rgb colour: text colour
        :returns: pygame font object
        """
        self.__font = pygame.font.SysFont(font, size)
        self.__text = self.__font.render(inp, True, colour)
        self.__text_rect = self.__text.get_rect()
        return self.__text, self.__text_rect

    def __rect_pos(self, rect_obj) -> tuple:
        """Return x, y coordinate for center of rectangle"""
        return rect_obj.centerx, rect_obj.centery

    def __create_screen(self) -> pygame.surface.Surface:
        """Create screen to draw on"""
        return pygame.display.set_mode((WIDTH, HEIGHT))

    def __create_rect(self, x, y, width, height) -> pygame.rect.Rect:
        """Create rectangle with width and height on x and y coordinate"""
        return pygame.Rect(x, y, width, height)

    def __show_score(self, screen, inp, x, y):
        """Show score of each player in the game

        :param pygame.Surface screen: screen to draw on
        :param str inp: text input
        :param int x: x coordinate
        :param int y: y coordinate
        """
        self.__text, self.__text_rect = self.__set_font(inp, 'Calibri', 24, TEXT_COLOUR)
        self.__text_rect.center = (x, y)
        screen.blit(self.__text, self.__text_rect)

    def __add_rect_text(self, screen, inp, rect_obj):
        """Add text to rectangle object

        :param pygame.Surface screen: screen to draw on
        :param str inp: text input
        :param pygame.rect.Rect rect_obj: rectangle object
        """
        self.__text, self.__text_rect = self.__set_font(inp, 'Calibri', 24, TEXT_COLOUR)
        x, y = self.__rect_pos(rect_obj)
        self.__text_rect.center = (x, y)
        screen.blit(self.__text, self.__text_rect)

    def __set_text(self, screen, inp, x, y):
        """Set text to screen

        :param pygame.Surface screen: screen to draw on
        :param str inp: text input
        :param int x: x coordinate
        :param int y: y coordinate
        """
        self.__text, self.__text_rect = self.__set_font(inp, 'Calibri', 24, TEXT_COLOUR)
        self.__text_rect.center = (x, y)
        screen.blit(self.__text, self.__text_rect)

    def __scale_image(self, image, x, y) -> pygame.surface.Surface:
        """Return scaled image of size x, y, which need to be in a tuple"""
        return pygame.transform.smoothscale(image, (x, y))

    def __draw_rect(self, screen, colour, rect_obj) -> pygame.rect.Rect:
        """Draw rectangle on screen with given colour"""
        return pygame.draw.rect(screen, colour, rect_obj)

    def __draw_title(self, screen, inp) -> None:
        """Draw title on screen with input inp"""
        self.__text, self.__text_rect = self.__set_font(inp, 'Calibri', 40, TEXT_COLOUR)
        self.__text_rect.center = ((WIDTH / 2), (HEIGHT / 10))
        screen.blit(self.__text, self.__text_rect)
