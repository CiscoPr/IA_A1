import pygame


# Define some colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Set the width and height of each block
BLOCK_WIDTH = 50
BLOCK_HEIGHT = 50

def map_generator(level_number):

    if level_number < 10:
        level_string = "0"+str(level_number)
    else:
        level_string = str(level_number)

    # Open the file containing the map
    with open("../src/maps/map"+level_string, "r") as f:
        # Read the map from the file
        map_data = [[int(num) for num in line.split()] for line in f]

    # Determine the dimensions of the map
    map_width = len(map_data[0])
    map_height = len(map_data)

    # Initialize Pygame
    pygame.init()

    # Set up the window
    size = (800, 600)
    screen = pygame.display.set_mode(size)

    # Set the title of the window
    pygame.display.set_caption("Map Viewer")

    # Load the background image
    background = pygame.image.load("../src/assets/images/background.jpg")

    # Calculate the margins needed to center the map
    left_margin = (size[0] - map_width * BLOCK_WIDTH) // 2
    top_margin = (size[1] - map_height * BLOCK_HEIGHT) // 2

    # Set the initial position of the red block
    red_block_pos = [0, 0]

    # Loop until the user clicks the close button
    done = False

    # Main game loop
    while not done:


        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # Handle arrow key presses to move the red block
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and red_block_pos[1] > 0:
                    red_block_pos[1] -= 1
                elif event.key == pygame.K_RIGHT and red_block_pos[1] < map_width - 1:
                    red_block_pos[1] += 1
                elif event.key == pygame.K_UP and red_block_pos[0] > 0:
                    red_block_pos[0] -= 1
                elif event.key == pygame.K_DOWN and red_block_pos[0] < map_height - 1:
                    red_block_pos[0] += 1

        # Blit the background image onto the screen
        screen.blit(background, (0, 0))

        # Draw the map
        for row in range(map_height):
            for col in range(map_width):
                if map_data[row][col] == 0:
                    continue
                elif map_data[row][col] == 1:
                    color = BLUE
                elif map_data[row][col] == 2:
                    color = RED
                elif map_data[row][col] == 3:
                    color = GREEN

                # Calculate the position of the block
                x = col * BLOCK_WIDTH + left_margin
                y = row * BLOCK_HEIGHT + top_margin

                # Draw the block
                pygame.draw.rect(screen, color, [x, y, BLOCK_WIDTH, BLOCK_HEIGHT])

        # Calculate the position of the red block
        red_block_x = red_block_pos[1] * BLOCK_WIDTH + left_margin
        red_block_y = red_block_pos[0] * BLOCK_HEIGHT + top_margin

        # Draw the red block
        pygame.draw.rect(screen, RED, [red_block_x, red_block_y, BLOCK_WIDTH, BLOCK_HEIGHT])

        # Update the screen
        pygame.display.flip()

# Clean up Pygame
pygame.quit()