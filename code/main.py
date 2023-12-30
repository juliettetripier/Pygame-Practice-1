import pygame
import sys
from random import randint
from settings import width, height, fps


class Game:
    def display_score(self):
        '''Calculate the current time, draw it onto the screen, and return it.'''
        current_time = int(pygame.time.get_ticks() / 1000) - self.start_time
        score_surface = self.test_font.render(f'Score: {current_time}',False,(64,64,64))
        score_rect = score_surface.get_rect(center = (400, 50))
        score_bg = score_rect.inflate(10,10)
        pygame.draw.rect(self.screen, '#c0e8ec', score_bg)
        self.screen.blit(score_surface, score_rect)
        return current_time
    
    def obstacle_movement(self, obstacle_list):
        if obstacle_list:
            for obstacle_rect in obstacle_list:
                obstacle_rect.x -= 5
                if obstacle_rect.bottom == 300:
                    self.screen.blit(self.snail_surface, obstacle_rect)
                else:
                    self.screen.blit(self.fly_surface, obstacle_rect)
            obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
            return obstacle_list
        return []

    def collisions(self, player, obstacles):
        if obstacles:
            for obstacle_rect in obstacles:
                if player.colliderect(obstacle_rect):
                    return False
        return True
    
    def player_animation(self):
        # play walking animation if character is on floor
        # display jump surface when player is not on floor
        if self.player_rect.bottom < 300:
            self.player_surface = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.player_surface = self.player_walk[int(self.player_index)]

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

        self.game_active = False

        self.start_time = 0
        self.score = 0

        self.sky_surface = pygame.image.load('../graphics/Sky.png').convert()
        self.ground_surface = pygame.image.load('../graphics/ground.png').convert()

        # Obstacles
        # Snail
        self.snail_frame_1 = pygame.image.load('../graphics/snail/snail1.png').convert_alpha()
        self.snail_frame_2 = pygame.image.load('../graphics/snail/snail2.png').convert_alpha()
        self.snail_frames = [self.snail_frame_1, self.snail_frame_2]
        self.snail_frame_index = 0
        self.snail_surface = self.snail_frames[self.snail_frame_index]

        # Fly
        self.fly_frame_1 = pygame.image.load('../graphics/fly/fly1.png').convert_alpha()
        self.fly_frame_2 = pygame.image.load('../graphics/fly/fly2.png').convert_alpha()
        self.fly_frames = [self.fly_frame_1, self.fly_frame_2]
        self.fly_frame_index = 0
        self.fly_surface = self.fly_frames[self.fly_frame_index]

        self.obstacle_rect_list = []

        # Player
        self.player_walk_1 = pygame.image.load('../graphics/player/player_walk_1.png').convert_alpha()
        self.player_walk_2 = pygame.image.load('../graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [self.player_walk_1,self.player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('../graphics/player/jump.png').convert_alpha()

        self.player_surface = self.player_walk[self.player_index]
        self.player_rect = self.player_surface.get_rect(midbottom = (80,300))
        self.player_gravity = 0

        # Intro screen
        self.player_stand = pygame.image.load('../graphics/player/player_stand.png').convert_alpha()
        self.player_stand = pygame.transform.rotozoom(self.player_stand, 0, 2)
        self.player_stand_rect = self.player_stand.get_rect(center = (400,200))

        self.game_name = self.test_font.render('Pixel Runner', False, (111,196,169))
        self.game_name_rect = self.game_name.get_rect(center = (400, 80))

        self.game_message = self.test_font.render('Press space to run', False, (111,196,169))
        self.game_message_rect = self.game_message.get_rect(center = (400, 330))

        # Timer
        self.obstacle_timer = pygame.USEREVENT + 1 # add +1 to each event you add
        pygame.time.set_timer(self.obstacle_timer, 1500)

        self.snail_animation_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(self.snail_animation_timer, 500)

        self.fly_animation_timer = pygame.USEREVENT + 3
        pygame.time.set_timer(self.fly_animation_timer, 200)
    

    def run(self):
        #set up a loop to keep your game running forever, until you reach a quit event
        #in your loop, draw all your elements and update everything
        while True:
            #set up event loop - get events and loop through each
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.game_active:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.player_rect.collidepoint(event.pos):
                            if self.player_rect.bottom == 300:
                                self.player_gravity = -20
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            if self.player_rect.bottom == 300:
                                self.player_gravity = -20
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.game_active = True
                            self.start_time = int(pygame.time.get_ticks() / 1000)

                if self.game_active:
                    if event.type == self.obstacle_timer:
                        if randint(0,2):
                            self.obstacle_rect_list.append(self.snail_surface.get_rect(midbottom = (randint(900,1100),300)))
                        else:
                            self.obstacle_rect_list.append(self.fly_surface.get_rect(midbottom = (randint(900,1100),210)))
                    
                    if event.type == self.snail_animation_timer:
                        if self.snail_frame_index == 0:
                            self.snail_frame_index = 1
                        else:
                            self.snail_frame_index = 0
                        self.snail_surface = self.snail_frames[self.snail_frame_index]
                    if event.type == self.fly_animation_timer:
                        if self.fly_frame_index == 0:
                            self.fly_frame_index = 1
                        else:
                            self.fly_frame_index = 0
                        self.fly_surface = self.fly_frames[self.fly_frame_index]

            
            if self.game_active:
                # Background
                # blit = "block image transfer" - put a surface on another surface
                # two arguments - blit(surface to place it on, position)
                self.screen.blit(self.sky_surface, (0,0))
                self.screen.blit(self.ground_surface, (0, 300))

                # Score
                self.score = self.display_score()

                # Player
                self.player_gravity += 1
                self.player_rect.y += self.player_gravity
                if self.player_rect.bottom >= 300:
                    self.player_rect.bottom = 300
                self.player_animation()
                self.screen.blit(self.player_surface, self.player_rect)

                # Obstacle Movement
                self.obstacle_rect_list = self.obstacle_movement(self.obstacle_rect_list)


                # Collision
                self.game_active = self.collisions(self.player_rect, self.obstacle_rect_list)
                
            else:
                self.screen.fill((94, 129, 162))
                self.screen.blit(self.player_stand, self.player_stand_rect)
                self.obstacle_rect_list.clear()
                self.player_rect.midbottom = (80,300)
                self.player_gravity = 0

                self.screen.blit(self.game_name, self.game_name_rect)
                score_message = self.test_font.render(f'Your score: {self.score}', False, (111,196,169))
                score_message_rect = score_message.get_rect(center = (400,330))

                if self.score == 0:
                    self.screen.blit(self.game_message, self.game_message_rect)
                else:
                    self.screen.blit(score_message, score_message_rect)
                

            #update the display surface so anything drawn inside the while loop is displayed
            pygame.display.update()

            #set the maximum framerate to make sure the game doesn't run too fast
            self.clock.tick(fps)

if __name__ == '__main__':
    game = Game()
    game.run()