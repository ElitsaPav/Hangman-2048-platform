import pygame
from pygame import MOUSEBUTTONDOWN
import random
import os
from Hangman.constants import *
from Hangman.button import Button

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Hangman Game!")

        self.fonts = {
            "letter": pygame.font.SysFont('comicsans', 40),
            "word": pygame.font.SysFont('comicsans', 60),
        }

        self.images = Game.load_images()
        self.hangman_status = 0
        self.words = ["CAT", "MOUSE", "FRIDGE", "PYTHON", "PHONE", "BABY", "ELEPHANT", "CUPBOARD", "SOFA",
                      "PENCIL", "UMBRELLA", "GUIDE", "CALIFORNIA", "UNIVERSITY", "CANDLE", "DESSERT",
                      "BATHROOM", "BANANA", "SUMMER", "PROJECT", "GARDEN", "ROAD", "PEPPER", "PARENT"
                      ]
        self.word = random.choice(self.words)
        self.clicked_letters = []
        self.buttons = Game.create_buttons()

    @staticmethod
    def load_images():
        images = []
        base_path = os.path.dirname(__file__)
        for i in range(7):
            curr_image = pygame.image.load(os.path.join(base_path, 'h' + str(i) + '.png'))
            new_size = (700, 500)
            resized_image = pygame.transform.scale(curr_image, new_size)
            images.append(resized_image)
        return images

    @staticmethod
    def create_buttons():
        buttons = []
        A = 65
        for i in range(26):
            x = BUTTONS_START_POS_X + (BUTTON_WIDTH + BUTTON_GAP) * (i % 5)
            y = BUTTONS_START_POS_Y + (i // 5) * (BUTTON_WIDTH + BUTTON_GAP)
            buttons.append(Button(x, y, chr(A + i)))
        return buttons

    def draw(self):
        self.screen.fill(WHITE)
        self.screen.blit(self.images[self.hangman_status], (0, 0))

        word_to_guess = " ".join(l if l in self.clicked_letters else "_" for l in self.word)
        text = self.fonts["word"].render(word_to_guess, 1, BLACK)
        self.screen.blit(text, (WORD_X, WORD_Y))

        for button in self.buttons:
            if button.available:
                button.draw_button(self.screen, self.fonts["letter"])
            else:
                pygame.draw.rect(self.screen, BLACK, (button.x, button.y, BUTTON_WIDTH, BUTTON_WIDTH))

        pygame.display.update()

    def end_game_message(self, message):
        pygame.time.delay(1000)
        self.screen.fill(WHITE)
        text = self.fonts["word"].render(message, 1, BLACK)
        self.screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
        pygame.display.update()
        pygame.time.delay(3000)

    def update_score(self):
        score_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'scores.txt')
        try:
            if os.path.exists(score_file_path):
                with open(score_file_path, "r") as file:
                    score = int(file.read().strip())
            else:
                score = 0
        except ValueError:
            score = 0

        score += 1

        with open(score_file_path, "w") as file:
            file.write(str(score))

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.click():
                            button.available = False
                            self.clicked_letters.append(button.letter)
                            if button.letter not in self.word:
                                self.hangman_status += 1

            self.draw()

            guessed = True
            for letter in self.word:
                if letter not in self.clicked_letters:
                    guessed = False

            if guessed:
                self.end_game_message("YOU ARE A WINNER!")
                self.update_score()
                break
            if self.hangman_status == 6:
                self.end_game_message("YOU LOST!")
                break