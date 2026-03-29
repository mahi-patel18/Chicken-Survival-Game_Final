import pygame
import sys
import random

pygame.init()

#setup + constants (dictionaries etc)
#Screen size
W = 800  #game width in pixels
H = 600  #game height in pixels
FPS = 60  #frames per second

screen = pygame.display.set_mode((W, H))  #opens the game window
pygame.display.set_caption("Chicken Survival Game")  #sets the title bar text
clock = pygame.time.Clock()  #controls the FPS

PLAYER_SPEED  = 180
PLAYER_HEALTH = 100
PLAYER_HUNGER = 100
PLAYER_ENERGY = 100
EGG_COOLDOWN  = 7

bombs  = []
waters = []
fences = []

popup_msg   = ""
popup_timer = 0.0

state          = "title"
player         = None
dt             = 0.0
selected_chick = 0
level_timer    = 0.0
level_count    = 0
fox            = None
farmer         = None

#Colors for future use
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)  #Health bar
YELLOW = (245, 230, 50)  #Energy warning
ORANGE = (230, 130, 40)  #Hunger warning
GREEN = (80, 180, 80)
DARK_GREEN = (40, 120, 40)
SKY = (135, 206, 235)
GRASS = (126, 200, 80)
BROWN = (160, 100, 50)
GRAY = (150, 150, 150)
DARK_GRAY = (50, 50, 50)  #Stats background
PINK = (225, 127, 162)

#Data for Chicken
Players = [
    {"id": "mahi",   "name": "Mahi Chick",   "image": "mahi.png"},
    {"id": "hilly",  "name": "Hilly Chick",  "image": "hilly.png"},
    {"id": "august", "name": "August Chick", "image": "august.png"},
    {"id": "leo",    "name": "Leo Chick",    "image": "leo.png"},
    {"id": "raj",    "name": "Raj Chick",    "image": "raj.png"},
]

#Data for each level
Levels = [
    {
        "level": 1,
        "eggs_needed": 1,
        "time_limit": 120,
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
        "time_limit": 120,
        "has_fox": False,
        "has_farmer": False,
        "bomb_count": 10,
        "fence_count": 3,
        "water_count": 5,
        "corn_max": 5,
        "bg_color": GRASS,
    },
    {
        "level": 3,
        "eggs_needed": 3,
        "time_limit": 100,
        "has_fox": True,
        "has_farmer": False,
        "bomb_count": 12,
        "fence_count": 4,
        "water_count": 5,
        "corn_max": 5,
        "bg_color": GRASS,
    },
    {
        "level": 4,
        "eggs_needed": 4,
        "time_limit": 80,
        "has_fox": False,
        "has_farmer": True,
        "bomb_count": 12,
        "fence_count": 4,
        "water_count": 5,
        "corn_max": 5,
        "bg_color": GRASS,
    },
    {
        "level": 5,
        "eggs_needed": 5,
        "time_limit": 60,
        "has_fox": True,
        "has_farmer": True,
        "bomb_count": 15,
        "fence_count": 4,
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


#drawing functions
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
    overlay = pygame.Surface((W, H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))
    screen.blit(font_big.render("GAME OVER", True, RED), (250, 200))
    screen.blit(font_medium.render("Press ENTER to retry  |  ESC for title", True, WHITE), (170, 320))

def draw_won():
    screen.fill(GRASS)
    overlay = pygame.Surface((W, H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))
    screen.blit(font_big.render("YOU WON", True, SKY), (275, 200))
    screen.blit(font_medium.render("Press ENTER for next level  |  ESC for title", True, WHITE), (170, 320))

def draw_levelsdone():
    screen.fill(GRASS)
    overlay = pygame.Surface((W, H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))
    screen.blit(font_big.render("All Levels Done!", True, SKY), (200, 200))
    screen.blit(font_medium.render("Press ENTER for title", True, WHITE), (275, 320))


def draw_hud():
    #background bar
    pygame.draw.rect(screen, DARK_GRAY, (0, 0, W, 50))

    #health bar
    pygame.draw.rect(screen, (80, 80, 80), (10, 8, 160, 16))
    pygame.draw.rect(screen, GREEN,          (10, 8, int(160 * player["health"] / 100), 16))
    screen.blit(font_small.render(f"HP  {int(player['health'])}", True, WHITE), (10, 28))

    #hunger bar
    pygame.draw.rect(screen, (80, 80, 80), (210, 8, 160, 16))
    pygame.draw.rect(screen, ORANGE,       (210, 8, int(160 * player["hunger"] / 100), 16))
    screen.blit(font_small.render(f"Hunger  {int(player['hunger'])}", True, WHITE), (210, 28))

    #energy bar
    pygame.draw.rect(screen, (80, 80, 80), (410, 8, 160, 16))
    pygame.draw.rect(screen, YELLOW,       (410, 8, int(160 * player["energy"] / 100), 16))
    screen.blit(font_small.render(f"Energy  {int(player['energy'])}", True, WHITE), (410, 28))

    #level timer
    pygame.draw.rect(screen, (80, 80, 80), (610, 8, 160, 16))
    time_ratio = max(0, level_timer / Levels[level_count]["time_limit"])
    pygame.draw.rect(screen, SKY, (610, 8, int(160 * time_ratio / 150), 16))
    screen.blit(font_small.render(f"Time Left  {int(level_timer)}", True, WHITE), (610, 28))


def draw_game():
    screen.fill(Levels[level_count]["bg_color"])

    #draw water
    for water in waters:
        screen.blit(images["water"], (int(water["x"]), int(water["y"])))

    #draw fences
    for fence in fences:
        screen.blit(images["fence"], (int(fence["x"]), int(fence["y"])))

    #draw nest
    screen.blit(images["nest"], (700, 60))

    #draw bombs
    for bomb in bombs:
        if bomb["alive"]:
            screen.blit(images["bomb"], (int(bomb["x"]), int(bomb["y"])))

    #draw fox if level has one
    if Levels[level_count]["has_fox"] and fox is not None:
        screen.blit(images["fox"], (int(fox["x"]), int(fox["y"])))

    #draw farmer if level has one
    if Levels[level_count]["has_farmer"] and farmer is not None:
        screen.blit(images["farmer"], (int(farmer["x"]), int(farmer["y"])))

    #draw chicken
    img = images[player["chick_id"]]
    if not player["facing_left"]:
        img = pygame.transform.flip(img, True, False)
    screen.blit(img, (int(player["x"]), int(player["y"])))

    #draw egg on chicken if carrying
    if player["carrying_egg"]:
        screen.blit(images["egg"], (int(player["x"]) + 40, int(player["y"]) - 10))

    #draws hud on top
    draw_hud()

    #draw popup
    if popup_timer > 0 and popup_msg:
        txt = font_medium.render(popup_msg, True, WHITE)
        bg  = pygame.Surface((txt.get_width() + 20, 36), pygame.SRCALPHA)
        bg.fill((0, 0, 0, 180))
        screen.blit(bg,  (W // 2 - bg.get_width()  // 2, H // 2 - 18))
        screen.blit(txt, (W // 2 - txt.get_width() // 2, H // 2 - 10))


#player movement + stats
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
        "egg_timer": 0.0, #for the start of the game to prevent laying eggs instantly
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
        player["energy"] = max(0.0, player["energy"] - (1.5 / FPS))

    player["egg_timer"] += dt
    if player["egg_timer"] >= 10.0:
        player["egg_timer"] = 0.0
        try_lay_eggs()


def try_lay_eggs():
    #Tries to lay an egg but you need hunger to be 50+ and energy to be 70+
    global player
    if player["carrying_egg"]:
        pop_up_message("Already carrying an egg!")
        return
    if player["egg_cooldown"] > 0:
        pop_up_message(f"Cooldown: {int(player['egg_cooldown'])}s")
        return
    if player["hunger"] < 50:
        pop_up_message("Need 50+ hunger to lay!")
        return
    if player["energy"] < 70:
        pop_up_message("Need 70+ energy to lay!")
        return
    player["carrying_egg"] = True
    player["hunger"] = max(0.0, player["hunger"] - 10.0)
    player["energy"] = max(0.0, player["energy"] - 15.0)
    player["egg_cooldown"] = float(EGG_COOLDOWN)
    pop_up_message("Egg laid! Bring it to the nest!")

#items + collisions
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
        water_rect   = pygame.Rect(water["x"],  water["y"],  water["w"], water["h"])
        if chicken_rect.colliderect(water_rect):
            player["energy"] = min(100.0, player["energy"] + 20.0 * dt)


def make_fence():
    return {
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


def check_nest():  #if the player is touching the nest
    global player
    nest_rect = pygame.Rect(700, 60, 90, 44)
    chicken_rect = pygame.Rect(player["x"], player["y"], 60, 60)
    if chicken_rect.colliderect(nest_rect):
        if player["carrying_egg"]:
            player["carrying_egg"] = False
            player["eggs_delivered"] += 1
            pop_up_message(f"Egg delivered! {player['eggs_delivered']}/{Levels[level_count]['eggs_needed']}")
        else:
            try_lay_eggs()

def make_fox() -> dict:
    return {
        "x":            100.0,
        "y":            100.0,
        "speed":        90.0,
        "hit_cooldown": 0.0,
    }

def move_fox() -> None:
    global fox, dt

    difference_x = player["x"] - fox["x"]
    difference_y = player["y"] - fox["y"]
    distance     = (difference_x**2 + difference_y**2) ** 0.5

    if distance > 0:
        fox["x"] = fox["x"] + (difference_x / distance) * fox["speed"] * dt
        fox["y"] = fox["y"] + (difference_y / distance) * fox["speed"] * dt

    #count down hit cooldown
    if fox["hit_cooldown"] > 0:
        fox["hit_cooldown"] = max(0.0, fox["hit_cooldown"] - dt)

def check_fox():
    global player, fox
    if fox is None:
        return
    #movement toward player
    distance_x = player["x"] - fox["x"]
    distance_y = player["y"] - fox["y"]

    distance = max(1, (distance_x**2 + distance_y**2) ** 0.5)

    speed = 2   #adjust speed here

    fox["x"] += speed * distance_x / distance
    fox["y"] += speed * distance_y / distance

    #collision
    chicken_rect = pygame.Rect(player["x"], player["y"], 60, 60)
    fox_rect = pygame.Rect(fox["x"], fox["y"], 60, 70)

    if chicken_rect.colliderect(fox_rect):
        player["health"] -= 20

def make_farmer() -> dict:
    return {
        "x":            600.0,
        "y":            200.0,
        "speed":        5.0,
        "direction":    1,
        "hit_cooldown": 0.0,
    }

def move_farmer() -> None:
    global farmer, dt
    if farmer is None:
        return

    #move left/right
    farmer["x"] += farmer["speed"] * farmer["direction"]

    #bounces at edges
    if farmer["x"] <= 0 or farmer["x"] >= W - 60:
        farmer["direction"] *= -1

    #count down hit cooldown
    if farmer["hit_cooldown"] > 0:
        farmer["hit_cooldown"] = max(0.0, farmer["hit_cooldown"] - dt)

def check_farmer():  #if farmer touches the chicken = damage
    global player, farmer
    chicken_rect = pygame.Rect(player["x"], player["y"], 60, 60)
    farmer_rect = pygame.Rect(farmer["x"], farmer["y"], 60, 80)

    if chicken_rect.colliderect(farmer_rect):
        if farmer["hit_cooldown"] <= 0:
            player["health"] -= 35
            if player["health"] < 0:
                player["health"] = 0
            farmer["hit_cooldown"] = 1.5 # seconds before farmer can hit again
            pop_up_message("The big bad farmer caught you! -35 health!")


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


#main game loop + screens
def pop_up_message(message):
    global popup_msg, popup_timer
    popup_msg   = message
    popup_timer = 2.0

def level_setup():
    #Sets up everything needed for each level
    global player, bombs, waters, fences, fox, farmer, level_timer
    player = make_player()
    bombs = [make_bomb() for _ in range(Levels[level_count]["bomb_count"])] #for _ in range - not interested in how many times it will loop
    waters = [make_water() for _ in range(Levels[level_count]["water_count"])]
    fences = [make_fence() for _ in range(Levels[level_count]["fence_count"])]
    level_timer = float(Levels[level_count]["time_limit"])
    fox = make_fox() if Levels[level_count]["has_fox"] else None
    farmer = make_farmer() if Levels[level_count]["has_farmer"] else None


def start_game():
    global state, player, dt, selected_chick, popup_timer, popup_msg, Levels, level_timer
    global bombs, waters, fences, fox, farmer
    level_count: int = 0

    while True:
        dt = clock.tick(FPS) / 1000.0

        #handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                #title screen, press enter to go to character select
                if state == "title":
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        state = "select"

                #character select, browse and confirm
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
                            fox = make_fox()
                        if Levels[level_count]["has_farmer"]:
                            farmer = make_farmer()
                        state  = "play"

                #game over, retry or go back to title
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

        #update
        if state == "play":
            check_nest()
            move_player()
            drain_stats()
            check_fence()
            check_water()
            check_bomb()

            #only if farmer is in the level
            if farmer is not None:
                move_farmer()
                check_farmer()

            #only if fox is in the level
            if fox is not None:
                check_fox()

            #count down popup
            if popup_timer > 0:
                popup_timer -= dt

            #level count down
            if level_timer >0:
                level_timer -= dt

            #check game won
            if player["eggs_delivered"] == Levels[level_count]["eggs_needed"]:
                state = "won"
                level_count += 1
                if level_count >= len(Levels)-1:
                    state = "levels_done"
                    level_count = 0


            #check game over
            elif player["health"] <= 0 or level_timer <= 0:
                state = "over"


        #draw
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

        #update display
        pygame.display.flip()


if __name__ == "__main__":
    start_game()
