import pygame
import os

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Danial's Music Player")

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GREEN = (0, 255, 127)
GRAY = (150, 150, 150)

font_main = pygame.font.SysFont("Arial", 24)
font_small = pygame.font.SysFont("Arial", 18)

music_dir = "music/"
if not os.path.exists(music_dir):
    os.makedirs(music_dir)

songs = [f for f in os.listdir(music_dir) if f.endswith(('.mp3', '.wav'))]
current_idx = 0

def play_song(idx):
    if songs:
        try:
            pygame.mixer.music.load(os.path.join(music_dir, songs[idx]))
            pygame.mixer.music.play()
        except pygame.error as e:
            print(f"Ошибка загрузки {songs[idx]}: {e}")

def draw_interface():
    screen.fill(BLACK)
    header = font_main.render("My Playlist", True, WHITE)
    screen.blit(header, (20, 20))

    for i, song in enumerate(songs):
        color = GREEN if i == current_idx else GRAY
        prefix = ">> " if i == current_idx else "   "
        text = font_small.render(f"{prefix}{song}", True, color)
        screen.blit(text, (30, 60 + i * 30))
    
    instr_text = "P: Play | S: Pause | N: Next | B: Back | Q: Quit"
    instr = font_small.render(instr_text, True, WHITE)
    pygame.draw.rect(screen, (50, 50, 50), (0, HEIGHT - 40, WIDTH, 40))
    screen.blit(instr, (20, HEIGHT - 30))

if songs:
    play_song(current_idx)
    pygame.mixer.music.pause()

running = True
is_paused = True

while running:
    draw_interface()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  
                pygame.mixer.music.unpause()
                is_paused = False
            
            elif event.key == pygame.K_s:  
                pygame.mixer.music.pause()
                is_paused = True
            
            elif event.key == pygame.K_n:  
                current_idx = (current_idx + 1) % len(songs)
                play_song(current_idx)
                is_paused = False
            
            elif event.key == pygame.K_b:  
                current_idx = (current_idx - 1) % len(songs)
                play_song(current_idx)
                is_paused = False
                
            elif event.key == pygame.K_q:  
                running = False
    pygame.display.flip()
pygame.quit()