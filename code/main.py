import pygame
import sys
from random import randint, choice
from settings import width, height, fps

def get_speed_modifier(game):
    if game.score >= 100:
        speed_modifier = 5
    else:
        speed_modifier = int(game.score / 20)
    return speed_modifier

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player_walk_1 = pygame.image.load('../graphics/player/player_walk_1.png').convert_alpha()
        self.player_walk_2 = pygame.image.load('../graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [self.player_walk_1,self.player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('../graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('../audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        
        if type == 'fly':
            fly_1 = pygame.image.load('../graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('../graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
            self.speed = 6
        else:
            snail_1 = pygame.image.load('../graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('../graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300
            self.speed = 6

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    # def get_speed_modifier(self, game):
    #     if game.score >= 100:
    #         speed_modifier = 5
    #     else:
    #         speed_modifier = int(game.score / 20)
    #     return speed_modifier

    def update(self):
        self.animation_state()
        self.rect.x -= self.speed + get_speed_modifier(game)
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

class Game:
    def display_score(self):
        '''Calculate the current time, draw it onto the screen, and return it.'''
        current_time = int(pygame.time.get_ticks() / 1000) - self.start_time
        score_surface = self.test_font.render(f'Score: {current_time}',False,(64,64,64))
        if self.high_score:
            score_rect = score_surface.get_rect(center = (200, 50))
        else:
            score_rect = score_surface.get_rect(center = (400, 50))
        score_bg = score_rect.inflate(10,10)
        pygame.draw.rect(self.screen, '#c0e8ec', score_bg)
        self.screen.blit(score_surface, score_rect)
        return current_time

    def display_high_score(self):
        if self.high_score:
            high_score_surface = self.test_font.render(f'High Score: {self.high_score}',False,(64,64,64))
            high_score_rect = high_score_surface.get_rect(center = (600, 50))
            high_score_bg = high_score_rect.inflate(10,10)
            pygame.draw.rect(self.screen, '#c0e8ec', high_score_bg)
            self.screen.blit(high_score_surface, high_score_rect)

    def collision_sprite(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.obstacle_group, False):
            self.obstacle_group.empty()
            return False
        return True

    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Practice Project 1')
        self.test_font = pygame.font.Font('../font/Pixeltype.ttf', 50)

        self.game_active = False

        self.start_time = 0
        self.score = 0
        self.high_score = 0

        self.bg_music = pygame.mixer.Sound('../audio/music.wav')
        self.bg_music.set_volume(0.2)
        self.bg_music.play(loops = -1)

        # Groups
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player())

        self.obstacle_group = pygame.sprite.Group()
        self.obstacle_group.update()

        # Background
        self.sky_surface = pygame.image.load('../graphics/Sky.png').convert()
        self.ground_surface = pygame.image.load('../graphics/ground.png').convert()

        # Intro screen
        self.player_stand = pygame.image.load('../graphics/player/player_stand.png').convert_alpha()
        self.player_stand = pygame.transform.rotozoom(self.player_stand, 0, 2)
        self.player_stand_rect = self.player_stand.get_rect(center = (400,200))

        self.game_name = self.test_font.render('Pixel Runner', False, (111,196,169))
        self.game_name_rect = self.game_name.get_rect(center = (400, 80))

        self.game_message = self.test_font.render('Press space to run', False, (111,196,169))
        self.game_message_rect = self.game_message.get_rect(center = (400, 330))

        # Timers
        self.obstacle_timer = pygame.USEREVENT + 1 # add +1 to each event you add
        pygame.time.set_timer(self.obstacle_timer, 1500)

        self.snail_animation_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(self.snail_animation_timer, 500)

        self.fly_animation_timer = pygame.USEREVENT + 3
        pygame.time.set_timer(self.fly_animation_timer, 200)
    

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if not self.game_active:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.game_active = True
                            self.start_time = int(pygame.time.get_ticks() / 1000)

                if self.game_active:
                    if event.type == self.obstacle_timer:
                        self.obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
                        pygame.time.set_timer(self.obstacle_timer, (1500 - (get_speed_modifier(self) * 150)))
            
            if self.game_active:

                self.screen.blit(self.sky_surface, (0,0))
                self.screen.blit(self.ground_surface, (0, 300))

                # Score
                self.score = self.display_score()
                self.display_high_score()

                # Player
                self.player.draw(self.screen)
                self.player.update()

                # Obstacles
                self.obstacle_group.draw(self.screen)
                self.obstacle_group.update()

                # Collision
                self.game_active = self.collision_sprite()
                
            else:
                self.screen.fill((94, 129, 162))
                self.screen.blit(self.player_stand, self.player_stand_rect)

                self.screen.blit(self.game_name, self.game_name_rect)
                score_message = self.test_font.render(f'Your score: {self.score}', False, (111,196,169))
                score_message_rect = score_message.get_rect(center = (400,330))
                high_score_message = self.test_font.render(f'High score! {self.score}', False, 'Yellow')
                high_score_message_rect = high_score_message.get_rect(center = (400,330))

                if self.score > self.high_score:
                    self.high_score = self.score

                if self.score == 0:
                    self.screen.blit(self.game_message, self.game_message_rect)
                elif self.score >= self.high_score:
                    self.screen.blit(high_score_message, high_score_message_rect)
                else:
                    self.screen.blit(score_message, score_message_rect)
                
            pygame.display.update()

            self.clock.tick(fps)

if __name__ == '__main__':
    game = Game()
    game.run()