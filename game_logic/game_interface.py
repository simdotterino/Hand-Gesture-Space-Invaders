import pygame as pg
import random
pg.init()
pg.mixer.init()

#Game components
from constants import *
from draw import *
from game_settings import GameSettings
from game_data import GameData
from events import handle_events
from spaceship import Spaceship
from enemy import Enemy

# main game loop 
def main():
    # Initialize pygame
    pg.init()

    # Create game objects
    settings = GameSettings()
    game_data = GameData()

    # Initialize display
    screen = pg.display.set_mode((settings.screen_width, settings.screen_height))
    font = pg.font.Font(None, settings.font_size)
    
    # Main game loop
    while game_data.running:
        # Handle events
        click_event = handle_events(game_data)
        
        # Update game state
        if game_data.is_game_over():
            game_data.current_state = GameState.GAME_OVER
        

        # Draw current screen and handle interactions
        if game_data.current_state == GameState.MENU:
            start_button = draw_menu(screen, font, settings)
            
            # Handle button clicks
            if click_event and click_event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                if start_button.is_clicked(mouse_pos):
                    # print("Game started!") 
                    ship_x = (Constants.window_width // 2)
                    ship_y = Constants.window_height - 40
                    # create a new spaceship object
                    game_data.spaceship = Spaceship(ship_x, ship_y) # type: ignore
                    game_data.current_state = GameState.PLAYING
                    SoundEffects.game_start_sound.play()

        # game logic, firing bullets, enemy spaceship colliiosn, enemy spawn, enemy being killed by the bullet
        elif game_data.current_state == GameState.PLAYING:
            draw_game(screen, game_data)
            
            # draw the spaceship on the screen 
            if game_data.spaceship:
                game_data.spaceship.draw(screen)
            
            # game difficulty adjustment happens here 
            if game_data.score >= game_data.score_for_next_level:
                game_data.level_up()
                game_data.score_for_next_level += 10 

            # draw the bullets on the screen 
            for bullet in game_data.bullets:
                # makes the new bullet 
                bullet.being_fired()
                # draw the bullet on the screen 
                bullet.draw(screen)
                # if the bullet is out of the screen, remove it 
                if bullet.y < 0:
                    game_data.bullets.remove(bullet)
            
            # enemy spawning 
            current_time_for_enemy_respawing = pg.time.get_ticks()
            if current_time_for_enemy_respawing - game_data.last_enemy_spawn_time > game_data.enemy_spawn_delay:
                # the 40 is the width of the enemy, change it accordingly as the enemy width changes
                new_enemy = Enemy(random.randint(0, Constants.window_width - 40), 0, enemy_speed=game_data.base_enemy_speed)
                # print(f"new_enemy created, speed:{new_enemy.enemy_speed}, {game_data.last_enemy_spawn_time}")
                # add the new eneemy to the enemy list 
                game_data.enemies.append(new_enemy)
                # update the last_enemy_spawn_time to current time 
                game_data.last_enemy_spawn_time = current_time_for_enemy_respawing 
            
            # enemy-bullet colllision detection, [:] is a list comprehension to iterate over a copy of the list
            for bullet in game_data.bullets[:]:
                for enemy in game_data.enemies[:]:
                    if bullet.bullet_rect.colliderect(enemy.enemy_rect):
                        SoundEffects.enemy_being_hit.play()
                        game_data.bullets.remove(bullet)
                        game_data.enemies.remove(enemy)
                        game_data.score += 1 
                        break
                    
            # enemy-spaceship collision detection 
            for enemy in game_data.enemies[:]:
                if enemy.enemy_rect.colliderect(game_data.spaceship.spaceship_rect):
                    SoundEffects.collision_sound.play()
                    game_data.lives -= 1
                    game_data.enemies.remove(enemy)
                    break


            # enemy movement
            for enemy in game_data.enemies[:]:
                enemy.move()
                enemy.draw(screen)
                # print(f"new_enemy drawn, speed:{new_enemy.enemy_speed}, {game_data.last_enemy_spawn_time}")
                # enemy hits the bottom of the screen? game over 
                if enemy.y + enemy.height >= Constants.window_height:
                    game_data.current_state = GameState.GAME_OVER
                    SoundEffects.game_over_sound.play()


        elif game_data.current_state == GameState.GAME_OVER:
            game_over_menu_button = draw_game_over(screen, font, game_data, settings)
            if click_event and click_event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                if game_over_menu_button.is_clicked(mouse_pos):
                    game_data.reset_game()
                    game_data.current_state = GameState.MENU
                    
        # Update display
        pg.display.flip()
    
    # end the game 
    pg.quit()



if __name__ == "__main__":
    main()


