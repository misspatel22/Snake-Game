import pygame
import random
import os
pygame.mixer.init()
pygame.init()

# colors
white = (255,255,255)
red = (255,0,0)
black = (0,0,0)
green = (38, 148, 37)
orange = (241, 104, 12)

# creating window
screen_width = 900
screen_heigth = 600
gameWindow = pygame.display.set_mode((screen_width,screen_heigth))

# backgroung image
bgimg = pygame.image.load("Snk_image.jpg")
bgimg = pygame.transform.scale(bgimg,(screen_width,screen_heigth)).convert_alpha()


#game title
pygame.display.set_caption("Snake Game")
pygame.display.update()

clock = pygame.time.Clock()
font = pygame.font.SysFont('Harrington',30)

def text_screen(text, color, X, Y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [X,Y])

def plot_snake(gameWindow, color, snk_list ,snake_size):
    for X,Y in snk_list:
        pygame.draw.rect(gameWindow,color,[X,Y,snake_size,snake_size])
snk_list = []
snk_length = 1

def welcome():
    exit_game = False
    while not exit_game:
        bgimg = pygame.image.load("snakelogo.png")
        bgimg = pygame.transform.scale(bgimg,(screen_width,screen_heigth)).convert_alpha()
        gameWindow.blit(bgimg,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('Snkgame_backgrd_music.mp3')
                    pygame.mixer.music.play()
                    gameloop()
        pygame.display.update()
        clock.tick(40)

# game loop
def gameloop():
    # game specific variable
    exit_game = False
    game_over = False
    snake_X = 45
    snake_Y = 55
    velocity_X = 0
    velocity_Y = 0
    snk_list = []
    snk_length = 1
    #check if hiscore file exists
    if(not os.path.exists("hiscore.txt")):
        with open("hiscore.txt","w") as f:
            f.write("0")
    with open("hiscore.txt","r") as f:
        hiscore = f.read()
    food_X = random.randint(20,screen_width/2)
    food_Y = random.randint(20,screen_heigth/2)
    score = 0
    init_velocity = 2
    snake_size = 20
    food_size = 15
    fps = 40
    while not exit_game:
        if game_over:
            with open("hiscore.txt","w") as f:
                f.write(str(hiscore))
            gameWindow.fill(white)
            backimg = pygame.image.load("snk_gameover_pic.jpg")
            backimg = pygame.transform.scale(backimg,(screen_width,screen_heigth)).convert_alpha()
            gameWindow.blit(backimg,(0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_X =  init_velocity
                        velocity_Y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_X = - init_velocity
                        velocity_Y = 0
                    if event.key == pygame.K_UP:
                        velocity_Y = - init_velocity
                        velocity_X = 0
                    if event.key == pygame.K_DOWN:
                        velocity_Y = init_velocity
                        velocity_X = 0

            snake_X = snake_X + velocity_X
            snake_Y = snake_Y + velocity_Y

            if abs(snake_X - food_X)<7 and abs(snake_Y - food_Y)<7:
                score += 10
                food_X = random.randint(20,screen_width/2)
                food_Y = random.randint(20,screen_heigth/2)
                snk_length += 3
                if score>int(hiscore):
                    hiscore = score


            gameWindow.fill(white)
            gameWindow.blit(bgimg,(0,0))
            text_screen("Score: " + str(score) + "  Hiscore:" + str(hiscore), red, 5, 5)
            pygame.draw.rect(gameWindow,orange,[food_X,food_Y,food_size,food_size])
            head = []
            head.append(snake_X)
            head.append(snake_Y)
            snk_list.append(head)
            if len(snk_list)>snk_length:
                del snk_list[0]
            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load('Gameover_music.mp3')
                pygame.mixer.music.play()
            if snake_X<0 or snake_X>screen_width or snake_Y<0 or snake_Y>screen_heigth:
                game_over = True
                pygame.mixer.music.load('Gameover_music.mp3')
                pygame.mixer.music.play()
            # pygame.draw.rect(gameWindow,black,[snake_X,snake_Y,snake_size,snake_size])
            plot_snake(gameWindow, green, snk_list,snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()
welcome()

