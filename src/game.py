#!/usr/bin/env python3

from random import Random
import os
import sys
import pygame


# Colour and screen size
WIDTH = 1000
HEIGHT = 800
BUTTON_COLOUR = (153, 204, 255)
WHITE = (255, 255, 255)
TEXT_COLOUR = (0, 0, 0)

# Current directory for this file
PARENT_DIR = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

# Images used
ROCK_IMG = pygame.image.load(os.path.join(PARENT_DIR, 'resources', 'images', 'rock.png'))
PAPER_IMG = pygame.image.load(os.path.join(PARENT_DIR, 'resources', 'images', 'paper.png'))
SCISSORS_IMG = pygame.image.load(
    os.path.join(PARENT_DIR, 'resources', 'images', 'scissors.png'))
IMG = [ROCK_IMG, PAPER_IMG, SCISSORS_IMG]

# Player actions
ROCK = "Rock"
PAPER = "Paper"
SCISSORS = "Scissors"
CHOICES = [ROCK, PAPER, SCISSORS]


class RockPaperScissor:
    """Game class"""

    def __init__(self) -> None:
        """Constructor"""
        pygame.init()

    def play(self) -> None:
        """Start the game"""
        self._draw()

    def _draw(self) -> None:
        """Create elements and draw the game"""
        computer_choice = 0
        computer_score = 0
        player_score = 0
        ret = 0

        # Create screen, fill background and add window title
        self.screen = self._create_screen()
        self.screen.fill(WHITE)
        pygame.display.set_caption('Rock Paper Scissors')

        # Create rectangles that will become buttons
        rock = self._create_rect(50, 600, 80, 40)
        paper = self._create_rect(150, 600, 80, 40)
        scissors = self._create_rect(250, 600, 80, 40)

        # Rectangles to cover text to avoid overlay
        cover_left = self._create_rect(WIDTH - 920, HEIGHT - 140, 230, 58)
        cover_middle = self._create_rect(WIDTH - 800, HEIGHT - 260, 555, 30)
        cover_right = self._create_rect(WIDTH - 350, HEIGHT - 190, 300, 80)

        # Draw on screen
        running = True
        while running:
            for event in pygame.event.get():
                # Quit if window is closed
                if event.type == pygame.QUIT:
                    running = False
                # Change layout when player takes action
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Mouse position and random generator
                    mouse_pos = pygame.mouse.get_pos()
                    rand = Random().randint(0, 2)
                    # If player pressed on a given button;
                    # output image, show winner and update
                    # points. Checks if mouse is over button
                    if rock.collidepoint(mouse_pos):
                        computer_choice = CHOICES[rand]
                        self.screen.blit(self._scale_image(
                            ROCK_IMG, 300, 300), (45, 200))
                        self.screen.blit(self._scale_image(
                            IMG[rand], 300, 300), (650, 200))
                        ret = self._compute(computer_choice, ROCK)
                    elif paper.collidepoint(mouse_pos):
                        computer_choice = CHOICES[rand]
                        self.screen.blit(self._scale_image(
                            PAPER_IMG, 300, 300), (45, 200))
                        self.screen.blit(self._scale_image(
                            IMG[rand], 300, 300), (650, 200))
                        ret = self._compute(computer_choice, PAPER)
                    elif scissors.collidepoint(mouse_pos):
                        computer_choice = CHOICES[rand]
                        self.screen.blit(self._scale_image(
                            SCISSORS_IMG, 300, 300), (45, 200))
                        self.screen.blit(self._scale_image(
                            IMG[rand], 300, 300), (650, 200))
                        ret = self._compute(computer_choice, SCISSORS)
                    else:
                        continue

                    # Set correct scores
                    if ret == 1:
                        player_score += 1
                    elif ret == 2:
                        computer_score += 1

            # Add title and text on the buttons
            self._draw_title(self.screen, 'Rock Paper Scissors')
            self._draw_rect(self.screen, BUTTON_COLOUR, rock)
            self._add_rect_text(self.screen, 'Rock', rock)
            self._draw_rect(self.screen, BUTTON_COLOUR, paper)
            self._add_rect_text(self.screen, 'Paper', paper)
            self._draw_rect(self.screen, BUTTON_COLOUR, scissors)
            self._add_rect_text(self.screen, 'Scissors', scissors)

            # Add computer choice, player score and computer score
            x, y = self._rect_pos(rock)
            self._show_score(
                self.screen, f'Player score: {player_score}', WIDTH - 810, HEIGHT - 125)
            self._set_text(
                self.screen, f'Computer choose: {computer_choice}', x + 700, y)
            self._show_score(
                self.screen, f'Computer score: {computer_score}', WIDTH - 210, HEIGHT - 125)

            # Set info text
            if player_score == 0 and computer_score == 0:
                self._set_text(
                    self.screen, 'Let the game begin! Start by choosing an action', WIDTH - 500, HEIGHT - 250)
            elif ret == 1:
                self._set_text(self.screen, 'Player wins',
                               WIDTH - 500, HEIGHT - 250)
            elif ret == 2:
                self._set_text(self.screen, 'Computer wins',
                               WIDTH - 500, HEIGHT - 250)
            else:
                self._set_text(self.screen, 'Its a draw',
                               WIDTH - 500, HEIGHT - 250)

            # Update screen for each new event
            pygame.display.flip()

            # Draw new rectangles to hide old text
            self._draw_rect(self.screen, WHITE, cover_left)
            self._draw_rect(self.screen, WHITE, cover_middle)
            self._draw_rect(self.screen, WHITE, cover_right)

        # Quit pygame and program
        pygame.quit()
        sys.exit()

    def _compute(self, computer_choice, player_choice) -> int:
        """Compute who wins the round and update scores

        Args:
            computer_choice (str): computer's action
            player_choice (str): player's action

        Returns:
            int: 1 -> player wins, 2 -> computer wins
        """
        # Compute winner
        if (player_choice == ROCK and computer_choice == SCISSORS
            or player_choice == PAPER and computer_choice == ROCK
                or player_choice == SCISSORS and computer_choice == PAPER):
            return 1
        elif (computer_choice == ROCK and player_choice == SCISSORS
              or computer_choice == PAPER and player_choice == ROCK
                or computer_choice == SCISSORS and player_choice == PAPER):
            return 2
        return 0

    def _set_font(self, inp, font, size, colour) -> tuple:
        """Set font for text

        Args:
            inp (str): text to input
            font (str): font type
            size (int): text size
            colour (rgb): text colour

        Returns:
            pygame.font.Font: return font object
        """
        self._font = pygame.font.SysFont(font, size)
        self._text = self._font.render(inp, True, colour)
        self._text_rect = self._text.get_rect()
        return self._text, self._text_rect

    def _rect_pos(self, rect_obj) -> tuple:
        """Return x, y coordinate for center of rectangle """
        return rect_obj.centerx, rect_obj.centery

    def _create_screen(self) -> pygame.Surface:
        """Create screen to draw on """
        return pygame.display.set_mode((WIDTH, HEIGHT))

    def _create_rect(self, x, y, width, height) -> pygame.rect.Rect:
        """Create rectangle with width and height on x and y coordinate """
        return pygame.Rect(x, y, width, height)

    def _show_score(self, screen, inp, x, y):
        """Show score of each player in the game

        Args:
            screen (pygame.Surface): screen to draw on
            inp (str): text input
            x (int): x coordinate
            y (int): y coordinate
        """
        self._text, self._text_rect = self._set_font(
            inp, 'Calibri', 24, TEXT_COLOUR)
        self._text_rect.center = (x, y)
        screen.blit(self._text, self._text_rect)

    def _add_rect_text(self, screen, inp, rect_obj):
        """Add text to rectangle object

        Args:
            screen (pygame.Surface): screen to draw on
            inp (str): text input
            rect_obj (pygame.rect.Rect): rectangle object
        """
        self._text, self._text_rect = self._set_font(
            inp, 'Calibri', 24, TEXT_COLOUR)
        x, y = self._rect_pos(rect_obj)
        self._text_rect.center = (x, y)
        screen.blit(self._text, self._text_rect)

    def _set_text(self, screen, inp, x, y):
        """Set text to screen

        Args:
            screen (pygame.Surface): screen to draw on
            inp (str): text input
            x (int): x coordinate
            y (int): y coordinate
        """
        self._text, self._text_rect = self._set_font(
            inp, 'Calibri', 24, TEXT_COLOUR)
        self._text_rect.center = (x, y)
        screen.blit(self._text, self._text_rect)

    def _scale_image(self, image, x, y) -> pygame.Surface:
        """Return scaled image of size x, y.
        These coordinates need to be in a tuple"""
        return pygame.transform.smoothscale(image, (x, y))

    def _draw_rect(self, screen, colour, rect_obj) -> pygame.rect.Rect:
        """Draw rectangle on screen with given colour"""
        return pygame.draw.rect(screen, colour, rect_obj)

    def _draw_title(self, screen, inp) -> None:
        """Draw title on screen with input inp"""
        self._text, self._text_rect = self._set_font(
            inp, 'Calibri', 40, TEXT_COLOUR)
        self._text_rect.center = ((WIDTH / 2), (HEIGHT / 10))
        screen.blit(self._text, self._text_rect)
