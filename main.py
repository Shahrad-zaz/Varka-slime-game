import pygame
from random import randint, uniform
import sys
import os
import pygame
from random import randint, uniform

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Cloud1(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0, window_width),randint(0,300)))
        self.diraction = pygame.math.Vector2()
        self.speed = 15

    def update(self,dt):
        self.diraction.x = 2
        self.rect.center += self.speed* self.diraction * dt
        if self.rect.left >= window_width:
            self.rect.right = 0            

class Cloud2(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0, window_width),randint(0,300)))
        self.diraction = pygame.math.Vector2()
        self.speed = 20

    def update(self,dt):
        self.diraction.x = 2
        self.rect.center += self.speed* self.diraction * dt
        if self.rect.left >= window_width:
            self.rect.right = 0        

class Cloud3(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0, window_width),randint(0,300)))
        self.diraction = pygame.math.Vector2()
        self.speed = 10

    def update(self,dt):
        self.diraction.x = 4.9
        self.rect.center += self.speed* self.diraction * dt
        if self.rect.left >= window_width:
            self.rect.right = 0      

class Player(pygame.sprite.Sprite):

    def __init__(self, groups):
        super().__init__(groups)
        self.image =  pygame.image.load("resources folder/varka_back_small.png").convert_alpha()
        self.rect  =  self.image.get_frect(midbottom = (window_width/2, window_height-20))
        self.diraction = pygame.math.Vector2()
        self.speed = 300

        # cooldown
        self.can_beer_shoot = True
        self.beer_shoot_time = 0
        self.cooldown_duration = 400

        # mask
        #self.mask = pygame.mask.from_surface(self.image)


    def Beer_timer(self):
        if not self.can_beer_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.beer_shoot_time >= self.cooldown_duration:
                self.can_beer_shoot = True


    def update(self, dt):
        keys = pygame.key.get_pressed()
        keys2 = pygame.key.get_just_pressed()
        
        self.diraction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.diraction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.diraction = self.diraction.normalize() if self.diraction else self.diraction
        self.rect.center += self.diraction * dt * self.speed

        if keys[pygame.K_SPACE] and self.can_beer_shoot:
            Beer(beer_surf, self.rect.midtop, (all_sprites,beer_sprits) )
            self.can_beer_shoot = False
            self.beer_shoot_time = pygame.time.get_ticks()
            music_random = randint(0,1)
            if music_random == 1:
                varak_sound1.play()
            else:
                varak_sound2.play()

        if keys[pygame.K_LSHIFT]:
            self.speed = 600
        else:
            self.speed = 300

        if self.rect.right >= window_width:
            self.rect.right = window_width

        if self.rect.left <= 0:
            self.rect.left = 0

        if self.rect.bottom >= window_height:
            self.rect.bottom = window_height

        if self.rect.top <= 500:
            self.rect.top = 500
        self.Beer_timer()

class Beer(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.original_surf = surf
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
        #self.mask = pygame.mask.from_surface(self.image)
        self.rotation_speed = randint(-1000,1000)
        self.rotation = 0

    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill() 
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation,1 )
        self.rect = self.image.get_frect(center = self.rect.center)

class Slime(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.diraction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(80,220)
    # mask
        #self.mask = pygame.mask.from_surface(self.image)


    def update(self, dt):
        self.rect.center += self.diraction* self.speed * dt  
        if self.rect.top > window_height:
                    self.kill()
        if self.rect.left <= 0:
            self.diraction.x *= -1 
        if self.rect.right >= window_width:
            self.diraction.x *= -1 

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center = pos)

    def update(self, dt):
        self.frame_index+=10 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()

def collisions():
    global running

    collidion_sprits = pygame.sprite.spritecollide(player, slime_sprites,True, pygame.sprite.collide_mask )
    if collidion_sprits :
        running = False

    for beer in beer_sprits:
        collided_sprits = pygame.sprite.spritecollide(beer, slime_sprites,True)
        if collided_sprits:
            beer.kill()
            AnimatedExplosion(explosion_frames, beer.rect.midtop, all_sprites)
            pop.play()

def display_score():
    current_time = pygame.time.get_ticks() // 1000 * 20
    text_surf = font.render(str(current_time), True, ('Blue'))
    text_rect = text_surf.get_frect(midbottom = (window_width-100,100))
    pygame.draw.rect(display_surface,'blue',text_rect.inflate(20,10).move(0,-1),5,10,10,10,10,10)
    display_surface.blit(text_surf,text_rect)
  
# general setup
pygame.init()
window_width, window_height = 1280, 720 
display_surface = pygame.display.set_mode((window_width, window_height))
running = True
clock = pygame.Clock()

# display of name and icon
icon_image = pygame.image.load("resources folder/icon.ico")
pygame.display.set_caption("Varkas journey ")
pygame.display.set_icon(icon_image)

# import
back_surf = pygame.image.load("resources folder/background.png").convert_alpha()
beer_surf = pygame.image.load("resources folder/weapon.png").convert_alpha()
slime_surf = pygame.image.load("resources folder/slimebig.png").convert_alpha()
cloud_surf1 =  pygame.image.load("resources folder/cloud1.png").convert_alpha()
cloud_surf2 =  pygame.image.load("resources folder/cloud2.png").convert_alpha()
cloud_surf3 =  pygame.image.load("resources folder/cloud3.png").convert_alpha()
font = pygame.font.Font("resources folder/zh-cn.ttf",40)
explosion_frames = [pygame.image.load(f"resources folder/animations/{i}.png").convert_alpha() for i in range(10)]
varak_sound1 = pygame.mixer.Sound("resources folder/audio/1.mp3")
varak_sound2 = pygame.mixer.Sound("resources folder/audio/2.mp3")
pop = pygame.mixer.Sound("resources folder/audio/4.mp3")
main_music = pygame.mixer.Sound("resources folder/audio/3.mp3")
main_music.set_volume(0.5)
main_music.play(loops=-1)

# sprite
all_sprites = pygame.sprite.Group()
slime_sprites = pygame.sprite.Group()
beer_sprits = pygame.sprite.Group()

# the clouds
for i in range(20):
    Cloud1(all_sprites, cloud_surf1)
for i in range(20):
    Cloud2(all_sprites,cloud_surf2)
for i in range(20):
    Cloud3(all_sprites,cloud_surf3)

# the player
player = Player(all_sprites)

# cutome event - slime event
slime_event = pygame.event.custom_type()
pygame.time.set_timer(slime_event,1200)

while running:
    dt = clock.tick() / 1000
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == slime_event:
            x, y = randint(50,window_width-50), randint(-200,-100)
            Slime(slime_surf, (x,y), (all_sprites,slime_sprites))
    # update
    all_sprites.update(dt)
    collisions()
    # draw game
    display_surface.fill('skyblue')
    display_surface.blit(back_surf, (0,0))
    all_sprites.draw(display_surface)
    display_score()



    pygame.display.update()

pygame.quit() 