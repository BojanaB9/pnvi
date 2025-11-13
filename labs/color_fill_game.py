import pygame
import sys

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 650
GRID_SIZE = 5
CELL_SIZE = 80
GRID_OFFSET_X = (WIDTH - GRID_SIZE * CELL_SIZE) // 2
GRID_OFFSET_Y = 100

COLORS = {
    'BACKGROUND': (128, 128, 128),
    'GRID': (173, 171, 179),
    'game_colors': [
        (146, 121, 232),  # violet
        (250, 167, 180),  # coral
        (143, 204, 242),  # blue
        (238, 163, 255)   # pink
]
}


class Board:
    def __init__(self):
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    def color_cell(self, row, col, color):
        if self.grid[row][col] is None:
            self.grid[row][col] = color
            return True
        return False

    def is_game_over(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.grid[row][col] is not None:
                    for rd, cd in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # rd - row direction, cd - col drection
                        newrow, newcol = row + rd, col + cd
                        if 0 <= newrow < GRID_SIZE and 0 <= newcol < GRID_SIZE:  # out of bounds check
                            if self.grid[row][col] == self.grid[newrow][newcol]:
                                return True
        return False

    def is_board_filled(self):
        return all(all(cell is not None for cell in row) for row in self.grid)


def draw_board(screen, board, selected_cell):
    screen.fill(COLORS['BACKGROUND'])
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = GRID_OFFSET_X + col * CELL_SIZE
            y = GRID_OFFSET_Y + row * CELL_SIZE
            color = COLORS['GRID'] if board.grid[row][col] is None else pygame.Color(board.grid[row][col])
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, (0, 0, 0), (x, y, CELL_SIZE, CELL_SIZE), 1)
            if selected_cell and (row, col) == selected_cell:
                # highlight cell
                pygame.draw.rect(screen, (98, 95, 107), (x, y, CELL_SIZE, CELL_SIZE))

    for i, color in enumerate(COLORS['game_colors']):
        pygame.draw.rect(screen, pygame.Color(color),
                         (GRID_OFFSET_X + i * (CELL_SIZE + 10),
                          HEIGHT - 100,
                          CELL_SIZE,
                          CELL_SIZE))
        pygame.draw.rect(screen, pygame.Color('black'),
                         (GRID_OFFSET_X + i * (CELL_SIZE + 10),
                          HEIGHT - 100,
                          CELL_SIZE,
                          CELL_SIZE), 2)


def endscreen(screen, message):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    font = pygame.font.Font(None, 48)
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
    screen.blit(text, text_rect)


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Color Fill")
    board = Board()
    game_state = "playing"
    selected_cell = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_state != "playing":
                    board = Board()
                    game_state = "playing"
                    continue
                x, y = event.pos
                if (GRID_OFFSET_X <= x <= GRID_OFFSET_X + GRID_SIZE * CELL_SIZE and
                        GRID_OFFSET_Y <= y <= GRID_OFFSET_Y + GRID_SIZE * CELL_SIZE):
                    grid_x = (x - GRID_OFFSET_X) // CELL_SIZE
                    grid_y = (y - GRID_OFFSET_Y) // CELL_SIZE
                    selected_cell = (grid_y, grid_x)
                if HEIGHT - 100 <= y <= HEIGHT - 100 + CELL_SIZE:
                    color_index = (x - GRID_OFFSET_X) // (CELL_SIZE + 10)
                    if 0 <= color_index < len(COLORS['game_colors']):
                        if selected_cell:
                            if board.color_cell(selected_cell[0], selected_cell[1],
                                                COLORS['game_colors'][color_index]):
                                selected_cell = None
                                if board.is_game_over():
                                    game_state = "game_over"
                                elif board.is_board_filled():
                                    game_state = "won"
        draw_board(screen, board, selected_cell)
        if game_state == "game_over":
            endscreen(screen, "Game Over!")
        elif game_state == "won":
            endscreen(screen, "You Won!")
        pygame.display.flip()

if __name__ == "__main__":
    main()