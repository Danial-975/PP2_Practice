import pygame
import math

def get_color(mode):
    colors = {
        'red': (255, 0, 0), 
        'green': (0, 255, 0), 
        'blue': (0, 0, 255), 
        'eraser': (255, 255, 255), 
        'black': (0, 0, 0)
    }
    return colors.get(mode, (0, 0, 0))

def flood_fill(surface, x, y, new_color):
    target_color = surface.get_at((x, y))
    if target_color == new_color: return
    
    pixels = [(x, y)]
    w, h = surface.get_size()
    while pixels:
        cx, cy = pixels.pop()
        if surface.get_at((cx, cy)) != target_color: continue
        surface.set_at((cx, cy), new_color)
        for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < w and 0 <= ny < h:
                pixels.append((nx, ny))

def draw_shape(screen, tool, color, start, end, width, preview=False):
    draw_width = 1 if preview else width
    x1, y1 = start
    x2, y2 = end
    dx, dy = x2 - x1, y2 - y1

    if tool == 'rect':
        pygame.draw.rect(screen, color, (min(x1, x2), min(y1, y2), abs(dx), abs(dy)), draw_width)
    elif tool == 'line':
        pygame.draw.line(screen, color, start, end, draw_width)
    elif tool == 'circle':
        r = int(math.hypot(dx, dy))
        if r > 0: pygame.draw.circle(screen, color, start, r, draw_width)
    elif tool == 'square':
        side = max(abs(dx), abs(dy))
        sq_x = x1 if x2 > x1 else x1 - side
        sq_y = y1 if y2 > y1 else y1 - side
        pygame.draw.rect(screen, color, (sq_x, sq_y, side, side), draw_width)
    elif tool == 'right_triangle':
        pts = [start, (x1, y2), end]
        pygame.draw.polygon(screen, color, pts, draw_width)
    elif tool == 'equilateral_triangle':
        side = dx
        height = side * math.sqrt(3) / 2
        pts = [start, (x1 + side, y1), (x1 + side/2, y1 - height)]
        pygame.draw.polygon(screen, color, pts, draw_width)
    elif tool == 'rhombus':
        pts = [(x1 + dx/2, y1), (x2, y1 + dy/2), (x1 + dx/2, y2), (x1, y1 + dy/2)]
        pygame.draw.polygon(screen, color, pts, draw_width)