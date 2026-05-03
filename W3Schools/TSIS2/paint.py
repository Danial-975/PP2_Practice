import pygame
from datetime import datetime
from tools import get_color, flood_fill, draw_shape

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pygame Paint Pro")
    
    canvas = pygame.Surface((800, 600))
    canvas.fill((255, 255, 255))
    
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18, bold=True)
    
    radius = 2 
    color_mode = 'blue'
    tool = 'pencil' 
    drawing = False
    start_pos = None
    
    text_active = False
    text_content = ""
    text_pos = (0,0)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        current_color = get_color(color_mode)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: color_mode = 'red'
                elif event.key == pygame.K_g: color_mode = 'green'
                elif event.key == pygame.K_b: color_mode = 'blue'
                elif event.key == pygame.K_0: color_mode = 'eraser'
                
                elif event.key == pygame.K_p: tool = 'pencil'
                elif event.key == pygame.K_l: tool = 'line'
                elif event.key == pygame.K_f: tool = 'fill'
                elif event.key == pygame.K_t: tool = 'text'
                
                elif event.key == pygame.K_1: tool = 'rect'
                elif event.key == pygame.K_2: tool = 'circle'
                elif event.key == pygame.K_3: tool = 'square'
                elif event.key == pygame.K_4: tool = 'right_triangle'
                elif event.key == pygame.K_5: tool = 'equilateral_triangle'
                elif event.key == pygame.K_6: tool = 'rhombus'
                
                if event.key == pygame.K_z: radius = 2
                elif event.key == pygame.K_x: radius = 5
                elif event.key == pygame.K_c: radius = 10
                
                if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    fname = f"paint_{datetime.now().strftime('%H%M%S')}.png"
                    pygame.image.save(canvas, fname)

                if text_active:
                    if event.key == pygame.K_RETURN:
                        t_surf = font.render(text_content, True, current_color)
                        canvas.blit(t_surf, text_pos)
                        text_active = False
                    elif event.key == pygame.K_ESCAPE:
                        text_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        text_content = text_content[:-1]
                    else:
                        text_content += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                if tool == 'fill':
                    flood_fill(canvas, *event.pos, current_color)
                elif tool == 'text':
                    text_active = True
                    text_pos = event.pos
                    text_content = ""
                else:
                    drawing = True
                    start_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                if drawing and tool != 'pencil':
                    draw_shape(canvas, tool, current_color, start_pos, event.pos, radius)
                drawing = False

            if event.type == pygame.MOUSEMOTION and drawing:
                if tool == 'pencil':
                    pygame.draw.line(canvas, current_color, start_pos, event.pos, radius)
                    start_pos = event.pos

        screen.fill((200, 200, 200))
        screen.blit(canvas, (0, 0)) 

        if drawing and tool != 'pencil':
            draw_shape(screen, tool, current_color, start_pos, mouse_pos, radius, preview=True)
        if text_active:
            screen.blit(font.render(text_content + "|", True, current_color), text_pos)
        pygame.draw.rect(screen, (230, 230, 230), (0, 0, 800, 45))
        status = f"Tool: {tool.upper()} | Color: {color_mode} | Size: {radius}"
        screen.blit(font.render(status, True, (50, 50, 50)), (15, 12))
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()