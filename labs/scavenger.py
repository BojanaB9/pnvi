import random, sys, pygame
from pygame.locals import *

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 243, 105)
BLACK = (9, 0, 30)

# Object constants
INITIAL_SIZE = 70
INITIAL_SPEED = 3
DAMAGE_INCREMENT = 2


def reset_game():
    # initialize game variables
    return {
        "spaceship": {"x": 50, "y": SCREEN_HEIGHT // 2 - 60},
        "life_points": 10,
        "crystal_points": 0,
        "asteroids": [],
        "crystals": [],
        "speed": INITIAL_SPEED,
        "damage": 1,
        "game_over": False,
        "win": False,
        "timer": 0,
    }


def move_spaceship(keys):
    if keys[pygame.K_UP] and GAME["spaceship"]["y"] > 10:
        GAME["spaceship"]["y"] -= GAME["speed"]
    if keys[pygame.K_DOWN] and GAME["spaceship"]["y"] < SCREEN_HEIGHT - 150:
        GAME["spaceship"]["y"] += GAME["speed"]


def create_objects():
    # create new asteroids and crystals
    if len(GAME["asteroids"]) < 1 or random.randint(0, 99) <= 1:
        GAME["asteroids"].append({"x": SCREEN_WIDTH, "y": random.randint(60, SCREEN_HEIGHT - 150 - GAME["damage"])})
    if len(GAME["crystals"]) < 1 or random.randint(0, 99) <= 1:
        GAME["crystals"].append({"x": SCREEN_WIDTH, "y": random.randint(60, SCREEN_HEIGHT - 150)})


def move_objects():
    for asteroid in GAME["asteroids"]:
        asteroid["x"] -= GAME["speed"]
    for crystal in GAME["crystals"]:
        crystal["x"] -= GAME["speed"]


def remove_offscreen_objects():
    GAME["asteroids"] = [a for a in GAME["asteroids"] if a["x"] > -150]
    GAME["crystals"] = [c for c in GAME["crystals"] if c["x"] > -150]


def detect_collisions():
    # the dimensions are a bit off, to take into account the padding of the image objects
    spaceship_rect = pygame.Rect(GAME["spaceship"]["x"], GAME["spaceship"]["y"], INITIAL_SIZE, INITIAL_SIZE - 15)

    for asteroid in GAME["asteroids"]:
        asteroid_rect = pygame.Rect(asteroid["x"], asteroid["y"] + 25, INITIAL_SIZE + 2 * GAME["damage"], INITIAL_SIZE + 2 * GAME["damage"] - 45)
        if spaceship_rect.colliderect(asteroid_rect) and not GAME["game_over"]:
            #CLASH_SOUND.play()
            GAME["life_points"] -= GAME["damage"]
            if GAME["life_points"] < 0:
                GAME["life_points"] = 0
            GAME["asteroids"].remove(asteroid)

    for crystal in GAME["crystals"]:
        crystal_rect = pygame.Rect(crystal["x"] + 5, crystal["y"] + 20, INITIAL_SIZE - 15, INITIAL_SIZE - 35)
        if spaceship_rect.colliderect(crystal_rect) and not GAME["game_over"]:
            # BEEP_SOUND.play()
            GAME["crystal_points"] += 5
            if GAME["crystal_points"] > 100:
                GAME["crystal_points"] = 100
            GAME["crystals"].remove(crystal)


def increase_difficulty():
    GAME["speed"] += 2
    GAME["damage"] += DAMAGE_INCREMENT
    GAME["timer"] = 0


def check_game_over():
    # if both conditions (win/lose) are true, let the player win
    if GAME["life_points"] <= 0:
        GAME["game_over"] = True
        GAME["win"] = False
    if GAME["crystal_points"] >= 100:
        GAME["game_over"] = True
        GAME["win"] = True


def draw_objects():
    DISPLAYSURF.blit(SPACESHIP_IMG, (GAME["spaceship"]["x"], GAME["spaceship"]["y"]))

    for asteroid in GAME["asteroids"]:
        scaled_asteroid = pygame.transform.scale(ASTEROID_IMG, (INITIAL_SIZE + 2 * GAME["damage"], INITIAL_SIZE + 2 * GAME["damage"]))
        DISPLAYSURF.blit(scaled_asteroid, (asteroid["x"], asteroid["y"]))

    for crystal in GAME["crystals"]:
        DISPLAYSURF.blit(CRYSTAL_IMG, (crystal["x"], crystal["y"]))



def draw_crystals_needed_to_win():
    font = pygame.font.Font(None, 36)
    crys_score = pygame.transform.scale(CRYSTAL_IMG, (INITIAL_SIZE -3, INITIAL_SIZE -3))
    DISPLAYSURF.blit(crys_score, (10, 30))
    crystals_needed = GAME["crystal_points"]
    crystals_needed_text = font.render(f" {crystals_needed} /100", True, YELLOW)
    DISPLAYSURF.blit(crystals_needed_text, (60, 50))


def draw_heart(surface, color, x, y, size):
    # The "top" part of the heart (two circles)
    pygame.draw.circle(surface, color, (x - size // 2, y - size // 2), size // 2)  # Left circle
    pygame.draw.circle(surface, color, (x + size // 2, y - size // 2), size // 2)  # Right circle

    # The "bottom" part of the heart (triangle)
    points = [(x - size+0.5 // 2, y-5), (x + size-0.5 // 2, y-5), (x, y + size-1 // 4)]
    pygame.draw.polygon(surface, color, points)


def draw_progress_bars():
    health_x_start = 20
    hp_size = 10
    spacing = 20

    for i in range(GAME["life_points"]):
        draw_heart(DISPLAYSURF, RED, health_x_start + i * (hp_size + spacing), 20, hp_size)



def display_game_over_message():
    font = pygame.font.Font(None, 74)
    message = "You Won!" if GAME["win"] else "You Lost!"
    text = font.render(message, True, WHITE)
    DISPLAYSURF.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height()))
    restart_text = pygame.font.Font(None, 36).render("Press R to Restart", True, WHITE)
    DISPLAYSURF.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))


def main():
    global DISPLAYSURF, FPSCLOCK, GAME
    global SPACESHIP_IMG, ASTEROID_IMG, CRYSTAL_IMG, CRYSTAL_ICON, HEART_ICON, BACKGROUND_IMG
    global BACKGROUND_MUSIC, CLASH_SOUND, BEEP_SOUND

    pygame.init()

    DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Scavenger")

    # image files
    SPACESHIP_IMG = pygame.image.load("assets/images/spaceship.png")
    ASTEROID_IMG = pygame.image.load("assets/images/asteroid.png")
    CRYSTAL_IMG = pygame.image.load("assets/images/energy_crystal.png")


    pygame.display.set_icon(SPACESHIP_IMG)

    SPACESHIP_IMG = pygame.transform.scale(SPACESHIP_IMG, (INITIAL_SIZE, INITIAL_SIZE))
    ASTEROID_IMG = pygame.transform.rotate(ASTEROID_IMG, -45)
    ASTEROID_IMG = pygame.transform.scale(ASTEROID_IMG, (INITIAL_SIZE, INITIAL_SIZE))
    CRYSTAL_IMG = pygame.transform.scale(CRYSTAL_IMG, (INITIAL_SIZE, INITIAL_SIZE))
    CRYSTAL_ICON = pygame.transform.scale(CRYSTAL_IMG, (45, 45))


    # audio files
    BACKGROUND_MUSIC = "assets/sounds/background_music.wav"
    #CLASH_SOUND = pygame.mixer.Sound("assets/sounds/clash_sound.wav")


    #pygame.mixer.music.load(BACKGROUND_MUSIC)

    GAME = reset_game()

    # start background music
    #pygame.mixer.music.play(-1)

    FPSCLOCK = pygame.time.Clock()

    while True:  # main game loop
        DISPLAYSURF.fill(BLACK)
        GAME["timer"] += FPSCLOCK.get_time()

        check_for_quit()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if GAME["game_over"] and event.key == pygame.K_r:
                    GAME = reset_game()

        if not GAME["game_over"]:
            keys = pygame.key.get_pressed()
            move_spaceship(keys)

        if not GAME["game_over"]:
            create_objects()

        move_objects()
        remove_offscreen_objects()

        if not GAME["game_over"]:
            detect_collisions()

        # increase speed and damage every 10 seconds
        if GAME["timer"] >= 10000:
            increase_difficulty()

        check_game_over()

        draw_objects()

        draw_progress_bars()
        draw_crystals_needed_to_win()

        if GAME["game_over"]:
            display_game_over_message()

        pygame.display.flip()
        FPSCLOCK.tick(60)


def terminate():
    pygame.quit()
    sys.exit()


def check_for_quit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)


if __name__ == '__main__':
    main()
