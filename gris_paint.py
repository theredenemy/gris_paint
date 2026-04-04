import pygame
import sys
import os
import time
pygame.init()
pygame.mixer.init()
pygame.event.get()
base_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
#pygame.mouse.set_visible(False)
canvas_rect = pygame.Rect(65, 0, 128, 128)
menu_button_rect = pygame.Rect(233, 104, 32, 32)
screen = pygame.display.set_mode((256, 128))
clock = pygame.time.Clock()
menu = False
x_y_list = []
rel_list = []
pos = [129, 64]
speed = 1
cursor_img = pygame.transform.smoothscale(pygame.image.load(os.path.join(base_dir, "files/imgs/cursor.png")).convert_alpha(), (10, 10))
draw_surface = pygame.Surface((canvas_rect.width, canvas_rect.height))
draw_surface.fill((255, 255, 255))
button_surface = pygame.Surface((menu_button_rect.width, menu_button_rect.height))
button_surface.fill((200, 50, 50))
screen.fill((0, 0, 0))
draw_surface.fill((100, 100, 100))
pygame.display.set_caption("GRIS")
pygame.mixer.music.load(os.path.join(base_dir, "files/sound/view1.wav"))
pygame.mixer.music.play()
def redraw_x_y_list():
    global x_y_list
    lock = open("redraw.lock", 'w')
    pygame.event.get()
    pygame.mixer.music.load(os.path.join(base_dir, "files/sound/screammachine.wav"))
    pygame.mixer.music.play(loops=-1)
    
    for x, y in x_y_list:
        pygame.event.get()
        pos = (x, y)
        screen.blit(cursor_img, pos)
        pygame.display.flip()
        clock.tick(60)
        time.sleep(0.01)
    pygame.mixer.music.stop()
    lock.close()
    os.remove("redraw.lock")
    return
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            redraw_x_y_list()
            pygame.quit()
            sys.exit()
    if pos[0] > screen.get_size()[0]:
        pos = [129, 64]
    if pos[1] > screen.get_size()[1]:
        pos = [129, 64]
    keys = pygame.key.get_pressed()
    if not canvas_rect.collidepoint(pos) or not menu_button_rect.collidepoint(pos):
        screen.fill((0, 0, 0))
    if not menu:
        if keys[pygame.K_LEFT]:
            pos[0] -= speed
        if keys[pygame.K_RIGHT]:
            pos[0] += speed
        if keys[pygame.K_UP]:
            pos[1] -= speed
        if keys[pygame.K_DOWN]:
            pos[1] += speed
    print(pygame.mouse.get_pos())
    screen.blit(draw_surface, (canvas_rect.x, canvas_rect.y))
    screen.blit(button_surface, (menu_button_rect.x, menu_button_rect.y))
    if pygame.key.get_focused():
            keys_just_pressed = pygame.key.get_just_pressed()
            if keys_just_pressed[pygame.K_m]:
                pygame.mixer.music.load(os.path.join(base_dir, "files/sound/view1.wav"))
                pygame.mixer.music.play()
    if canvas_rect.collidepoint(pos):
         if keys[pygame.K_d]:
            rel_x = pos[0] - canvas_rect.x
            rel_y = pos[1] - canvas_rect.y
            x_y_list.append((pos[0], pos[1]))
            pygame.draw.circle(draw_surface, (0, 0, 0), (rel_x, rel_y), 5)
    
    screen.blit(cursor_img, pos)
    
    pygame.display.flip()
    clock.tick(60)