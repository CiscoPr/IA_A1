import pygame

pygame.init()

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
options = ["Start Game", "Options", "Quit Game"]
option_rects = []

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

# Clean up
pygame.quit()
