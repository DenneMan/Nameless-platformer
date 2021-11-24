import pygame

display = pygame.display.set_mode((10, 10))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            print(pygame.key.name(event.key))