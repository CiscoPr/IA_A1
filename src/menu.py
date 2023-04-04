import pygame
import os
from level import *
from instructions import *
from game import AiLevel


def level_selector(title_font, screen: Surface, size: tuple[int, int], background: Surface, font, pointer_x, isAi: bool, mode: AiLevel = AiLevel.BFS) -> None:
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

        title_surface = title_font.render(
            "Level selector", True, (255, 255, 255))
        title_rect = title_surface.get_rect(
            center=(screen.get_width() // 2, 150))
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
                elif event.key == pygame.K_RIGHT:
                    selected_option += 4
                    if selected_option >= len(options):
                        selected_option = 0
                elif event.key == pygame.K_LEFT:
                    selected_option -= 4
                    if selected_option < 0:
                        selected_option = len(options) - 1
                elif event.key == pygame.K_RETURN:
                    is_selected = True
                    if options[selected_option] == "Return":
                        done3 = True
                    else:
                        filepath = "../src/maps/map{0}".format(
                            selected_option+1)
                        if isAi:
                            gamestate = start_game(filepath, True, mode)
                        else:
                            gamestate = start_game(filepath, False)

                        number_of_moves = game_loop(gamestate, screen, size)
                        print("Number of moves: ", number_of_moves)

                    print("Selected option:", options[selected_option])

        # Clear the screen
        screen.blit(background, (0, 0))
        # Draw title
        screen.blit(title_surface, title_rect)

        num_options = len(options)
        num_columns = (num_options + 3) // 4  # round up to nearest integer
        column_width = screen.get_width() // num_columns
        column_offset = (screen.get_width() - num_columns * column_width)
        for i, option in enumerate(options):
            option_surface = font.render(option, True, (255, 255, 255))
            column_index = i // 4
            x = column_offset + column_index * column_width + column_width // 2
            y = 300 + (i % 4) * 50
            if option == "Return":
                x = screen.get_width() // 2
                y = 500
                option_rect = option_surface.get_rect(center=(x, y))
                option_rects.append(option_rect)
                screen.blit(option_surface, option_rect)
            else:
                option_rect = option_surface.get_rect(center=(x, y))
                option_rects.append(option_rect)
                screen.blit(option_surface, option_rect)

            # Check if Enter button is pressed and change pointer size
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            pointer_size = font.size("> ")[1] + 10
        else:
            pointer_size = font.size("> ")[1]
        # Draw pointer
        x, y = option_rects[selected_option].center
        pointer_x = x - font.size("> ")[0] - 80
        pointer_rect = pygame.Rect(
            pointer_x, option_rects[selected_option].centery - pointer_size // 2, pointer_size, pointer_size)

        pygame.draw.rect(screen, (255, 255, 255), pointer_rect)
        # if is_selected:
        #    pygame.draw.rect(screen, (255, 255, 255), pointer_rect)
        # else:

        # Flip the display
        pygame.display.flip()

        # Wait for a bit to control the animation speed
        pygame.time.wait(20)


def ai_select(title_font, screen: Surface, size: tuple[int, int], font, pointer_x, background: Surface) -> None:
    options = ["Beginner - BFS", "Beginner - DFS", "Medium - Greedy",
               "Expert - A*", "Expert - Weighted A*", "Return"]
    option_rects = []

    done = False
    selected_option = 0

    while not done:

        title_surface = title_font.render("Play Game", True, (255, 255, 255))
        title_rect = title_surface.get_rect(
            center=(screen.get_width() // 2, 150))
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
                        done = True
                    elif options[selected_option] == "Beginner - BFS":
                        print("Beginner - BFS")
                        level_selector(
                            title_font, screen, size, background, font, pointer_x, True, AiLevel.BFS)
                    elif options[selected_option] == "Beginner - DFS":
                        print("Beginner - DFS")
                        level_selector(
                            title_font, screen, size, background, font, pointer_x, True, AiLevel.DFS)
                    elif options[selected_option] == "Medium - Greedy":
                        print("Medium - Greedy")
                        level_selector(
                            title_font, screen, size, background, font, pointer_x, True, AiLevel.GREEDY)
                    elif options[selected_option] == "Expert - A*":
                        print("Expert - A*")
                        level_selector(
                            title_font, screen, size, background, font, pointer_x, True, AiLevel.ASTAR)
                    elif options[selected_option] == "Expert - Weighted A*":
                        print("Expert - Weighted A*")
                        level_selector(
                            title_font, screen, size, background, font, pointer_x, True, AiLevel.WASTAR)
                    print("Selected option:", options[selected_option])

        # Clear the screen
        screen.blit(background, (0, 0))
        # Draw title
        screen.blit(title_surface, title_rect)

        for i, option in enumerate(options):
            option_surface = font.render(option, True, (255, 255, 255))
            option_rect = option_surface.get_rect(
                center=(screen.get_width() // 2, 300 + i * 50))
            option_rects.append(option_rect)
            screen.blit(option_surface, option_rect)

            # Check if Enter button is pressed and change pointer size
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            pointer_size = font.size("> ")[1] + 10
        else:
            pointer_size = font.size("> ")[1]

        # Draw pointer
        if selected_option == 2:
            x, y = option_rects[selected_option].center
            pointer_x = x - font.size("> ")[0] - 190
        elif selected_option == 3:
            x, y = option_rects[selected_option].center
            pointer_x = x - font.size("> ")[0] - 140
        elif selected_option == 4:
            x, y = option_rects[selected_option].center
            pointer_x = x - font.size("> ")[0] - 250
        elif selected_option == 5:
            x, y = option_rects[selected_option].center
            pointer_x = x - font.size("> ")[0] - 80
        else:
            x, y = option_rects[selected_option].center
            pointer_x = x - font.size("> ")[0] - 175

        # Draw pointer
        pointer_rect = pygame.Rect(
            pointer_x, option_rects[selected_option].centery - pointer_size // 2, pointer_size, pointer_size)

        pygame.draw.rect(screen, (255, 255, 255), pointer_rect)
        # if is_selected:
        #    pygame.draw.rect(screen, (255, 255, 255), pointer_rect)
        # else:

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

        title_surface = title_font.render("Play Game", True, (255, 255, 255))
        title_rect = title_surface.get_rect(
            center=(screen.get_width() // 2, 150))
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
                        level_selector(title_font, screen, size,
                                       background, font, pointer_x, False)
                    elif options[selected_option] == "AI Mode":
                        ai_select(title_font, screen, size,
                                  font, pointer_x, background)
                        # level_selector(title_font, screen, size, background, font, pointer_x, True)       # probably gonna change this for
                        # AI mode
                    print("Selected option:", options[selected_option])

        # Clear the screen
        screen.blit(background, (0, 0))
        # Draw title
        screen.blit(title_surface, title_rect)

        for i, option in enumerate(options):
            option_surface = font.render(option, True, (255, 255, 255))
            option_rect = option_surface.get_rect(
                center=(screen.get_width() // 2, 300 + i * 50))
            option_rects.append(option_rect)
            screen.blit(option_surface, option_rect)

            # Check if Enter button is pressed and change pointer size
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            pointer_size = font.size("> ")[1] + 10
        else:
            pointer_size = font.size("> ")[1]
        # Draw pointer
        pointer_rect = pygame.Rect(
            pointer_x, option_rects[selected_option].centery - pointer_size // 2, pointer_size, pointer_size)

        pygame.draw.rect(screen, (255, 255, 255), pointer_rect)
        # if is_selected:
        #    pygame.draw.rect(screen, (255, 255, 255), pointer_rect)
        # else:

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
    title_font = pygame.font.Font(
        "../src/assets/fonts/PressStart2P-Regular.ttf", 48)

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
                        mode_selector(title_font, size, screen,
                                      font, pointer_x, background)
                    elif options[selected_option] == "Instructions":
                        display_instructions(screen, background)
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
            option_rect = option_surface.get_rect(
                center=(screen.get_width() // 2, 300 + i * 50))
            option_rects.append(option_rect)
            screen.blit(option_surface, option_rect)

        # Check if Enter button is pressed and change pointer size
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            pointer_size = font.size("> ")[1] + 10
        else:
            pointer_size = font.size("> ")[1]
        # Draw pointer
        pointer_rect = pygame.Rect(
            pointer_x, option_rects[selected_option].centery - pointer_size // 2, pointer_size, pointer_size)

        pygame.draw.rect(screen, (255, 255, 255), pointer_rect)
        # if is_selected:
        #    pygame.draw.rect(screen, (255, 255, 255), pointer_rect)
        # else:

        # Flip the display
        pygame.display.flip()

        # Wait for a bit to control the animation speed
        pygame.time.wait(20)
