

import pygame, sys
from pygame import mixer
import os
import random



player_lives = 4
score = 0
best_score = 0



targets = ["Laptop_Virus", "Phone_Virus", "Tablet_Virus","Computer_Virus", "Computer", "Laptop", "Phone", "Tablet"]



HEIGHT, WIDTH = 980 , 1820

#WIDTH, HEIGHT= 1000, 700
FPS = 10


#make the game center
x_axis_gamescreen = 0
y_axis_gamescreen = 0


#for the scoring draw text
x_axis_text_score = 100
y_axis_text_score = 100

#offset trail affect
offset_x = 70
offset_y = 70
max_cursor_positions = 8



pygame.init()
pygame.mixer.pre_init()
pygame.display.set_caption("Slice and Dice")

programIcon = pygame.image.load("CursorTrail\Kunai.png")
pygame.display.set_icon(programIcon)


#Display_Game = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
Display_Game = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()


WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)




game_music = pygame.mixer.Sound("sfx\Daisy.mp3")
slicing_sfx = pygame.mixer.Sound("sfx\slice_sfx.mp3")
destruction_sfx = pygame.mixer.Sound("sfx\slice_techs.mp3")


background = pygame.image.load("background6.png")
font = pygame.font.Font(os.path.join(os.getcwd(), "brownie-stencil-font\COMPUTERRobot.ttf"), 60)
score_text = font.render(f"Score: {score}", True, (WHITE))
best_score_text = font.render(f"Best Score: {best_score}", True, (WHITE))

lives_icon = pygame.image.load("images\heart2.png")



def generate_random_targets(target):
    target_path = "tech_targets/" + target + ".png"
    data[target] = {
        'img': pygame.image.load(target_path),
        'x': random.randint(300, 1520),
        'y': HEIGHT,
        'speed_x': random.randint(-10, 10),
        'speed_y': random.randint(-100, -60),
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



font_name = pygame.font.match_font("brownie-stencil-font\COMPUTERRobot.ttf")


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
    Display_Game.blit(background, (x_axis_gamescreen,y_axis_gamescreen))
    draw_text(Display_Game, "SLICE AND DICE!!", 64, WIDTH / 2, HEIGHT / 4)
    if not game_over:
        draw_text(Display_Game, f"Score: {score}", 40, WIDTH / 2, 450)
        draw_text(Display_Game, f"Best Score: {best_score}", 40, WIDTH / 2, 600)


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


trail_images = [pygame.image.load(f"CursorTrail\cursorTrail{i}.png") for i in range(1, 9)]  # Replace with your image paths
cursor_trail = []


change_cursor = pygame.image.load("CursorTrail\Kunai.png")
change_cursor = pygame.transform.scale(change_cursor, (126, 126))

pygame.mouse.set_visible(False)



game_music.play(-1)
while game_running:
    if game_over:
        if first_round:
            show_gameover_screen()
            first_round = False
        game_over = False
        player_lives = 4
        draw_lives(Display_Game, 1500, 5, player_lives, 'images/heart2.png')
        score = 0
        best_score = best_score

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False




    Display_Game.blit(background, (x_axis_gamescreen,y_axis_gamescreen))
    Display_Game.blit(score_text, (x_axis_gamescreen,y_axis_gamescreen))
    Display_Game.blit(best_score_text, (0,40))
    draw_lives(Display_Game, 1500, 5, player_lives, 'images/heart2.png')


    cursor_pos = pygame.mouse.get_pos()
    Display_Game.blit(change_cursor, cursor_pos)


    mouse_pos = pygame.mouse.get_pos()
    cursor_trail.append(mouse_pos)
    if len(cursor_trail) > max_cursor_positions:
        cursor_trail.pop(0)

    # Render cursor trail
    for i, pos in enumerate(cursor_trail):
        trail_image = trail_images[i % len(trail_images)]  # Cycle through images
        trail_pos = (pos[0] + offset_x, pos[1] + offset_y)
        Display_Game.blit(trail_image, trail_pos )




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

            if (not value['hit'] and current_position[0] > value['x'] and current_position[0] < value['x'] + 100 and
                    current_position[1] > value['y'] and current_position[1] < value['y'] + 100):

                slicing_sfx.play()

                if key in [ 'Laptop', 'Phone', 'Tablet', 'Computer']:  # Check if the key is one of the targets to lose life
                    player_lives -= 1
                    score -= 1
                    if player_lives < 0:
                        show_gameover_screen()
                        game_over = True
                    else:
                        hide_cross_lives(1500 + 5 * (3 - player_lives), 15)  # Adjusting heart position based on lives left

                    half_fruit_path = "images/explosion.png"
                else:
                    half_fruit_path = "tech_targets/Break_" + key + ".png"

                value['img'] = pygame.image.load(half_fruit_path)
                value['speed_x'] += 10

                if key in ['Laptop_Virus', 'Phone_Virus', 'Tablet_Virus', 'Computer_Virus']:
                    score += 1
                    destruction_sfx.play()
                    if score > best_score:
                        best_score = score

                score_text = font.render('Score : ' + str(score), True, (255, 255, 255))
                best_score_text = font.render('\nBest Score: ' + str(best_score), True, (255, 255, 255))

                value['hit'] = True
        else:
            generate_random_targets(key)

    pygame.display.update()
    clock.tick(FPS)



pygame.quit()

