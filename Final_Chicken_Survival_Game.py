import pygame
import sys
import random

pygame.init()

#possible Screen size, it will be measured in pixel by pixel size
W = 800
H = 600
FPS = 60

#called to open the game window
screen = pygame.display.set_mode((W, H))
#sets the title bar text, so when run, it will the title beside the cross button
pygame.display.set_caption("Chicken Survival Game")
#controls the FPS to avoid lagging
clock = pygame.time.Clock()

#this will be the basic stats needed
#planning
player_speed = 180
player_health = 100
player_hunger = 100
player_energy = 100
egg_cooldown = 7

#items that we need more than one
#each level will have different amount of the items below so it will be a list
bombs  = []
waters = []
fences = []
corns = []

#popup message will be string
popup_msg = ""
#popup is temporary, we need this to control how long it will stay on the screen for
popup_timer = 0.0

#stores the starting game's stats, they will be updated depending on each levels.
state = "title"
player = None
dt = 0.0
selected_chick = 0
level_timer = 0.0
level_count = 0
fox = None
farmer = None
mother_hawk = None
child_hawks = []
corn_spawn_timer = 0
corn_spawn_delay = random.randint(2000, 5000)

White = (255, 255, 255)
Black = (0, 0, 0)
Red = (220, 50, 50)
Yellow = (245, 230, 50)
Orange = (230, 130, 40)
Green = (80, 180, 80)
Dark_green = (40, 120, 40)
Sky = (135, 206, 235)
Grass = (126, 200, 80)
Brown = (160, 100, 50)
Gray = (150, 150, 150)
Gray_2 = (80, 80, 80)
Dark_Gray = (50, 50, 50)
Pink = (225, 127, 162)

#to easily access the data for all the chickens
#as we want the game to allow the player to select their chick
Players = [
    {"id": "mahi",   "name": "Mahi Chick",   "image": "mahi.png"},
    {"id": "hilly",  "name": "Hilly Chick",  "image": "hilly.png"},
    {"id": "august", "name": "August Chick", "image": "august.png"},
    {"id": "leo",    "name": "Leo Chick",    "image": "leo.png"},
    {"id": "raj",    "name": "Raj Chick",    "image": "raj.png"},
]

#for now - 5 levels, we can change the timer and other counts too
#dictionaries for levels
#each dictionary is 1 level
#this allows us to manage the difficulty of the game in each level and what we want
Levels = [
    {
        #easy 1
        "level": 1,
        "eggs_needed": 1,
        "time_limit": 120,
        "has_fox": False,
        "has_farmer": False,
        "bomb_count": 3,
        "fence_count": 3,
        "water_count": 2,
        "corn_max": 4,
        "bg_color": Grass,
    },
    {
        #easy 2
        "level": 2,
        "eggs_needed": 2,
        "time_limit": 120,
        "has_fox": False,
        "has_farmer": False,
        "bomb_count": 10,
        "fence_count": 3,
        "water_count": 5,
        "corn_max": 3,
        "bg_color": Grass,
    },
    {
        #slightly hard
        "level": 3,
        "eggs_needed": 3,
        "time_limit": 100,
        "has_fox": True,
        "has_farmer": False,
        "bomb_count": 12,
        "fence_count": 4,
        "water_count": 5,
        "corn_max": 3,
        "bg_color": Grass,
    },
    {
        #hard
        "level": 4,
        "eggs_needed": 4,
        "time_limit": 80,
        "has_fox": False,
        "has_farmer": True,
        "bomb_count": 12,
        "fence_count": 4,
        "water_count": 5,
        "corn_max": 2,
        "bg_color": Grass,
    },
    {
        #super hard
        "level": 5,
        "eggs_needed": 5,
        "time_limit": 60,
        "has_fox": True,
        "has_farmer": True,
        "bomb_count": 15,
        "fence_count": 4,
        "water_count": 5,
        "corn_max": 1,
        "bg_color": Grass,
        "final_boss": False,
    },
    {
        #boss level
        "level": 6,
        "eggs_needed": 0,
        "time_limit": 75,
        "has_fox": False,
        "has_farmer": False,
        "bomb_count": 10,
        "fence_count": 2,
        "water_count": 2,
        "corn_max": 4,
        "bg_color": Sky,
        "final_boss": True,
    },
]

#loads all the images that we will be using in the game
#reference https://www.geeksforgeeks.org/python/python-display-images-with-pygame/
def load_image(filename, w, h):
    image = pygame.image.load("Images/" + filename).convert_alpha()
    return pygame.transform.scale(image, (w, h))

#instead of loading images everytime, this will easily helps us acces the imges
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
    "cloud": load_image("cloud.png", 90, 63),
    "fence":  load_image("fence.png",   90, 63),
    "bomb":   load_image("bomb.png",    20, 20),
    "fox":    load_image("fox.png",     60, 70),
    "mother_hawk": load_image("hawk.png", 120, 130),
    "hawk":   load_image("childhawk.png", 65, 75),
    "farmer": load_image("farmer.png",  60, 80),
}

#font sizes
#use basic font Arial
font_big    = pygame.font.SysFont("Arial", 48, bold=True)
font_medium = pygame.font.SysFont("Arial", 22, bold=True)
font_small  = pygame.font.SysFont("Arial", 16)

#for screen.blit - https://www.geeksforgeeks.org/python/pygame-surface-blit-function/
#https://gjenkinsedu.com/post/pygame_surface_blit_0005/
#displays title
def draw_title():
    screen.fill(Sky)
    screen.blit(font_big.render("Chicken Survival Game", True, White), (140, 200))
    screen.blit(font_medium.render("Press ENTER to start", True, White), (270, 320))

#This function pulls Player info that stores in dictionary and displays them at the specific position on the screen
#draws hint instruction on the screen
def draw_select():
    screen.fill(Sky)
    screen.blit(font_big.render("CHOOSE YOUR CHICK", True, White), (125, 60))

    chicks_position = [80, 210, 340, 470, 600]

    for i, chick in enumerate(Players):
        if i == selected_chick:
            pygame.draw.rect(screen, White, (chicks_position[i] - 40, 150, 80, 80), 3)
        screen.blit(images[chick["id"]], (chicks_position[i] - 30, 160))
        screen.blit(font_small.render(chick["name"], True, White), (chicks_position[i] - 30, 260))

    screen.blit(font_small.render("use ← → to browse then Enter To Play", True, White), (220, 380))


def is_final_boss_level():
    return Levels[level_count].get("final_boss", False)

#It displays another state of the game after selecting the chicks.
#It fills the background and draws environmental objects such as water, fences, and bombs on the screen.
def draw_game():
    screen.fill(Levels[level_count]["bg_color"])

    #draw water
    for water in waters:
        screen.blit(images["water"], (int(water["x"]), int(water["y"])))

    #draw fences
    for fence in fences:
        fence_image = images["cloud"] if is_final_boss_level() else images["fence"]
        screen.blit(fence_image, (int(fence["x"]), int(fence["y"])))

    #draws corn
    for corn in corns:
        screen.blit(images["corn"], (int(corn["x"]), int(corn["y"])))

    #draw nest
    if not is_final_boss_level():
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

    if is_final_boss_level() and mother_hawk is not None:
        hawk_image = images["mother_hawk"]
        if mother_hawk["direction"] < 0:
            hawk_image = pygame.transform.flip(hawk_image, True, False)
        screen.blit(hawk_image, (int(mother_hawk["x"]), int(mother_hawk["y"])))

        for child_hawk in child_hawks:
            child_image = images["hawk"]
            if child_hawk["x"] < player["x"]:
                child_image = pygame.transform.flip(child_image, True, False)
            screen.blit(child_image, (int(child_hawk["x"]), int(child_hawk["y"])))

    #draw chicken
    img = images[player["chick_id"]]
    if not player["facing_left"]:
        img = pygame.transform.flip(img, True, False)
    screen.blit(img, (int(player["x"]), int(player["y"])))

    #draw egg on chicken if carrying
    if player["carrying_egg"] and not is_final_boss_level():
        screen.blit(images["egg"], (int(player["x"]) + 40, int(player["y"]) - 10))

    if popup_timer > 0 and popup_msg:
        txt = font_medium.render(popup_msg, True, White)
        bg  = pygame.Surface((txt.get_width() + 20, 36), pygame.SRCALPHA)
        bg.fill((0, 0, 0, 180))
        screen.blit(bg,  (W // 2 - bg.get_width()  // 2, H // 2 - 18))
        screen.blit(txt, (W // 2 - txt.get_width() // 2, H // 2 - 10))

    draw_hud()

#reference - https://www.youtube.com/watch?v=E82_hdoe06M, https://www.youtube.com/watch?v=pUEZbUAMZYA
#displays HUD, the area where it shows health, hunger, energy bar stats and timer.
#This function will be called in main game loop to display them in every frames
def draw_hud():
    if is_final_boss_level():
        def draw_stat_bar(x, label, value, fill_color):
            panel_rect = pygame.Rect(x, 10, 250, 44)
            bar_rect = pygame.Rect(x + 12, 26, 226, 10)
            fill_width = int(bar_rect.width * max(0, min(value, 100)) / 100)

            pygame.draw.rect(screen, Dark_Gray, panel_rect, border_radius=10)
            pygame.draw.rect(screen, White, panel_rect, 2, border_radius=10)
            screen.blit(font_small.render(label, True, White), (x + 12, 10))
            screen.blit(font_small.render(f"{int(value)}/100", True, White), (x + 182, 10))
            pygame.draw.rect(screen, Black, bar_rect, border_radius=5)
            pygame.draw.rect(screen, fill_color, (bar_rect.x, bar_rect.y, fill_width, bar_rect.height), border_radius=5)
            pygame.draw.rect(screen, White, bar_rect, 2, border_radius=5)

        draw_stat_bar(10, "Health", player["health"], Red)
        draw_stat_bar(275, "Energy", player["energy"], Gray)
        draw_stat_bar(540, "Hawk Life", mother_hawk["lifeline"] if mother_hawk is not None else 0, Red)
        return

    pygame.draw.rect(screen, Dark_Gray, (0, 0, W, 50))

    pygame.draw.rect(screen, Gray_2, (10, 8, 160, 16))
    pygame.draw.rect(screen, Green,(10, 8, int(160 * player["health"] / 100), 16))
    screen.blit(font_small.render(f"HP{int(player['health'])}", True, White), (10, 28))

    pygame.draw.rect(screen, Gray_2, (210, 8, 160, 16))
    pygame.draw.rect(screen, Orange,(210, 8, int(160 * player["hunger"] / 100), 16))
    screen.blit(font_small.render(f"Hunger{int(player['hunger'])}", True, White),(210, 28))

    pygame.draw.rect(screen, Gray_2, (410, 8, 160, 16))
    pygame.draw.rect(screen, Yellow, (410, 8, int(160 * player["energy"] / 100), 16))
    screen.blit(font_small.render(f"Energy{int(player['energy'])}", True, White),(410, 28))

    pygame.draw.rect(screen, Gray_2, (610, 8, 160, 16))
    pygame.draw.rect(screen, Sky, (610, 8, int(160 * level_timer / Levels[level_count]["time_limit"]), 16))
    screen.blit(font_small.render(f"Time Left  {int(level_timer)}", True, White), (610, 28))


def draw_gameover():
    screen.fill(Grass)
    overlay = pygame.Surface((W, H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))
    screen.blit(font_big.render("GAME OVER", True, Red), (250, 200))
    screen.blit(font_medium.render("Press ENTER to retry or ESC for title", True, White), (170, 320))

def draw_won():
    screen.fill(Grass)
    overlay = pygame.Surface((W, H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))
    screen.blit(font_big.render("YOU WON", True, Sky), (275, 200))
    screen.blit(font_medium.render("Press ENTER for next level or ESC for title", True, White), (170, 320))

def draw_levelsdone():
    screen.fill(Grass)
    overlay = pygame.Surface((W, H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))
    screen.blit(font_big.render("Congrats! You WONNN:)", True, Sky), (120, 200))
    screen.blit(font_medium.render("Press ENTER to go back to title", True, White), (230, 320))

    #draws hud
    draw_hud()


def make_player():
    #what every player will have at the start
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
        "egg_timer": 0.0,
        "egg_cooldown": 0.0,
        "eggs_delivered": 0,
        "hunger_timer": 0.0,
        "standing_timer": 0.0,
        "chick_id": Players[selected_chick]["id"],
    }


def move_player():
    #geeksforgeeks.org/python/python-moving-an-object-in-pygame
    global player, dt
    keys = pygame.key.get_pressed()
    #to check which direction keys are pressed
    direction_x = 0
    direction_y = 0

    #for both arrow keys and WASD
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

    #check if chicken is moving at all or not
    player["moving"] = direction_x != 0 or direction_y != 0

    # for diagnal
    # https://gamedev.stackexchange.com/questions/104437/diagonal-movement-with-pygame-rect-class
    if direction_x != 0 and direction_y != 0:
        direction_x *= 0.707
        direction_y *= 0.707

    #slows down the chick when energy is low at like a specific energy levek
    current_speed = player["speed"]
    if player["energy"] < 20:
        current_speed *= 0.45
    elif player["energy"] < 50:
        current_speed *= 0.70

    #need it so check_fence() can push chicken back if it hits a fence
    player["previous_x"] = player["x"]
    player["previous_y"] = player["y"]

    #actually moves the chicken
    #new position = old position + directionxspeedxtime
    player["x"] += direction_x * current_speed * dt
    player["y"] += direction_y * current_speed * dt

    # stops the chicken from walking off screen
    if player["x"] < 0:
        player["x"] = 0
    if player["x"] > W - 60:
        player["x"] = W - 60
    if player["y"] < 60:
        player["y"] = 60
    if player["y"] > H - 60:
        player["y"] = H - 60

def drain_stats():
    #handles every stats
    global player, dt

    if is_final_boss_level():
        if player["moving"]:
            player["energy"] = max(0.0, player["energy"] - (1.5 / FPS))
        return

    if player["egg_cooldown"] > 0:
        player["egg_cooldown"] = max(0.0, player["egg_cooldown"] - dt)

    player["hunger_timer"] += dt
    if player["hunger_timer"] >= 5.0:
        player["hunger_timer"] -= 5.0
        player["hunger"] = max(0.0, player["hunger"] - 2.0)

    if player["hunger"] == 0:
        player["health"] = max(0.0, player["health"] - 2.0 * dt)

    if player["moving"]:#when the player is moving it should decrease the energy, just like how realistically when we walk we get tired
        player["energy"] = max(0.0, player["energy"] - (1.5 / FPS))

    player["egg_timer"] += dt
    if player["egg_timer"] >= 10.0:
        player["egg_timer"] = 0.0
        try_lay_eggs()


def make_corn():
    return {
        "x": random.randint(100, W - 100),
        "y": random.randint(100, H - 100),
        "alive": True,
        "hunger": 10,
        "timer": 420
    }

def make_water():
    return {
        "x": random.randint(100, W - 150),
        "y": random.randint(100, H - 100),
        "w": 80,
        "h": 52,
    }

def make_fence():
    return {
        "x": random.randint(100, W - 200),
        "y": random.randint(100, H - 150),
        "w": 90,
        "h": 63,
    }

def make_fox() -> dict:
    return {
        "x":            100.0,
        "y":            100.0,
        "speed":        90.0,
        "hit_cooldown": 0.0,
    }

def make_farmer() -> dict:
    return {
        "x":            600.0,
        "y":            200.0,
        "speed":        5.0,
        "direction":    1,
        "hit_cooldown": 0.0,
    }

def make_mother_hawk() -> dict:
    return {
        "x": float(W - 120),
        "y": 62.0,
        "speed": 145.0,
        "direction": -1,
        "lifeline": 100.0,
        "life_timer": 0.0,
        "wave_ready": True,
        "wave_index": 0,
        "phase_two": False,
        "corner_spawn_timer": 0.0,
    }

def make_child_hawk(spawn_x, spawn_y) -> dict:
    return {
        "x": spawn_x,
        "y": spawn_y,
        "speed": 95.0,
        "age": 0.0,
    }

def make_bomb():
    return {
        "x":     random.randint(100, W - 100),
        "y":     random.randint(100, H - 100),
        "alive": True,
        "damage": 30
    }

def check_water():
    global player, dt, waters
    for water in waters:
        chicken_rect = pygame.Rect(player["x"], player["y"], 60, 60)
        water_rect   = pygame.Rect(water["x"],  water["y"],  water["w"], water["h"])
        if chicken_rect.colliderect(water_rect):
            player["energy"] = min(100.0, player["energy"] + 20.0 * dt)#gain 20+ energy

def check_fence():
    global player, fences
    chicken_rect = pygame.Rect(player["x"], player["y"], 60, 60)
    for fence in fences:
        fence_rect = pygame.Rect(fence["x"], fence["y"], fence["w"], fence["h"])
        if chicken_rect.colliderect(fence_rect):
            player["x"] = player["previous_x"]
            player["y"] = player["previous_y"]

def check_nest():
    global player
    if is_final_boss_level():
        return
    nest_rect = pygame.Rect(700, 60, 90, 44)
    chicken_rect = pygame.Rect(player["x"], player["y"], 60, 60)
    if chicken_rect.colliderect(nest_rect):
        if player["carrying_egg"]:
            player["carrying_egg"] = False
            player["eggs_delivered"] += 1
            pop_up_message(f"Egg has been delivered! {player['eggs_delivered']}/{Levels[level_count]['eggs_needed']}")
        else:
            try_lay_eggs()

def check_farmer():
    global player, farmer
    chicken_rect = pygame.Rect(player["x"], player["y"], 60, 60)
    farmer_rect = pygame.Rect(farmer["x"], farmer["y"], 60, 80)

    if chicken_rect.colliderect(farmer_rect):
        if farmer["hit_cooldown"] <= 0:
            player["health"] -= 35
            if player["health"] < 0:
                player["health"] = 0
            farmer["hit_cooldown"] = 1.5
            pop_up_message("The farmer has caught you! -35 health!")

def spawn_child_hawk(offset_x, offset_y):
    global child_hawks, mother_hawk

    child_hawks.append(make_child_hawk(mother_hawk["x"] + offset_x, mother_hawk["y"] + offset_y))


def spawn_corner_hawks():
    global child_hawks

    child_hawks.extend([
        make_child_hawk(0.0, 60.0),
        make_child_hawk(float(W - 65), 60.0),
        make_child_hawk(0.0, float(H - 75)),
        make_child_hawk(float(W - 65), float(H - 75)),
    ])


def move_mother_hawk():
    global mother_hawk, dt
    if mother_hawk is None:
        return

    if mother_hawk["phase_two"]:
        # Phase two switches from lane movement to direct pursuit.
        distance_x = player["x"] - mother_hawk["x"]
        distance_y = player["y"] - mother_hawk["y"]
        distance = max(1.0, (distance_x ** 2 + distance_y ** 2) ** 0.5)
        chase_speed = mother_hawk["speed"] * 0.65
        mother_hawk["direction"] = -1 if distance_x < 0 else 1
        mother_hawk["x"] += (distance_x / distance) * chase_speed * dt
        mother_hawk["y"] += (distance_y / distance) * chase_speed * dt
        mother_hawk["x"] = max(0, min(mother_hawk["x"], W - 120))
        mother_hawk["y"] = max(60, min(mother_hawk["y"], H - 130))
        return

    mother_hawk["x"] += mother_hawk["speed"] * mother_hawk["direction"] * dt
    if mother_hawk["x"] <= 0:
        mother_hawk["x"] = 0
        mother_hawk["direction"] = 1
    elif mother_hawk["x"] >= W - 120:
        mother_hawk["x"] = W - 120
        mother_hawk["direction"] = -1
        mother_hawk["wave_ready"] = True


def move_child_hawks():
    global child_hawks, player, dt

    remaining_hawks = []
    for child_hawk in child_hawks:
        distance_x = player["x"] - child_hawk["x"]
        distance_y = player["y"] - child_hawk["y"]
        distance = max(1.0, (distance_x ** 2 + distance_y ** 2) ** 0.5)
        child_hawk["x"] += (distance_x / distance) * child_hawk["speed"] * dt
        child_hawk["y"] += (distance_y / distance) * child_hawk["speed"] * dt
        child_hawk["age"] += dt

        if child_hawk["age"] < 20.0:
            remaining_hawks.append(child_hawk)

    child_hawks = remaining_hawks


def check_mother_hawk():
    global player, mother_hawk
    if mother_hawk is None:
        return

    chicken_rect = pygame.Rect(player["x"] + 10, player["y"] + 10, 40, 40)
    hawk_rect = pygame.Rect(mother_hawk["x"] + 18, mother_hawk["y"] + 18, 78, 84)
    if chicken_rect.colliderect(hawk_rect):
        player["health"] = 0
        pop_up_message("The mother hawk caught you!")


def check_child_hawks():
    global player
    chicken_rect = pygame.Rect(player["x"] + 10, player["y"] + 10, 40, 40)

    for child_hawk in child_hawks:
        hawk_rect = pygame.Rect(child_hawk["x"] + 15, child_hawk["y"] + 15, 45, 50)
        if chicken_rect.colliderect(hawk_rect):
            player["health"] = max(0.0, player["health"] - 35.0 * dt)
            pop_up_message("A child hawk is attacking!")


def update_mother_hawk():
    global mother_hawk, dt
    if mother_hawk is None:
        return

    mother_hawk["life_timer"] += dt
    while mother_hawk["life_timer"] >= 1.0:
        mother_hawk["life_timer"] -= 1.0
        mother_hawk["lifeline"] = max(0.0, mother_hawk["lifeline"] - (100.0 / 60.0))

    if mother_hawk["lifeline"] <= 30.0:
        mother_hawk["phase_two"] = True

    if mother_hawk["phase_two"]:
        # Once enraged, corner waves replace the lane-based spawn pattern.
        mother_hawk["corner_spawn_timer"] += dt
        while mother_hawk["corner_spawn_timer"] >= 10.0:
            mother_hawk["corner_spawn_timer"] -= 10.0
            spawn_corner_hawks()
        return

    if not mother_hawk["wave_ready"]:
        return

    travel_ratio = mother_hawk["x"] / float(W - 120)
    spawn_pattern = [
        ("right", lambda ratio: ratio >= 0.9, -5, 55),
        ("center", lambda ratio: 0.45 <= ratio <= 0.55, 10, 70),
        ("left", lambda ratio: ratio <= 0.08, 20, 55),
    ]

    _, condition, offset_x, offset_y = spawn_pattern[mother_hawk["wave_index"]]
    if condition(travel_ratio):
        spawn_child_hawk(offset_x, offset_y)
        mother_hawk["wave_index"] += 1

        if mother_hawk["wave_index"] >= len(spawn_pattern):
            mother_hawk["wave_index"] = 0
            mother_hawk["wave_ready"] = False

def make_fox_follow():
    global player, fox
    if fox is None:
        return
    distance_x = player["x"] - fox["x"]
    distance_y = player["y"] - fox["y"]
    distance = max(1, (distance_x**2 + distance_y**2) ** 0.5)

    speed = 2
    fox["x"] += speed * distance_x / distance
    fox["y"] += speed * distance_y / distance
    chicken_rect = pygame.Rect(player["x"], player["y"], 60, 60)
    fox_rect = pygame.Rect(fox["x"], fox["y"], 60, 70)
    if chicken_rect.colliderect(fox_rect):
        player["health"] -= 20 * dt
        pop_up_message("The fox has caught you! your health is decreasing!")


def move_farmer() -> None:
    global farmer, dt
    if farmer is None:
        return
    farmer["x"] += farmer["speed"] * farmer["direction"]
    if farmer["x"] <= 0 or farmer["x"] >= W - 60:
        farmer["direction"] *= -1
    if farmer["hit_cooldown"] > 0:
        farmer["hit_cooldown"] = max(0.0, farmer["hit_cooldown"] - dt)

def take_bomb_damage():
    global player, bombs
    for bomb in bombs:
        if bomb["alive"]:
            chicken_rect = pygame.Rect(player["x"], player["y"], 60, 60)
            bomb_rect    = pygame.Rect(bomb["x"],   bomb["y"],   20, 20)
            if chicken_rect.colliderect(bomb_rect):
                bomb["alive"] = False
                player["health"] -= 30
                pop_up_message("BOOM! -30 health!")

def spawn_corn():
    global player, corns
    if random.randint(1, 900) == 1:
        corns.append(make_corn())

    for corn in corns:
        corn["timer"] -= 1

        if corn["timer"] <= 0:
            corns.remove(corn)
            continue

        if corn["alive"]:
            chicken_rect = pygame.Rect(player["x"], player["y"], 60, 60)
            corn_rect    = pygame.Rect(corn["x"],   corn["y"],   35, 50)
            if chicken_rect.colliderect(corn_rect):
                corn["alive"] = False
                if is_final_boss_level():
                    if player["health"] < 100:
                        player["health"] = min(100, player["health"] + 10)
                        pop_up_message("Corn collected! +10 health")
                    else:
                        pop_up_message("Health is full already!")
                elif player["hunger"] < 100:
                    player["hunger"] = min(100, player["hunger"] + corn["hunger"])
                    corn["alive"] = False
                else:
                    pop_up_message("Hunger is full already!")
        if not corn["alive"]:
            corns.remove(corn)

def try_lay_eggs():
    global player
    if is_final_boss_level():
        return
    if player["carrying_egg"]:
        pop_up_message("Already carrying an egg!")
        return
    if player["egg_cooldown"] > 0:
        pop_up_message(f"Cooldown: {int(player['egg_cooldown'])}s")
        return
    if player["hunger"] < 50:
        pop_up_message("Need 50+ hunger to lay!")
        return
    if (player["energy"] < 70):
        pop_up_message("Need 70+ energy to lay!")
        return
    player["carrying_egg"] = True
    player["hunger"] = max(0.0, player["hunger"] - 15.0)
    player["energy"] = max(0.0, player["energy"] - 20.0)
    player["egg_cooldown"] = float(egg_cooldown)

def pop_up_message(message):
    global popup_msg, popup_timer
    popup_msg   = message
    popup_timer = 2.0

def level_setup():
    #to prevent repeating this after every state = "play"
    global player, bombs, waters, fences, fox, farmer, mother_hawk, child_hawks, level_timer, corns
    player = make_player()
    bombs = [make_bomb() for i in range(Levels[level_count]["bomb_count"])]
    waters = [make_water() for i in range(Levels[level_count]["water_count"])]
    corns = [make_corn() for i in range(Levels[level_count]["corn_max"])]
    fences = [make_fence() for i in range(Levels[level_count]["fence_count"])]
    level_timer = float(Levels[level_count]["time_limit"])
    fox = make_fox() if Levels[level_count]["has_fox"] else None
    farmer = make_farmer() if Levels[level_count]["has_farmer"] else None
    mother_hawk = make_mother_hawk() if is_final_boss_level() else None
    child_hawks = []


def start_game():
    #title -> select chick -> levels[1-6]
    global state, player, dt, selected_chick, popup_timer, popup_msg, Levels, level_timer, level_count
    global bombs, waters, fences, fox, farmer, mother_hawk, child_hawks, corns
    level_count = 0

    while True:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if state == "title":
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        state = "select"
                elif state == "select":
                    if event.key == pygame.K_LEFT:
                        selected_chick = (selected_chick - 1) % len(Players)
                    if event.key == pygame.K_RIGHT:
                        selected_chick = (selected_chick + 1) % len(Players)
                    if event.key == pygame.K_RETURN:
                        level_timer = Levels[level_count]["time_limit"]
                        level_setup()
                        state  = "play"
                elif state == "won":
                    if event.key == pygame.K_RETURN:
                        level_setup()
                        state = "play"
                    if event.key == pygame.K_ESCAPE:
                        state = "title"
                elif state == "over":
                    if event.key == pygame.K_RETURN:
                        level_setup()
                        state  = "play"
                    if event.key == pygame.K_ESCAPE:
                        state = "title"
                elif state == "levels_done":
                    if event.key == pygame.K_RETURN:
                        state = "title"

        if state == "play":
            # The boss level reuses the main loop but swaps in hawk-specific updates.
            if not is_final_boss_level():
                check_nest()
            move_player()
            drain_stats()
            check_fence()
            check_water()
            take_bomb_damage()
            spawn_corn()

            if farmer is not None:
                move_farmer()
                check_farmer()
            if fox is not None:
                make_fox_follow()
            if mother_hawk is not None:
                move_mother_hawk()
                move_child_hawks()
                check_mother_hawk()
                check_child_hawks()
                update_mother_hawk()

            if popup_timer > 0:
                popup_timer -= dt
            if level_timer >0:
                level_timer -= dt

            if is_final_boss_level():
                if mother_hawk is not None and mother_hawk["lifeline"] <= 0:
                    state = "levels_done"
                    level_count = 0
                elif player["health"] <= 0 or level_timer <= 0:
                    state = "over"
            elif player["eggs_delivered"] == Levels[level_count]["eggs_needed"]:
                level_count += 1
                if level_count >= len(Levels):
                    state = "levels_done"
                    level_count = 0
                else:
                    state = "won"
            elif player["health"] <= 0 or level_timer <= 0:
                state = "over"

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

        pygame.display.flip()


if __name__ == "__main__":
    start_game()
