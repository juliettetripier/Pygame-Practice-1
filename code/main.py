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
            #update the display surface so anything drawn inside the while loop is displayed
            pygame.display.update()
            #set the maximum framerate to make sure the game doesn't run too fast
            self.clock.tick(fps)

if __name__ == '__main__':
    game = Game()
    game.run()