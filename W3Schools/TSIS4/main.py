import pygame, sys, json, os
from db import create_tables, get_top10
from game import run_game

pygame.init()
screen = pygame.display.set_mode((600,600))
font = pygame.font.SysFont(None,40)

def input_name():
    name = ""
    while True:
        screen.fill((0,0,0))
        txt = font.render("Enter name: " + name, True, (255,255,255))
        screen.blit(txt, (100, 250))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT: sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN: return name if name else "Guest"
                elif e.key == pygame.K_BACKSPACE: name = name[:-1]
                else: name += e.unicode

def show_leaderboard():
    data = get_top10()
    while True:
        screen.fill((0,0,0))
        y = 100
        for row in data:
            txt = font.render(f"{row[0]}: {row[1]} pts (Lvl {row[2]})", True, (255,255,255))
            screen.blit(txt, (100, y))
            y += 40
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                return

def save_settings(settings):
    with open("settings.json", "w") as f:
        json.dump(settings, f, indent=4)

def settings_menu():
    if not os.path.exists("settings.json"):
        settings = {"snake_color": [0, 255, 0], "grid": True, "sound": True}
    else:
        with open("settings.json") as f:
            settings = json.load(f)

    colors = [[0, 255, 0], [255, 105, 180], [0, 0, 255], [255, 255, 0]]
    color_names = ["Green", "Pink", "Blue", "Yellow"]
    
    current_color_idx = 0
    for i, c in enumerate(colors):
        if settings.get("snake_color") == c:
            current_color_idx = i

    selected = 0
    while True:
        screen.fill((0,0,0))
        options = [
            f"Color: {color_names[current_color_idx]}",
            f"Grid: {'ON' if settings['grid'] else 'OFF'}",
            f"Sound: {'ON' if settings['sound'] else 'OFF'}"
        ]
        
        for i, opt in enumerate(options):
            color = (255, 255, 0) if i == selected else (255, 255, 255)
            screen.blit(font.render(opt, True, color), (100, 200 + i*50))
        
        screen.blit(font.render("ESC - Save & Back", True, (150,150,150)), (100, 400))
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT: sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    save_settings(settings)
                    return
                if e.key == pygame.K_DOWN: selected = (selected + 1) % 3
                if e.key == pygame.K_UP: selected = (selected - 1) % 3
                if e.key == pygame.K_RETURN:
                    if selected == 0:
                        current_color_idx = (current_color_idx + 1) % len(colors)
                        settings["snake_color"] = colors[current_color_idx]
                    elif selected == 1: settings["grid"] = not settings["grid"]
                    elif selected == 2: settings["sound"] = not settings["sound"]

def menu():
    create_tables()
    while True:
        screen.fill((0,0,0))
        screen.blit(font.render("1. Play", True, (255,255,255)), (200, 200))
        screen.blit(font.render("2. Leaderboard", True, (255,255,255)), (200, 260))
        screen.blit(font.render("3. Settings", True, (255,255,255)), (200, 320))
        screen.blit(font.render("4. Quit", True, (255,255,255)), (200, 380))
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT: sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_1:
                    user = input_name()
                    while run_game(user) == "retry": pass
                if e.key == pygame.K_2: show_leaderboard()
                if e.key == pygame.K_3: settings_menu()
                if e.key == pygame.K_4: sys.exit()

if __name__ == "__main__":
    menu()