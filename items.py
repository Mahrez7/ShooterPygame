import pygame
from random import randint

class Item(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('assets/health.png'),(50,50))
        self.rect = self.image.get_rect()
        self.rect.x= randint(100,1000)
        self.rect.y = 530
        self.game = game
    def add_health(self):
        if self.game.check_collision(self, self.game.all_players) and self.game.player.health <self.game.player.max_health:
            self.game.player.health +=20
            self.image = pygame.image.load('assets/image-vide.png')