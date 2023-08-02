import pygame
import sys
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event,my_settings,screen,ship,bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(my_settings,screen,ship,bullets)


        
    


def check_keyup_events(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False
    

  

def check_events(my_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,my_settings,screen,ship,bullets)


        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type  == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(my_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y)

def check_play_button(my_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active: 
        pygame.mixer.init()
        pygame.mixer.music.load('music/giao.wav')
        pygame.mixer.music.play(0)
        pygame.mixer.music.set_volume(0.4)
        my_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.game_active = True
        sb.prep_score()
        sb.prep_level()
        aliens.empty()
        bullets.empty()

        create_fleet(my_settings,screen,ship,aliens)
        ship.center_ship()
            

def update_screen(my_settings,screen,stats,sb,ship,alien,bullets,play_button):
    screen.fill(my_settings.bg_color)
    sb.show_score()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
       # bullet.update()
    ship.blitme()
    alien.draw(screen)
    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()

def update_bullets(aliens,bullets,my_settings,stats,ship,screen,sb):
    bullets.update()
    for bullet in bullets.copy():  #   不能从编组（Group）中直接删除元素，所以使用copy（）
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        pygame.mixer.init()
        s= pygame.mixer.Sound('music/self_giao.wav')
        s.play(0)
        s.set_volume(0.9)
        stats.score += my_settings.alien_points
        check_high_score(stats,sb)
        sb.prep_score()


def fire_bullet(my_settings,screen,ship,bullets):
     if len(bullets) < my_settings.bullets_allowed:
        new_bullet  = Bullet(my_settings,screen,ship)
        bullets.add(new_bullet)
    
def create_fleet(my_settings,screen,ship,aliens):
    alien = Alien(my_settings,screen)
    number_aliens_x =  get_number_alien_x(my_settings,alien.rect.width)
    number_rows = get_number_rows(my_settings,ship.rect.height, alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(my_settings,screen,aliens,alien_number,row_number)

def get_number_alien_x(my_settings,alien_width):
    available_space_x = my_settings.screen_width - 2 * alien_width
    number_aliens_x = int (available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(my_settings,screen,aliens,alien_number,row_number):
    alien = Alien(my_settings,screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height+ 2 * alien.rect.height * row_number
    aliens.add(alien)

def get_number_rows(my_settings,ship_height,alien_height):
    availble_space_y = (my_settings.screen_height - (3 * alien_height) -  ship_height)

    number_rows = int(availble_space_y/(2 * alien_height))
    return number_rows

def change_fleet_direction(my_settings,aliens):
    for alien in aliens.sprites():
        alien.rect.y += my_settings.fleet_drop_speed
    my_settings.fleet_direction *= -1

def check_fleet_edges(my_settings,aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(my_settings,aliens)
            break


def update_aliens(my_settings,stats,sb,screen,ship,bullets,aliens):
    aliens.update()
    check_fleet_edges(my_settings,aliens)
    if len(aliens) == 0:
        bullets.empty()
        my_settings.increase_speed()
        stats.level +=1
        sb.prep_level()
        create_fleet(my_settings,screen,ship,aliens)
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(my_settings,stats,screen,ship,aliens,bullets)

def ship_hit(my_settings,stats,screen,ship,aliens,bullets):
    if stats.ship_left >0:
        stats.ship_left -= 1

        pygame.mixer.init()
        pygame.mixer.music.load('music/ENDING.wav')
        pygame.mixer.music.play(0)

        aliens.empty()
        bullets.empty()

        create_fleet(my_settings,screen,ship,aliens)
        ship.center_ship()

        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_high_score(stats,sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
