import pygame
import sys
from Hangman.constants import OUTLINE_COLOR
from Hangman.game import Game as Game_hangman
from game_2048.game import Game as Game_2048
from games_scores import run_loop as get_scores

pygame.init()

WIDTH, HEIGHT = 800, 800
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("The Classics Hub")

WHITE = (255, 255, 255)
PINK = (234, 69, 192)

font = pygame.font.SysFont('comicsans', 40)
clock = pygame.time.Clock()
button_hangman = pygame.Rect(250, 150, 300, 100)
button_2048 = pygame.Rect(250, 300, 300, 100)
button_scores = pygame.Rect(250, 450, 300, 100)

def draw_menu():
    screen.fill(OUTLINE_COLOR)
    pygame.draw.rect(screen, PINK, button_hangman)
    pygame.draw.rect(screen, PINK, button_2048)
    pygame.draw.rect(screen, PINK, button_scores)

    text_hangman = font.render("Play Hangman", 1, WHITE)
    text_2048 = font.render("Play 2048", 1, WHITE)
    text_scores = font.render("Scores", 1, WHITE)
    screen.blit(text_hangman, (button_hangman.x + 30, button_hangman.y + 15))
    screen.blit(text_2048, (button_2048.x + 60, button_2048.y + 15))
    screen.blit(text_scores, (button_scores.x + 80, button_scores.y + 15))
    pygame.display.flip()

def run_hangman():
    game_hangman = Game_hangman()
    game_hangman.run()

def run_2048():
    game_2048_game = Game_2048()
    game_2048_game.run()

while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_hangman.collidepoint(event.pos):
                run_hangman()

            if button_2048.collidepoint(event.pos):
                run_2048()

            if button_scores.collidepoint(event.pos):
                get_scores()

        draw_menu()




