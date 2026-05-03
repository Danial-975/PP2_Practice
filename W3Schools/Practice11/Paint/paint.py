import pygame
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pygame Paint Pro")
    clock = pygame.time.Clock()
    
    font = pygame.font.SysFont("Arial", 18, bold=True)
    
    radius = 2
    color_mode = 'blue'
    tool = 'brush'
    
    points = [] 
    shapes = [] 
    drawing = False
    start_pos = None

    while True:
        screen.fill((255, 255, 255))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: color_mode = 'red'
                elif event.key == pygame.K_g: color_mode = 'green'
                elif event.key == pygame.K_b: color_mode = 'blue'
                
                elif event.key == pygame.K_1: tool = 'brush'
                elif event.key == pygame.K_2: tool = 'rect'
                elif event.key == pygame.K_3: tool = 'circle'
                elif event.key == pygame.K_4: tool = 'square'
                elif event.key == pygame.K_5: tool = 'right_triangle'
                elif event.key == pygame.K_6: tool = 'equilateral_triangle'
                elif event.key == pygame.K_7: tool = 'rhombus'
                elif event.key == pygame.K_e: 
                    tool = 'brush'
                    color_mode = 'eraser'

            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                start_pos = event.pos
                if event.button == 4: radius = min(100, radius + 1)
                if event.button == 5: radius = max(1, radius - 1)

            if event.type == pygame.MOUSEBUTTONUP:
                if tool != 'brush' and drawing:
                    shapes.append((tool, color_mode, start_pos, event.pos, radius))
                drawing = False

            if event.type == pygame.MOUSEMOTION and drawing:
                if tool == 'brush':
                    points.append((event.pos, radius, color_mode))

        for s_type, s_color, s_start, s_end, s_width in shapes:
            draw_shape(screen, s_type, s_color, s_start, s_end, s_width)

        for pos, r, mode in points:
            pygame.draw.circle(screen, get_color(mode), pos, r)

        if drawing and tool != 'brush':
            draw_shape(screen, tool, color_mode, start_pos, pygame.mouse.get_pos(), radius, preview=True)

        pygame.draw.rect(screen, (230, 230, 230), (0, 0, 800, 45))
        pygame.draw.line(screen, (150, 150, 150), (0, 45), (800, 45), 2)

        status_text = (f"Tool: {tool.replace('_', ' ').upper()} (1-7, E) | "
                       f"Color: {color_mode.upper()} (R, G, B) | "
                       f"Size: {radius}")
        
        text_surface = font.render(status_text, True, (50, 50, 50))
        screen.blit(text_surface, (15, 12))

        pygame.display.flip()
        clock.tick(60)

def get_color(mode):
    colors = {'red': (255, 0, 0), 'green': (0, 255, 0), 'blue': (0, 0, 255), 'eraser': (255, 255, 255)}
    return colors.get(mode, (0, 0, 0))

def draw_shape(screen, tool, mode, start, end, width, preview=False):
    color = get_color(mode)
    draw_width = 2 if preview else width
    x1, y1 = start
    x2, y2 = end
    dx, dy = x2 - x1, y2 - y1

    if tool == 'rect':
        pygame.draw.rect(screen, color, (min(x1, x2), min(y1, y2), abs(dx), abs(dy)), draw_width)
        
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

if __name__ == "__main__":
    main()