import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self,my_settings,screen):
        super(Alien,self).__init__()
        self.screen = screen
        self.my_settings = my_settings

        self.image = pygame.image.load('images/yilong.bmp')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image,self.rect)

    
    def update(self):
        self.x = self.x + (self.my_settings.alien_speed_factor * self.my_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True

        elif self.rect.left <= 0:
            return True