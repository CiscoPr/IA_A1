import pygame

def ai_select(title_font, screen, font, pointer_x, background):
    options = ["Beginner - BFS", "Beginner - DFS", "Expert - A*" , "Return"]
    option_rects = []

    done = False
    selected_option = 0

    while not done:

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
                        done = True
                    elif options[selected_option] == "Beginner - BFS":      # TODO- add the AI mode
                        print("Beginner - BFS")
                    elif options[selected_option] == "Beginner - DFS":      # TODO- add the AI mode
                        print("Beginner - DFS")
                    elif options[selected_option] == "Expert - A*":         # TODO- add the AI mode
                        print("Expert - A*")
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
