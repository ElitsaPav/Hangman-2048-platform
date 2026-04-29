import pygame
import math
from game_2048.constants import *
class Tile:

    COLORS = {
        2: (170, 80, 169),
        4: (234, 69, 192),
        8: (250, 186, 178),
        16: (67, 144, 112),
        32: (66, 54, 152),
        64: (56, 138, 91),
        128: (151, 87, 254),
        256: (122, 206, 170),
        512: (135, 210, 162),
        1024: (169, 187, 248),
        2048: (66, 169, 78)
    }

    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.x = col * TILE_WIDTH
        self.y = row * TILE_HEIGHT

    def get_color(self):
        return self.COLORS[self.value]

    def draw(self, screen):
        color = self.get_color()
        pygame.draw.rect(screen, color, (self.x, self.y, TILE_WIDTH, TILE_HEIGHT))

        text = FONT.render(str(self.value), 1, BLACK)
        screen.blit(
            text,
            (
                self.x + (TILE_WIDTH / 2 - text.get_width() / 2),
                self.y + (TILE_HEIGHT / 2 - text.get_height() / 2),
            ),
        )

    def set_pos(self, ceil=False):
        if ceil:
            self.row = math.ceil(self.y / TILE_HEIGHT)
            self.col = math.ceil(self.x / TILE_WIDTH)
        else:
            self.row = math.floor(self.y / TILE_HEIGHT)
            self.col = math.floor(self.x / TILE_WIDTH)

    def move(self, delta):
        self.x += delta[0]
        self.y += delta[1]
