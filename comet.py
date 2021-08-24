import pygame
import random
from monster import Mummy
from monster import Alien
class Comet(pygame.sprite.Sprite):
    def __init__(self, comet_event):
        super().__init__()
        self.velocity = random.randint(3,10)
        self.attack = 20
        self.image = pygame.image.load('assets/comet.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(20,800)
        self.rect.y = -random.randint(0,800)
        self.comet_event = comet_event
    def remove(self):
        self.comet_event.all_comets.remove(self)
        if len(self.comet_event.all_comets) == 0:
            self.comet_event.reset_percent()
            self.comet_event.game.mummies_number += 1
            self.comet_event.game.aliens_number += 0.5
            self.comet_event.game.step_finished+=1
            for i in range(0,self.comet_event.game.mummies_number):
                self.comet_event.game.spawn_monster(Mummy)
            for i in range(0,self.comet_event.game.mummies_number):
                self.comet_event.game.spawn_monster(Alien)
    def fall(self):
        self.rect.y += self.velocity
        if self.rect.y >=500:
            self.remove()
            if len(self.comet_event.all_comets) == 0:
                self.comet_event.fall_mode = False
                self.comet_event.reset_percent()
        if self.comet_event.game.check_collision(self,self.comet_event.game.all_players):
            self.remove()
            self.comet_event.game.player.damage(self.attack)
            self.comet_event.game.sound_manager.play('shoot')