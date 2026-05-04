import pygame, random
from pygame.locals import *

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/images/player.png")
        self.rect = self.image.get_rect(center=(160, 520))
        self.shielded = False

    def move(self):
        keys = pygame.key.get_pressed()
        if self.rect.left > 0 and keys[K_LEFT]: self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and keys[K_RIGHT]: self.rect.move_ip(5, 0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/images/enemy.png")
        self.rect = self.image.get_rect()
        self.spawn([])

    def spawn(self, groups):
        attempts = 0
        while attempts < 50:
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -100)
            if not any(pygame.sprite.spritecollideany(self, g) for g in groups):
                break
            attempts += 1

    def move(self, speed, groups):
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.spawn(groups)
            return True
        return False

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img_raw = pygame.image.load("assets/images/coin.png")
        self.weight = 1
        self.spawn([])

    def spawn(self, groups):
        self.weight = random.randint(1, 3)
        size = 30 + (self.weight * 7)
        self.image = pygame.transform.scale(self.img_raw, (size, size))
        self.rect = self.image.get_rect()
 
        attempts = 0
        while attempts < 100:
            attempts += 1
            new_x = random.randint(40, 360)
            new_y = random.randint(-800, -100)
            self.rect.center = (new_x, new_y)
            
            collision = False
            for group in groups:
                if pygame.sprite.spritecollideany(self, group):
                    collision = True
                    break
                for sprite in group:
                    if self.rect.colliderect(sprite.rect.inflate(50, 50)):
                        collision = True
                        break
                if collision: break
                
            if not collision:
                return
            
        self.rect.center = (200, -1000)

    def move(self, speed, groups):
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.spawn(groups)

class Hazard(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.type = type 
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        color = (0, 0, 0) if type == "slow" else (128, 128, 128)
        pygame.draw.circle(self.image, color, (10, 10), 10)
        self.rect = self.image.get_rect()
        self.spawn([])

    def spawn(self, groups):
        attempts = 0
        while attempts < 50:
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(-500, -50))
            if not any(pygame.sprite.spritecollideany(self, g) for g in groups):
                break
            attempts += 1

    def move(self, speed, groups):
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.spawn(groups)

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.kind = random.choice(["nitro", "shield", "repair"])
        
        if self.kind == "shield":
            self.image = pygame.image.load("assets/images/shield.png")
        else:
            self.image = pygame.Surface((30, 30))
            if self.kind == "nitro":
                self.image.fill((0, 0, 255)) 
            elif self.kind == "repair":
                self.image.fill((255, 165, 0)) 
        
        self.rect = self.image.get_rect(center=(random.randint(40, 360), -100))
        self.spawn_time = pygame.time.get_ticks()

    def update(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT or pygame.time.get_ticks() - self.spawn_time > 7000:
            self.kill()