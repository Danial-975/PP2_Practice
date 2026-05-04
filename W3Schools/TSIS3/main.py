import pygame, sys, racer, ui, persistence as db
from pygame.locals import *

pygame.init()
pygame.mixer.init()
DISPLAYSURF = pygame.display.set_mode((400, 600))
clock = pygame.time.Clock()

settings = db.load_settings()
coin_sound = pygame.mixer.Sound('assets/sounds/coin.wav')
crash_sound = pygame.mixer.Sound('assets/sounds/crash.wav')
background = pygame.image.load("assets/images/street.png")

state = "MENU"
user_name = ""

def game_loop():
    global state
    player = racer.Player()
    enemies = pygame.sprite.Group(racer.Enemy())
    coins = pygame.sprite.Group(racer.Coin())
    powerups = pygame.sprite.Group()
    hazards = pygame.sprite.Group(racer.Hazard("slow"), racer.Hazard("break"))
    all_sprites = pygame.sprite.Group(player, *enemies, *coins, *hazards)

    diff_map = {"Easy": 3, "Medium": 5, "Hard": 8}
    base_speed = diff_map.get(settings["difficulty"], 5)
    speed = base_speed
    score, coin_score, distance = 0, 0, 0
    n_threshold = 10

    nitro_active = False
    nitro_start_time = 0
    NITRO_DURATION = 3000
    NITRO_BOOST = 5        
    is_broken = False 

    while True:
        if settings["sound"]: pygame.mixer.unpause()
        else: pygame.mixer.pause()

        current_time = pygame.time.get_ticks()
        nitro_display_time = 0
        if nitro_active:
            passed_time = current_time - nitro_start_time
            if passed_time < NITRO_DURATION:
                current_speed = speed + NITRO_BOOST
                nitro_display_time = round((NITRO_DURATION - passed_time) / 1000, 1)
            else:
                nitro_active = False
                current_speed = speed
        else:
            current_speed = speed
        if is_broken:
            current_speed *= 0.5
            ui.draw_text(DISPLAYSURF, "ENGINE FAILURE!", 15, 200, 80, (100, 100, 100))
        for event in pygame.event.get():
            if event.type == QUIT: pygame.quit(); sys.exit()

        player.move()
        spawn_groups = [enemies, hazards, powerups] 
        for e in list(all_sprites):
            if isinstance(e, (racer.Coin, racer.Hazard)):
                e.move(current_speed, spawn_groups)
            if isinstance(e, racer.Enemy):
                if e.move(current_speed, [enemies]): score += 1
            
        powerups.update(speed)
        distance += current_speed * 0.05

        if len(powerups) == 0 and pygame.time.get_ticks() % 200 == 0:
            p = racer.PowerUp()
            powerups.add(p); all_sprites.add(p)
        
        slow_hits = pygame.sprite.spritecollide(player, hazards, False)
        for h in slow_hits:
            if h.type == "slow":
                speed = max(3, speed - 0.1) 
                h.spawn(spawn_groups)

        for h in slow_hits:
            if h.type == "break":
                is_broken = True
                h.spawn(spawn_groups)

        if pygame.sprite.spritecollideany(player, enemies):
            if player.shielded:
                player.shielded = False
                pygame.sprite.spritecollide(player, enemies, True)
                enemies.add(racer.Enemy()); all_sprites.add(*enemies)
            else:
                if settings["sound"]: crash_sound.play()
                db.update_leaderboard(user_name, score + coin_score, distance)
                state = "GAMEOVER"; return

        for c in pygame.sprite.spritecollide(player, coins, False):
            coin_score += c.weight
            if settings["sound"]: coin_sound.play()
            if coin_score >= n_threshold:
                speed += 1; n_threshold += 10
            c.spawn(spawn_groups)

        for p in pygame.sprite.spritecollide(player, powerups, True):
            if p.kind == "repair":
                is_broken = False 
            if p.kind == "nitro":
                if not is_broken:
                    nitro_active = True
                    nitro_start_time = pygame.time.get_ticks()
            elif p.kind == "shield":
                player.shielded = True


        DISPLAYSURF.blit(background, (0,0))
        for e in all_sprites: DISPLAYSURF.blit(e.image, e.rect)
        ui.draw_text(DISPLAYSURF, f"Score: {score}", 20, 60, 20)
        ui.draw_text(DISPLAYSURF, f"Coins: {coin_score}", 20, 330, 20)

        if player.shielded:
            ui.draw_text(DISPLAYSURF, "SHIELD ACTIVE", 20, 200, 50, (0, 150, 255))

        if nitro_active:
            ui.draw_text(DISPLAYSURF, f"NITRO: {nitro_display_time}s", 25, 200, 150, (0, 0, 255))
            
            bar_width = (nitro_display_time * 100) / (NITRO_DURATION / 1000) 
            pygame.draw.rect(DISPLAYSURF, (0, 0, 255), (150, 180, bar_width * 1, 10))

        if is_broken:
            ui.draw_text(DISPLAYSURF, "ENGINE BROKEN!", 20, 200, 120, (255, 0, 0))
        
        pygame.display.update()
        clock.tick(60)

while True:
    DISPLAYSURF.fill((240, 240, 240))
    for event in pygame.event.get():
        if event.type == QUIT: pygame.quit(); sys.exit()
        if state == "MENU" and event.type == KEYDOWN:
            if event.key == K_BACKSPACE: user_name = user_name[:-1]
            else: user_name += event.unicode

    if state == "MENU":
        ui.draw_text(DISPLAYSURF, "SUPER RACER", 40, 200, 100)
        ui.draw_text(DISPLAYSURF, f"Name: {user_name}", 20, 200, 200)
        if ui.button(DISPLAYSURF, "START", 200, 350, 120, 50, (200,200,200), (170,170,170)) and user_name:
            state = "GAME"; game_loop()
        if ui.button(DISPLAYSURF, "LEADERBOARD", 200, 420, 150, 40, (200,200,200), (170,170,170)): state = "LB"
        if ui.button(DISPLAYSURF, "SETTINGS", 200, 480, 150, 40, (200,200,200), (170,170,170)): state = "SET"

    elif state == "LB":
        ui.draw_text(DISPLAYSURF, "TOP 10", 30, 200, 50)
        scores = db.load_data("leaderboard.json", [])
        for i, s in enumerate(scores):
            ui.draw_text(DISPLAYSURF, f"{i+1}. {s['name']}: {s['score']}", 18, 200, 100 + i*30)
        if ui.button(DISPLAYSURF, "BACK", 200, 550, 100, 40, (200,200,200), (170,170,170)): state = "MENU"

    elif state == "SET":
        ui.draw_text(DISPLAYSURF, "SETTINGS", 30, 200, 100)
        txt = "Sound: ON" if settings["sound"] else "Sound: OFF"
        if ui.button(DISPLAYSURF, txt, 200, 200, 150, 40, (200,200,200), (170,170,170)):
            settings["sound"] = not settings["sound"]
            db.save_data("settings.json", settings)
        diff_txt = f"Difficulty: {settings['difficulty']}"
        if ui.button(DISPLAYSURF, diff_txt, 200, 280, 200, 40, (200,200,200), (170,170,170)):
            modes = ["Easy", "Medium", "Hard"]
            curr_idx = modes.index(settings["difficulty"])
            settings["difficulty"] = modes[(curr_idx + 1) % len(modes)]
            db.save_settings(settings)
        if ui.button(DISPLAYSURF, "BACK", 200, 500, 100, 40, (200,200,200), (170,170,170)): state = "MENU"

    elif state == "GAMEOVER":
        ui.draw_text(DISPLAYSURF, "CRASHED!", 50, 200, 200, (255,0,0))
        if ui.button(DISPLAYSURF, "RETRY", 200, 350, 120, 50, (200,200,200), (170,170,170)): state = "GAME"; game_loop()
        if ui.button(DISPLAYSURF, "MENU", 200, 420, 120, 50, (200,200,200), (170,170,170)): state = "MENU"

    pygame.display.update()
    clock.tick(60)