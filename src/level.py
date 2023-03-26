import pygame
import time
from game import *


def game_loop( gamestate,screen, size):

    while True:
        game_display(gamestate, screen, size )
        gamestate = game_move(gamestate)
        if Victory(gamestate):
            display_endgame(screen, 0)
            time.sleep(3)
            break
        elif Defeat(gamestate):
            display_endgame(screen, 1)
            time.sleep(3)
            break

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

    # Horizontal display of cube
    player_blockh1 = pygame.image.load("../src/assets/images/player_blockh1.png")
    player_blockh2 = pygame.image.load("../src/assets/images/player_blockh2.png")

    # Vertical display of cube
    player_blockv1 = pygame.image.load("../src/assets/images/player_blockv1.png")
    player_blockv2 = pygame.image.load("../src/assets/images/player_blockv2.png")

    # Portal display
    portal = pygame.image.load("../src/assets/images/end_portal.png")

    # Path block display
    path_block = pygame.image.load("../src/assets/images/path_block.png")

    # Blit the background image onto the screen
    screen.blit(background, (0, 0))

    # Draw the map
    for row in range(map_height):
        for col in range(map_width):
            if gamestate.board[row][col] == 0:
                continue
            elif gamestate.board[row][col] == 1 or gamestate.board[row][col] == 2:
                x = col * BLOCK_WIDTH + left_margin
                y = row * BLOCK_HEIGHT + top_margin
                screen.blit(path_block, (x, y))

            elif gamestate.board[row][col] == 3:
                 x = col * BLOCK_WIDTH + left_margin
                 y = row * BLOCK_HEIGHT + top_margin
                 screen.blit(portal, (x, y))


    x = gamestate.piece.position[0]* BLOCK_WIDTH + left_margin
    y = gamestate.piece.position[1]* BLOCK_HEIGHT + top_margin
    if gamestate.piece.piece_state == PieceState.UP:
        screen.blit(player_blockh1, (x, y))
    elif gamestate.piece.piece_state == PieceState.VERTICAL:
         screen.blit(player_blockv1, (x, y))
         screen.blit(player_blockv2, (x, y + BLOCK_HEIGHT))
    elif gamestate.piece.piece_state == PieceState.HORIZONTAL:
         screen.blit(player_blockh1, (x, y))
         screen.blit(player_blockh2, (x + BLOCK_WIDTH, y))

    # Draw Piece
        # Update the screen
    pygame.display.flip()

# Clean up Pygame
#pygame.quit()

def game_move(gamestate):

    done = False
    # Handle events
    while not done:
        for event in pygame.event.get():
    #        zif event.type == pygame.QUIT:
    #            done = True
    # Handle arrow key presses to move the red block
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    gamestate= execute_move(gamestate, MoveDirection.LEFT)
                    done = True
                elif event.key == pygame.K_RIGHT:
                    gamestate = execute_move(gamestate, MoveDirection.RIGHT)
                    done = True
                elif event.key == pygame.K_UP:
                    gamestate = execute_move(gamestate, MoveDirection.UP)
                    done = True
                elif event.key == pygame.K_DOWN:
                    gamestate = execute_move(gamestate, MoveDirection.DOWN)
                    done = True
    return gamestate

def display_endgame(screen, w_or_l):
    print(w_or_l)
    if w_or_l == 0:
        endscreen = pygame.image.load("../src/assets/images/you_win.png")
    else:
        endscreen = pygame.image.load("../src/assets/images/you_lose.png")
    screen.blit(endscreen, (0, 0))
    pygame.display.flip()


def start_game(filepath):
    board: list(list(int)) = []
    piece: Piece = Piece((0,0), PieceState.UP,2)
    with open(filepath) as f:
        lines = f.read().splitlines()
        for (y, line) in enumerate(lines):
            current_row = []
            for (x, char) in enumerate(line.split(' ')):
                if (char == '2'):
                    piece.position = (x, y)
                    current_row.append(1)
                    continue
                current_row.append(int(char))
            board.append(current_row)
    return GameState(board, piece)