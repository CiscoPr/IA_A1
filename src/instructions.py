from pygame import Surface
import pygame
def display_instructions(screen: Surface, background: Surface) -> None:

    first_instruction = pygame.image.load("../src/assets/images/instructions1.png")
    second_instruction = pygame.image.load("../src/assets/images/instructions2.png")

    # Set up a boolean to keep track of whether the loop should continue
    running = True

    screen.blit(background, (0, 0))

    while running:
        screen.blit(first_instruction, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    screen.blit(second_instruction, (0, 0))
                    pygame.display.flip()
                    running2 = True
                    while running2:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_RETURN:
                                    running2 = False
                    running = False

        pygame.display.flip()