import pygame
import sys
import time


from game import Piece, PieceState, execute_move, Victory, Defeat, Teleport, MoveDirection, GameState, breadth_first_search


def game_loop(gamestate,screen, size):
    number_moves = 0
    font = pygame.font.Font("../src/assets/fonts/PressStart2P-Regular.ttf", 20)
    while True:
        game_display(gamestate, screen, size)

        moves_text = font.render("Moves: {}".format(number_moves), True, (255,255,255))
        moves_rect = moves_text.get_rect()
        moves_rect.topright = (size[0]-10, 10)
        screen.blit(moves_text, moves_rect)
        pygame.display.flip()
        gamestate = game_move(gamestate)
        number_moves += 1
        if gamestate == 0:
            return number_moves
        elif Victory(gamestate):
            display_endgame(screen, 0)
            time.sleep(3)
            return number_moves
        elif Defeat(gamestate):
            display_endgame(screen, 1)
            time.sleep(3)
            return number_moves

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

    # Tp block display
    tp_block = pygame.image.load("../src/assets/images/tp_portal.png")

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

            elif gamestate.board[row][col] == 4:
                 x = col * BLOCK_WIDTH + left_margin
                 y = row * BLOCK_HEIGHT + top_margin
                 screen.blit(tp_block, (x,y))


    x = gamestate.piece.position[0]* BLOCK_WIDTH + left_margin
    y = gamestate.piece.position[1]* BLOCK_HEIGHT + top_margin
    if gamestate.piece.piece_state == PieceState.UP:
        screen.blit(player_blockh1, (x, y))
    elif gamestate.piece.piece_state == PieceState.VERTICAL:
        for blocks in range(gamestate.piece.height):
            screen.blit(player_blockv1, (x, y+BLOCK_HEIGHT*blocks))
    elif gamestate.piece.piece_state == PieceState.HORIZONTAL:
        for blocks in range(gamestate.piece.height):
            screen.blit(player_blockh1, (x+blocks*BLOCK_WIDTH, y))
         

    # Draw Piece
        # Update the screen
    pygame.display.flip()

# Clean up Pygame
#pygame.quit()

def game_move(gamestate):
    if gamestate.isAi:
        next_move = gamestate.getAiMove()
        gamestate = execute_move(gamestate, next_move, True)[0]
    else:
        done = False
        # Handle events
        while not done:
            for event in pygame.event.get():
        # Handle arrow key presses to move the red block
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return 0
                    elif event.key == pygame.K_LEFT:
                        gamestate= execute_move(gamestate, MoveDirection.LEFT, False)[0]
                        done = True
                    elif event.key == pygame.K_RIGHT:
                        gamestate = execute_move(gamestate, MoveDirection.RIGHT, False)[0]
                        done = True
                    elif event.key == pygame.K_UP:
                        gamestate = execute_move(gamestate, MoveDirection.UP, False)[0]
                        done = True
                    elif event.key == pygame.K_DOWN:
                        gamestate = execute_move(gamestate, MoveDirection.DOWN, False)[0]
                        done = True
    return gamestate

def display_endgame(screen, w_or_l):
    # print(w_or_l)
    if w_or_l == 0:
        endscreen = pygame.image.load("../src/assets/images/you_win.png")
    else:
        endscreen = pygame.image.load("../src/assets/images/you_lose.png")
    screen.blit(endscreen, (0, 0))
    pygame.display.flip()


def start_game(filepath, isAi, mode = 0):
    board: list(list(int)) = []
    piece: Piece = Piece((0,0), PieceState.UP,2)
    firstPortal: tuple[int, int] = None
    secondPortal: tuple[int, int] = None
    portalMap: dict[tuple[int, int], tuple[int, int]] = {}

    with open(filepath) as f:
        lines = f.read().splitlines()
        height=lines.pop(0)
        piece.height=int(height)
        for (y, line) in enumerate(lines):
            current_row = []
            for (x, char) in enumerate(line.split(' ')):

                if (char == '2'):
                    piece.position = (x, y)
                    current_row.append(1)
                    continue

                elif (char == '4'):
                    if firstPortal is None:
                        firstPortal = (x,y)
                    else:
                        secondPortal = (x,y)

                current_row.append(int(char))
            board.append(current_row)

    if (firstPortal is None and (secondPortal is not None)) or (secondPortal is None and (firstPortal is not None)):
        sys.stderr.write("Map contains only one portal.")
        exit(1)
    elif firstPortal is not None and secondPortal is not None:
        portalMap[firstPortal] = secondPortal
        portalMap[secondPortal] = firstPortal

    if isAi:
        initialGameState = GameState(board, piece, portalMap, isAi=True, aiLevel=mode)
        initialGameState.setAiMoves()
        return initialGameState
    return GameState(board, piece, portalMap, isAi=False)