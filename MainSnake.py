#Made by: Kouah Mohammed Aymen
#Computer science student at "National Computer science Engineering School, Algiers (ESI)"
#E-mail: jm_kouah@esi.dz
#Github: https://github.com/aymenkouah

#Requires installaling "pygame"
#https://www.pygame.org/news

#Keep the mp3s, wav, photos and the code in the same folder
#if encountering any problem with the music, just comment the Pygame.mixer... lines

#note that there are many bugs with the game as multiple levels which were not implemented and instead were commented
#if you want to use multiple levels, there exists a "borders" function which creates the border
#most of the other functions already are suitable for multiple levels, and it only requires adding few lines of code
#use the variable border to help you(alrready defined)

import pygame
from random import randint
from time import sleep

screen_dim = (1000, 800)
running = True
snake_width = 50
snake_height = 50
initial_x = round(screen_dim[0] / 2)
initial_y = round(screen_dim[1] / 2)
snake_color = (204, 102, 153)
food_color = (randint(0, 255), randint(0, 255), randint(0, 255))
direction = 5
clock = pygame.time.Clock()
ex = []
score = 0
background_color = (149, 202, 228)
level = 0
pause = False

pygame.mixer.init()
pygame.init()

screen = pygame.display.set_mode(screen_dim)


pygame.mixer.music.load(
    "Nostalgia.mp3")
pygame.mixer.music.play(loops=-1)

eat_sound = pygame.mixer.Sound("sf.wav")

game_over = pygame.mixer.Sound(
    "gameover.wav")


pygame.display.set_caption("Kinda like snake")
icon = pygame.image.load("snake.png")
pygame.display.set_icon(icon)


# funcions
snake = [[initial_x, initial_y]]
food = []


def food_gen(food, border):
    if len(food) == 0:
        food = []
        x = (randint(1, screen_dim[0]//snake_width)-1) * snake_width 
        y = (randint(1, screen_dim[1]//snake_height)-1) * snake_height
        return [x, y]

    return food


def move_snake(snake, direction):
    for sn in range(1, len(snake)):
        snake[len(snake) - sn][0] = snake[len(snake) - sn - 1][0]
        snake[len(snake) - sn][1] = snake[len(snake) - sn - 1][1]

    if snake[0][0] < 0:
        snake[0][0] = screen_dim[0]-snake_width
    elif snake[0][0] >= screen_dim[0]:
        snake[0][0] = 0
    elif snake[0][1] < 0:
        snake[0][1] = screen_dim[1]-snake_height
    elif snake[0][1] >= screen_dim[1]:
        snake[0][1] = 0
    else:
        if direction == 1:
            snake[0][0] += snake_width
        elif direction == 2:
            snake[0][1] += snake_height
        elif direction == -1:
            snake[0][0] -= snake_width
        elif direction == -2:
            snake[0][1] -= snake_height

    return snake


def eat(snake, food, eat_sound):
    if snake[0][0] == food[0] and snake[0][1] == food[1]:
        food = []
        eat_sound.play()
    return food

border = []
# def borders(level):
#     border = []
#     if level == 1:
#         for i in range(0, screen_dim[0]//snake_width):
#             border.append([i*snake_width, 0])
#             border.append([i*snake_width, screen_dim[1]-snake_height])
#         for s in range(1, screen_dim[1] // snake_height):
#             border.append([0, (s-1)*snake_height])
#             border.append([screen_dim[0]-snake_width, (s-1)*snake_height])

#     elif level == 2:
#         border = [
#             [0, 0],
#             [0, screen_dim[1] - snake_height],
#             [screen_dim[0] - snake_width, 0],
#             [screen_dim[0]-snake_width, screen_dim[1]-snake_height]
#         ]
#         pos_x_max = screen_dim[0]//snake_width - 4
#         for i in range(4, pos_x_max):
#             border.append([i * snake_width, 4*snake_height])
#             border.append([i * snake_width, screen_dim[1] - 4*snake_height])

#     elif level == 3:
#         for i in range(0, 11):
#             border.append([0, i*snake_height])
#         for i in range(0, 5):
#             border.append([round(screen_dim[0]/2) - 2 *
#                            snake_width, i*snake_height])
#         for i in range(0, 5):
#             border.append([i*snake_width, 6*snake_height])
#         for i in range(4, round(screen_dim[1]/snake_height)):
#             border.append([screen_dim[0]/2 + snake_width, i*snake_height])
#         for i in range(round(screen_dim[0]/(2*snake_width)) + 2, round(screen_dim[0]/snake_width)):
#             border.append([snake_width*i, 5*snake_height])

#     elif level == 4:
#         for i in range(0, int(screen_dim[0]/snake_width), 2):
#             for k in range(1, int(screen_dim[1]/snake_height) - 1):
#                 border.append([i*snake_width, k*snake_height])

#     return border


def gameover(snake, running, border):
    for sn in range(4, len(snake)):
        if snake[0][0] == snake[sn][0] and snake[0][1] == snake[sn][1]:
            return False
    return running


def game_over_text(score):
    font = pygame.font.SysFont(None, 50)
    screen_text = font.render("Game Over", True, (250, 0, 0))
    screen.blit(screen_text, [screen_dim[0]/2 - 100, screen_dim[1]/2 - 40])
    stext = "Your score is: " + str(score)
    score_text = font.render(stext, True, (250, 0, 0))
    screen.blit(score_text, [screen_dim[0]/2 - 150, screen_dim[1]/2 + 10])


def pause_text():
    font = pygame.font.SysFont(None, 100)
    screen_text = font.render("Pause", True, (250, 0, 0))
    screen.blit(screen_text, [screen_dim[0]/2 - 100, screen_dim[1]/2 - 40])


def next_level(level):
    font = pygame.font.SysFont(None, 100)
    level_text = "Next level: " + str(level+1)
    level_text_n = font.render(level_text, True, (250, 100, 20))
    screen.blit(level_text_n, [screen_dim[0]/2 - 150, screen_dim[1]/2 - 40])


music_p = True
mm = 0
while running:
    
    screen.fill(background_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and (direction != -1 or len(snake) == 1):
                direction = 1
            elif event.key == pygame.K_DOWN and (direction != -2 or len(snake) == 1):
                direction = 2
            elif event.key == pygame.K_LEFT and (direction != 1 or len(snake) == 1):
                direction = -1
            elif event.key == pygame.K_UP and (direction != 2 or len(snake) == 1):
                direction = -2
            elif event.key == pygame.K_SPACE:
                pause = not pause

    if pause == True:
        pygame.mixer.music.pause()
        screen.fill(background_color)
        pause_text()
        pygame.display.update()
        mm = 0
        continue

    if music_p != pause and mm == 0:
        pygame.mixer.music.unpause()
    mm += 1


    food = food_gen(food, border)

    snake = move_snake(snake, direction)


    for bord in border:
        pygame.draw.rect(screen, (255, 0, 0),
                         (bord[0], bord[1], snake_width, snake_height))
        pygame.draw.rect(screen, (0, 0, 0),
                         (bord[0], bord[1], snake_width, snake_height), 3)

    pygame.draw.rect(screen, food_color,
                     (food[0], food[1], snake_width, snake_height), 0)
    pygame.draw.rect(screen, (0, 0, 0),
                     (food[0], food[1], snake_width, snake_height), 3)

    for snak in range(0, len(snake)):
        pygame.draw.rect(
            screen, snake_color, (snake[snak][0], snake[snak][1], snake_width, snake_height))
        pygame.draw.rect(
            screen, (0, 0, 0), (snake[snak][0], snake[snak][1], snake_width, snake_height), 2)


    food = eat(snake, food, eat_sound)

    if len(food) == 0:
        score += 1
        snake.append([10000, 10000])

    clock.tick(8)
    running = gameover(snake, running, border)

    if running == False:
        sleep(1)
        pygame.mixer.music.stop()
        screen.fill(background_color)
        game_over_text(score)
        pygame.display.update()
        game_over.play()
        sleep(3)

    print(border)
    print(food)
    pygame.display.update()

pygame.mixer.quit()


pygame.quit()
quit()
