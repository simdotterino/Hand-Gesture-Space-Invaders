import pygame as pg
from enum import Enum


# constant class to store all the constants for the game 
class Constants:
    # Window size setting 
    window_width = 540
    window_height = 540

    # Button size setting 
    button_width = 200
    button_height = 100
    button_font = 50  # Font sizes for different text elements
    button_font_size = 36


    game_text_font_size = 24
    score_font_size = 20
    lives_font_size = 20

    # Colors codes (RGB values)
    white = (255, 255, 255)
    navy = (25, 25, 112)
    black = (0, 0, 0)

    # Game values settings
    initial_lives = 5
    initial_score = 0
    initial_level = 0

# Game state enum class to store the game state 
class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    GAME_OVER = "game_over"


# Game settings class to store game settings

class GameSettings:
    def __init__(self):
        self.screen_width = Constants.window_width
        self.screen_height = Constants.window_height
        self.button_width = Constants.button_width
        self.button_height = Constants.button_height
        self.font_size = Constants.game_text_font_size
        
        # Calculate center coordinates once
        self.center_x = self.screen_width // 2 - self.button_width // 2
        self.center_y = self.screen_height // 2 - self.button_height // 2



# game data class to store game data such as score, lives, level, and running state
class GameData:
    def __init__(self):
        self.current_state = GameState.MENU
        self.score = Constants.initial_score
        self.lives = Constants.initial_lives
        self.level = Constants.initial_level
        self.running = True
    
    def is_game_over(self):
        return self.lives <= 0
    
    def reset_game(self):
        self.score = Constants.initial_score
        self.lives = Constants.initial_lives
        self.level = Constants.initial_level


# button class to create a button object
class Button:
    def __init__(self, x, y, width, height, button_text_content, font_size, color=Constants.navy):
        self.rect = pg.Rect(x, y, width, height)
        self.text = button_text_content
        self.font = font_size
        self.color = color
        self.text_surface = None
        self.text_rect = None
        self._create_text()
    
    # create text surface and position it on button 
    def _create_text(self):
        self.text_surface = self.font.render(self.text, True, Constants.white)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = self.rect.center
    
    # draw button and text on screen 
    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surface, self.text_rect)
    
    # check if button was clicked
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)



# ----------------------------------------------------------------------------
# Gmae Functions - game logics 
# ----------------------------------------------------------------------------


# handel all pygame events 
def handle_events(game_data):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_data.running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            return event  # Return the click event for button handling
    return None

# draw the menu screen and return the start button 
def draw_menu(screen, font, settings):
    # initialize the screen with black color 
    screen.fill(Constants.black)
    
    # Create and draw start button
    start_button = Button(
        settings.center_x, 
        settings.center_y, 
        settings.button_width, 
        settings.button_height, 
        "Start Game", 
        font
    )
    start_button.draw(screen)
    
    return start_button

# draw the game screen 
def draw_game(screen, game_data):
    screen.fill(Constants.black)

    # I will make the game UI here and the logic as well 
    # For now, just show a simple game screen
    font = pg.font.Font(None,36)
    game_text = font.render(f"Game Screen - Score: {game_data.score}", True, Constants.white)
    text_rect = game_text.get_rect(center=(Constants.window_width//2, Constants.window_height//2))
    screen.blit(game_text, text_rect)


# draw the game over screen 
def draw_game_over(screen, font, game_data):
    screen.fill(Constants.black)
    game_over_text = font.render("Game Over!", True, Constants.white)
    text_rect = game_over_text.get_rect(center=(Constants.window_width//2, Constants.window_height//2))
    screen.blit(game_over_text, text_rect)

# ----------------------------------------------------------------------------
# Main game loop 
# ----------------------------------------------------------------------------

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
                    game_data.current_state = GameState.PLAYING
                    print("Game started!")  # Debug message
        
        elif game_data.current_state == GameState.PLAYING:
            draw_game(screen, game_data)
            # Add game logic here
            # game_data.score +=1 #le score increment for testing
        
        elif game_data.current_state == GameState.GAME_OVER:
            draw_game_over(screen, font, game_data)
        
        # Update display
        pg.display.flip()
    
    # end the game 
    pg.quit()


# ============================================================================
# ENTRY POINT - Standard Python main guard
# ============================================================================
if __name__ == "__main__":
    main()


