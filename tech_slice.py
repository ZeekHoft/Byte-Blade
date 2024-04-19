
import threading



def play_game():
    from main_game import generate_random_targets, hide_cross_lives, \
        draw_text, draw_lives, show_gameover_screen
    generate_random_targets()
    hide_cross_lives()
    draw_text()
    draw_lives()
    show_gameover_screen()

def control_cursor():
    from eye import mouse_control
    mouse_control()

def main():
    game_thread = threading.Thread(target=play_game)
    cursor_thread = threading.Thread(target=control_cursor)

    cursor_thread.start()

    game_thread.start()

    game_thread.join()
    cursor_thread.join()

if __name__ == '__main__':
    main()







