import pygame as pg
from constants import Constants, GameState

# handle all events such as move, fire, start game, etc 
def handle_events(game_data):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_data.running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            return event 
        elif event.type == pg.KEYDOWN and game_data:
            if event.key == pg.K_LEFT and game_data.spaceship:
                game_data.spaceship.move("left", Constants.window_width) # type: ignore
                # print("mmovign left ")
            elif event.key == pg.K_RIGHT and game_data.spaceship:
                game_data.spaceship.move("right", Constants.window_width) # type: ignore
                # print("moving right")
            elif event.key == pg.K_SPACE and game_data.spaceship:
                current_time_for_bullet_charging = pg.time.get_ticks()
                if current_time_for_bullet_charging - game_data.last_shot_time > game_data.bullet_cooldown:
                    # print("firing bullet, space bar is pressed")
                    # create a a new bullet objet 
                    bullet = game_data.spaceship.fire()
                    # added to the bulelt list 
                    game_data.bullets.append(bullet)
                    # upate the last shot time 
                    game_data.last_shot_time = current_time_for_bullet_charging
        
    return None