import pygame
import os
from Hangman.constants import OUTLINE_COLOR

WIDTH = 800
HEIGHT = 800
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.font.init()
font = pygame.font.SysFont("comicsans", 40)

def read_hangman_score():
    score_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'scores.txt')
    try:
        with open(score_file_path, "r") as file:
            score = file.read().strip()
            return int(score)
    except FileNotFoundError:
        return 0

def read_2048_score():
    score_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'scores_2048.txt')
    try:
        with open(score_file_path, "r") as file:
            score = file.read().strip()
            return int(score)
    except FileNotFoundError:
        return 0

def display_scores(hangman_score, game_2048_score, screen):
    screen.fill(OUTLINE_COLOR)

    hangman_text = font.render(f"Score of game Hangman: {hangman_score}", 1, BLACK)
    game_2048_text = font.render(f"Score of game 2048: {game_2048_score}", 1, BLACK)

    screen.blit(hangman_text, (WIDTH / 2 - hangman_text.get_width() / 2, HEIGHT / 3 - hangman_text.get_height() / 2))
    screen.blit(game_2048_text,
                (WIDTH / 2 - game_2048_text.get_width() / 2, HEIGHT / 2 - game_2048_text.get_height() / 2))

    pygame.display.update()

def run_loop():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game Scores")

    hangman_score = read_hangman_score()
    game_2048_score = read_2048_score()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        display_scores(hangman_score, game_2048_score, screen)

if __name__ == "__main__":
    run_loop()


