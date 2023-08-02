import pygame
import sys
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
def run_game():
    pygame.init() 
    my_settings = Settings()
    screen = pygame.display.set_mode((my_settings.screen_width, my_settings.screen_height)) 
    pygame.display.set_caption("CANADA DRAGON CHIKEN FIGHT") ##窗口的命名4
    play_button = Button(my_settings,screen,"JUST FUCKING PLAY IT")
    stats = GameStats(my_settings)
    sb = Scoreboard(my_settings,screen,stats)
    ship = Ship(my_settings,screen)
    bullets = Group()
    aliens = Group()
    gf.create_fleet(my_settings,screen,ship,aliens)
    bg_color = (230,230,230)##颜色采用的 是RGB的颜色设置
    alien = Alien(my_settings,screen)

    while True:
        gf.check_events(my_settings,screen,stats,sb,play_button,ship,aliens,bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(aliens,bullets,my_settings,stats,ship,screen,sb)
            gf.update_aliens(my_settings,stats,sb,screen,ship,bullets,aliens)
            bullets.update()
        gf.update_screen(my_settings,screen,stats,sb,ship,aliens,bullets,play_button)

run_game()