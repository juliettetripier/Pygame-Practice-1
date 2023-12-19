import pygame, sys
from settings import *

class Game:
    def __init__(self):

        pygame.init() #starts pygame
        #create your display
        self.screen = pygame.display.set_mode((width, height))
        #create clock object
        self.clock = pygame.time.Clock()
        #set game title
        pygame.display.set_caption('Practice Project 1')
        #set up font - pygame.font.Font(font type, font size)
        self.test_font = pygame.font.Font('../font/Pixeltype.ttf', 50)

        self.sky_surface = pygame.image.load('../graphics/Sky.png').convert()
        self.ground_surface = pygame.image.load('../graphics/ground.png').convert()

        self.snail_surface = pygame.image.load('../graphics/snail/snail1.png').convert_alpha()
        self.snail_rect = self.snail_surface.get_rect(midbottom = (600, 300))

        self.player_surface = pygame.image.load('../graphics/player/player_walk_1.png').convert_alpha()
        #set up the player rectangle using get_rect() to draw a rectangle around the surface
        self.player_rect = self.player_surface.get_rect(midbottom = (80,300))

        #for rendering fonts: render(text info, anti-alias boolean, color)
        self.text_surface = self.test_font.render('My game', False, 'Black')

    def run(self):
        #set up a loop to keep your game running forever, until you reach a quit event
        #in your loop, draw all your elements and update everything
        while True:
            #set up event loop - get events and loop through each
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.screen.fill('black')
            # blit = "block image transfer" - put a surface on another surface
            # two arguments - blit(surface to place it on, position)
            self.screen.blit(self.sky_surface, (0,0))
            self.screen.blit(self.ground_surface, (0, 300))

            self.snail_rect.x -= 4
            if self.snail_rect.right < 0:
                self.snail_rect.left = 800
            self.screen.blit(self.snail_surface, self.snail_rect)

            self.player_rect.left += 1
            self.screen.blit(self.player_surface, self.player_rect)

            self.screen.blit(self.text_surface, (300,50))
            #update the display surface so anything drawn inside the while loop is displayed
            pygame.display.update()
            #set the maximum framerate to make sure the game doesn't run too fast
            self.clock.tick(fps)

if __name__ == '__main__':
    game = Game()
    game.run()