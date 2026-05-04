import pygame, random, json, os
from db import save_score, get_best

WIDTH, HEIGHT = 600, 600
CELL = 20

def load_settings():
    if not os.path.exists("settings.json"):
        return {"snake_color": [0, 255, 0], "grid": True, "sound": True}
    with open("settings.json") as f:
        return json.load(f)

def run_game(username):
    pygame.init()
    settings = load_settings()
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 30)
    
    snake_color = tuple(settings.get("snake_color", [0, 255, 0]))

    eat_sound = None
    if settings["sound"]:
        pygame.mixer.init()
        if os.path.exists("eat.wav"):
            eat_sound = pygame.mixer.Sound("eat.wav")

    snake = [(100,100),(80,100),(60,100)]
    direction = (20,0)

    def gen_food():
        while True:
            f = (random.randrange(0, WIDTH, CELL), random.randrange(0, HEIGHT, CELL))
            if f not in snake: return f

    food = gen_food()
    food_spawn_time = pygame.time.get_ticks()
    
    poison = gen_food()
    poison_spawn_time = pygame.time.get_ticks()
    
    power = None
    power_time = 0
    power_type = None
    obstacles = []

    score = 0
    level = 1
    speed = 10
    best = get_best(username)

    shield = False
    effect_end_time = 0
    effect_type = None

    while True:
        current_time = pygame.time.get_ticks()
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return "menu"
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP and direction != (0, 20): direction = (0, -20)
                if e.key == pygame.K_DOWN and direction != (0, -20): direction = (0, 20)
                if e.key == pygame.K_LEFT and direction != (20, 0): direction = (-20, 0)
                if e.key == pygame.K_RIGHT and direction != (-20, 0): direction = (20, 0)

        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        if current_time - food_spawn_time > 8000:
            food = gen_food()
            food_spawn_time = current_time
        if current_time - poison_spawn_time > 8000:
            poison = gen_food()
            poison_spawn_time = current_time

        snake.insert(0, head)

        if head in snake[1:] or head in obstacles or head[0]<0 or head[1]<0 or head[0]>=WIDTH or head[1]>=HEIGHT:
            if shield:
                shield = False
                effect_type = None
            else:
                save_score(username, score, level)
                return game_over_screen(screen, score, level, best)

        if head == food:
            if eat_sound: eat_sound.play()
            score += 1
            food = gen_food()
            food_spawn_time = current_time
            if score % 3 == 0:
                level += 1
                speed += 2
                if level >= 3:
                    obstacles.append(gen_food())
        else:
            snake.pop()

        if head == poison:
            if len(snake) > 2:
                snake.pop()
                snake.pop()
                poison = gen_food()
                poison_spawn_time = current_time
            else:
                save_score(username, score, level)
                return game_over_screen(screen, score, level, best)

        if not power and random.random() < 0.01:
            power = gen_food()
            power_time = current_time
            power_type = random.choice(["speed", "slow", "shield"])

        if power and current_time - power_time > 8000:
            power = None

        if power and head == power:
            if power_type == "speed":
                speed += 5
                effect_type = "speed"
                effect_end_time = current_time + 5000
            elif power_type == "slow":
                speed = max(5, speed - 5)
                effect_type = "slow"
                effect_end_time = current_time + 5000
            elif power_type == "shield":
                shield = True
            power = None

        if effect_type in ["speed", "slow"] and current_time > effect_end_time:
            speed = 10 + (level - 1) * 2
            effect_type = None

        screen.fill((0, 0, 0))
        if settings["grid"]:
            for x in range(0, WIDTH, CELL): pygame.draw.line(screen, (40,40,40), (x,0), (x,HEIGHT))
            for y in range(0, HEIGHT, CELL): pygame.draw.line(screen, (40,40,40), (0,y), (WIDTH,y))

        for s in snake: pygame.draw.rect(screen, snake_color, (*s, CELL-1, CELL-1))
        pygame.draw.rect(screen, (255, 0, 0), (*food, CELL, CELL))
        pygame.draw.rect(screen, (150, 0, 0), (*poison, CELL, CELL))
        for o in obstacles: pygame.draw.rect(screen, (100, 100, 100), (*o, CELL, CELL))

        if power:
            p_color = (0, 255, 255) if power_type == "speed" else (255, 165, 0) if power_type == "slow" else (0, 0, 255)
            pygame.draw.rect(screen, p_color, (*power, CELL, CELL))

        text = font.render(f"Score:{score} Level:{level} Best:{best}", True, (255, 255, 255))
        screen.blit(text, (10, 10))
        
        pygame.display.flip()
        clock.tick(speed)

def game_over_screen(screen, score, level, best):
    font_big = pygame.font.SysFont(None, 60)
    font = pygame.font.SysFont(None, 40)
    while True:
        screen.fill((0, 0, 0))
        screen.blit(font_big.render("GAME OVER", True, (255,0,0)), (150, 150))
        screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (200, 250))
        screen.blit(font.render(f"Best: {best}", True, (255,255,255)), (200, 350))
        screen.blit(font.render("R - Retry  M - Menu", True, (0,255,0)), (150, 450))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return "menu"
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r: return "retry"
                if e.key == pygame.K_m: return "menu"