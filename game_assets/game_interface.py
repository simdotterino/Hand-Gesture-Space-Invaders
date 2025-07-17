from tracemalloc import start
import pygame as pg
pg.init() 
# pg.init()

# initialize window size 
window_height = 540
window_width = 540

# initialize start game button size 
start_game_button_height = 100 
start_game_button_width = 200

# initialize center coordinates of the screen to place the start_game_button
center_x = window_width // 2 - start_game_button_width // 2
center_y = window_height // 2 - start_game_button_height // 2


# screen = pg.display.set_mode((window_height, window_width))
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

# initialize white colour code 
white_corlour_code = (255, 255, 255)
navy_colour_code = (25, 25, 112)

# game state variable, initially set to menu

# running variable to control the main loop

# start_game function to display the start game button and to start the game 
def start_game_button(screen):
    global font 
    # create a rectangle object for the start game button 
    game_start_button = pg.Rect(center_x, center_y, start_game_button_width, start_game_button_height)
    # make it visible on the screen 
    pg.draw.rect(screen, navy_colour_code, game_start_button)
    # initialize start_game text for the start_game_button
    start_game_text = font.render('Start Game', True, white_corlour_code)
    # get the rectangle object for the start_game_text
    start_game_text_rect = start_game_text.get_rect()
    # center the start_game_text on the start_game_button
    start_game_text_rect.center = game_start_button.center
    # make it visible on the screen 
    screen.blit(start_game_text, start_game_text_rect)

    # update the display 
    pg.display.flip()

    return game_start_button

def start_game(screen):
    screen.fill((255, 255, 255)) 
    pg.display.flip()


def handle_start_game_button_click(start_button):
    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()
            if start_button.collidepoint(mouse_pos):
                return True
    return False


def main():

    global font 


    running = True
    game_state = "menu"

    pg.init()
    screen = pg.display.set_mode((window_height, window_width))
    


    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        if game_state == "menu":
            start_game_button(screen)
            if handle_start_game_button_click(start_game_button(screen)):
                game_state = "game"

        elif game_state == "game":
            start_game(screen)

    pg.quit()




if __name__ == "__main__":
    main()


