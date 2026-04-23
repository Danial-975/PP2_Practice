import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pygame Paint Pro")
    clock = pygame.time.Clock()
    
    font = pygame.font.SysFont("Arial", 18, bold=True)
    
    radius = 15
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
                elif event.key == pygame.K_e: 
                    tool = 'brush'
                    color_mode = 'eraser'

            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                start_pos = event.pos
                if event.button == 4: radius = min(100, radius + 1)
                if event.button == 5: radius = max(1, radius - 1)

            if event.type == pygame.MOUSEBUTTONUP:
                if tool in ['rect', 'circle'] and drawing:
                    shapes.append((tool, color_mode, start_pos, event.pos, radius))
                drawing = False

            if event.type == pygame.MOUSEMOTION and drawing:
                if tool == 'brush':
                    points.append((event.pos, radius, color_mode))

        for s_type, s_color, s_start, s_end, s_width in shapes:
            draw_shape(screen, s_type, s_color, s_start, s_end, s_width)

        for pos, r, mode in points:
            pygame.draw.circle(screen, get_color(mode), pos, r)

        if drawing and tool in ['rect', 'circle']:
            draw_shape(screen, tool, color_mode, start_pos, pygame.mouse.get_pos(), radius, preview=True)

        pygame.draw.rect(screen, (230, 230, 230), (0, 0, 800, 40))
        pygame.draw.line(screen, (150, 150, 150), (0, 40), (800, 40), 2)

        status_text = (f"Tool: {tool.upper()} (1-3, E) | "
                       f"Color: {color_mode.upper()} (R, G, B) | "
                       f"Size: {radius} (Scroll)")
        
        text_surface = font.render(status_text, True, (50, 50, 50))
        screen.blit(text_surface, (15, 10))

        pygame.display.flip()
        clock.tick(60)

def get_color(mode):
    if mode == 'red': return (255, 0, 0)
    if mode == 'green': return (0, 255, 0)
    if mode == 'blue': return (0, 0, 255)
    if mode == 'eraser': return (255, 255, 255)
    return (0, 0, 0)

def draw_shape(screen, tool, mode, start, end, width, preview=False):
    color = get_color(mode)
    draw_width = 2 if preview else width
    
    x1, y1 = start
    x2, y2 = end
    
    if tool == 'rect':
        rect_x, rect_y = min(x1, x2), min(y1, y2)
        rect_w, rect_h = abs(x1 - x2), abs(y1 - y2)
        if rect_w > 0 and rect_h > 0:
            pygame.draw.rect(screen, color, (rect_x, rect_y, rect_w, rect_h), draw_width)
        
    elif tool == 'circle':
        r = int(((x1 - x2)**2 + (y1 - y2)**2)**0.5)
        if r > 0:
            pygame.draw.circle(screen, color, start, r, draw_width)

main()