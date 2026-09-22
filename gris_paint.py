import pygame
import sys
import os
import time
import json
pygame.init()
pygame.mixer.init()
pygame.event.get()
base_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
pygame.mouse.set_visible(False)
canvas_rect = pygame.Rect(65, 0, 128, 128)
menu_button_rect = pygame.Rect(233, 104, 32, 32)
screen = pygame.display.set_mode((256, 128))
clock = pygame.time.Clock()
menu = False
draw_circle = False
x_y_list = []

pos = [129, 64]
speed = 1
cursor_img = pygame.transform.smoothscale(pygame.image.load(os.path.join(base_dir, "files/imgs/cursor.png")).convert_alpha(), (10, 10))
draw_surface = pygame.Surface((canvas_rect.width, canvas_rect.height))
draw_surface.fill((255, 255, 255))
button_surface = pygame.Surface((menu_button_rect.width, menu_button_rect.height))
button_surface.fill((200, 50, 50))
screen.fill((0, 0, 0))
draw_surface.fill((100, 100, 100))
font = pygame.font.SysFont("Arial", 18)
pygame.display.set_caption("GRIS")
pygame.mixer.music.load(os.path.join(base_dir, "files/sound/view1.wav"))
pygame.mixer.music.play()
def save_paint_data(xylist=[], pos=[129, 64]):
    data = {"pos": pos, "x_y_list": xylist}
    with open("draw.json", 'w', encoding='utf-8', errors='ignore') as f:
        json.dump(data, f)
    return True
def draw_menu():
    overlay = draw_surface.copy()
    overlay = pygame.transform.scale(overlay, (256, 128))
    screen.blit(overlay, (0, 0))
    menu_options = ["SAVE AND QUIT?", "A Cancel", "B Save And Quit", "C Reset"]
    for i, text in enumerate(menu_options):
        menu_text = font.render(text, True, (200, 200, 200))
        screen.blit(menu_text, (0, 0 + (i * 20)))
    pygame.display.flip()
def redraw_x_y_list():
    global x_y_list
    
    lock = open("redraw.lock", 'w')
    log = open("log.txt", 'w', encoding="utf-8", errors='ignore')
    for pos in x_y_list:
        log.write(f"{pos[0]} {pos[1]}\n")
    draw_surface_sc = pygame.Surface((canvas_rect.width, canvas_rect.height), pygame.SRCALPHA)
    x_y_list_redraw_menu(canvas_rect, menu_button_rect, screen, x_y_list, draw_surface_sc, button_surface)
    pygame.image.save(draw_surface_sc, "gris_draw.png")
    pygame.event.get()
    pygame.mixer.music.load(os.path.join(base_dir, "files/sound/screammachine.wav"))
    pygame.mixer.music.play(loops=-1)
    
    for x, y in x_y_list:
        pygame.event.get()
        pos = (x, y)
        screen.blit(cursor_img, pos)
        pygame.display.flip()
        clock.tick(60)
        time.sleep(0.011)
    pygame.mixer.music.stop()
    lock.close()
    log.close()

    os.remove("redraw.lock")
    if os.path.isfile("autoexec.bat"):
        os.system("start autoexec.bat")
    return
def draw():
    if canvas_rect.collidepoint(pos) and not menu:
         
        rel_x = pos[0] - canvas_rect.x
        rel_y = pos[1] - canvas_rect.y
        x_y_list.append((pos[0], pos[1]))
        pygame.draw.circle(draw_surface, (0, 0, 0), (rel_x, rel_y), 5)
        
    save_paint_data(x_y_list, pos)
    return

def x_y_list_redraw_menu(canvas_rect, menu_button_rect, screen, x_y_list, draw_surface, button_surface):
    lock = open("redraw_x_y.lock", 'w')
    for x, y in x_y_list:
        screen.blit(draw_surface, (canvas_rect.x, canvas_rect.y))
        screen.blit(button_surface, (menu_button_rect.x, menu_button_rect.y))
        rel_x = x - canvas_rect.x
        rel_y = y - canvas_rect.y
        pygame.draw.circle(draw_surface, (0, 0, 0), (rel_x, rel_y), 5)
        pygame.display.flip()
        #clock.tick(60)
    lock.close()
    os.remove("redraw_x_y.lock")
    return

if os.path.isfile("draw.json"):
    with open("draw.json", 'r', encoding='utf-8', errors='ignore') as f:
        json_data = json.load(f)
        x_y_list = json_data["x_y_list"]
        pos = json_data["pos"]
    x_y_list_redraw_menu(canvas_rect, menu_button_rect, screen, x_y_list, draw_surface, button_surface)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #redraw_x_y_list()
            save_paint_data(x_y_list, pos)
            pygame.quit()
            sys.exit()
    draw_circle = False
    if pos[0] > screen.get_size()[0]:
        pos = [129, 64]
    if pos[1] > screen.get_size()[1]:
        pos = [129, 64]
    keys = pygame.key.get_pressed()
    if not canvas_rect.collidepoint(pos) or not menu_button_rect.collidepoint(pos) and not menu:
        screen.fill((0, 0, 0))
    if not menu:
        if keys[pygame.K_LEFT]:
            pos[0] -= speed
            draw()
        if keys[pygame.K_RIGHT]:
            pos[0] += speed
            draw()
        if keys[pygame.K_UP]:
            pos[1] -= speed
            draw()
        if keys[pygame.K_DOWN]:
            pos[1] += speed
            draw()
    else:
        if keys[pygame.K_a]:
            screen.fill((0, 0, 0))
            draw_surface.fill((255, 255, 255))
            button_surface.fill((200, 50, 50))
            save_paint_data(x_y_list, pos)
            draw_surface.fill((100, 100, 100))
            pygame.display.flip()
            x_y_list_redraw_menu(canvas_rect, menu_button_rect, screen, x_y_list, draw_surface, button_surface)
            pygame.mixer.music.load(os.path.join(base_dir, "files/sound/button24.wav"))
            pygame.mixer.music.play()
            menu = False
        if keys[pygame.K_b]:
            screen.fill((0, 0, 0))
            draw_surface.fill((255, 255, 255))
            button_surface.fill((200, 50, 50))
            save_paint_data([])
            draw_surface.fill((100, 100, 100))
            pygame.display.flip()
            x_y_list_redraw_menu(canvas_rect, menu_button_rect, screen, x_y_list, draw_surface, button_surface)
            pygame.mixer.music.load(os.path.join(base_dir, "files/sound/button24.wav"))
            pygame.mixer.music.play()
            menu = False
            time.sleep(0.1)
            redraw_x_y_list()
            os.remove("draw.json")
            pygame.quit()
            sys.exit()
        if keys[pygame.K_c]:
            screen.fill((0, 0, 0))
            draw_surface.fill((255, 255, 255))
            button_surface.fill((200, 50, 50))
            save_paint_data([])
            draw_surface.fill((100, 100, 100))
            pygame.display.flip()
            x_y_list = []
            pygame.mixer.music.load(os.path.join(base_dir, "files/sound/button24.wav"))
            pygame.mixer.music.play()
            menu = False
            pos = [129, 64]

    if pygame.key.get_focused():
                keys_just_pressed = pygame.key.get_just_pressed()
                if keys_just_pressed[pygame.K_m]:
                    pygame.mixer.music.load(os.path.join(base_dir, "files/sound/view1.wav"))
                    pygame.mixer.music.play()
    if menu:
        continue


    #print(pygame.mouse.get_pos())
    screen.blit(draw_surface, (canvas_rect.x, canvas_rect.y))
    screen.blit(button_surface, (menu_button_rect.x, menu_button_rect.y))
    if menu_button_rect.collidepoint(pos):
        pos[0] -= 4
        pos[1] -= 4
        save_paint_data(x_y_list, pos)
        pygame.mixer.music.load(os.path.join(base_dir, "files/sound/button24.wav"))
        pygame.mixer.music.play()
        draw_menu()
        menu = True

    
    screen.blit(cursor_img, pos)
    
    pygame.display.flip()
    clock.tick(60)