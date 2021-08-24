from projectile import MegaProjectile
import pygame
from player import Player
from monster import Mummy, Alien
from comet_event import CometFallEvent
from sound import SoundManager
from pause import Pause
from items import Item

class Game:
    def __init__(self):
        #get the best score
        with open('bestscore','r') as file:
            self.bestscore = int(file.readlines()[0])

        #init the fonts list
        self.fonts = {'Ubuntu' : pygame.font.Font('assets/Ubuntu-Bold.ttf', 30), 'Montserrat' : pygame.font.Font('assets/Montserrat-Light.ttf', 30)}
        
        #set default game context
        self.waiting_steps = 3
        self.available_items = pygame.sprite.Group()
        self.mega_projectile_available = False
        self.score = 0
        self.is_playing = False
        self.is_paused = False
        self.pressed = {}
        self.mummies_number = 2
        self.aliens_number = 1
        self.comet_event = CometFallEvent(self)
        self.sound_manager = SoundManager()
        self.pause_menu = Pause(self)
        self.step_finished = 0

        
        #init the player and monsters
        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
        self.all_players.add(self.player)
        self.all_monsters =pygame.sprite.Group()
        self.spawn_monster(Mummy)
        self.spawn_monster(Mummy)
        self.spawn_monster(Alien)

    def update(self, screen):
        if self.step_finished>0 and self.step_finished%5 == 0:
            self.mega_projectile_available=True
        if self.is_paused:
            if self.pause_menu.helping:
                self.pause_menu.help(screen)
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.pause_menu.return_button_rect.collidepoint(event.pos):
                            self.pause_menu.helping = False
            elif self.pause_menu.exitting:
                self.pause_menu.exit(screen)
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.pause_menu.confirm_exit_button.rect.collidepoint(event.pos):
                            self.is_playing=False
                        elif self.pause_menu.cancel_exit_button.rect.collidepoint(event.pos):
                            self.pause_menu.exitting=False
            else:
                self.pause_menu.pause(screen)
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.pause_menu.continue_button.rect.collidepoint(event.pos):
                            self.is_paused = False
                        elif self.pause_menu.help_button.rect.collidepoint(event.pos):
                            self.pause_menu.helping=True
                        elif self.pause_menu.exit_button.rect.collidepoint(event.pos):
                            self.pause_menu.exitting = True
        else:
            #check the items
            if self.step_finished-6%self.waiting_steps == 0 and self.step_finished-6/self.waiting_steps > len(self.available_items):
                    self.available_items.add(Item(self))
            #print pause button
            screen.blit(self.pause_menu.button, self.pause_menu.button_rect)
            #print score and bestscore
            score_text= self.fonts['Ubuntu'].render(f"Score : {self.score}", 1, (255,0,0))
            screen.blit(score_text, (80,20))
            bestscore_text = self.fonts['Ubuntu'].render(f'Best Score : {self.bestscore}', 1, (255,0,0))
            screen.blit(bestscore_text, (80,70))

            if self.mega_projectile_available:
                screen.blit(MegaProjectile(self.player).image, (900,50))

            #print the player and the monsters and the event progress, and the items
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
            for item in self.available_items:
                screen.blit(item.image, item.rect)
                item.add_health()
            self.player.all_projectiles.draw(screen)
            self.all_monsters.draw(screen)
            self.comet_event.all_comets.draw(screen)

            #move the player
            if self.pressed.get(pygame.K_RIGHT) and self.player.rect.x < screen.get_width() - self.player.rect.width:
                self.player.move_right()
            elif self.pressed.get(pygame.K_LEFT) and self.player.rect.x > 0:
                self.player.move_left()
                
    def game_over(self):
        self.sound_manager.play('game_over')
        if self.score > self.bestscore:
            file = open('bestscore','w')
            file.write(str(self.score))
            file.close()
        self.__init__()


    def spawn_monster(self, monster_class_name):
        self.all_monsters.add(monster_class_name.__call__(self))


    def check_collision(self, sprite,group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite .collide_mask)

        
    def add_score(self, points=10):
        self.score += points