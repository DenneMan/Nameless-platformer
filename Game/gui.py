import pygame
import engine

class GUI():
    def __init__(self):
        self.enemies = []
        for e in engine.entities:
            if e.name == "player":
                self.player = e
            if e.name == "enemy":
                self.enemies.append(e)
    def update(self, surface, offset):
        self.enemies = []
        for e in engine.entities:
            if e.name == "player":
                self.player = e
            if e.name == "enemy":
                self.enemies.append(e)
        #player health
        player_health_percentage = self.player.controller.health / self.player.controller.max_health
        pygame.draw.rect(surface, (27, 27, 27), pygame.Rect((self.player.collider.l + self.player.collider.w/2) + offset.x - 83, (self.player.collider.t) + offset.y - 13, 166, 26))
        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect((self.player.collider.l + self.player.collider.w/2) + offset.x - 80, (self.player.collider.t) + offset.y - 10, 160*player_health_percentage, 20))

        #enemy health
        for e in self.enemies:
            health_percentage = e.controller.health / e.controller.max_health
            pygame.draw.rect(surface, (27, 27, 27), pygame.Rect((e.collider.l + e.collider.w/2) + offset.x - 83, (e.collider.t) + offset.y - 13, 166, 26))
            pygame.draw.rect(surface, (255, 0, 0), pygame.Rect((e.collider.l + e.collider.w/2) + offset.x - 80, (e.collider.t) + offset.y - 10, 160*health_percentage, 20))
        #dash bar