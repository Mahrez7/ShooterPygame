import pygame
class Projectile(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.velocity = 7
        self.player = player
        self.image = pygame.image.load('assets/projectile.png')
        self.image = pygame.transform.scale(self.image,(50,50))
        self.rect = self.image.get_rect()
        self.rect.x = self.player.rect.x + 120
        self.rect.y = self.player.rect.y + 80
        self.origin_image = self.image
        self.angle = 0
    def rotate(self):
        self.angle += 12
        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)
    def remove(self):
        self.player.all_projectiles.remove(self)
    def move(self):
        self.rect.x += self.velocity
        self.rotate()
        for monster in self.player.game.check_collision(self,self.player.game.all_monsters):
            if monster.health > self.player.attack:
                self.remove()
            monster.damage(self.player.attack)
        if self.rect.x > 1080:
            self.remove()

class MegaProjectile(Projectile):
    def __init__(self, player):
        super().__init__(player)
        self.image = pygame.transform.scale(pygame.image.load('assets/projectile.png'), (100, 100))
        self.velocity = 8
        self.player = player
        self.rect = self.image.get_rect()
        self.rect.x = self.player.rect.x+120
        self.rect.y = self.player.rect.y+80
        self.origin_image = self.image
        self.angle=0
    def move(self):
        self.rect.x += self.velocity
        self.rotate()
        for monster in self.player.game.check_collision(self,self.player.game.all_monsters):
            if monster.health > self.player.attack+100:
                self.remove()
            monster.damage(self.player.attack+100)
        if self.rect.x > 1080:
            self.remove()