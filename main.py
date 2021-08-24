import pygame
from math import ceil
from game import Game

#initialize the pygame modules
pygame.init()

#fps
clock = pygame.time.Clock()
FPS = 60

#prepare the icon
icon = pygame.image.load('assets/banner.png')
icon = pygame.transform.scale(icon, (50, 50))

#create and setup the window
pygame.display.set_caption('Comet Fall Game')
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((1080,720))

#print the background, banner, play button
background = pygame.image.load('assets/bg.jpg')
banner = pygame.image.load('assets/banner.png')
banner = pygame.transform.scale(banner,(500,500))
banner_rect = banner.get_rect()
banner_rect.x = ceil(screen.get_width()/4)
play_button = pygame.image.load('assets/button.png')
play_button = pygame.transform.scale(play_button, (400,150))
play_button_rect = play_button.get_rect()
play_button_rect.x = ceil(screen.get_width()/3.33)
play_button_rect.y = ceil(screen.get_height()/2)

#create the game object
game = Game()
running = True

#game loop
while running:
    screen.blit(background,(0,-200))
    clock.tick(FPS)

    if game.is_playing:
        game.update(screen)
    else :
        screen.blit(play_button, play_button_rect)
        screen.blit(banner,banner_rect)
    pygame.display.flip()

    #events gestion
    for event in pygame.event.get():
        #if the user closes the window
        if event.type == pygame.QUIT:
            exit()
        #if a key is pressed
        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True
            if event.key == pygame.K_SPACE:
                    game.player.launch_projectile()
            if event.key == 13 and game.mega_projectile_available:
                game.player.launch_super_projectile()
                game.mega_projectile_available=False
        #if a key stops being pressed
        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False
        #if the user clicks
        elif event.type == pygame.MOUSEBUTTONDOWN:
            game.sound_manager.play('click')
            if play_button_rect.collidepoint(event.pos):
                game.is_playing = True
            elif game.pause_menu.button_rect.collidepoint(event.pos):
                game.is_paused = True
        clock.tick(FPS)