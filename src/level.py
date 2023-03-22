import pygame


# Define some colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Set the width and height of each block
BLOCK_WIDTH = 50
BLOCK_HEIGHT = 50



def game_display(gamestate, screen, size):
    
    # Determine the dimensions of the map
    map_width = len(gamestate.board[0])
    map_height = len(gamestate.board)

    # Load the background image
    background = pygame.image.load("../src/assets/images/background.jpg")

    # Calculate the margins needed to center the map
    left_margin = (size[0] - map_width * BLOCK_WIDTH) // 2
    top_margin = (size[1] - map_height * BLOCK_HEIGHT) // 2


    # Blit the background image onto the screen
    screen.blit(background, (0, 0))

    # Draw the map
    for row in range(map_height):
        for col in range(map_width):
            if gamestate.board[row][col] == 0:
                continue
            elif gamestate.board[row][col] == 1:
                color = BLUE
            elif gamestate.board[row][col] == 2:
                color = RED
            elif gamestate.board[row][col] == 3:
                color = GREEN

            # Calculate the position of the block
            x = col * BLOCK_WIDTH + left_margin
            y = row * BLOCK_HEIGHT + top_margin

                # Draw the block
            pygame.draw.rect(screen, color, [x, y, BLOCK_WIDTH, BLOCK_HEIGHT])

        # Update the screen
        pygame.display.flip()

# Clean up Pygame
#pygame.quit()
    
    
    
    
    
    
    
    # Loop until the user clicks the close button
    #done = False
#
    ## Main game loop
    #while not done:
#
    #    # Handle events
    #    for event in pygame.event.get():
    #        if event.type == pygame.QUIT:
    #            done = True
#
    #        # Handle arrow key presses to move the red block
    #        elif event.type == pygame.KEYDOWN:
    #            if event.key == pygame.K_LEFT and red_block_pos[1] > 0:
    #                red_block_pos[1] -= 1
    #            elif event.key == pygame.K_RIGHT and red_block_pos[1] < map_width - 1:
    #                red_block_pos[1] += 1
    #            elif event.key == pygame.K_UP and red_block_pos[0] > 0:
    #                red_block_pos[0] -= 1
    #            elif event.key == pygame.K_DOWN and red_block_pos[0] < map_height - 1:
    #                red_block_pos[0] += 1