import pygame

WIDTH, HEIGHT = 800, 800
ROWS = 4
COLS = 4
TILE_WIDTH = WIDTH // COLS
TILE_HEIGHT = HEIGHT // ROWS
pygame.font.init()
FONT = pygame.font.SysFont("comicsans", 60, bold=True)
LINE_THICKNESS = 10
FPS = 60
MOVE_VEL = 20

BLACK = (0, 0, 0)
OUTLINE_COLOR = (255, 192, 203)
BACKGROUND_COLOR = (255, 228, 235)


