import pygame
from sys import exit
from random import randint, choice
from pygame.sprite import Group

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font("font/Pixeltype.ttf", 50)
game_active = True
start_time = 0
score = 0
bg_Music = pygame.mixer.Sound("audio/music.wav")
bg_Music.play(loops = -1)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()
        
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound("audio/jump.mp3")
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == 300:
            self.jump_sound.play()
            self.gravity = -20
        if keys[pygame.K_LEFT]:
            self.rect.x -= 4
            if player_rectangle.right <= 0:
                player_rectangle.left = 0
        if keys[pygame.K_RIGHT]:
            self.rect.x += 4
            if player_rectangle.left >= 800:
                player_rectangle.right = 800

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
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        
        if type == "fly":
            fly_1 = pygame.image.load("graphics/fly/Fly1.png").convert_alpha()
            fly_2 = pygame.image.load("graphics/fly/Fly2.png").convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
            snail_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))
    
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index > len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()  
        self.rect.x -= 6
    
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


# Score Counter
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = test_font.render(f"Score: {current_time}", False, (64, 64, 64))
    score_rectangle = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface, score_rectangle)
    return current_time

# Obstacle Movement
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rectangle in obstacle_list:
            obstacle_rectangle.x -= 5

            if obstacle_rectangle.bottom == 300:
                screen.blit(snail_surface, obstacle_rectangle)
            else:
                screen.blit(fly_surface, obstacle_rectangle)

            

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else: return []

# Collisions    
def collisions(player, obstacles):
    if obstacles:
        for obstacle_rectangle in obstacles:
            if player.colliderect(obstacle_rectangle): return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else: return True

# Player Animation
def player_animation():
    global player_surface, player_index

    if player_rectangle.bottom < 300:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surface = player_walk[int(player_index)]

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())    

obstacle_group = pygame.sprite.Group()

# Title
title_text = pygame.font.Font("font/Pixeltype.ttf", 100)
title_text_surface = title_text.render("Pixel Runner", False, "Blue")
title_text_rectangle = title_text_surface.get_rect(center = (400, 50))

# AnyKey
space_text = pygame.font.Font("font/Pixeltype.ttf", 25)
space_text_surface = space_text.render("Press 'space' to continue...", False, (64, 64, 64))
space_text_rectangle = space_text_surface.get_rect(midbottom = (650, 375))

# Welt
sky_surface = pygame.image.load("graphics/Sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()

# Obstacles
    # Snail
snail_frame_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_frame_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]

    # Fly
fly_frame_1 = pygame.image.load("graphics/fly/Fly1.png").convert_alpha()
fly_frame_2 = pygame.image.load("graphics/fly/Fly2.png").convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]

obstacle_rectangle_list = []

# Spieler
player_walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()

player_surface = player_walk[player_index]
player_rectangle = player_walk_1.get_rect(midbottom = (80,300))
player_gravity = 0

# Intro Screen
player_stand = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rectangle = player_stand.get_rect(center = (400, 300))

# Game Over Text
dead_text = pygame.font.Font("font/Pixeltype.ttf", 50)
dead_text_surface = dead_text.render("Game Over", False, (64, 64, 64))
dead_text_rectangle = dead_text_surface.get_rect(center = (400, 175))

# Timer

    # Obstacle Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

    # Snail Animation Timer
snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)
    
    # Fly Animation Timer
fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)




pygame.key.set_repeat(100,5)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_active:

            
            # Jump Mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rectangle.collidepoint(event.pos): 
                    player_gravity = -20
            
            # Jump Keyboard
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and player_rectangle.bottom == 300:
                    player_gravity = -20
            
            # Move left        
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                player_rectangle.x -= 4
                if player_rectangle.right <= 0:
                    player_rectangle.left = 0

            # Move right
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                player_rectangle.x += 4
                if player_rectangle.left >= 800:
                    player_rectangle.right = 800
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

        if game_active:        
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(["fly", "snail", "snail"])))
                #if randint(0, 2):
                #    obstacle_rectangle_list.append(snail_surface.get_rect(midbottom = (randint(900, 1100), 300)))
                #else: 
                #    obstacle_rectangle_list.append(fly_surface.get_rect(midbottom = (randint(900, 1100), 210)))
        
            if event.type == snail_animation_timer:
                snail_surface = snail_frames[snail_frame_index]
                if snail_frame_index == 0: 
                    snail_frame_index = 1
                else: snail_frame_index = 0

            if event.type == fly_animation_timer:
                fly_surface = fly_frames[fly_frame_index]
                if fly_frame_index == 0: 
                    fly_frame_index = 1
                else: fly_frame_index = 0

    if game_active:
        screen.blit(sky_surface,(0, 0))
        screen.blit(ground_surface,(0, 300))
        score = display_score()


        # Player
        #player_gravity += 1
        #player_rectangle.y += player_gravity
        #if player_rectangle.bottom >= 300:
        #    player_rectangle.bottom = 300
        #player_animation()
        #screen.blit(player_surface,player_rectangle)
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        # Obstacle Movement
        #obstacle_rectangle_list = obstacle_movement(obstacle_rectangle_list)

        # Collision
        game_active = collision_sprite()
        #game_active = collisions(player_rectangle, obstacle_rectangle_list)
    
    else:
        screen.fill("Red")
        screen.blit(dead_text_surface, dead_text_rectangle)
        obstacle_rectangle_list.clear()
        player_rectangle.midbottom = (80, 300)
        player_gravity = 0

        screen.blit(player_stand, player_stand_rectangle)
        screen.blit(title_text_surface, title_text_rectangle)
        screen.blit(space_text_surface, space_text_rectangle)

        score_message = test_font.render(f"Your score: {score}", False, (64, 64, 64))
        score_message_rectangle = score_message.get_rect(midbottom = (120, 300))
        screen.blit(score_message, score_message_rectangle)
        
    pygame.display.update()
    clock.tick(60)            
