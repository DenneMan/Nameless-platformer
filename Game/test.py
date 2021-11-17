import pygame,engine

pygame.init()

display = pygame.display.set_mode((500, 500))

healthbar = engine.load_spritesheet('assets\\sprites\\Healthbar.png', 38, 9)
temp = []
for i in healthbar:
    temp.append(pygame.transform.scale(i, (38*4, 9*4)))
healthbar = temp

progress = 0
while True:
    dt = engine.deltaTime()
    pygame.event.get()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        break
    if keys[pygame.K_UP]:
        progress += dt
        progress = min(1, progress)
    if keys[pygame.K_DOWN]:
        progress -= dt
        progress = max(0, progress)

    display.fill((0, 0, 0))

    display.blit(healthbar[0], (0, 0))
    pygame.draw.rect(display, (193, 42, 68), pygame.Rect(12, 4, 132 * progress, 28))

    display.blit(healthbar[1], (132 * progress - 12, 0))

    display.blit(healthbar[2], (0, 0))

    pygame.display.update()
    
