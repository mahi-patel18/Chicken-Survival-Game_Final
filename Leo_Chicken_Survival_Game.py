import pygame
import sys
import os
import random

pygame.init()

# person 1 – setup + constants (dictionaries etc)
# Screen size
W = 800  # game width in pixels
H = 600  # game height in pixels
FPS = 60  # frames per second

screen = pygame.display.set_mode((W, H))  # opens the game window
pygame.display.set_caption("Chicken Survival Game")  # sets the title bar text
clock = pygame.time.Clock()  # controls the FPS

PLAYER_SPEED = 180  # Pixels per second — same for all chicks
PLAYER_HEALTH = 100  # Starting health
PLAYER_HUNGER = 100  # Starting hunger
PLAYER_ENERGY = 100  # Starting energy
EGG_COOLDOWN = 7  # Seconds between laying eggs
GAME_TIMER = 150 #seconds for level
bombs = []  # list of all bombs on the map
waters = []  # list of water on the map
fences = []  # list of fences

# popup globals
popup_msg   = ""
popup_timer = 0.0

# game state
state = "title"  # can be "title", "select", "play", "over"
player = None
dt = 0.0
selected_chick = 0


# Colors for future use
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)  # Health bar
YELLOW = (245, 230, 50)  # Energy warning
ORANGE = (230, 130, 40)  # Hunger warning
GREEN = (80, 180, 80)
DARK_GREEN = (40, 120, 40)
SKY = (135, 206, 235)
GRASS = (126, 200, 80)
BROWN = (160, 100, 50)
GRAY = (150, 150, 150)
DARK_GRAY = (50, 50, 50)  # Stats background
PINK = (225, 127, 162)

# Data for Chicken
Players = [
    {"id": "mahi",   "name": "Mahi Chick",   "image": "mahi.png"},
    {"id": "hilly",  "name": "Hilly Chick",  "image": "hilly.png"},
    {"id": "august", "name": "August Chick", "image": "august.png"},
    {"id": "leo",    "name": "Leo Chick",    "image": "leo.png"},
    {"id": "raj",    "name": "Raj Chick",    "image": "raj.png"},
]

# Data for each level
Levels = [
    {
        "level": 1,
        "eggs_needed": 1,
        "time_limit": 5,
        "has_fox": False,
        "has_farmer": False,
        "bomb_count": 3,
        "fence_count": 3,
        "water_count": 2,
        "corn_max": 5,
        "bg_color": GRASS,
    },
{
        "level": 2,
        "eggs_needed": 2,
        "time_limit": 5,
        "has_fox": False,
        "has_farmer": False,
        "bomb_count": 10,
        "fence_count": 3,
        "water_count": 5,
        "corn_max": 5,
        "bg_color": GRASS,
    }
]


# load images
def load_image(filename, w, h):
    image = pygame.image.load("Images/" + filename).convert_alpha()
    return pygame.transform.scale(image, (w, h))


images = {
    "mahi":   load_image("mahi.png",    60, 60),
    "hilly":  load_image("hilly.png",   60, 60),
    "august": load_image("august.png",  60, 60),
    "leo":    load_image("leo.png",     60, 60),
    "raj":    load_image("raj.png",     60, 60),
    "corn":   load_image("corn.png",    35, 50),
    "egg":    load_image("egg.png",     30, 30),
    "nest":   load_image("nest.png",    90, 44),
    "water":  load_image("water.png",   80, 52),
    "fence":  load_image("fence.png",   90, 63),
    "bomb":   load_image("bomb.png",    20, 20),
    "fox":    load_image("fox.png",     60, 70),
    "farmer": load_image("farmer.png",  60, 80),
}

font_big    = pygame.font.SysFont("Arial", 48, bold=True)
font_medium = pygame.font.SysFont("Arial", 22, bold=True)
font_small  = pygame.font.SysFont("Arial", 16)


# person 2 – drawing functions
def draw_title():
    screen.fill(SKY)
    screen.blit(font_big.render("CHICKEN GAME", True, WHITE), (200, 200))
    screen.blit(font_medium.render("Press ENTER to start", True, WHITE), (250, 320))


def draw_select():
    screen.fill(SKY)
    screen.blit(font_big.render("CHOOSE YOUR CHICK", True, WHITE), (125, 60))

    chicks_position = [80, 210, 340, 470, 600]

    for i, chick in enumerate(Players):
        if i == selected_chick:
            pygame.draw.rect(screen, WHITE, (chicks_position[i] - 40, 150, 80, 80), 3)
        screen.blit(images[chick["id"]], (chicks_position[i] - 30, 160))
        screen.blit(font_small.render(chick["name"], True, WHITE), (chicks_position[i] - 30, 260))

    screen.blit(font_small.render("← → TO BROWSE | ENTER TO PLAY", True, WHITE), (220, 380))


def draw_gameover():
    screen.fill(GRASS)
    # dark overlay
    overlay = pygame.Surface((W, H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))
    screen.blit(font_big.render("GAME OVER", True, RED), (250, 200))
    screen.blit(font_medium.render("Press ENTER to retry  |  ESC for title", True, WHITE), (170, 320))

def draw_won():
    screen.fill(GRASS)
    # dark overlay
    overlay = pygame.Surface((W, H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))
    screen.blit(font_big.render("YOU WON", True, SKY), (275, 200))
    screen.blit(font_medium.render("Press ENTER for next level  |  ESC for title", True, WHITE), (170, 320))

def draw_levelsdone():
    screen.fill(GRASS)
    # dark overlay
    overlay = pygame.Surface((W, H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))
    screen.blit(font_big.render("All Levels Done!", True, SKY), (200, 200))
    screen.blit(font_medium.render("Press ENTER for title", True, WHITE), (275, 320))


def draw_hud():
    # background bar
    pygame.draw.rect(screen, DARK_GRAY, (0, 0, W, 50))

    # health bar
    pygame.draw.rect(screen, (80, 80, 80), (10, 8, 160, 16))
    pygame.draw.rect(screen, GREEN,          (10, 8, int(160 * player["health"] / 100), 16))
    screen.blit(font_small.render(f"HP  {int(player['health'])}", True, WHITE), (10, 28))

    # hunger bar
    pygame.draw.rect(screen, (80, 80, 80), (210, 8, 160, 16))
    pygame.draw.rect(screen, ORANGE,       (210, 8, int(160 * player["hunger"] / 100), 16))
    screen.blit(font_small.render(f"Hunger  {int(player['hunger'])}", True, WHITE), (210, 28))

    # energy bar
    pygame.draw.rect(screen, (80, 80, 80), (410, 8, 160, 16))
    pygame.draw.rect(screen, YELLOW,       (410, 8, int(160 * player["energy"] / 100), 16))
    screen.blit(font_small.render(f"Energy  {int(player['energy'])}", True, WHITE), (410, 28))

    # level timer
    pygame.draw.rect(screen, (80, 80, 80), (610, 8, 160, 16))
    pygame.draw.rect(screen, SKY, (610, 8, int(160 * level_timer / 150), 16))
    screen.blit(font_small.render(f"Time Left  {int(level_timer)}", True, WHITE), (610, 28))


def draw_game():
    screen.fill(GRASS)

    # draw water
    for water in waters:
        screen.blit(images["water"], (int(water["x"]), int(water["y"])))

    # draw fences
    for fence in fences:
        screen.blit(images["fence"], (int(fence["x"]), int(fence["y"])))

    # draw bombs
    for bomb in bombs:
        if bomb["alive"]:
            screen.blit(images["bomb"], (int(bomb["x"]), int(bomb["y"])))

    # draw chicken
    img = images[player["chick_id"]]
    if not player["facing_left"]:
        img = pygame.transform.flip(img, True, False)
    screen.blit(img, (int(player["x"]), int(player["y"])))

    # draw hud on top
    draw_hud()

    # draw popup
    if popup_timer > 0 and popup_msg:
        txt = font_medium.render(popup_msg, True, WHITE)
        bg  = pygame.Surface((txt.get_width() + 20, 36), pygame.SRCALPHA)
        bg.fill((0, 0, 0, 180))
        screen.blit(bg,  (W // 2 - bg.get_width()  // 2, H // 2 - 18))
        screen.blit(txt, (W // 2 - txt.get_width() // 2, H // 2 - 10))


# person 3 – player movement + stats
def make_player():
    return {
        "x": 60.0,
        "y": 500.0,
        "previous_x": 60.0,
        "previous_y": 500.0,
        "speed": 180.0,
        "facing_left": True,
        "moving": False,
        "health": 100.0,
        "hunger": 100.0,
        "energy": 100.0,
        "carrying_egg": False,
        "egg_cooldown": 0.0,
        "eggs_delivered": 0,
        "hunger_timer": 0.0,
        "standing_timer": 0.0,
        "chick_id": Players[selected_chick]["id"],
    }


def move_player():
    global player, dt
    keys = pygame.key.get_pressed()
    direction_x = 0
    direction_y = 0

    if keys[pygame.K_LEFT]  or keys[pygame.K_a]:
        direction_x = -1
        player["facing_left"] = True
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        direction_x = 1
        player["facing_left"] = False
    if keys[pygame.K_UP]    or keys[pygame.K_w]:
        direction_y = -1
    if keys[pygame.K_DOWN]  or keys[pygame.K_s]:
        direction_y = 1

    player["moving"] = direction_x != 0 or direction_y != 0

    if direction_x != 0 and direction_y != 0:
        direction_x *= 0.707
        direction_y *= 0.707

    current_speed = player["speed"]
    if player["energy"] < 20:
        current_speed *= 0.45
    elif player["energy"] < 50:
        current_speed *= 0.70

    player["previous_x"] = player["x"]
    player["previous_y"] = player["y"]

    player["x"] += direction_x * current_speed * dt
    player["y"] += direction_y * current_speed * dt

    player["x"] = max(0, min(W - 60, player["x"]))
    player["y"] = max(60, min(H - 60, player["y"]))


def drain_stats():
    global player, dt

    if player["egg_cooldown"] > 0:
        player["egg_cooldown"] = max(0.0, player["egg_cooldown"] - dt)

    player["hunger_timer"] += dt
    if player["hunger_timer"] >= 5.0:
        player["hunger_timer"] -= 5.0
        player["hunger"] = max(0.0, player["hunger"] - 2.0)

    if player["hunger"] == 0:
        player["health"] = max(0.0, player["health"] - 2.0 * dt)

    if player["moving"]:
        player["energy"] = max(0.0, player["energy"] - (1.0 / FPS))


def try_lay_eggs():
    pass

def carry_to_nest():
    pass


# person 4 – items + collisions
def spawn_corn():
    pass

def disappear_corn():
    pass


def make_water():
    return {
        "x": random.randint(100, W - 150),
        "y": random.randint(100, H - 100),
        "w": 80,
        "h": 52,
    }


def check_water():
    global player, dt, waters
    for water in waters:
        chicken_rect = pygame.Rect(player["x"], player["y"], 60, 60)
        water_rect   = pygame.Rect(water["x"],  water["y"],  water["w"], water["h"])  # fixed: was waters["x"]
        if chicken_rect.colliderect(water_rect):
            player["energy"] = min(100.0, player["energy"] + 20.0 * dt)


def make_fence():
    return {  # fixed: was missing return
        "x": random.randint(100, W - 200),
        "y": random.randint(100, H - 150),
        "w": 90,
        "h": 63,
    }


def check_fence():
    global player, fences
    chicken_rect = pygame.Rect(player["x"], player["y"], 60, 60)
    for fence in fences:
        fence_rect = pygame.Rect(fence["x"], fence["y"], fence["w"], fence["h"])
        if chicken_rect.colliderect(fence_rect):
            player["x"] = player["previous_x"]
            player["y"] = player["previous_y"]


def check_nest():
    pass

def make_fox():
    pass

def move_fox():
    pass

def check_fox():
    pass

def make_farmer():
    pass

def move_farmer():
    pass

def check_farmer():
    pass


def make_bomb():
    return {
        "x":     random.randint(100, W - 100),
        "y":     random.randint(100, H - 100),
        "alive": True,
        "damage": 30
    }


def check_bomb():
    global player, bombs
    for bomb in bombs:
        if bomb["alive"]:
            chicken_rect = pygame.Rect(player["x"], player["y"], 60, 60)
            bomb_rect    = pygame.Rect(bomb["x"],   bomb["y"],   20, 20)
            if chicken_rect.colliderect(bomb_rect):
                bomb["alive"] = False
                player["health"] = max(0, player["health"] - bomb["damage"])
                pop_up_message(f"BOOM! -{bomb['damage']} health!")


# person 5 – main game loop + screens
def pop_up_message(message):  # fixed: was missing parameter
    global popup_msg, popup_timer
    popup_msg   = message
    popup_timer = 2.0


def start_game():
    global state, player, dt, selected_chick, popup_timer, popup_msg, Levels, level_timer
    global bombs, waters, fences
    level_count: int = 0

    while True:
        dt = clock.tick(FPS) / 1000.0

        # 1. handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                # title screen — press enter to go to character select
                if state == "title":
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        state = "select"

                # character select — browse and confirm
                elif state == "select":
                    if event.key == pygame.K_LEFT:
                        selected_chick = (selected_chick - 1) % len(Players)
                    if event.key == pygame.K_RIGHT:
                        selected_chick = (selected_chick + 1) % len(Players)
                    if event.key == pygame.K_RETURN:
                        # set up the game
                        level_timer = Levels[level_count]["time_limit"]
                        player = make_player()
                        bombs = [make_bomb() for i in range(Levels[level_count]["bomb_count"])]
                        waters = [make_water() for i in range(Levels[level_count]["water_count"])]
                        fences = [make_fence() for i in range(Levels[level_count]["fence_count"])]
                        if Levels[level_count]["has_fox"]:
                            make_fox()
                        if Levels[level_count]["has_farmer"]:
                            make_farmer()
                        state  = "play"

                # game over — retry or go back to title
                elif state == "won":
                    if event.key == pygame.K_RETURN:
                        level_timer = Levels[level_count]["time_limit"]
                        player = make_player()
                        bombs = [make_bomb() for i in range(Levels[level_count]["bomb_count"])]
                        waters = [make_water() for i in range(Levels[level_count]["water_count"])]
                        fences = [make_fence() for i in range(Levels[level_count]["fence_count"])]
                        if Levels[level_count]["has_fox"]:
                            make_fox()
                        if Levels[level_count]["has_farmer"]:
                            make_farmer()
                        state = "play"
                    if event.key == pygame.K_ESCAPE:
                        state = "title"
                elif state == "over":
                    if event.key == pygame.K_RETURN:
                        level_timer = Levels[level_count]["time_limit"]
                        player = make_player()
                        bombs  = [make_bomb() for i in range(Levels[level_count]["bomb_count"])]
                        waters = [make_water() for i in range(Levels[level_count]["water_count"])]
                        fences = [make_fence() for i in range(Levels[level_count]["fence_count"])]
                        state  = "play"
                        if Levels[level_count]["has_fox"]:
                            make_fox()
                        if Levels[level_count]["has_farmer"]:
                            make_farmer()
                    if event.key == pygame.K_ESCAPE:
                        state = "title"
                elif state == "levels_done":
                    if event.key == pygame.K_RETURN:
                        state = "title"

        # 2. update
        if state == "play":
            check_nest()
            move_player()
            drain_stats()
            check_fence()
            check_water()
            check_bomb()
            check_fox()
            check_farmer()

            # count down popup
            if popup_timer > 0:
                popup_timer -= dt

            # level count down
            if level_timer >0:
                level_timer -= dt

            # check game won
            if player["eggs_delivered"] == Levels[level_count]["eggs_needed"]:
                state = "won"
                level_count += 1
                if level_count >= len(Levels)-1:
                    state = "levels_done"
                    level_count = 0


            # check game over
            elif player["health"] <= 0 or level_timer <= 0:
                state = "over"





        # 3. draw
        if state == "title":
            draw_title()
        elif state == "select":
            draw_select()
        elif state == "play":
            draw_game()
        elif state == "won":
            draw_won()
        elif state == "over":
            draw_gameover()
        elif state == "levels_done":
            draw_levelsdone()

        # 4. update display
        pygame.display.flip()


if __name__ == "__main__":
    start_game()