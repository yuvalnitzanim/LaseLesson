from classes.Game import *
import pygame
new_game = None


def main():
    pygame.init()
    # Create the screen and show it
    screen_size = (WINDOW_WIDTH, WINDOW_HEIGHT)
    screen = pygame.display.set_mode(screen_size)

    pygame.display.set_caption('Super Mario')

    global new_game
    new_game = Game(screen)

    # Display all drawings we have defined
    pygame.display.flip()

    status = running()
    while status:
        if new_game.is_game_over():
            show_game_over(screen)
        else:
            # Check if the player wants to end the game
            status = running()
            if status:
                on_tick()

    # Close The window
    pygame.quit()


def on_tick():
    if not new_game.is_game_over():
        new_game.move_objects()
        new_game.show_points_text()
        new_game.display_objects_to_screen()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            new_game.move_mario("left")
        elif keys[pygame.K_RIGHT]:
            new_game.move_mario("right")
        if keys[pygame.K_UP]:
            new_game.move_mario("jump")
        elif keys[pygame.K_DOWN]:
            new_game.move_mario("bend")
        # time.sleep(0.3)


def running():
    """
    The function checks when the game will end.
    In addition, the function checks the mouse click events.
    :return: None
    """
    status = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            status = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 1 is the left mouse button, 2 is middle, 3 is right.
            if event.button == 1:
                new_game.on_click(event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                status = False

    pygame.display.flip()

    return status


def show_game_over(screen):
    draw_text(screen, "GAME OVER", 64, WINDOW_WIDTH / 2 - 180, WINDOW_HEIGHT / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting = False
                pygame.quit()


def draw_text(screen, text, size, width, height):
    font = pygame.font.SysFont('Arial', size)
    img = font.render(text, True, BLACK)
    screen.blit(img, (width, height))


main()
