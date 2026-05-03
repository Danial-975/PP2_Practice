import pygame
import random
import time

pygame.init()

WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)

WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20 

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Extended Snake Game')

clock = pygame.time.Clock()
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def display_ui(score, level):
    value = score_font.render(f"Score: {score}  Level: {level}", True, YELLOW)
    screen.blit(value, [10, 10])

def generate_food(snake_list):
    while True:
        food_x = round(random.randrange(BLOCK_SIZE, WIDTH - BLOCK_SIZE * 2) / BLOCK_SIZE) * BLOCK_SIZE
        food_y = round(random.randrange(BLOCK_SIZE, HEIGHT - BLOCK_SIZE * 2) / BLOCK_SIZE) * BLOCK_SIZE
        
        if [food_x, food_y] not in snake_list:
            weight = random.randint(1, 3)
            spawn_time = pygame.time.get_ticks() 
            return food_x, food_y, weight, spawn_time

def game_loop():
    game_over = False
    game_close = False

    x, y = WIDTH / 2, HEIGHT / 2
    x_speed, y_speed = 0, 0

    snake_list = []
    snake_length = 1

    score = 0
    level = 1
    base_speed = 10
    FOOD_LIFETIME = 5000 
    
    food_x, food_y, food_weight, food_timer = generate_food(snake_list)

    while not game_over:
        while game_close:
            screen.fill(BLACK)
            msg = font_style.render("Game Over! Press C-Play Again or Q-Quit", True, RED)
            screen.blit(msg, [WIDTH / 6, HEIGHT / 3])
            display_ui(score, level)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_speed == 0:
                    x_speed, y_speed = -BLOCK_SIZE, 0
                elif event.key == pygame.K_RIGHT and x_speed == 0:
                    x_speed, y_speed = BLOCK_SIZE, 0
                elif event.key == pygame.K_UP and y_speed == 0:
                    y_speed, x_speed = -BLOCK_SIZE, 0
                elif event.key == pygame.K_DOWN and y_speed == 0:
                    y_speed, x_speed = BLOCK_SIZE, 0

        current_time = pygame.time.get_ticks()
        if current_time - food_timer > FOOD_LIFETIME:
            food_x, food_y, food_weight, food_timer = generate_food(snake_list)

        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True

        x += x_speed
        y += y_speed
        screen.fill(BLACK)
        
        color = GREEN
        if food_weight == 2: color = YELLOW
        elif food_weight == 3: color = RED
        
        pygame.draw.rect(screen, color, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])
        
        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        for segment in snake_list:
            pygame.draw.rect(screen, WHITE, [segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE])

        display_ui(score, level)
        pygame.display.update()

        if x == food_x and y == food_y:
            score += food_weight
            snake_length += 1
            food_x, food_y, food_weight, food_timer = generate_food(snake_list)
            
            new_level = (score // 10) + 1
            if new_level > level:
                level = new_level
                base_speed += 2 

        clock.tick(base_speed)

    pygame.quit()
    quit()

game_loop()