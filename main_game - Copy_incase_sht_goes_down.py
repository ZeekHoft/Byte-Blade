

import pygame, sys
from pygame import mixer
import os
import random



player_lives = 4
score = 0
best_score = 0

targets = ["apple", "watermelon", "tomato", "bomb"]



WIDTH = 1000
HEIGHT = 700
FPS = 10


pygame.init()
pygame.mixer.pre_init()
pygame.display.set_caption("Slice and Dice")
Display_Game = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)





slicing_sfx = pygame.mixer.Sound("sfx\slice_sfx.mp3")



background = pygame.image.load("background3.png")
font = pygame.font.Font(os.path.join(os.getcwd(), "brownie-stencil-font\BrownieStencil-8O8MJ.ttf"), 32)
score_text = font.render(f"Score: {score}", True, (WHITE))
best_score_text = font.render(f"Best Score: {best_score}", True, (WHITE))
lives_icon = pygame.image.load("images\heart.png")



def generate_random_targets(target):
    target_path = "targets/" + target + ".png"
    data[target] = {
        'img': pygame.image.load(target_path),
        'x': random.randint(100, 500),
        'y': HEIGHT,
        'speed_x': random.randint(-10, 10),
        'speed_y': random.randint(-80, -60),
        'throw': False,
        't':0,
        'hit': False,

    }

    if random.random() >= 0.75:
        data[target]['throw'] = True
    else:
        data[target]['throw'] = False

data =  {}
for target in targets:
    generate_random_targets(target)



def hide_cross_lives(x,y):
    Display_Game.blit(pygame.image.load("images/x_heart.png"), (x,y))



font_name = pygame.font.match_font("brownie-stencil-font\BrownieStencil-8O8MJ.ttf")


def draw_text(display, text, size, x,y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    Display_Game.blit(text_surface, text_rect)



def draw_lives(display, x, y, lives, image):
    for i in range(lives):
        img = pygame.image.load(image)
        img_rect = img.get_rect()
        img_rect.x = int(x + 80 * i)
        img_rect.y = y
        display.blit(img, img_rect)



def show_gameover_screen():
    Display_Game.blit(background, (0,0))
    draw_text(Display_Game, "SLICE AND DICE!!", 64, WIDTH / 2, HEIGHT / 4)
    if not game_over:
        draw_text(Display_Game, f"Score: {score}", 40, WIDTH / 2, 450)
        draw_text(Display_Game, f"Best Score: {best_score}", 40, WIDTH / 2 , 600)


    draw_text(Display_Game, "Press Enter to play!", 24, WIDTH/ 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False





first_round = True
game_over = True
game_running = True
while game_running:
    if game_over:
        if first_round:
            show_gameover_screen()
            first_round = False

        game_over = False
        player_lives = 4
        draw_lives(Display_Game, 700, 5, player_lives, 'images/heart.png')
        score = 0
        best_score = best_score 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False


    Display_Game.blit(background, (0,0))
    Display_Game.blit(score_text, (0,0))
    Display_Game.blit(best_score_text, (0,40))
    draw_lives(Display_Game, 690, 5, player_lives, 'images/heart.png')



    for key, value in data.items():
        if value['throw']:
            value['x'] += value['speed_x']
            value['y'] += value['speed_y']
            value['speed_y'] += (1 * value['t'])
            value['t'] += 1

            if value['y'] <= HEIGHT:
                Display_Game.blit(value['img'], (value['x'], value['y']))

            else:
                generate_random_targets(key)

            current_position = pygame.mouse.get_pos()

            if (not value['hit'] and current_position[0] > value['x'] and current_position[0] < value['x'] + 70 #giya kw kaiad sa sensitivity ka mouse to the target pos
                and current_position[1] > value['y'] and current_position[1] < value['y'] + 70):
                slicing_sfx.play()

                if key == 'bomb':
                    player_lives -= 1
                    if player_lives == 0:
                        hide_cross_lives(690, 15)
                    elif player_lives == 1:
                        hide_cross_lives(725, 15)
                    elif player_lives == 2:
                        hide_cross_lives(760, 15)
                    if player_lives < 0:
                        show_gameover_screen()
                        game_over = True

                    half_fruit_path = "images/explosion.png"
                else:
                    half_fruit_path = "targets/" + "half_" + key + ".png"

                value['img'] = pygame.image.load(half_fruit_path)
                value['speed_x'] += 10
                if key!= 'bomb':
                    score += 1
                    if key != 'bomb' and score >= best_score:
                        best_score += 1


                score_text = font.render('Score : ' + str(score), True, (255, 255, 255))
                best_score_text = font.render('Best Score: ' + str(best_score), True, (255, 255, 255))
                value['hit'] = True
        else:
            generate_random_targets(key)

    pygame.display.update()
    clock.tick(FPS)



pygame.quit()

