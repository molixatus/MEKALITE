# game_stages.py

import pygame

def handle_stage_transitions(event, mmState, mmStage, screen, colBlack, current_display_index):
    """
    Handles stage transitions based on key presses.
    Returns updated mmStage, mmState, and current_display_index.
    """
    if event.type == pygame.KEYDOWN:
        if mmStage == 1 and event.key == pygame.K_SPACE:
            mmStage = 2
            screen.fill(colBlack)  # Clear screen for new stage
            current_display_index = 0  # Reset for the new display sequence
            print("Transitioning to Stage 2: Head Customization")
        elif mmStage == 2:
            if event.key == pygame.K_d:
                current_display_index = (current_display_index + 1) % 4
                print(f"Head display: {current_display_index + 1}/4")
            elif event.key == pygame.K_a:
                current_display_index = (current_display_index - 1 + 4) % 4
                print(f"Head display: {current_display_index + 1}/4")
            elif event.key == pygame.K_RETURN:
                # Assuming ENTER confirms the selection and moves to the next part (e.g., body)
                print(f"Head (1/4) selected. Moving to next customization part.")
                mmStage = 3 # Example: Move to stage 3 for body customization
                screen.fill(colBlack)
                current_display_index = 0
            elif event.key == pygame.K_ESCAPE:
                # Go back to main menu or previous stage
                mmStage = 1
                screen.fill(colBlack)
                mmState = 0 # Reset menu selection
                current_display_index = 0
                print("Exiting Head Customization, returning to main menu.")

    return mmStage, mmState, current_display_index

def draw_stage2_content(screen, colWhite, current_display_index):
    """
    Draws the 'head (X/4)' text on the screen for mmStage 2.
    """
    font = pygame.font.Font('DTM-Mono.otf', 42)
    text = f'head ({current_display_index + 1}/4)'
    text_surface = font.render(text, True, colWhite)
    text_rect = text_surface.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
    screen.blit(text_surface, text_rect)

    # You might also want to display a placeholder graphic for the head here
    # For example:
    # head_image = pygame.image.load(f'head_asset_{current_display_index + 1}.png')
    # head_rect = head_image.get_rect(midbottom=(screen.get_width() / 2, screen.get_height() / 2 - 50))
    # screen.blit(head_image, head_rect)