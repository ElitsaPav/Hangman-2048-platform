import pygame
from Hangman.constants import GRAY, BLACK, BUTTON_WIDTH, OUTLINE_COLOR


class Button:
    def __init__(self, x, y, letter):
        self.x = x
        self.y = y
        self.letter = letter
        self.available = True

    def draw_button(self, scr, font):
        pygame.draw.rect(scr, OUTLINE_COLOR, (self.x, self.y, BUTTON_WIDTH, BUTTON_WIDTH))
        text = font.render(self.letter, 1, BLACK)
        text_width, text_height = text.get_size()
        scr.blit(text, (self.x + (BUTTON_WIDTH - text_width) // 2, self.y + (BUTTON_WIDTH - text_height) // 2))

    def click(self):
        if self.available:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            return self.x <= mouse_x <= self.x + BUTTON_WIDTH and self.y <= mouse_y <= self.y + BUTTON_WIDTH
        return False