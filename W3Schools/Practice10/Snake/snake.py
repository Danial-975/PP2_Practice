import pygame
import random
import time

# --- Configuration & Initialization ---
pygame.init()

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)

# Screen Dimensions
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20 # Size of snake segment and food

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Extended Snake Game')

clock = pygame.time.Clock()
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def display_ui(score, level):
    """Displays current score and level on the screen."""
    value = score_font.render(f"Score: {score}  Level: {level}", True, YELLOW)
    screen.blit(value, [10, 10])

def generate_food(snake_list):
    """
    Generates food at a random position. 
    Ensures food is not placed on the snake's body or the borders.
    """
    while True:
        # Calculate random coordinates aligned with the grid
        food_x = round(random.randrange(BLOCK_SIZE, WIDTH - BLOCK_SIZE * 2) / BLOCK_SIZE) * BLOCK_SIZE
        food_y = round(random.randrange(BLOCK_SIZE, HEIGHT - BLOCK_SIZE * 2) / BLOCK_SIZE) * BLOCK_SIZE
        
        # Check if the food position overlaps with any part of the snake
        if [food_x, food_y] not in snake_list:
            return food_x, food_y

def game_loop():
    game_over = False
    game_close = False

    # Snake initial position (center)
    x, y = WIDTH / 2, HEIGHT / 2
    x_speed, y_speed = 0, 0

    snake_list = []
    snake_length = 1

    # Initial Game State
    score = 0
    level = 1
    base_speed = 10
    
    # Generate first food
    food_x, food_y = generate_food(snake_list)

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

        # --- Wall Collision Check ---
        # Checks if the head hits the boundaries
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True

        x += x_speed
        y += y_speed
        screen.fill(BLACK)
        
        # Draw Food
        pygame.draw.rect(screen, GREEN, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])
        
        # Update Snake Body
        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # --- Self-Collision Check ---
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        # Draw Snake
        for segment in snake_list:
            pygame.draw.rect(screen, WHITE, [segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE])

        display_ui(score, level)
        pygame.display.update()

        # --- Food Consumption & Leveling ---
        if x == food_x and y == food_y:
            food_x, food_y = generate_food(snake_list)
            snake_length += 1
            score += 1
            
            # Level Up Logic: Every 4 foods
            if score % 4 == 0:
                level += 1
                base_speed += 2 # Increase speed

        # Control the frame rate based on the current level speed
        clock.tick(base_speed)

    pygame.quit()
    quit()

game_loop()