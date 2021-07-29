import pygame
import discord
from random import randint
from player import Player
from monster import Monster
from monster import Mummy
from monster import Alien
from comet_event import CometFallEvent
from sound import SoundManager
class Game:
    def __init__(self):
        self.font = pygame.font.Font('assets/Ubuntu-Bold.ttf', 30)
        self.score = 0
        self.is_playing = False
        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
        self.all_players.add(self.player)
        self.all_monsters =pygame.sprite.Group()
        self.pressed = {}
        self.mummies_number = 2
        self.aliens_number = 1
        self.spawn_monster(Mummy)
        self.spawn_monster(Mummy)
        self.spawn_monster(Alien)
        self.comet_event = CometFallEvent(self)
        self.sound_manager = SoundManager()
    def update(self, screen):
        score_text= self.font.render(f"Score : {self.score}", 1, (255,0,0))
        screen.blit(score_text, (20,20))
        screen.blit(self.player.image, self.player.rect)
        self.player.update_health_bar(screen)
        self.comet_event.update_bar(screen)
        self.player.update_animation()
        for projectile in self.player.all_projectiles:
            projectile.move()
        for monster in self.all_monsters:
            monster.forward()
            monster.update_health_bar(screen)
            monster.update_animation()
        for comet in self.comet_event.all_comets:
            comet.fall()
        self.player.all_projectiles.draw(screen)
        self.all_monsters.draw(screen)
        self.comet_event.all_comets.draw(screen)
        if self.pressed.get(pygame.K_RIGHT) and self.player.rect.x < screen.get_width() - self.player.rect.width:
            self.player.move_right()
        elif self.pressed.get(pygame.K_LEFT) and self.player.rect.x > 0:
            self.player.move_left()
    def game_over(self):
        self.sound_manager.play('game_over')
        self.is_playing = False
        for monster in self.all_monsters:
            monster.remove()
            monster.rect.x = 1000 + randint(0,100)
        self.player.health = 100
        self.score = 0
    def spawn_monster(self, monster_class_name):
        self.all_monsters.add(monster_class_name.__call__(self))
    def check_collision(self, sprite,group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite .collide_mask)
    def add_score(self, points=10):
        self.score += points