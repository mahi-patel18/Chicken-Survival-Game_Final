
import pygame
import sys
import random

pygame.init()

#possible Screen size, it will be measured in pixel by pixel size
W = 800  #game width in pixels
H = 600  #game height in pixels
FPS = 60  #frames per second for real time movement

screen = pygame.display.set_mode((W, H))  #called to open the game window
pygame.display.set_caption("Chicken Survival Game") #sets the title bar text, so when run, it will the title beside the cross button
clock = pygame.time.Clock()  #controls the FPS to avoid lagging

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
popup_msg = "" #so we can store the possible messages for popup
popup_timer = 0.0 #popup is temporary, we need this to control how long it will stay on the screen for

#stores the starting game's stats, they will be updated depending on each levels.
state = "title"
player = None
dt = 0.0
selected_chick = 0
level_timer = 0.0
level_count = 0
fox = None
farmer = None
corn_spawn_timer = 0
corn_spawn_delay = random.randint(2000, 5000)  #2–5 seconds

#all colors we will possibly be using
White = (255, 255, 255)
Black = (0, 0, 0)
Red = (220, 50, 50)  #use this for Health bar
Yellow = (245, 230, 50)  #use this for Energy warning
Orange = (230, 130, 40)  #use this for Hunger warning
Green = (80, 180, 80)
Dark_green = (40, 120, 40)
Sky = (135, 206, 235) #this should be for the title screen
Grass = (126, 200, 80)
Brown = (160, 100, 50)
Gray = (150, 150, 150)
Gray_2 = (80, 80, 80)
Dark_Gray = (50, 50, 50)  #use this for HUD background
Pink = (225, 127, 162) #testing

#to easily access the data for all the chickens
#as we want the game to allow the player to select their chick
#player should be list
#each player should have a unique id, the name it will display when we show the display page
#the image is there so we can easily load the imahes
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
        "corn_max": 2,
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
    }
]

#loads all the images that we will be using in the game
#reference https://www.geeksforgeeks.org/python/python-display-images-with-pygame/
def load_image(filename, w, h):
    image = pygame.image.load("Images/" + filename).convert_alpha()
    return pygame.transform.scale(image, (w, h))

#instead of loading images everytime, this will easily helps us acces the imges
images = {
    #players
    "mahi":   load_image("mahi.png",    60, 60),
    "hilly":  load_image("hilly.png",   60, 60),
    "august": load_image("august.png",  60, 60),
    "leo":    load_image("leo.png",     60, 60),
    "raj":    load_image("raj.png",     60, 60),

    #items and obstacles
    "corn":   load_image("corn.png",    35, 50),
    "egg":    load_image("egg.png",     30, 30),
    "nest":   load_image("nest.png",    90, 44),
    "water":  load_image("water.png",   80, 52),
    "fence":  load_image("fence.png",   90, 63),
    "bomb":   load_image("bomb.png",    20, 20), #slightly small but will be easy to add multiple of them
    "fox":    load_image("fox.png",     60, 70),
    "farmer": load_image("farmer.png",  60, 80),
}

#font sizes
#use basic font Arial
font_big    = pygame.font.SysFont("Arial", 48, bold=True)
font_medium = pygame.font.SysFont("Arial", 22, bold=True)
font_small  = pygame.font.SysFont("Arial", 16)

#for screen.blit - https://www.geeksforgeeks.org/python/pygame-surface-blit-function/
#https://gjenkinsedu.com/post/pygame_surface_blit_0005/
def draw_title():
    screen.fill(Sky)
    screen.blit(font_big.render("Chicken Survival Game", True, White), (140, 200))
    screen.blit(font_medium.render("Press ENTER to start", True, White), (270, 320))

def draw_select():
    screen.fill(Sky)
    screen.blit(font_big.render("CHOOSE YOUR CHICK", True, White), (125, 60))

    chicks_position = [80, 210, 340, 470, 600]

    for i, chick in enumerate(Players):
        #goes through every players
        if i == selected_chick:
            pygame.draw.rect(screen, White, (chicks_position[i] - 40, 150, 80, 80), 3)
        screen.blit(images[chick["id"]], (chicks_position[i] - 30, 160))
        screen.blit(font_small.render(chick["name"], True, White), (chicks_position[i] - 30, 260))

    screen.blit(font_small.render("use ← → to browse then Enter To Play", True, White), (220, 380))

def draw_gameover():
    screen.fill(Grass)
    overlay = pygame.Surface((W, H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))
    #for transparency
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
    screen.blit(font_big.render("Congrats! You WONNN:)", True, Sky), (200, 200))
    screen.blit(font_medium.render("Press ENTER to go back to title", True, White), (275, 320))

def draw_hud():
    #reference - https://www.youtube.com/watch?v=E82_hdoe06M
    #background bar
    pygame.draw.rect(screen, Dark_Gray, (0, 0, W, 50))

    #health bar
    pygame.draw.rect(screen, Gray_2, (10, 8, 160, 16))
    pygame.draw.rect(screen, Green,(10, 8, int(160 * player["health"] / 100), 16))
    screen.blit(font_small.render(f"HP{int(player['health'])}", True, White), (10, 28))

    #hunger bar
    pygame.draw.rect(screen, Gray_2, (210, 8, 160, 16))
    pygame.draw.rect(screen, Orange,(210, 8, int(160 * player["hunger"] / 100), 16))
    screen.blit(font_small.render(f"Hunger{int(player['hunger'])}", True, White),(210, 28))

    #energy bar
    pygame.draw.rect(screen, Gray_2, (410, 8, 160, 16))
    pygame.draw.rect(screen, Yellow, (410, 8, int(160 * player["energy"] / 100), 16))
    screen.blit(font_small.render(f"Energy{int(player['energy'])}", True, White),(410, 28))

    #level timer
    pygame.draw.rect(screen, Gray_2, (610, 8, 160, 16))
    time_ratio = max(0, level_timer / Levels[level_count]["time_limit"])
    pygame.draw.rect(screen, Sky, (610, 8, int(160 * time_ratio / 150), 16))
    screen.blit(font_small.render(f"Time Left  {int(level_timer)}", True, White), (610, 28))


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

    #draw corn
    for corn in corns:
        if corn["alive"]:
            screen.blit(images["corn"], (int(corn["x"]), int(corn["y"])))

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

    #draws hud
    draw_hud()

    if popup_timer > 0 and popup_msg:
        txt = font_medium.render(popup_msg, True, White)
        bg  = pygame.Surface((txt.get_width() + 20, 36), pygame.SRCALPHA)
        bg.fill((0, 0, 0, 180))
        screen.blit(bg,  (W // 2 - bg.get_width()  // 2, H // 2 - 18))
        screen.blit(txt, (W // 2 - txt.get_width() // 2, H // 2 - 10))

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
        "egg_timer": 0.0, #for the start of the game to prevent laying eggs instantly, there will be a 10 sec countdown
        "egg_cooldown": 0.0,
        "eggs_delivered": 0,
        "hunger_timer": 0.0,
        "standing_timer": 0.0, #for the energy to stop going down
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
        direction_x = -1 #for left
        player["facing_left"] = True #for the flipping of the image
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        direction_x = 1 #for right
        player["facing_left"] = False
    if keys[pygame.K_UP]    or keys[pygame.K_w]:
        direction_y = -1 #for up
    if keys[pygame.K_DOWN]  or keys[pygame.K_s]:
        direction_y = 1 #for down

    #check if chicken is moving at all or not
    player["moving"] = direction_x != 0 or direction_y != 0

    # for diagnal
    # https://gamedev.stackexchange.com/questions/104437/diagonal-movement-with-pygame-rect-class
    # right + down = √(10² + 10²) = 14.1 total speed but we are doing right+down  = √(7.07² + 7.07²) = 10 which makes it equal
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
    #multiplying by dt makes movement the same speed on every computer
    #eg 60(normal speed set in game)+ 1(presed 1 right) * 180(chick speed) * dt
    player["x"] += direction_x * current_speed * dt
    player["y"] += direction_y * current_speed * dt

    # stops the chicken from walking off screen
    if player["x"] < 0:
        player["x"] = 0  # stop at left edge
    if player["x"] > W - 60:
        player["x"] = W - 60  # stop at right edge
    if player["y"] < 60:
        player["y"] = 60  # stop at top edge (btw 60 is the HUD height)
    if player["y"] > H - 60:
        player["y"] = H - 60  # stop at bottom edge

#handles every stats
def drain_stats():
    global player, dt

    if player["egg_cooldown"] > 0:
        player["egg_cooldown"] = max(0.0, player["egg_cooldown"] - dt)

    player["hunger_timer"] += dt
    if player["hunger_timer"] >= 5.0: #decrease every 5 sec
        player["hunger_timer"] -= 5.0
        player["hunger"] = max(0.0, player["hunger"] - 2.0)

    if player["hunger"] == 0: #drops health when the player is hungry
        player["health"] = max(0.0, player["health"] - 2.0 * dt)

    if player["moving"]:#when the player is moving it should decrease the energy, just like how realistically when we walk we get tired
        player["energy"] = max(0.0, player["energy"] - (1.5 / FPS))

    player["egg_timer"] += dt
    if player["egg_timer"] >= 10.0: #countdown of about 10 sec to see if the they can lay egg or not then
        player["egg_timer"] = 0.0
        try_lay_eggs()

#items + collisions

def make_corn():
    return {
        "x": random.randint(100, W - 100),  # spawns randomly
        "y": random.randint(100, H - 100),
        "alive": True,  # too check if the corn is active or not
        "hunger": 10, # once the player collects a corn then it gain hunger points by 10
        "timer": 420 #7 sec for the 60 FPS 60*7 = 420
    }

def make_water():
    return {
        "x": random.randint(100, W - 150), # to make sure it doesnt spawn beyond the game border
        "y": random.randint(100, H - 100),
        "w": 80,
        "h": 52,
    }

def make_fence():
    return {
        "x": random.randint(100, W - 200),  # to make sure it doesnt spawn beyond the game border
        "y": random.randint(100, H - 150),
        "w": 90,
        "h": 63,
    }

def make_fox() -> dict:
    return {
        "x":            100.0,
        "y":            100.0,
        "speed":        90.0, #a bit slower than the chicken
        "hit_cooldown": 0.0,
    }

def make_farmer() -> dict:
    return {
        "x":            600.0,
        "y":            200.0,
        "speed":        5.0, #speed is calculated through FPS
        "direction":    1, #to make the farmer move left to right
        "hit_cooldown": 0.0,
    }

def make_bomb():
    return {
        "x":     random.randint(100, W - 100), #bomb also spawns randomly
        "y":     random.randint(100, H - 100),
        "alive": True, #too check if the bomb is active or has it been blasted
        "damage": 30 # once the player hits the bomb it will decrease the health by 30
    }

#for most of all check functions
#an invisible rect has been for each item and also for the chick
#this is to check whether the rect is touching the item
#this will help us decide how the item will affect the stats(drain or gain)
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
            player["x"] = player["previous_x"] #prevents the chick to touch the fence and pushes it back to prev position
            player["y"] = player["previous_y"]

def check_nest():
    global player
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
            farmer["hit_cooldown"] = 1.5 # seconds before farmer can hit again
            pop_up_message("The farmer has caught you! -35 health!")

def make_fox_follow():
    global player, fox
    if fox is None:
        return
    distance_x = player["x"] - fox["x"]
    distance_y = player["y"] - fox["y"]
    distance = max(1, (distance_x**2 + distance_y**2) ** 0.5)

    speed = 2   #adjust speed here
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
    if farmer["x"] <= 0 or farmer["x"] >= W - 60: #again to avoid farmer to move further the border
        farmer["direction"] *= -1
    if farmer["hit_cooldown"] > 0: #cooldown if the farmer hits the chicken to
        farmer["hit_cooldown"] = max(0.0, farmer["hit_cooldown"] - dt)

def take_bomb_damage():
    global player, bombs
    for bomb in bombs:
        if bomb["alive"]:
            chicken_rect = pygame.Rect(player["x"], player["y"], 60, 60)
            bomb_rect    = pygame.Rect(bomb["x"],   bomb["y"],   20, 20)
            if chicken_rect.colliderect(bomb_rect):
                bomb["alive"] = False #if the bomb is active and the chick hits it
                #it will take in the damage that has been preset to -30 health
                player["health"] -= 30
                pop_up_message("BOOM! -20 health!")

def spawn_corn(): #very similar to bomb except hunger is gained
    global player, corns
    #this is for it to appear randomly and disappear
    if random.randint(1, 900) == 1:
        corns.append(make_corn())

    for corn in corns:
        corn["timer"] -= 1 #every frame per sec the timer decreases

        if corn["timer"] <= 0: #once it hits the timer
            corns.remove(corn) #it will remove the corn
            continue #this will skip the loop and go to the next item

        if corn["alive"]:
            chicken_rect = pygame.Rect(player["x"], player["y"], 60, 60)
            corn_rect    = pygame.Rect(corn["x"],   corn["y"],   35, 50)
            if chicken_rect.colliderect(corn_rect):
                corn["alive"] = False
                if player["hunger"] < 100:
                    player["hunger"] = min(100, player["hunger"] + corn["hunger"])
                    corn["alive"] = False
                else:
                    pop_up_message("Hunger is full already!")
        if not corn["alive"]:
            corns.remove(corn)

def try_lay_eggs():
    global player
    #chicken cannot lay an egg if it holding one, so this will check if the chickenhas an egg or not
    if player["carrying_egg"]:
        pop_up_message("Already carrying an egg!")
        return
    #too avoid making the game be more easy, we need a cooldown so the eggs arent laid in one go
    if player["egg_cooldown"] > 0:
        pop_up_message(f"Cooldown: {int(player['egg_cooldown'])}s")
        return
    #1st condition, chicken must have 50+ to lay an egg
    if player["hunger"] < 50:
        pop_up_message("Need 50+ hunger to lay!")
        return
    #2nd condition, chicken must have 70+ to lay an egg
    if (player["energy"] < 70):
        pop_up_message("Need 70+ energy to lay!")
        return
    #so once they have an egg, carrying egg becomes true
    player["carrying_egg"] = True
    #once laid, the stats must be drained in order to make it more difficult
    player["hunger"] = max(0.0, player["hunger"] - 15.0)
    player["energy"] = max(0.0, player["energy"] - 20.0)
    player["egg_cooldown"] = float(egg_cooldown)

#main game loop
def pop_up_message(message):
    global popup_msg, popup_timer
    popup_msg   = message
    popup_timer = 2.0 #pop up message will last 2 sec

#used in order to prevent repeating this after every state = "play"
def level_setup():
    global player, bombs, waters, fences, fox, farmer, level_timer, corns
    player = make_player()
    bombs = [make_bomb() for _ in range(Levels[level_count]["bomb_count"])] #for _ in range - not interested in how many times it will loop
    waters = [make_water() for _ in range(Levels[level_count]["water_count"])]
    corns = [make_corn() for _ in range(Levels[level_count]["corn_max"])]
    fences = [make_fence() for _ in range(Levels[level_count]["fence_count"])]
    level_timer = float(Levels[level_count]["time_limit"])
    fox = make_fox() if Levels[level_count]["has_fox"] else None
    farmer = make_farmer() if Levels[level_count]["has_farmer"] else None


#title -> select chick -> levels[1-5]
def start_game():
    #to modify the variables outside this function.
    global state, player, dt, selected_chick, popup_timer, popup_msg, Levels, level_timer, level_count
    global bombs, waters, fences, fox, farmer, corns
    level_count = 0

    while True:
        #To keep the game running until the player quiets
        #we will use dt - the delta time to conver miliseconds to seconds and to also make sure the game runs smoothly
        dt = clock.tick(FPS) / 1000.0

        #we will check all possible events of what the player will click onto
        for event in pygame.event.get():
            #if th player decided to exit or quit the game it will close the game window and quit safely without any errors
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN: #for enter or return
                #depnedig on the state of the game, if enter is pressed when player is on title page
                #it will take the player to the select chick page
                if state == "title":
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        state = "select"
                #when they have entered the select page
                elif state == "select":
                    #this will allow the player to go through each chickens that have been displayed using arrow keys.
                    #only left to right
                    if event.key == pygame.K_LEFT:
                        selected_chick = (selected_chick - 1) % len(Players)
                    if event.key == pygame.K_RIGHT:
                        selected_chick = (selected_chick + 1) % len(Players)
                    #once player has selected the chick, they can press Enter to start the first level.
                    if event.key == pygame.K_RETURN:
                        level_timer = Levels[level_count]["time_limit"]
                        #This will create the player, Spawns all the bombs, water, fences,and adds fox and farmer if the level has it
                        player = make_player()
                        bombs = [make_bomb() for i in range(Levels[level_count]["bomb_count"])]
                        waters = [make_water() for i in range(Levels[level_count]["water_count"])]
                        fences = [make_fence() for i in range(Levels[level_count]["fence_count"])]
                        corns = [make_corn() for i in range(Levels[level_count]["corn_max"])]
                        if Levels[level_count]["has_fox"]:
                            fox = make_fox()
                        else: fox = None
                        if Levels[level_count]["has_farmer"]:
                            farmer = make_farmer()
                        else: farmer = None
                        state  = "play"
                #This is for if the have won the gaem or not
                elif state == "won":
                    #if the won they have option to go back and enter to start new level
                    if event.key == pygame.K_RETURN:
                        level_setup() #need to be called to update the game stats
                        state = "play"
                    if event.key == pygame.K_ESCAPE:
                        state = "title" # back to title is the press esc
                #game over screen
                elif state == "over":
                    if event.key == pygame.K_RETURN:
                        level_setup() #resets and allows them to replay
                        state  = "play"
                    if event.key == pygame.K_ESCAPE:
                        state = "title" #if the quit
                elif state == "levels_done": #if all levels are done
                    if event.key == pygame.K_RETURN:
                        state = "title" #only possible option to go back and replay the whole game

        if state == "play": #everytime the player is playing
            #below functions will be called to make the game logics work
            check_nest()
            move_player()
            drain_stats()
            check_fence()
            check_water()
            take_bomb_damage()
            spawn_corn()

            #Moves the farmer and fox and checks wheter they collide with the player.
            if farmer is not None:
                move_farmer()
                check_farmer()
            if fox is not None:
                make_fox_follow()

            #real time countdown for both level and popups
            if popup_timer > 0:
                popup_timer -= dt
            if level_timer >0:
                level_timer -= dt

            #if player delivers all eggs they win the level and go to next
            if player["eggs_delivered"] == Levels[level_count]["eggs_needed"]:
                state = "won"
                level_count += 1 #to move to next level
                if level_count >= len(Levels)-1:
                    state = "levels_done" #once all level has been passed, levels done will be shown
                    level_count = 0

            elif player["health"] <= 0 or level_timer <= 0:
                state = "over"

        #for every state = it will call the function taht the state has been assigned
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
