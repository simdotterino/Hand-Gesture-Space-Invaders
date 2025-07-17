from tracemalloc import start
import pygame as pg
pg.init()

# initialize window size 
window_height = 540
window_width = 540

# initialize start game button size 
start_game_button_height = 100 
start_game_button_width = 200

# initialize center coordinates of the screen to place the start_game_button
center_x = window_width // 2 - start_game_button_width // 2
center_y = window_height // 2 - start_game_button_height // 2


screen = pg.display.set_mode((window_height, window_width))
# font object to be used for text rendering 
font = pg.font.Font(None, 50)
# initialize score value 
score = 0
# initialize lives value 
lives = 5
# initialize difficulty value 
levels = 0
# initialize game over value 
game_over = lives == 0
# initialize font object 
font = pg.font.Font(None, 50)
# initialize game state 
game_state = "menu"

white_corlour_code = (255, 255, 255)

# start_game function to display the start game button and to start the game 
def start_game():
    # create a rectangle object for the start game button 
    game_start_button = pg.Rect(center_x, center_y, start_game_button_width, start_game_button_height)
    # make it visible on the screen 
    pg.draw.rect(screen, white_corlour_code, game_start_button)
    # initialize start_game text for the start_game_button
    start_game_text = font.render('Start Game', True, white_corlour_code)




    # get the rectangle object for the start_game_text
    # start_game_text_rect = start_game_text.get_rect()
    # # center the start_game_text on the start_game_button
    # start_game_text_rect.center = game_start_button.center
    # # make it visible on the screen 
    # screen.blit(start_game_text, start_game_text_rect)



    start_game_text = font.render('Start Game', True, (255,255,255))
    start_game_text_rect = start_game_text.get_rect()
    start_game_text_rect.center = game_start_button.center

    screen.blit(start_game_text, start_game_text_rect)

    # game_start_button = pg.Rect(100, 100, 200, 50)
    # pg.draw.rect(screen, (255, 255, 255), game_start_button)
    # text_surface = font.render('Start Game', True, (255,255,255))
    # text_rect = text_surface.get_rect()
    # text_rect.center = game_start_button.center

    # screen.blit(text_surface, text_rect)




running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    game_start_button = pg.Rect(540, 360, 200, 50)
    pg.draw.rect(screen, (255, 255, 255), game_start_button)
    start_game_text = font.render('Start Game', True, (255,255,255))
    start_game_text_rect = start_game_text.get_rect()
    start_game_text_rect.center = game_start_button.center

    screen.blit(start_game_text, start_game_text_rect)

    pg.display.flip()

pg.quit()

