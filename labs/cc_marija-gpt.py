import pygame
import random

# --- Constants ---
WIDTH, HEIGHT = 640, 700
GRID_SIZE = 8
TILE_SIZE = WIDTH // GRID_SIZE
FPS = 30
CANDY_TYPES = 4

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Candy Crush – Full Version")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28, bold=True)

# --- Load Images ---
def get_img(path):
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))

IMAGES = [
    get_img('circle.png'),
    get_img('triangle.png'),
    get_img('square.png'),
    get_img('stop.png')
]

# --- Board Creation ---
def create_board():
    board = [[random.randint(0, CANDY_TYPES - 1) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    while find_matches(board):
        remove_matches(board, find_matches(board))
        apply_gravity(board)
    return board

# --- Match Detection (Rows, Columns, Diagonals, 3+) ---
def find_matches(board):
    matches = set()

    # Horizontal
    for r in range(GRID_SIZE):
        c = 0
        while c < GRID_SIZE - 2:
            start = c
            val = board[r][c]
            while c < GRID_SIZE and board[r][c] == val:
                c += 1
            if c - start >= 3:
                for x in range(start, c): matches.add((r, x))
            if start == c: c += 1

    # Vertical
    for c in range(GRID_SIZE):
        r = 0
        while r < GRID_SIZE - 2:
            start = r
            val = board[r][c]
            while r < GRID_SIZE and board[r][c] == val:
                r += 1
            if r - start >= 3:
                for x in range(start, r): matches.add((x, c))
            if start == r: r += 1

    # Diagonal ↘
    for r in range(GRID_SIZE - 2):
        for c in range(GRID_SIZE - 2):
            val = board[r][c]
            k = 0
            while r + k < GRID_SIZE and c + k < GRID_SIZE and board[r + k][c + k] == val:
                k += 1
            if k >= 3:
                for i in range(k): matches.add((r + i, c + i))

    # Diagonal ↙
    for r in range(GRID_SIZE - 2):
        for c in range(2, GRID_SIZE):
            val = board[r][c]
            k = 0
            while r + k < GRID_SIZE and c - k >= 0 and board[r + k][c - k] == val:
                k += 1
            if k >= 3:
                for i in range(k): matches.add((r + i, c - i))

    '''Samo ova dodaj go vo na marija kodot za da ima i doagonalno spojjuvanje
    def find_matches(board):
    to_rem = set()
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):

            # Horizontal
            if c < GRID_SIZE - 2 and board[r][c] == board[r][c + 1] == board[r][c + 2]:
                to_rem.update([(r, c), (r, c + 1), (r, c + 2)])

            # Vertical
            if r < GRID_SIZE - 2 and board[r][c] == board[r + 1][c] == board[r + 2][c]:
                to_rem.update([(r, c), (r + 1, c), (r + 2, c)])

            # ✅ Diagonal ↘ (top-left → bottom-right)
            if r < GRID_SIZE - 2 and c < GRID_SIZE - 2 and \
               board[r][c] == board[r + 1][c + 1] == board[r + 2][c + 2]:
                to_rem.update([(r, c), (r + 1, c + 1), (r + 2, c + 2)])

            # ✅ Diagonal ↙ (top-right → bottom-left)
            if r < GRID_SIZE - 2 and c > 1 and \
               board[r][c] == board[r + 1][c - 1] == board[r + 2][c - 2]:
                to_rem.update([(r, c), (r + 1, c - 1), (r + 2, c - 2)])'''

    return to_rem

    return matches

# --- Remove Matches ---
def remove_matches(board, matches):
    for r, c in matches:
        board[r][c] = -1

# --- Gravity ---
def apply_gravity(board):
    for c in range(GRID_SIZE):
        stack = [board[r][c] for r in range(GRID_SIZE) if board[r][c] != -1]
        while len(stack) < GRID_SIZE:
            stack.insert(0, random.randint(0, CANDY_TYPES - 1))
        for r in range(GRID_SIZE):
            board[r][c] = stack[r]

# --- Drawing ---
def draw(board, selected, score):
    screen.fill((245, 245, 245))
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            screen.blit(IMAGES[board[r][c]], (c * TILE_SIZE, r * TILE_SIZE))

    if selected:
        pygame.draw.rect(screen, (0, 200, 0),
                         (selected[1] * TILE_SIZE, selected[0] * TILE_SIZE, TILE_SIZE, TILE_SIZE), 4)

    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, HEIGHT - 50))
    pygame.display.flip()

# --- Main Loop ---
def main():
    board = create_board()
    selected = None
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); return

            if event.type == pygame.MOUSEBUTTONDOWN:
                c, r = event.pos[0] // TILE_SIZE, event.pos[1] // TILE_SIZE
                if r >= GRID_SIZE: continue

                if not selected:
                    selected = (r, c)
                else:
                    r1, c1 = selected
                    if abs(r1 - r) + abs(c1 - c) == 1:
                        board[r1][c1], board[r][c] = board[r][c], board[r1][c1]
                        matches = find_matches(board)
                        if matches:
                            while matches:
                                score += len(matches)
                                remove_matches(board, matches)
                                apply_gravity(board)
                                matches = find_matches(board)
                        else:
                            board[r1][c1], board[r][c] = board[r][c], board[r1][c1]
                    selected = None

        draw(board, selected, score)
        clock.tick(FPS)

if __name__ == '__main__':
    main()
