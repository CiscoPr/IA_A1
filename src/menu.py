import pygame
import os
from level import *


def level_selector(title_font, screen, size, background, font, pointer_x):
    number_of_levels = 0
    maps_folder = "../src/maps"

    for level in os.listdir(maps_folder):
        if os.path.isfile(os.path.join(maps_folder, level)):
            number_of_levels += 1

    print("Number of levels: ", number_of_levels)

    options = []
    option_rects = []
    for i in range(1, number_of_levels+1):
        options.append("Level " + str(i))

    options.append("Return")
    done3 = False
    selected_option = 0

    while not done3:

        title_surface = title_font.render("Level selector", True, (255,255,255))
        title_rect = title_surface.get_rect(center=(screen.get_width() // 2, 150))
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option -= 1
                    if selected_option < 0:
                        selected_option = len(options) - 1
                elif event.key == pygame.K_DOWN:
                    selected_option += 1
                    if selected_option >= len(options):
                        selected_option = 0
                elif event.key == pygame.K_RETURN:
                    is_selected = True
                    if options[selected_option] == "Return":
                        done3 = True
                    else:
                        filepath = "../src/maps/map{0}".format(selected_option+1)
                        gamestate = GameState(filepath)
                        game_loop(gamestate, screen, size)

                    print("Selected option:", options[selected_option])



        # Clear the screen
        screen.blit(background, (0, 0))
        # Draw title
        screen.blit(title_surface, title_rect)

        for i, option in enumerate(options):
            option_surface = font.render(option, True, (255, 255, 255))
            option_rect = option_surface.get_rect(center=(screen.get_width() // 2, 300 + i * 50))
            option_rects.append(option_rect)
            screen.blit(option_surface, option_rect)

            # Check if Enter button is pressed and change pointer size
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            pointer_size = font.size("> ")[1] + 10
        else:
            pointer_size = font.size("> ")[1]
        # Draw pointer
        pointer_rect = pygame.Rect(pointer_x, option_rects[selected_option].centery - pointer_size // 2, pointer_size, pointer_size)

        pygame.draw.rect(screen, (255, 255, 255), pointer_rect)
        #if is_selected:
        #    pygame.draw.rect(screen, (255, 255, 255), pointer_rect)
        #else:


        # Flip the display
        pygame.display.flip()

        # Wait for a bit to control the animation speed
        pygame.time.wait(20)




def mode_selector(title_font, size, screen, font, pointer_x, background):
    options = ["Player Mode", "AI Mode", "Return"]
    option_rects = []

    done2 = False
    selected_option = 0

    while not done2:

        title_surface = title_font.render("Play Game", True, (255,255,255))
        title_rect = title_surface.get_rect(center=(screen.get_width() // 2, 150))
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option -= 1
                    if selected_option < 0:
                        selected_option = len(options) - 1
                elif event.key == pygame.K_DOWN:
                    selected_option += 1
                    if selected_option >= len(options):
                        selected_option = 0
                elif event.key == pygame.K_RETURN:
                    if options[selected_option] == "Return":
                        done2 = True
                    elif options[selected_option] == "Player Mode":
                        level_selector(title_font, screen, size, background, font, pointer_x)
                    elif options[selected_option] == "AI Mode":
                        level_selector()
                    print("Selected option:", options[selected_option])



        # Clear the screen
        screen.blit(background, (0, 0))
        # Draw title
        screen.blit(title_surface, title_rect)

        for i, option in enumerate(options):
            option_surface = font.render(option, True, (255, 255, 255))
            option_rect = option_surface.get_rect(center=(screen.get_width() // 2, 300 + i * 50))
            option_rects.append(option_rect)
            screen.blit(option_surface, option_rect)

            # Check if Enter button is pressed and change pointer size
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            pointer_size = font.size("> ")[1] + 10
        else:
            pointer_size = font.size("> ")[1]
        # Draw pointer
        pointer_rect = pygame.Rect(pointer_x, option_rects[selected_option].centery - pointer_size // 2, pointer_size, pointer_size)

        pygame.draw.rect(screen, (255, 255, 255), pointer_rect)
        #if is_selected:
        #    pygame.draw.rect(screen, (255, 255, 255), pointer_rect)
        #else:


        # Flip the display
        pygame.display.flip()

        # Wait for a bit to control the animation speed
        pygame.time.wait(20)


def main_menu():


    # Set up the window
    size = (800, 600)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Space Block")

    # Set up the fonts
    font = pygame.font.Font("../src/assets/fonts/PressStart2P-Regular.ttf", 24)
    title_font = pygame.font.Font("../src/assets/fonts/PressStart2P-Regular.ttf", 48)

    # Load background image
    background = pygame.image.load("../src/assets/images/background.jpg")

    # Set up menu options
    options = ["Start Game", "Instructions", "Quit Game"]


    # Set up pointer
    pointer_size = font.size("> ")[1]
    pointer_x = 200
    pointer_y = 50
    selected_option = 0
    is_selected = False

    # Set up title
    title_surface = title_font.render("Space Block", True, (255, 255, 255))
    title_rect = title_surface.get_rect(center=(screen.get_width() // 2, 150))




    # Loop until the user clicks the close button.
    done = False


    # Main game loop
    while not done:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option -= 1
                    if selected_option < 0:
                        selected_option = len(options) - 1
                elif event.key == pygame.K_DOWN:
                    selected_option += 1
                    if selected_option >= len(options):
                        selected_option = 0
                elif event.key == pygame.K_RETURN:
                    is_selected = True
                    if options[selected_option] == "Start Game":
                        mode_selector(title_font, size, screen, font, pointer_x, background)
                    #elif options[selected_option] == "Instructions":

                    elif options[selected_option] == "Quit Game":
                        done = True
                    print("Selected option:", options[selected_option])

        # Clear the screen
        screen.blit(background, (0, 0))

        # Draw title
        screen.blit(title_surface, title_rect)

        # Draw menu options
        option_rects = []
        for i, option in enumerate(options):
            option_surface = font.render(option, True, (255, 255, 255))
            option_rect = option_surface.get_rect(center=(screen.get_width() // 2, 300 + i * 50))
            option_rects.append(option_rect)
            screen.blit(option_surface, option_rect)


        # Check if Enter button is pressed and change pointer size
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            pointer_size = font.size("> ")[1] + 10
        else:
            pointer_size = font.size("> ")[1]
        # Draw pointer
        pointer_rect = pygame.Rect(pointer_x, option_rects[selected_option].centery - pointer_size // 2, pointer_size, pointer_size)

        pygame.draw.rect(screen, (255, 255, 255), pointer_rect)
        #if is_selected:
        #    pygame.draw.rect(screen, (255, 255, 255), pointer_rect)
        #else:


        # Flip the display
        pygame.display.flip()

        # Wait for a bit to control the animation speed
        pygame.time.wait(20)

