import pygame

def draw_text(surface, text, size, x, y, color=(0,0,0)):
    font = pygame.font.SysFont("Verdana", size)
    img = font.render(str(text), True, color)
    rect = img.get_rect(center=(x, y))
    surface.blit(img, rect)

def button(surface, text, x, y, w, h, inactive_col, active_col):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x - w/2, y - h/2, w, h)
    
    action = False
    if rect.collidepoint(mouse):
        pygame.draw.rect(surface, active_col, rect)
        if click[0] == 1:
            action = True
    else:
        pygame.draw.rect(surface, inactive_col, rect)
    
    draw_text(surface, text, 20, x, y)
    return action