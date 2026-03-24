import dt
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
bombs = []  # list of all bombs on the map

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
    {
        "id": "mahi", "name": "Mahi Chick", "image": "mahi.png"
    },
    {
        "id": "hilly", "name": "Hilly Chick", "image": "hilly.png"
    },
    {
        "id": "august", "name": "August Chick", "image": "august.png"
    },

    {
        "id": "leo", "name": "Leo Chick", "image": "leo.png"
    },

    {
        "id": "raj", "name": "Raj Chick", "image": "raj.png"
    },
]

# Data for each level
Levels = [
    {
        # Level 1: Easy(Example btw)
        "level": 1,
        "eggs_needed": 1,
        "time_limit": 150,  # Seconds
        "has_fox": False,
        "has_farmer": False,
        "has_bomb": False,
        "corn_max": 5,
        "bg_color": GRASS,  # Background color for this level
    },
    # copy this block for each level
]


# load images
def load_image(filename, w, h):
    image = pygame.image.load("Images/" + filename).convert_alpha()
    return pygame.transform.scale(image, (w, h))


images = {
    "mahi": load_image("mahi.png", 60, 60),
    "hilly": load_image("hilly.png", 60, 60),
    "august": load_image("august.png", 60, 60),
    "leo": load_image("leo.png", 60, 60),
    "raj": load_image("raj.png", 60, 60),
    "corn": load_image("corn.png", 35, 50),
    "egg": load_image("egg.png", 30, 30),
    "nest": load_image("nest.png", 90, 44),
    "water": load_image("water.png", 80, 52),
    "fence": load_image("fence.png", 90, 63),
    "bomb": load_image("bomb.png", 20, 20),
    "fox": load_image("fox.png", 60, 70),
    "farmer": load_image("farmer.png", 60, 80),
}

font_big = pygame.font.SysFont("Arial", 48, bold=True)  # big font for titles
font_medium = pygame.font.SysFont("Arial", 22, bold=True)  # medium font for HUD
font_small = pygame.font.SysFont("Arial", 16)  # small font for labels


# person 2 – drawing functions
# title screen
def draw_title():
    screen.fill(SKY)  # paints background blue
    screen.blit(font_big.render("CHICKEN GAME", True, WHITE), (200, 200))  # draws title
    screen.blit(font_medium.render("Press ENTER to start", True, WHITE), (250, 320))  # draws hint


selected_chick = 0


def draw_select():
    screen.fill(SKY)  # blue background

    # title
    screen.blit(font_big.render("CHOOSE YOUR CHICK", True, WHITE), (200, 60))  # title text

    # chick positions on screen
    chicks_position = [80, 210, 340, 470, 600]

    # draw each chick one by one
    for i, chick in enumerate(Players):

        # draw white box around the selected chick
        if i == selected_chick:
            pygame.draw.rect(screen, WHITE, (chicks_position[i] - 40, 150, 80, 80), 3)  # white border

        # draw chick image
        screen.blit(images[chick["id"]], (chicks_position[i] - 30, 160))  # chick picture

        # draw chick name
        screen.blit(font_small.render(chick["name"], True, WHITE), (chicks_position[i] - 30, 260))  # chick name

    # draw hint at bottom
    screen.blit(font_small.render("← → to browse, then ENTER to play", True, WHITE), (220, 380))  # hint text


def draw_gameover():


def draw_bar(surface, fonts, x, y, value, max_value, color, label):
    BAR_WIDTH  = 150
    BAR_HEIGHT = 14

    pygame.draw.rect(screen, (80, 80, 80), (x, y, BAR_WIDTH, BAR_HEIGHT))
    fill_width = int(BAR_WIDTH * value/max_value)
    label_surf = fonts["small"].render(label, True, WHITE)
    surface.blit(label_surf, (x, y -20))
    if fill_width > 0:
        pygame.draw.rect(surface, color, (x, y, fill_width, BAR_HEIGHT))
    pygame.draw.rect(surface, (255, 255, 255), (x, y, BAR_WIDTH, BAR_HEIGHT), 1)

def draw_hud(screen, fonts, health, hunger, energy, time_left, eggs, eggs_needed):
    pygame.draw.rect(screen, (40,40,40),(0, 0, W, 50))
    draw_bar(screen, fonts,20, 25, health,100, GRASS,'HEALTH')
    draw_bar(screen, fonts, 200,25, hunger, 100, ORANGE,'HUNGER')
    draw_bar(screen, fonts, 380,25,energy,100, YELLOW,'ENERGY')
#timer
    col = RED if time_left < 20 else WHITE
    screen.blit(fonts["small"].render(f"Time: {int(time_left)}s", True, col), (W - 120, 8))
#eggs
    screen.blit(fonts["small"].render(f"Eggs:{eggs}/{eggs_needed}", True, WHITE), (W-120, 28))

def draw_game():


# person 3 – player movement + stats
def make_player():
    # creates a new player dictionary with all starting values
    player = {
        # position
        "x": 60.0,  # starting position from left
        "y": 500.0,  # starting position from top
        "previous_x": 60.0,  # saves last position before moving
        "previous_y": 500.0,  # saves last position before moving

        # movement
        "speed": 180.0,  # how fast the chicken moves in pixels per second
        "facing_left": True,  # is the chicken facing left?
        "moving": False,  # is the chicken moving right now?

        # HUD stats
        "health": 100.0,  # starts at 100, game over when 0
        "hunger": 100.0,  # starts at 100, drains over time
        "energy": 100.0,  # starts at 100, drains when moving

        # egg
        "carrying_egg": False,  # is the chicken holding an egg?
        "egg_cooldown": 0.0,  # cooldown before chicken can lay again
        "eggs_delivered": 0,  # how many eggs delivered to nest so far

        # timer
        "hunger_timer": 0.0,  # counts up to 5 seconds then hunger drops
        "standing_timer": 0.0,  # counts how long chicken has been standing still

        # selected chick id
        "chick_id": Players[selected_chick]["id"],  # which chick image to use
    }

    return player

def move_player():
    #geeksforgeeks.org/python/python-moving-an-object-in-pygame
    keys = pygame.key.get_pressed()
    global player, dt
    # check which direction keys are pressed
    direction_x = 0   # left and right
    direction_y = 0   # up and down

    #for both arrow keys and WASD
    if keys[pygame.K_LEFT]  or keys[pygame.K_a]:
        direction_x = -1              # moving left
        player["facing_left"] = True  # face left(for the flip of the image)

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        direction_x = 1               # moving right
        player["facing_left"] = False # face right(for the flip of the image)

    if keys[pygame.K_UP]    or keys[pygame.K_w]:
        direction_y = -1              # moving up

    if keys[pygame.K_DOWN]  or keys[pygame.K_s]:
        direction_y = 1               # moving down

    #check if chicken is moving at all
    player["moving"] = direction_x != 0 or direction_y != 0

    #for diagnal
    #https://gamedev.stackexchange.com/questions/104437/diagonal-movement-with-pygame-rect-class
    #right + down = √(10² + 10²) = 14.1 total speed but we are doing right+down  = √(7.07² + 7.07²) = 10 which makes it equal
    if direction_x != 0 and direction_y != 0:
        direction_x = direction_x * 0.707
        direction_y = direction_y * 0.707

    # slow down when energy is low
    current_speed = player["speed"]

    if player["energy"] < 20:
        current_speed = current_speed * 0.45   # very slow
    elif player["energy"] < 50:
        current_speed = current_speed * 0.70   # a bit slow

    # position BEFORE moving
    #need it so check_fence() can push chicken back if it hits a fence
    player["previous_x"] = player["x"]
    player["previous_y"] = player["y"]

    #actually moves the chicken
    #new position = old position + directionxspeedxtime
    #multiplying by dt makes movement the same speed on every computer
    #eg 60(normal speed set in game)+ 1(presed 1 right) * 180(chick speed) * dt
    player["x"] = player["x"] + direction_x * current_speed * dt
    player["y"] = player["y"] + direction_y * current_speed * dt

    #stops the chicken from walking off screen
    if player["x"] < 0:
        player["x"] = 0    #stop at left edge
    if player["x"] > W - 60:
        player["x"] = W - 60    #stop at right edge
    if player["y"] < 60:
        player["y"] = 60    #stop at top edge (btw 60 is the HUD height)
    if player["y"] > H - 60:
        player["y"] = H - 60    #stop at bottom edge

def drain_stats():


def try_lay_eggs():


def carry_to_nest():


# person 4 – items + collisions
def spawn_corn():


def disappear_corn():


def check_water():  # if the player is touching the water


def check_fence():  # if the player is touching the fence


def check_nest():  # if the player is touching the nest


def move_fox()  # chases the chicken


def check_fox()  # if fox touches the chicken = take damage


def move_farmer()  # patrols left and right


def check_farmer()  # if farmer touches the chicken = take damage or die


def make_bomb():
    # creates a bomb at a random position on the map
    #randir is a powerful tool for generating random integers between two specified values
    bomb = {
        "x":     random.randint(100, W - 100),  # random position from left
        "y":     random.randint(100, H - 100),  # random position from top
        "alive": True,  # True = still on map, False = exploded
    }
    return bomb

def check_bomb():
    global player, bombs

    # loops through every bomb on the map
    for bomb in bombs:
        # only check bombs that are still alive
        if bomb["alive"] == True:
            # create a rectangle around the chicken
            chicken_rectangle = pygame.Rect(player["x"], player["y"], 60, 60)
            # create a rectangle around the bomb
            bomb_rectangle = pygame.Rect(bomb["x"], bomb["y"], 20, 20)
            # check if chicken rectangle and bomb rectangle are touching
            if chicken_rectangle.colliderect(bomb_rectangle):
                # bomb explodes and remove it from map
                bomb["alive"] = False
                # chicken loses 30 health
                player["health"] = player["health"] - 30
                # make sure health never goes below 0
                if player["health"] < 0:
                    player["health"] = 0
                # show popup message
                pop_up_message("BOOM! -30 health!")

# person 5 – main game loop + screens
def pop_up_message():


def start_game():
