import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5        
SCORE = 0        
COIN_SCORE = 0   
N = 10           

font_small = pygame.font.SysFont("Verdana", 20)
font_big = pygame.font.SysFont("Verdana", 60)
game_over = font_big.render("Game Over", True, BLACK)

background = pygame.image.load("images/street.png")
coin_sound = pygame.mixer.Sound('sounds/coin.wav')
crash_sound = pygame.mixer.Sound('sounds/crash.wav')

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/enemy.png")
        self.rect = self.image.get_rect() 
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def spawn(self, coins_group):
        collision = True
        while collision:
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
            self.rect.top = 0
            if not pygame.sprite.spritecollideany(self, coins_group):
                collision = False

    def move(self, coins_group):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > SCREEN_HEIGHT):
            SCORE += 1
            self.spawn(coins_group)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_original = pygame.image.load("images/coin.png")
        self.weight = 1
        self.image = self.image_original
        self.rect = self.image_original.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def spawn(self, enemies_group):
        self.weight = random.randint(1, 3)
        new_size = 30 + (self.weight * 7) 
        self.image = pygame.transform.scale(self.image_original, (new_size, new_size))
        self.rect = self.image.get_rect()

        collision = True
        while collision:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
            if not pygame.sprite.spritecollideany(self, enemies_group):
                collision = False

    def move(self, enemies_group):
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > SCREEN_HEIGHT):
            self.spawn(enemies_group)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

enemies = pygame.sprite.Group()
coins = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies.add(E1)
coins.add(C1)
all_sprites.add(P1, E1, C1)

C1.spawn(enemies)
E1.spawn(coins)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0, 0))
    
    score_img = font_small.render(f"Score: {SCORE}", True, BLACK)
    coin_img = font_small.render(f"Coins: {COIN_SCORE}", True, BLACK)
    DISPLAYSURF.blit(score_img, (10, 10))
    DISPLAYSURF.blit(coin_img, (SCREEN_WIDTH - 110, 10))

    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        if isinstance(entity, Coin):
            entity.move(enemies)
        elif isinstance(entity, Enemy):
            entity.move(coins)
        else:
            entity.move()

    collided_coins = pygame.sprite.spritecollide(P1, coins, False)
    for coin in collided_coins:
        COIN_SCORE += coin.weight
        coin_sound.play()
        
        if COIN_SCORE >= N:
            SPEED += 1
            N += 10
            
        coin.spawn(enemies)

    if pygame.sprite.spritecollideany(P1, enemies):
        crash_sound.play()
        time.sleep(0.5)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)