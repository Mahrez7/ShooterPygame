from typing import Iterable, Iterator
import pygame

class Pause:
    def __init__(self, game):
        #create default state
        self.menu=PauseMenu(game)
        self.helping=False
        self.exitting=False

        #create pause button
        self.button = pygame.image.load('assets/pause-solid.png')
        self.button = pygame.transform.scale(self.button, (50, 50))
        self.button_rect = self.button.get_rect()
        self.button_rect.x = 10
        self.button_rect.y = 10

        self.game = game

        #create the pause menu items
        self.help_button = MenuItem(game,'Help',(500,150))
        self.continue_button = MenuItem(game, 'Continue', (500,300))
        self.exit_button = MenuItem(game,'Exit Game', (500,450))

        self.help_message = self.game.fonts['Montserrat'].render('Type arrows left and right to move and space to attack.', True, (255,255,255))

        #create buttons
        self.confirm_exit_button = ButtonImage('assets/ok.png',400,300)
        self.cancel_exit_button=ButtonImage('assets/times-solid.png',600,300)
        self.cancel_exit_button.image=pygame.transform.scale(self.cancel_exit_button.image, (35, 51))
        self.return_button = pygame.image.load('assets/back.png')
        self.return_button = pygame.transform.scale(self.return_button, (25, 51))
        self.return_button_rect = self.return_button.get_rect()
        self.return_button_rect.x=self.return_button_rect.y=50


    def pause(self, screen:pygame.Surface):
        screen.blit(self.continue_button.content, self.continue_button.rect)
        screen.blit(self.help_button.content,self.help_button.rect)
        screen.blit(self.exit_button.content,self.exit_button.rect)
    def help(self, screen):
        screen.blit(self.return_button,self.return_button_rect)
        screen.blit(self.game.fonts['Ubuntu'].render('Help', True, (255,0,0)), (520, 50))
        screen.blit(self.help_message, (200,150))
    def exit(self, screen):
        screen.blit(self.game.fonts['Ubuntu'].render('Do you want to exit game ?', True, (255,0,0)), (350, 200))
        screen.blit(self.confirm_exit_button.image,self.confirm_exit_button.rect)
        screen.blit(self.cancel_exit_button.image,self.cancel_exit_button.rect)


class PauseMenu():
    def __init__(self,game):
        self.continue_playing = game.fonts['Montserrat'].render('Continue', True, (255,255,255))
        self.help = game.fonts['Montserrat'].render('Help', True, (255,255,255))
        self.exit = game.fonts['Montserrat'].render('Exit', True, (255,255,255))
    def __iter__(self) -> Iterator:
        return [self.continue_playing, self.help,self.exit].__iter__()

class MenuItem():
    def __init__(self,game,  content:str, pos:Iterable):
        self.game = game
        self.content = game.fonts['Ubuntu'].render(content, True, (255,255,255))
        self.rect = self.content.get_rect()
        self.rect.x = pos[0]
        self.rect.y=pos[1]

class ButtonImage():
    def __init__(self, path:str, x, y) -> None:
        self.image = pygame.transform.scale(pygame.image.load(path),(50,50))
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y