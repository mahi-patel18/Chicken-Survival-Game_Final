import pygame
import sys
import os
import random

#person 1 – setup + constants (dictionaries etc)
#Screen size
W = 800 # game width in pixels
H = 600 # game height in pixels
FPS = 60 # frames per second

PLAYER_SPEED  = 180  #Pxels per second — same for all chicks
PLAYER_HEALTH = 100  #Starting health
PLAYER_HUNGER = 100  #Starting hunger
PLAYER_ENERGY = 100  #Starting energy
EGG_COOLDOWN  = 7    #Seconds between laying eggs

#Colors for future use
WHITE      = (255, 255, 255)
BLACK      = (0,   0,   0)
RED        = (220,  50,  50)    #Health bar
YELLOW     = (245, 230,  50)    #Energy warning
ORANGE     = (230, 130,  40)    #Hunger warning
GREEN      = (80,  180,  80)
DARK_GREEN = (40,  120,  40)
SKY        = (135, 206, 235)
GRASS      = (126, 200,  80)
BROWN      = (160, 100,  50)
GRAY       = (150, 150, 150)
DARK_GRAY  = (50,   50,  50)  #Stats background
PINK = (225, 127, 162)

#Data for Chicken
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

#Data for each level
Levels = [
    {
    #Level 1: Easy(Example btw)
        "level":       1,
        "eggs_needed": 1,
        "time_limit":  150,     #Seconds
        "has_fox":     False,
        "has_farmer":  False,
        "has_bomb":    False,
        "corn_max":    5,
        "bg_color":    GRASS,   #Background color for this level
    },
# copy this block for each level
]

# load images
def load_image(filename, w, h):
    image = pygame.image.load("Images/" + filename).convert_alpha()
    return pygame.transform.scale(image, (w, h))

images = {
    "mahi":   load_image("mahi.png",   60, 60),
    "hilly":  load_image("hilly.png",  60, 60),
    "august": load_image("august.png", 60, 60),
    "leo":    load_image("leo.png",    60, 60),
    "raj":    load_image("raj.png",    60, 60),
    "corn":   load_image("corn.png",   35, 50),
    "egg":    load_image("egg.png",    30, 30),
    "nest":   load_image("nest.png",   90, 44),
    "water":  load_image("water.png",  80, 52),
    "fence":  load_image("fence.png",  90, 63),
}

screen = pygame.display.set_mode((W, H))        # opens the game window
pygame.display.set_caption("Chicken Survival Game")       # sets the title bar text
clock  = pygame.time.Clock()                     # controls the FPS

font_big = pygame.font.SysFont("Arial", 48, bold=True)  # big font for titles
font_medium = pygame.font.SysFont("Arial", 22, bold=True)  # medium font for HUD
font_small = pygame.font.SysFont("Arial", 16)             # small font for labels
#person 2 – drawing functions
#title screen
def draw_title():
    screen.fill(SKY)                                                         # paints background blue
    screen.blit(font_big.render("CHICKEN GAME",       True, WHITE), (200, 200))  # draws title
    screen.blit(font_medium.render("Press ENTER to start", True, WHITE), (250, 320)) # draws hint
    
selected_chick = 0

def draw_select():
    screen.fill(SKY)                                                                    # blue background

    # title
    screen.blit(font_big.render("CHOOSE YOUR CHICK", True, WHITE), (200, 60))            # title text

    # chick positions on screen
    chicks_position = [80, 210, 340, 470, 600]

    # draw each chick one by one
    for i, chick in enumerate(Players):

        # draw white box around the selected chick
        if i == selected_chick:
            pygame.draw.rect(screen, WHITE, (chicks_position[i]-40, 150, 80, 80), 3)                 # white border

        # draw chick image
        screen.blit(images[chick["id"]], (chicks_position[i]-30, 160))                                 # chick picture

        # draw chick name
        screen.blit(font_small.render(chick["name"], True, WHITE), (chicks_position[i]-30, 260))        # chick name

    # draw hint at bottom
    screen.blit(font_small.render("← → to browse, then ENTER to play", True, WHITE), (220, 380)) # hint text

def draw_gameover(): 
    
def draw_hud(): 
    
def draw_game():
#person 3 – player movement + stats
def make_player():

def move_player():

def drain_stats():

def try_lay_eggs():

def carry_to_nest():
#person 4 – items + collisions
def spawn_corn():

def disappear_corn():

def check_water():  #if the player is touching the water

def check_fence(): #if the player is touching the fence

def check_nest(): #if the player is touching the nest
#person 5 – main game loop + screens
def pop_up_message():

def start_game():
