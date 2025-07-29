import pygame as pg
from enum import Enum
import random
pg.init()
pg.mixer.init()
laser_sound = pg.mixer.Sound("game_assets/sound/laser-312360.wav")
collision_sound = pg.mixer.Sound("game_assets/sound/small-explosion-103931.mp3")
game_start_sound = pg.mixer.Sound("game_assets/sound/gamestart-272829.mp3")


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


    game_text_font_size = 28


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
        self.spaceship = None
        self.bullets = []
        self.enemies = []
        self.enemy_spawn_delay = 2000
        # initilaizd to a number bigger than cooldown so, in the event_handling, current - last_shot_time is greater than bullet_cooldown
        self.last_shot_time = -4000
        # bullet delay is 1 seoncs for ow, will be changed later
        self.bullet_cooldown = 3000
    
    def is_game_over(self):
        return self.lives <= 0 
        # || enemy.y == Constants.height
    
    def reset_game(self):
        self.score = Constants.initial_score
        self.lives = Constants.initial_lives
        self.level = Constants.initial_level
        self.spaceship = None 


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

class Spaceship:
    def __init__(self, x, y, width= 40, height =40, spaceship_speed=40):
        # spacceship horizontal position  
        self.x = x
        # spaceship vertical position 
        self.y = y
        # spaceship width(affect the width of the spaceship)
        self.width = width
        # spaceship height(affect the height of the spaceship)
        self.height = height
        # by default, the spaceship speed is 10, but increase or decrease it to make it faster of slower
        self.spaceship_speed = spaceship_speed
        # still need this recteangle for positioning of the spaceship and collision detection 
        self.spaceship_rect = pg.Rect(x, y, width, height)
        # spaceship image 
        self.spaceship_image = pg.image.load("game_assets/icons/space-invaders.png")
        self.spaceship_image = pg.transform.scale(self.spaceship_image, (self.width, self.height))

    def move(self, direction, screen_width):
        print(f"before moving, x={self.x}, direction={direction}, screen_width={screen_width}")
        if direction == "left" and self.x > 0:
            self.x -= self.spaceship_speed
            print(f"moving left, x={self.x},")
        elif direction == "right" and self.x < screen_width - self.width:
            self.x += self.spaceship_speed
            print(f"moving right spaceship function is called, x={self.x}")

        self.spaceship_rect.x = self.x
        print(f"after moving, x={self.x}, y={self.y}")

    def draw(self, screen):
        print(f"drawing spaceship, x={self.x}, y={self.y}")
        screen.blit(self.spaceship_image, (self.x, self.y))

    def get_center(self):
        return (self.x + self.width // 2, self.y)

    def fire(self): 
        # inital x, y positions of the bullet 
        bullet_x = self.x + self.width // 2 
        bullet_y = self.y
        print("bullet created")
        laser_sound.play()

        return Bullet(bullet_x, bullet_y)


class Bullet: 
    def __init__(self, x, y, width=5, height=10, bullet_speed=10):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bullet_speed =  bullet_speed
        self.bullet_rect = pg.Rect(x,y,width,height)

    def being_fired(self):
        # change the y position of the bullet
        self.y -= self.bullet_speed
        # update the bullet rect position to match the new y position 
        self.bullet_rect.y = self.y
        print(f"bullet being fired, y={self.y}")  

    def draw(self, screen):
        pg.draw.rect(screen, Constants.white, self.bullet_rect)




class Enemy:
    def __init__(self, x, y, width=40, height=40, enemy_speed=0.3, spawn_delay=2000):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.enemy_speed = enemy_speed
        self.enemy_rect = pg.Rect(x,y,width,height)
        self.enemy_image = pg.image.load("game_assets/icons/enemy.png")
        self.enemy_image = pg.transform.scale(self.enemy_image, (self.width, self.height))
        self.spawn_delay = spawn_delay
   
    def move(self):
        self.y += self.enemy_speed
        self.enemy_rect.y = self.y
    
    def draw(self, screen):
        print(f"drawing enemy, x={self.x}, y={self.y}")
        screen.blit(self.enemy_image, (self.x, self.y))





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

# draw the game screen, COME BACK TO THIS LATER AND FIX THE RESPONSIVENESS OF THE UI
def draw_game(screen, game_data):
    screen.fill(Constants.black)

    # I will make the game UI here and the logic as well, align the labels properly!!!, will fix it later, leaving it like this for now for demo purpose
    # create different fonts for different labels 
    score_font = pg.font.Font(None, Constants.game_text_font_size)
    lives_font = pg.font.Font(None, Constants.game_text_font_size)
    level_font = pg.font.Font(None, Constants.game_text_font_size)

    # draw score label at the top left corner of the screen 
    score_label = score_font.render(f"Score: {game_data.score}", True, Constants.white)
    screen.blit(score_label, (10, 10))

    # draw lives label at the top right corner of the screen
    lives_label = lives_font.render(f"Lives: {game_data.lives}", True, Constants.white)
    screen.blit(lives_label, (Constants.window_width - 90, 10))

    # draw level label at the top center of the screen 
    level_label = level_font.render(f"Level: {game_data.level}", True, Constants.white)
    screen.blit(level_label, (Constants.window_width//2 - 50, 10))
 


# draw the game over screen 
def draw_game_over(screen, font, game_data, settings):
    screen.fill(Constants.black)
    game_over_text = font.render("Game Over!", True, Constants.white)
    text_rect = game_over_text.get_rect(center=(Constants.window_width//2 , Constants.window_height//2 - 50))
    screen.blit(game_over_text, text_rect)
    # Display the player's score below the game over text
    score_text = font.render(f"Your Score: {game_data.score}", True, Constants.white)
    score_rect = score_text.get_rect(center=(Constants.window_width//2, Constants.window_height//2))
    screen.blit(score_text, score_rect)


    back_to_menu_button = Button(
        settings.center_x,
        settings.center_y + 90,  # Position below the score
        settings.button_width,
        settings.button_height,
        "Main Menu", # Changed text here
        font
    )
    back_to_menu_button.draw(screen)

    return back_to_menu_button # Return the button so its clicks can be handled




# handel all events such as move, fire, start game, etc 
def handle_events(game_data):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_data.running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            return event 
        elif event.type == pg.KEYDOWN and game_data:
            if event.key == pg.K_LEFT and game_data.spaceship:
                game_data.spaceship.move("left", Constants.window_width) # type: ignore
                print("mmovign left ")
            elif event.key == pg.K_RIGHT and game_data.spaceship:
                game_data.spaceship.move("right", Constants.window_width) # type: ignore
                print("moving right")
            elif event.key == pg.K_SPACE and game_data.spaceship:
                current_time_for_bullet_charging = pg.time.get_ticks()
                if current_time_for_bullet_charging - game_data.last_shot_time > game_data.bullet_cooldown:
                    print("firing bullet, space bar is pressed")
                    # create a a new bullet objet 
                    bullet = game_data.spaceship.fire()
                    # added to the bulelt list 
                    game_data.bullets.append(bullet)
                    # upate the last shot time 
                    game_data.last_shot_time = current_time_for_bullet_charging
        
            # rn the click event for button handling
    return None

# main game loop 
def main():
    # Initialize pygame
    pg.init()

    
    # Create game objects
    settings = GameSettings()
    game_data = GameData()
    # game_data.last_shot_time = -1000

    
    # Initialize display
    screen = pg.display.set_mode((settings.screen_width, settings.screen_height))
    font = pg.font.Font(None, settings.font_size)
    last_enemy_spawn_time = pg.time.get_ticks()

    
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
                    print("Game started!") 
                    ship_x = (Constants.window_width // 2)
                    ship_y = Constants.window_height - 40
                    # create a new spaceship object
                    game_data.spaceship = Spaceship(ship_x, ship_y) # type: ignore
                    game_data.current_state = GameState.PLAYING
                    if game_data.spaceship:
                        print("spaceship is created!")
                    else: 
                        print("No spaceship created!")
                    game_start_sound.play()

        # game logic, firing bullets, enemy spaceship colliiosn, enemy spawn, enemy being killed by the bullet
        elif game_data.current_state == GameState.PLAYING:
            draw_game(screen, game_data)
            
            # draw the spaceship on the screen 
            if game_data.spaceship:
                game_data.spaceship.draw(screen)

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
            if current_time_for_enemy_respawing - last_enemy_spawn_time > game_data.enemy_spawn_delay:
                # the 40 is the width of the enemy, change it accordingly as the enemy width changes
                new_enemy = Enemy(random.randint(0, Constants.window_width - 40), 0)
                # add the new eneemy to the enemy list 
                game_data.enemies.append(new_enemy)
                # update the last_enemy_spawn_time to current time 
                last_enemy_spawn_time = current_time_for_enemy_respawing 
            
            # enemy-bullet colllision detection, [:] is a list comprehension to iterate over a copy of the list
            for bullet in game_data.bullets[:]:
                for enemy in game_data.enemies[:]:
                    if bullet.bullet_rect.colliderect(enemy.enemy_rect):
                        game_data.bullets.remove(bullet)
                        game_data.enemies.remove(enemy)
                        game_data.score += 1 
                        break
                    
            # enemy-spaceship collision detection 
            for enemy in game_data.enemies[:]:
                if enemy.enemy_rect.colliderect(game_data.spaceship.spaceship_rect):
                    collision_sound.play()
                    game_data.lives -= 1
                    game_data.enemies.remove(enemy)
                    break


            # enemy movement
            for enemy in game_data.enemies[:]:
                enemy.move()
                enemy.draw(screen)
                # enemy hits the bottom of the screen? game over 
                if enemy.y + enemy.height >= Constants.window_height:
                    game_data.current_state = GameState.GAME_OVER

    
        elif game_data.current_state == GameState.GAME_OVER:
            game_over_menu_button = draw_game_over(screen, font, game_data, settings)
            if click_event and click_event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                if game_over_menu_button.is_clicked(mouse_pos):
                    print("going back to main menue")
                    game_data.reset_game()
                    game_data.current_state = GameState.MENU
        # Update display
        pg.display.flip()
    
    # end the game 
    pg.quit()



if __name__ == "__main__":
    main()


