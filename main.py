import pygame, sys
from random import choice, randint
import os 


def resource_path(relative_path):
    """
    Obtém o caminho absoluto para o recurso, funciona para desenvolvimento e para PyInstaller.
    """
    try:
        
        base_path = sys._MEIPASS
    except Exception:
        
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


pygame.init()
pygame.mixer.init()

score = 0
GRAVITY = 1000 # Gravidade para o salto
pulo_chance = 0.5 # 50% de chance de o pato pular

font = pygame.font.Font(None, 40)

display_surface = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()

# --- CARREGAMENTO DE ASSETS USANDO resource_path() ---
rifle_surface = pygame.image.load(resource_path("assets/rifle.png")).convert_alpha()
rifle_rect = rifle_surface.get_rect()
rifle_rect.y = 500

duck_surface = pygame.image.load(resource_path("assets/duck.png")).convert_alpha()
ducks = []
duck_timer = pygame.USEREVENT + 1
pygame.time.set_timer(duck_timer, 1000)

crosshair_surface = pygame.image.load(resource_path("assets/crosshair.png")).convert_alpha()
crosshair_rect = crosshair_surface.get_rect()

background_surface = pygame.image.load(resource_path("assets/background.png")).convert_alpha()
stall_surface = pygame.image.load(resource_path("assets/stall.png")).convert_alpha()

pygame.mixer.music.load(resource_path("assets/music.ogg"))
pygame.mixer.music.play(-1)
# -----------------------------------------------------

while True:
    deltaTime = clock.tick()/1000

    # check for all events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() # close window
            sys.exit()
        if event.type == duck_timer:
            duck_x = choice([-40,1280+40])
            duck_y = randint(350,500)
            duck_rect = duck_surface.get_frect(center =(duck_x, duck_y))
            
            # Condição para o pato pular
            if randint(0, 100)/100 < pulo_chance:
                duck_jump_speed = -randint(300, 500)
            else:
                duck_jump_speed = 0

            if duck_x == -40:
                duck_direction = pygame.math.Vector2(1,0)
            else:
                duck_direction = pygame.math.Vector2(-1,0)

            duck_speed = randint(200, 600)

            ducks.append({
                'rect': duck_rect,
                'direction': duck_direction,
                'speed': duck_speed,
                'jump_speed': duck_jump_speed,
                'kill': False
            })

    display_surface.fill('white')

    display_surface.blit(background_surface)

    if ducks: 
        for duck in ducks:
            # Movimento do pato (horizontal e vertical)
            
            if duck['jump_speed'] != 0:
                duck['jump_speed'] += GRAVITY * deltaTime
            
            duck['rect'].centerx += duck['direction'].x * duck['speed'] * deltaTime
            duck['rect'].centery += duck['jump_speed'] * deltaTime

            if duck['direction'].x == 1:
                display_surface.blit(duck_surface, duck['rect'])
            else:
                display_surface.blit(pygame.transform.flip(duck_surface, True, False), duck['rect'])

        ducks = [duck for duck in ducks if -100 < duck['rect'].x < 1280+100]

    mouse_x, mouse_y = pygame.mouse.get_pos()
    crosshair_rect.centerx = mouse_x
    crosshair_rect.centery = mouse_y
    display_surface.blit(crosshair_surface, crosshair_rect)

    if ducks: 
        mouse_click = pygame.mouse.get_pressed()[0]
        for duck in ducks:
            if not mouse_click:
                continue

            if duck['rect'].collidepoint(crosshair_rect.center):
                duck['kill'] = True
                score +=1

        ducks = [duck for duck in ducks if not duck['kill']]

    display_surface.blit(stall_surface)

    rifle_rect.x = mouse_x
    display_surface.blit(rifle_surface, rifle_rect)

    text_surf = font.render(f'Your score: {score}', True, 'White')
    text_rect = text_surf.get_rect(center = (1280/ 2, 20))
    display_surface.blit(text_surf, text_rect)
    
    pygame.display.update()
