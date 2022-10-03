from ast import main
from pyexpat.errors import XML_ERROR_UNEXPECTED_STATE
import time
import pygame,sys, random
from pygame.math import Vector2
import button
import pickle

class SNAKE:
    def __init__(self):
        block1 = Vector2(3,7)                      #pos of body
        block2 = Vector2(4,7)
        block3 = Vector2(5,7)                      
        self.body = [block3, block2, block1]        #at first snake length of 3
        self.direction = Vector2(0,0)               #doesn't move by default
        self.new_block = False

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()                        # just loading in images and sounds
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()

        self.eating_sound = pygame.mixer.Sound('Sound/eating_sound.wav')
        self.eating_sound.set_volume(0.02)
        self.arcade_game_over_sound = pygame.mixer.Sound('Sound/arcade_game_cover.wav')
        self.arcade_game_over_sound.set_volume(0.02)

    def draw_snake(self):

        self.update_head_graphics()             # puts the images above to the coressponding places to get a smooth snake
        self.update_tail_graphics()

        for index, block in enumerate(self.body):                   # goes through all 'body parts'
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:                                          # draw the head
                screen.blit(self.head, block_rect)
            elif index == (len(self.body)-1):                       # draw the tail
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index+1] - block         # draw the body (horizontal and vertical image)
                next_block = self.body[index-1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical,block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal,block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1 :         # images for taking corners
                        screen.blit(self.body_tl,block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1 :
                        screen.blit(self.body_bl,block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1 :
                        screen.blit(self.body_tr,block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1 :
                        screen.blit(self.body_br,block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]         #updates head direction
        if head_relation == Vector2(1,0):
            self.head = self.head_left
        elif head_relation == Vector2(-1,0):
            self.head = self.head_right
        elif head_relation == Vector2(0,1):
            self.head = self.head_up
        elif head_relation == Vector2(0,-1):
            self.head = self.head_down

    def update_tail_graphics(self):                         # updates tail direction
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0,1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1):
            self.tail = self.tail_down

    def move_snake(self):
        if self.direction != Vector2(0,0):                                                  # dont shorten snake before it starts moving
            if self.new_block == True:
                body_copy = self.body[:]                                                    #dont remove last element because snake 'ate' fruit
                body_copy.insert(0, body_copy[0] + self.direction)                          #movement by adding new element into the ongoing direction
                self.body = body_copy[:]
                self.new_block = False
            else:
                body_copy = self.body[:-1]                                                  #remove last element because snake doesnt get 'bigger'
                body_copy.insert(0, body_copy[0] + self.direction)                          #movement by adding new element into the ongoing direction
                self.body = body_copy[:]

    def add_block(self):                                                                    # if snake.head on fruit
        self.new_block = True

    def play_crunch_sound(self):
        self.eating_sound.play()

    def play_game_over_sound(self):
        self.arcade_game_over_sound.play()

    def reset(self):
        block1 = Vector2(3,7)                      #resetting the snake to the original position
        block2 = Vector2(4,7)
        block3 = Vector2(5,7)                      
        self.direction = Vector2(0,0)
        self.body = [block3, block2, block1]        #at first snake length of 3

class FRUIT:
    def __init__(self):                                                                         # initialize fruit pos
        self.pos = Vector2(12, 7)
        self.fruits = [self.pos]
    
    def draw_fruit(self):

        for fruit in self.fruits:
            x_pos = int(fruit.x * cell_size)
            y_pos = int(fruit.y * cell_size)
            fruit_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)      #create rect
            screen.blit(apple, fruit_rect)                                                                      #draw fruit

    def randomize(self):                                                                        # random fruit position

        self.x = random.randint(0, cell_number-1)
        self.y = random.randint(0, cell_number-1)
        self.pos = Vector2(self.x, self.y)

    def reset_fruit(self):                                                                      # reset fruit position after game over
        
        self.pos = Vector2(12, 7)
        self.fruits = [self.pos]
    
    def add_fruit(self):

        self.fruits.append(self.pos)

class BRICKS:
    def __init__(self):
        self.wall = pygame.image.load('Graphics/wall.png').convert_alpha()
        self.pos = Vector2(12, 7)
        self.bricks = []

    def draw_bricks(self):

        for brick in self.bricks:
            x_pos = int(brick.x * cell_size)
            y_pos = int(brick.y * cell_size)
            brick_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)      #create rect
            screen.blit(self.wall, brick_rect)     

    def reset_bricks(self):                                                                      # reset fruit position after game over
        
        self.pos = Vector2(12, 7)
        self.bricks = []    

    def randomize(self):                                                                        # random fruit position

        self.x = random.randint(0, cell_number-1)
        self.y = random.randint(0, cell_number-1)
        self.pos = Vector2(self.x, self.y)    

    def add_brick(self):
        self.randomize()
        self.bricks.append(self.pos)

class MAIN:
    def __init__(self):
        #Highscore
        self.highscore = 0
        try:
            with open('score.dat', 'rb') as file:
                self.highscore = int(pickle.load(file))
        except:
            self.highscore = 0
        #Entities
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.bricks = BRICKS()

        #Modes

        self.brickable = True
        self.eaten = 0

        self.standard = True
        self.fruity = False
        self.bricky = False

        #Button Modes

        self.starting = True
        self.starting_theme = True

        self.diff_pos_x = 25             # difficulty border pos
        self.diff_pos_y = 150

        self.theme_pos_x = 199
        self.theme_pos_y = 300

        self.cross_pos_x = 205
        self.cross_pos_y = 305

        self.mode_pos_x = 225
        self.mode_pos_y = 125

        #Buttons

        self.sound_on = True
        self.music_on = True

        self.sound = pygame.image.load('Graphics/sound.png').convert_alpha()
        self.sound_muted = pygame.image.load('Graphics/sound_muted.png').convert_alpha()
        self.music = pygame.image.load('Graphics/music.png').convert_alpha()
        self.music_muted = pygame.image.load('Graphics/music_muted.png').convert_alpha()

        self.button_green = pygame.image.load('Graphics/green_button02.png').convert_alpha()
        self.green_box = pygame.image.load('Graphics/green_button06.png').convert_alpha()
        self.green_check = pygame.image.load('Graphics/green_boxCheckmark.png').convert_alpha()
        self.green_cross = pygame.image.load('Graphics/green_boxCross.png').convert_alpha()

        self.button_grey = pygame.image.load('Graphics/grey_button01.png').convert_alpha()
        self.grey_box = pygame.image.load('Graphics/grey_button10.png').convert_alpha()
        self.grey_check = pygame.image.load('Graphics/grey_boxCheckmark.png').convert_alpha()
        self.grey_cross = pygame.image.load('Graphics/grey_boxCross.png').convert_alpha()

        self.button_red = pygame.image.load('Graphics/red_button01.png').convert_alpha()
        self.red_box = pygame.image.load('Graphics/red_button03.png').convert_alpha()
        self.red_check = pygame.image.load('Graphics/red_boxCheckmark.png').convert_alpha()
        self.red_cross = pygame.image.load('Graphics/red_boxCross.png').convert_alpha()

        self.button_color = self.button_green

        #Colors
        self.green1 = (175, 215, 70)    #lighter color
        self.green2 = (167,209,61)      #darker tone
        self.green_border = (56,74,12)

        self.red1 = (150, 60, 0)
        self.red2 = (160, 71, 10)
        self.red_border = (51, 10, 0)

        self.grey1 = (64, 64, 64)
        self.grey2 = (72, 72, 72)
        self.grey_border = (32, 32, 32)

        self.color1 = self.green1
        self.color2 = self.green2
        self.border = self.green_border

        self.color_check = self.green_check

        #Game_States
        self.game_menu = True
        self.pre_game = False
        self.pause_menu = True
        self.settings_menu = False
        self.mode_menu = False
        self.paused = False

        #Images
        self.buttons_image = pygame.image.load('Graphics/arrows.png').convert_alpha()
        self.clicking_image =  pygame.image.load('Graphics/clicking.png').convert_alpha()
        self.trophy = pygame.image.load('Graphics/winner.png').convert_alpha() 
        self.trophy_small = pygame.image.load('Graphics/winner_small.png').convert_alpha() 

        #Sounds
        self.click_sound = pygame.mixer.Sound('Sound/click1.wav')
        self.click_sound.set_volume(0.25)
        self.movement_sound = pygame.mixer.Sound('Sound/gameboy.wav')
        self.movement_sound.set_volume(0.03)

        self.old_direction = Vector2(0,0)

        #Difficulty

        self.diff = "easy"

        self.easy_pressed = True
        self.medium_pressed = False
        self.hard_pressed = False

        try:
            with open('diff.dat', 'rb') as file:
                self.diff = str(pickle.load(file))
                if self.diff == "easy":
                    self.easy_press()
                elif self.diff == "medium":
                    self.medium_press()
                elif self.diff == "hard":
                    self.hard_press()
        except:
            self.theme = "easy"
        
        #Theme

        self.theme = "green"

        self.theme_green = True
        self.theme_red = False
        self.theme_grey = False

        try:
            with open('theme.dat', 'rb') as file:
                self.theme = str(pickle.load(file))
                if self.theme == "green":
                    self.green_press()
                elif self.theme == "red":
                    self.red_press()
                elif self.theme == "grey":
                    self.grey_press()
        except:
            self.theme = "green"

    def update(self):   
        self.snake.move_snake()                                                                 #move snake, check if it eats fruit, check if hits an object (snake or walls)          
        self.check_collision()
        self.check_fail()

    def draw_elements(self):                                                                    #draw all objects on screen
        self.draw_grass()
        self.draw_score()
        self.fruit.draw_fruit()
        if self.bricky:
            self.bricks.draw_bricks()
        self.snake.draw_snake()
        if self.pre_game:
            self.draw_pre_game()
        elif self.game_menu:
            self.draw_sound()
            self.draw_highscore_menu()
            if self.settings_menu:
                self.draw_settings()
            elif self.mode_menu:
                self.draw_mode()
            else:
                self.draw_menu()
        elif self.paused:
            self.draw_sound()
            if self.snake.direction != Vector2(0,0):
                self.old_direction = self.snake.direction
            self.snake.direction = Vector2(0,0)
            self.pause_game()

    def check_collision(self):
        
        for i, fruit in enumerate(self.fruit.fruits):
            if fruit == self.snake.body[0]:
                self.fruit.randomize()
                if not self.fruity:
                    self.fruit.fruits.pop(i)
                self.eaten +=1
                self.fruit.add_fruit()  
                self.snake.add_block()
                self.snake.play_crunch_sound()
                self.brickable = True
            if self.bricky:
                for brick in self.bricks.bricks:
                    if self.snake.body[0] == brick:
                        self.snake.play_game_over_sound()
                        self.game_over()
                        break

        for block in self.snake.body[1:]:
            for i, fruit in enumerate(self.fruit.fruits):
                if block == fruit:
                    self.fruit.randomize()  
                    self.fruit.add_fruit()  
                    self.fruit.fruits.pop(i)
                    break
            if self.bricky:
                for i, brick in enumerate(self.bricks.bricks):
                    if block == brick:
                        self.bricks.randomize()
                        self.bricks.add_brick() 
                        self.bricks.bricks.pop(i)
                        break

        if self.bricky:
            score = int(len(self.snake.body) - 3)
            if score % 5 == 0 and (0 < score < 50) and self.brickable and self.eaten > 2:
                self.bricks.add_brick()
                self.brickable = False
                self.eaten = 0

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
            self.snake.play_game_over_sound()

        for i, block in enumerate(self.snake.body[1:]):
            if self.snake.body[0] == block:
                self.snake.play_game_over_sound()
                self.game_over()

    def game_over(self):
        score = int(len(self.snake.body) - 3)  
        if self.highscore < score:
            self.highscore = score 
            with open('score.dat', 'wb') as file:                       # save new potential highscore
                pickle.dump(self.highscore, file)   
        self.snake.reset()
        self.fruit.reset_fruit()
        if self.bricky:
            self.bricks.reset_bricks()
        self.game_menu = True

    def draw_grass(self):
        grass_color = self.color2                                                                    #checked backround, colors alternating between cells
        for row in range(cell_number):
            if row%2 == 0:
                for col in range(cell_number):
                    if col%2 == 0:
                        grass_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col%2 == 1:
                        grass_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)                                                  # draws score with fruits eaten at the bottom right
        game_font = pygame.font.Font('Font/kenvector_future.ttf',25)
        score_surface = game_font.render(score_text, True, self.border)
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left,score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top,apple_rect.width + score_rect.width + 10 ,apple_rect.height)
        
        pygame.draw.rect(screen, self.color2, bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen,self.border,bg_rect,2)

    def play_click_sound(self):
        self.click_sound.play()

    def draw_highscore_menu(self):
        highscore_text = str(self.highscore)                                                  # draws highscore at the top right
        game_font = pygame.font.Font('Font/kenvector_future.ttf', 40)
        highscore_surface = game_font.render(highscore_text, True, self.border)

        highscore_x = int(575)
        highscore_y = int(40)
        highscore_rect = highscore_surface.get_rect(center = (highscore_x, highscore_y))
        trophy_rect = self.trophy_small.get_rect(midright = (highscore_rect.left - 20, highscore_rect.centery))
        bg_rect = pygame.Rect(trophy_rect.left-10, trophy_rect.top , trophy_rect.width + highscore_rect.width + 40 , trophy_rect.height)
        
        pygame.draw.rect(screen, self.color2, bg_rect)
        screen.blit(highscore_surface, highscore_rect)
        screen.blit(self.trophy_small, trophy_rect)
        pygame.draw.rect(screen,self.border,bg_rect,2)

    def draw_highscore(self):
        highscore_text = str(self.highscore)                                                  # draws highscore during pause in the middle
        game_font = pygame.font.Font('Font/kenvector_future.ttf', 40)
        highscore_surface = game_font.render(highscore_text, True, self.border)
        highscore_x = int(380)
        highscore_y = int(250)
        highscore_rect = highscore_surface.get_rect(center = (highscore_x, highscore_y))
        trophy_rect = self.trophy.get_rect(midright = (highscore_rect.left - 20, highscore_rect.centery))
        bg_rect = pygame.Rect(trophy_rect.left-10, trophy_rect.top , trophy_rect.width + highscore_rect.width + 40 , trophy_rect.height)
        
        pygame.draw.rect(screen, self.color2, bg_rect)
        screen.blit(highscore_surface, highscore_rect)
        screen.blit(self.trophy, trophy_rect)
        pygame.draw.rect(screen,self.border,bg_rect,2)

    def pause_game(self):
        # show score
        # show highscore
        # resume button
        resume_image = self.button_color
        resume_button = button.Button(225, 100, resume_image, 1)

        restart_image = self.button_color
        restart_button = button.Button(225, 350, restart_image, 1)

        menu_image = self.button_color
        menu_button = button.Button(225, 450, menu_image, 1)

        if resume_button.draw(screen):  #if resume button is clicked resume game 
            self.play_click_sound()
            self.snake.direction = self.old_direction
            self.paused = False 
            time.sleep(0.1)
        if restart_button.draw(screen): #if restart button is clicked load pre_game screen
            self.play_click_sound()
            self.paused = False
            self.game_over()
            self.game_menu = False
            self.pre_game = True
            time.sleep(0.1)
        if menu_button.draw(screen):    #if menu button is clicked return to menu
            self.play_click_sound()
            self.game_over()
            self.paused = False
            time.sleep(0.1)

        self.draw_highscore()                                          

        resume_font = pygame.font.Font('Font/kenvector_future.ttf',30)                          # draw actual button with text on it

        resume_text = "RESUME"
        resume_surface = resume_font.render(resume_text, True, self.border)
        resume_rect = resume_surface.get_rect(center = (int(320), int(123)))
        screen.blit(resume_surface, resume_rect)

        restart_text = "RESTART"
        restart_surface = resume_font.render(restart_text, True, self.border)
        restart_rect = restart_surface.get_rect(center = (int(322), int(373)))
        screen.blit(restart_surface, restart_rect)

        menu_text = "MENU"
        menu_surface = resume_font.render(menu_text, True, self.border)
        menu_rect = menu_surface.get_rect(center = (int(322), int(473)))
        screen.blit(menu_surface, menu_rect)
    
    def draw_pre_game(self):
        shape_surface = pygame.Surface((int(6 * cell_size), int(3.5 * cell_size)))  # the size of your rect
        shape_surface.set_alpha(100)                                                # alpha level
        shape_surface.fill((0,0,0))                                                 # this fills the entire surface 
        background_rect = pygame.Rect(int(5 * cell_size), int(2 * cell_size), int(6 * cell_size), int(3.5 * cell_size))
        pygame.draw.rect(screen, (100,100,100), background_rect,  2, 2)                             # draw thin border
        screen.blit(shape_surface,background_rect)                                                  # draw transparent background

        arrows_rect = pygame.Rect(int(6.7 * cell_size), int(2 * cell_size), 1, 1)                   # draw arrows
        screen.blit(main_game.buttons_image, arrows_rect)
        clicking_rect = pygame.Rect(int(8 * cell_size), int(3 * cell_size), 1, 1)                   # draw hand
        screen.blit(main_game.clicking_image, clicking_rect)                                        

        if self.snake.direction != Vector2(0,0):                                                    # if a button for movement is pressed, remove pre_game images
            self.pre_game = False

    def draw_menu(self):                                            # draw main_menu
        play_font = pygame.font.Font('Font/kenvector_future.ttf',30)                            # load in all menu buttons
        play_image = self.button_color
        play_button = button.Button(225, 125, play_image, 1)
        settings_image = self.button_color
        settings_button = button.Button(225, 225, settings_image, 1)
        mode_image = self.button_color
        mode_button = button.Button(225, 325, mode_image, 1)
        quit_image = self.button_color
        quit_button = button.Button(225, 425, quit_image, 1)

        if play_button.draw(screen):                                                          #if button is clicked do something
            self.play_click_sound()
            time.sleep(0.1)
            self.game_menu = False                                                              
            self.pre_game = True
        if settings_button.draw(screen):
            self.play_click_sound()
            time.sleep(0.1)
            self.settings_menu = True 
        if mode_button.draw(screen):
            self.play_click_sound()
            time.sleep(0.1)
            self.mode_menu = True
        if quit_button.draw(screen):
            self.play_click_sound()
            time.sleep(0.1)
            pygame.quit()
            sys.exit()

        play_text = "PLAY"                                                                  # texts that are overlayed over the buttons
        play_surface = play_font.render(play_text, True, self.border)
        play_rect = play_surface.get_rect(center = (int(320), int(148)))
        screen.blit(play_surface, play_rect)

        settings_font = pygame.font.Font('Font/kenvector_future.ttf',25)

        settings_text = "SETTINGS"
        settings_surface = settings_font.render(settings_text, True, self.border)
        settings_rect = settings_surface.get_rect(center = (int(320), int(248)))
        screen.blit(settings_surface, settings_rect)

        mode_text = "MODE"
        mode_surface = play_font.render(mode_text, True, self.border)
        mode_rect = mode_surface.get_rect(center = (int(320), int(348)))
        screen.blit(mode_surface, mode_rect)

        quit_text = "QUIT"
        quit_surface = play_font.render(quit_text, True, self.border)
        quit_rect = quit_surface.get_rect(center = (int(320), int(448)))
        screen.blit(quit_surface, quit_rect)

    def draw_mode(self):                                                                        # function to draw the mode_menu

        play_font = pygame.font.Font('Font/kenvector_future.ttf',30)                            # load in all menu buttons

        standard_image = self.button_color
        standard_button = button.Button(225, 125, standard_image, 1)
        fruity_image = self.button_color
        fruity_button = button.Button(225, 225, fruity_image, 1)
        bricky_image = self.button_color
        bricky_button = button.Button(225, 325, bricky_image, 1)
        back_image = self.button_color
        back_button = button.Button(225, 425, back_image, 1)

        if standard_button.draw(screen) and not self.standard:  #activate standard game mode
            self.mode_pos_x = 225
            self.mode_pos_y = 125
            self.standard = True
            self.fruity = False
            self.bricky = False
            self.play_click_sound()
            time.sleep(0.1)
        if fruity_button.draw(screen) and not self.fruity:  #activate fruity game mode
            self.mode_pos_x = 225
            self.mode_pos_y = 225
            self.standard = False
            self.fruity = True
            self.bricky = False
            self.play_click_sound()
            time.sleep(0.1)
        if bricky_button.draw(screen) and not self.bricky:  #activate bricky game mode
            self.mode_pos_x = 225
            self.mode_pos_y = 325
            self.standard = False
            self.fruity = False
            self.bricky = True
            self.play_click_sound()
            time.sleep(0.1)
        if back_button.draw(screen):                # go back to main_menu
            self.play_click_sound()
            self.mode_menu = False
            time.sleep(0.1)

        settings_font = pygame.font.Font('Font/kenvector_future.ttf',25)

        mode_rect = pygame.Rect(self.mode_pos_x,self.mode_pos_y,190,50)
        pygame.draw.rect(screen,self.border,mode_rect,4)

        standard_text = "STANDARD"                                                      # texts that are overlayed over the buttons
        standard_surface = settings_font.render(standard_text, True, self.border)
        standard_rect = standard_surface.get_rect(center = (int(320), int(148)))
        screen.blit(standard_surface, standard_rect)

        fruity_text = "FRUITY"
        fruity_surface = play_font.render(fruity_text, True, self.border)
        fruity_rect = fruity_surface.get_rect(center = (int(320), int(248)))
        screen.blit(fruity_surface, fruity_rect)

        bricky_text = "BRICKY"
        bricky_surface = play_font.render(bricky_text, True, self.border)
        bricky_rect = bricky_surface.get_rect(center = (int(320), int(348)))
        screen.blit(bricky_surface, bricky_rect) 

        back_text = "BACK"
        back_surface = play_font.render(back_text, True, self.border)
        back_rect = back_surface.get_rect(center = (int(320), int(448)))
        screen.blit(back_surface, back_rect)
    
    def draw_settings(self): 

        button_font = pygame.font.Font('Font/kenvector_future.ttf',23)                            # load in all menu buttons
        difficulty_image = self.button_color
        difficulty_button = button.Button(225, 75, difficulty_image, 1)
        easy_image = self.button_color
        easy_button = button.Button(25, 150, easy_image, 1)
        medium_image = self.button_color
        medium_button = button.Button(225, 150, medium_image, 1)
        hard_image = self.button_color
        hard_button = button.Button(425, 150, hard_image, 1)

        color_image = self.button_color
        color_button = button.Button(225, 225, color_image, 1)
        green_theme = self.green_box
        green_button = button.Button(200, 300, green_theme, 1)
        red_theme = self.red_box
        red_button = button.Button(300, 300, red_theme, 1)
        grey_theme = self.grey_box
        grey_button = button.Button(400, 300, grey_theme, 1)

        back_image = self.button_color
        back_button = button.Button(225, 380, back_image, 1)

        if back_button.draw(screen):                                            #settings buttons for diffulty and color theme
            self.play_click_sound()
            self.settings_menu = False
            time.sleep(0.1)
        if difficulty_button.draw(screen):
            pass
        if easy_button.draw(screen) and not self.easy_pressed:
            self.easy_press()
        if medium_button.draw(screen) and not self.medium_pressed:
            self.medium_press()
        if hard_button.draw(screen) and not self.hard_pressed:
            self.hard_press()
        if color_button.draw(screen):
            pass
        if green_button.draw(screen) and not self.theme_green:
            self.green_press()
        if red_button.draw(screen) and not self.theme_red:
            self.red_press()
        if grey_button.draw(screen) and not self.theme_grey:
            self.grey_press()

        difficulty_text = "DIFFICULTY"
        difficulty_surface = button_font.render(difficulty_text, True, self.border)
        difficulty_rect = difficulty_surface.get_rect(center = (int(322), int(100)))
        screen.blit(difficulty_surface, difficulty_rect)

        easy_text = "EASY"
        easy_surface = button_font.render(easy_text, True, self.border)
        easy_rect = easy_surface.get_rect(center = (int(120), int(173)))
        screen.blit(easy_surface, easy_rect)

        medium_text = "MEDIUM"
        medium_surface = button_font.render(medium_text, True, self.border)
        medium_rect = medium_surface.get_rect(center = (int(320), int(173)))
        screen.blit(medium_surface, medium_rect)

        hard_text = "HARD"
        hard_surface = button_font.render(hard_text, True, self.border)
        hard_rect = hard_surface.get_rect(center = (int(520), int(173)))
        screen.blit(hard_surface, hard_rect)

        theme_text = "THEME"
        theme_surface = button_font.render(theme_text, True, self.border)
        theme_rect1 = theme_surface.get_rect(center = (int(320), int(248)))
        screen.blit(theme_surface, theme_rect1)

        diff_rect = pygame.Rect(self.diff_pos_x,self.diff_pos_y,190,50)
        pygame.draw.rect(screen,self.border,diff_rect,4)

        theme_rect = pygame.Rect(self.theme_pos_x,self.theme_pos_y,50,49)
        pygame.draw.rect(screen,self.border,theme_rect,3)

        cross_rect = pygame.Rect(self.cross_pos_x,self.cross_pos_y,55,55)

        screen.blit(self.color_check,cross_rect)

        back_text = "BACK"
        back_surface = button_font.render(back_text, True, self.border)
        back_rect = back_surface.get_rect(center = (int(320), int(401)))
        screen.blit(back_surface, back_rect)
        
    def draw_sound(self):   # draw the sound icons on the top left
        
        sound_image = self.sound
        sound_button = button.Button(23, 13, sound_image, 1)

        sound_muted_image = self.sound_muted
        sound_muted_button = button.Button(13, 13, sound_muted_image, 1)

        music_image = self.music
        music_button = button.Button(100, 13, music_image, 1)

        music_muted_image = self.music_muted
        music_muted_button = button.Button(100, 13, music_muted_image, 1)

        # mute sound effects and music on click
        if self.sound_on:
            if sound_button.draw(screen):
                self.sound_on = False
                self.play_click_sound()
                self.mute_sound()
                time.sleep(0.1)
        else:
            if sound_muted_button.draw(screen):
                self.sound_on = True
                self.play_click_sound()
                self.set_sound()
                time.sleep(0.1)

        if self.music_on:
            if music_button.draw(screen):
                self.music_on = False
                self.play_click_sound()
                self.mute_music()
                time.sleep(0.1)
        else:
            if music_muted_button.draw(screen):
                self.music_on = True
                self.play_click_sound()
                self.set_music()
                time.sleep(0.1)

    def set_sound(self):
        self.snake.eating_sound.set_volume(0.02)
        self.snake.arcade_game_over_sound.set_volume(0.02)
        self.click_sound.set_volume(0.25)
        self.movement_sound.set_volume(0.03)

    def mute_sound(self):
        self.snake.eating_sound.set_volume(0)
        self.snake.arcade_game_over_sound.set_volume(0)
        self.click_sound.set_volume(0)
        self.movement_sound.set_volume(0)

    def set_music(self):
        pygame.mixer.music.set_volume(0.03)
    
    def mute_music(self):
        pygame.mixer.music.set_volume(0)


    def easy_press(self):
        self.easy_pressed = True
        self.medium_pressed = False
        self.hard_pressed = False
        self.diff_pos_x = 25             # difficulty border pos
        self.dif_pos_y = 150
        self.diff = "easy"
        with open('diff.dat', 'wb') as file:                       # save theme
                pickle.dump(self.diff, file)
        if not self.starting:
            self.play_click_sound()
        else:
            self.starting = False  
        time.sleep(0.1)
        pygame.time.set_timer(SCREEN_UPDATE,125)

    def medium_press(self):
        self.easy_pressed = False
        self.medium_pressed = True
        self.hard_pressed = False
        self.diff_pos_x = 225             # difficulty border pos
        self.diff_pos_y = 150
        self.diff = "medium"
        with open('diff.dat', 'wb') as file:                       # save theme
                pickle.dump(self.diff, file)   
        if not self.starting:
            self.play_click_sound()
        else:
            self.starting = False  
        time.sleep(0.1)
        pygame.time.set_timer(SCREEN_UPDATE,100)
    
    def hard_press(self):
        self.easy_pressed = False
        self.medium_pressed = False
        self.hard_pressed = True
        self.diff_pos_x = 425             # difficulty border pos
        self.diff_pos_y = 150
        self.diff = "hard"
        with open('diff.dat', 'wb') as file:                       # save theme
                pickle.dump(self.diff, file)   
        if not self.starting:
            self.play_click_sound()
        else:
            self.starting = False  
        time.sleep(0.1)
        pygame.time.set_timer(SCREEN_UPDATE,75)

    def green_press(self):  #green theme
        self.theme_pos_x = 199
        self.theme_pos_y = 300
        self.cross_pos_x = 205
        self.cross_pos_y = 305
        self.color_check = self.green_check
        self.theme_green = True
        self.theme_red = False
        self.theme_grey = False
        self.button_color = self.button_green
        self.color1 = self.green1
        self.color2 = self.green2
        self.border = self.green_border
        self.theme = "green"
        with open('theme.dat', 'wb') as file:                       # save theme
                pickle.dump(self.theme, file)   
        if not self.starting_theme:
            self.play_click_sound()
        else:
            self.starting_theme = False  
        time.sleep(0.1)

    def red_press(self): #red theme
        self.theme_pos_x = 299
        self.theme_pos_y = 300
        self.cross_pos_x = 305
        self.cross_pos_y = 305
        self.color_check = self.red_check
        self.theme_green = False
        self.theme_red = True
        self.theme_grey = False
        self.button_color = self.button_red
        self.color1 = self.red1
        self.color2 = self.red2
        self.border = self.red_border
        self.theme = "red"
        with open('theme.dat', 'wb') as file:                       # save theme
                pickle.dump(self.theme, file) 
        if not self.starting_theme:
            self.play_click_sound()
        else:
            self.starting_theme = False  
        time.sleep(0.1)
    
    def grey_press(self): #grey theme
        self.theme_pos_x = 399
        self.theme_pos_y = 300
        self.cross_pos_x = 405
        self.cross_pos_y = 305
        self.color_check = self.grey_check
        self.theme_green = False
        self.theme_red = False
        self.theme_grey = True
        self.button_color = self.button_grey
        self.color1 = self.grey1
        self.color2 = self.grey2
        self.border = self.grey_border
        self.theme = "grey"
        with open('theme.dat', 'wb') as file:                       # save theme
                pickle.dump(self.theme, file) 
        if not self.starting_theme:
            self.play_click_sound()
        else:
            self.starting_theme = False  
        time.sleep(0.1)

    def draw_sound_buttons(self):
        pass

    def direction_sound(self):
        self.movement_sound.play()
        self.movement_sound.fadeout(1000)


pygame.mixer.pre_init(44100,-16,2,512)                      # some sound settings
pygame.init()
cell_size = 40                                              # screen size
cell_number = 16
pygame.display.set_caption("Snakestar")                     # game name
screen = pygame.display.set_mode((cell_size*cell_number, cell_size*cell_number))        #create screen with predefined dimensions
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple.png').convert_alpha()                         # load apple graphic

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,125)                                                # screen gets updated every 100 ms

music = pygame.mixer.music.load('Sound/League_of_Legends_-_Burn_It_All_Down.wav')
pygame.mixer.music.set_volume(0.03)
pygame.mixer.music.play(-1)

main_game = MAIN()

while True:

    screen.fill(pygame.Color(main_game.color1))

    for event in pygame.event.get():                                                    # close window with the X
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:                                                # change direction of snake when arrow key gets pressed
            if not main_game.game_menu:
                if not main_game.paused:
                    if event.key == pygame.K_UP:
                        if main_game.snake.direction.y != 1 and main_game.snake.direction.y != -1: 
                            main_game.snake.direction = Vector2(0,-1)
                            main_game.direction_sound()
                    if event.key == pygame.K_DOWN:
                        if main_game.snake.direction.y != 1 and main_game.snake.direction.y != -1:
                            main_game.snake.direction = Vector2(0,1)
                            main_game.direction_sound()
                    if event.key == pygame.K_LEFT and main_game.snake.direction != Vector2(0):      # so that u cant run into yourself at the beginning of the game
                        if main_game.snake.direction.x != 1 and main_game.snake.direction.x != -1:
                            main_game.snake.direction = Vector2(-1,0)
                            main_game.direction_sound()
                    if event.key == pygame.K_RIGHT:
                        if main_game.snake.direction.x != 1 and main_game.snake.direction.x != -1:
                            main_game.snake.direction = Vector2(1,0)
                            main_game.direction_sound()
            if event.key == pygame.K_ESCAPE:                                                        # escape button to navigate in menu or pause game
                if main_game.settings_menu:
                    main_game.game_menu = True
                    main_game.settings_menu = False
                    main_game.play_click_sound()
                elif main_game.mode_menu:
                    main_game.game_menu = True
                    main_game.mode_menu = False
                    main_game.play_click_sound()
                elif main_game.pre_game:
                    main_game.game_menu = True
                    main_game.pre_game = False
                    main_game.play_click_sound()
                elif main_game.paused:
                    main_game.paused = False
                    main_game.snake.direction = main_game.old_direction
                    main_game.play_click_sound()
                    break
                elif not main_game.paused and not main_game.game_menu:
                    main_game.paused = True    
                    main_game.play_click_sound() 
            if event.key == pygame.K_RETURN and not main_game.settings_menu and not main_game.mode_menu:                                            # enter to go to game screen from menu
                if not main_game.paused and main_game.game_menu == True:
                    main_game.play_click_sound()
                    main_game.pre_game = True
                main_game.game_menu = False

    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)                                                                  

# maybe background music
# some sort of menu to change speed, game mode (game mode with walls e.g)
# change theme in menu 
# direction list that remembers which direction u want to go in for smoother feel
# highscore