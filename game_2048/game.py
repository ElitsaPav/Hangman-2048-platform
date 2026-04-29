import pygame
import os
import random
from game_2048.constants import *
from game_2048.tile import Tile

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("2048 Game!")
        self.tiles = {}
        self.clock = pygame.time.Clock()

    def draw_grid(self):
        for row in range(1, ROWS):
            y = row * TILE_HEIGHT #the starting position of every horizontal line
            pygame.draw.line(self.screen, OUTLINE_COLOR, (0, y), (WIDTH, y), LINE_THICKNESS)
        for col in range(1, COLS):
            x = col * TILE_WIDTH #the starting position of every vertical line
            pygame.draw.line(self.screen, OUTLINE_COLOR, (x, 0), (x, HEIGHT), LINE_THICKNESS)
        pygame.draw.rect(self.screen, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), LINE_THICKNESS)

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)

        for tile in self.tiles.values():
            tile.draw(self.screen)
        self.draw_grid()

        pygame.display.update()

    def get_random_pos(self):
        row = None
        col = None
        while True:
            row = random.randrange(0, ROWS)
            col = random.randrange(0, COLS)

            if f"{row}{col}" not in self.tiles:
                break

        return row, col

    def generate_tiles(self):
        for _ in range(2):
            row, col = self.get_random_pos()
            self.tiles[f"{row}{col}"] = Tile(2, row, col)

        return self.tiles

    def move_tiles(self, direction):
        updated = True
        blocks = set() #tiles already merged in a movement so do not merge again

        if direction == "left":
            sort_func = lambda x: x.col
            reverse = False
            delta = (-MOVE_VEL, 0) #moving negative to the x direction
            boundary_check = lambda tile: tile.col == 0
            get_next_tile = lambda tile: self.tiles.get(f"{tile.row}{tile.col - 1}")
            merge_check = lambda tile, next_tile: tile.x > next_tile.x + MOVE_VEL #to keep moving or is in the position to merge
            move_check = (
                lambda tile, next_tile: tile.x > next_tile.x + TILE_WIDTH + MOVE_VEL
            )
            ceil = True #to set the location of a tile after move
        elif direction == "right":
            sort_func = lambda x: x.col
            reverse = True
            delta = (MOVE_VEL, 0)
            boundary_check = lambda tile: tile.col == COLS - 1
            get_next_tile = lambda tile: self.tiles.get(f"{tile.row}{tile.col + 1}")
            merge_check = lambda tile, next_tile: tile.x < next_tile.x - MOVE_VEL
            move_check = (
                lambda tile, next_tile: tile.x + TILE_WIDTH + MOVE_VEL < next_tile.x
            )
            ceil = False
        elif direction == "up":
            sort_func = lambda x: x.row
            reverse = False
            delta = (0, -MOVE_VEL)
            boundary_check = lambda tile: tile.row == 0
            get_next_tile = lambda tile: self.tiles.get(f"{tile.row - 1}{tile.col}")
            merge_check = lambda tile, next_tile: tile.y > next_tile.y + MOVE_VEL
            move_check = (
                lambda tile, next_tile: tile.y > next_tile.y + TILE_HEIGHT + MOVE_VEL
            )
            ceil = True
        elif direction == "down":
            sort_func = lambda x: x.row
            reverse = True
            delta = (0, MOVE_VEL)
            boundary_check = lambda tile: tile.row == ROWS - 1
            get_next_tile = lambda tile: self.tiles.get(f"{tile.row + 1}{tile.col}")
            merge_check = lambda tile, next_tile: tile.y < next_tile.y - MOVE_VEL
            move_check = (
                lambda tile, next_tile: tile.y + TILE_HEIGHT + MOVE_VEL < next_tile.y
            )
            ceil = False

        #performing the movement
        while updated:
            self.clock.tick(FPS)
            updated = False
            sorted_tiles = sorted(self.tiles.values(), key=sort_func, reverse=reverse)

            for i, tile in enumerate(sorted_tiles):
                if boundary_check(tile):
                    continue

                next_tile = get_next_tile(tile)
                if not next_tile:
                    tile.move(delta)
                elif (
                        tile.value == next_tile.value
                        and tile not in blocks
                        and next_tile not in blocks
                ):
                    if merge_check(tile, next_tile):
                        tile.move(delta)
                    else:
                        next_tile.value *= 2
                        sorted_tiles.pop(i)
                        blocks.add(next_tile)
                elif move_check(tile, next_tile):
                    tile.move(delta)
                else:
                    continue

                tile.set_pos(ceil)
                updated = True

            self.update_tiles(sorted_tiles)

        return self.end_move()

    def end_move(self):
        if len(self.tiles) == 16:
            return "lost"

        row, col = self.get_random_pos()
        self.tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)
        return "continue"

    def update_tiles(self, sorted_tiles):
        self.tiles.clear()
        for tile in sorted_tiles:
            self.tiles[f"{tile.row}{tile.col}"] = tile

        self.draw()

    def end_game_message(self, message):
        pygame.time.delay(1000)
        self.screen.fill(BACKGROUND_COLOR)
        text = FONT.render(message, 1, BLACK)
        self.screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
        pygame.display.update()
        pygame.time.delay(3000)

    def update_score(self):
        score_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'scores_2048.txt')
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
        running = True
        tiles = self.generate_tiles()
        while running:
            self.clock.tick(FPS)
            res = ""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        res = self.move_tiles("left")
                    if event.key == pygame.K_RIGHT:
                        res = self.move_tiles("right")
                    if event.key == pygame.K_UP:
                        res = self.move_tiles("up")
                    if event.key == pygame.K_DOWN:
                        res = self.move_tiles("down")

            for tile in self.tiles.values():
                if tile.value == 2048:
                    self.end_game_message("YOU ARE A WINNER!")
                    self.update_score()
                    break

            if res == "lost":
                self.end_game_message("YOU LOST!")
                running = False
                break

            self.draw()






