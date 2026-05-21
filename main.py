# main_game.py (your existing game file, modified)

import pygame
from pygame import mixer
import time
from itertools import cycle
# Import the new module
from game_stages import handle_stage_transitions, draw_stage2_content

def clicksound():
    click = pygame.mixer.Sound("click.wav")
    click.play()

def mmMusic():
    mixer.init()
    mixer.music.load("T4.mp3")
    mixer.music.set_volume(0.1)
    mixer.music.play()

def mmMusicStop():
    mixer.music.stop()

def initPygame(colBlack):
    pygame.init()
    WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("CMD MECHA")
    screen.fill(colBlack)
    programIcon = pygame.image.load('mol.png')
    pygame.display.set_icon(programIcon)
    clock = pygame.time.Clock()
    mmMusic()
    return screen, clock

def blinker(colBlack, colWhite):
    font = getfont(42)
    onText = font.render('>>>', False, pygame.Color(colWhite))
    offText = font.render('>>>', False, pygame.Color(colBlack))
    blink_surfaces = cycle([onText, offText])
    return blink_surfaces

def eventHandle(event, colBlack, colWhite, mmState, mmStage, buts, blink_surfaces, BLINK_EVENT, screen):
    running = True
    
    # Delegate stage transitions to the new function
    # Note: current_display_index is handled by handle_stage_transitions, but needs to be passed in from main loop
    # We will adjust main() to manage current_display_index
    
    if event.type == pygame.QUIT:
        running = False
    elif event.type == BLINK_EVENT:
        if mmStage == 0:
            if blink_surfaces is None:
                blink_surfaces = blinker(colBlack, colWhite)
            
            blink_surface = next(blink_surfaces)
            blink_rect = blink_surface.get_rect(topleft=(10, 10))
            screen.blit(blink_surface, blink_rect)
    elif event.type == pygame.KEYDOWN:
        clicksound()
        if mmStage == 0:
            mmStage += 1
            screen.fill(colBlack)
        # The main menu key presses (W, S, A, D, ESC, RETURN, SPACE) for mmStage 1 
        # are now implicitly handled here if not caught by stage 2 logic first.
        # This part of eventHandle is primarily for menu navigation, stage 0 transition,
        # and general game exit. Stage-specific logic (like stage 2's D/A keys)
        # will be handled by the imported function.
        if mmStage == 1: # Only process these for main menu navigation
            if event.key == pygame.K_w:
                print("W key pressed!")
                if mmState > 0:
                    mmState -= 1
            elif event.key == pygame.K_s:
                print("S key pressed!")
                if mmState < buts - 1:
                    mmState += 1
            elif event.key == pygame.K_a:
                print("A key pressed!")
            elif event.key == pygame.K_d:
                print("D key pressed!")
            elif event.key == pygame.K_ESCAPE:
                print("ESCAPE key pressed! Exiting...")
                running = False
            elif event.key == pygame.K_RETURN:
                print("RETURN key pressed!")
            elif event.key == pygame.K_SPACE:
                print("SPACE key pressed!")
    
    return running, mmState, mmStage, blink_surfaces

def getfont(size):
    font = pygame.font.Font('DTM-Mono.otf', size)
    return font

def draw_linear_gradient_rect(surface, rect, color1, color2, horizontal=True):
    for i in range(rect.width if horizontal else rect.height):
        interp_factor = i / (rect.width if horizontal else rect.height)
        r = int(color1[0] + (color2[0] - color1[0]) * interp_factor)
        g = int(color1[1] + (color2[1] - color1[1]) * interp_factor)
        b = int(color1[2] + (color2[2] - color1[2]) * interp_factor)
        
        if horizontal:
            pygame.draw.line(surface, (r, g, b), (rect.x + i, rect.y), (rect.x + i, rect.y + rect.height - 1))
        else:
            pygame.draw.line(surface, (r, g, b), (rect.x, rect.y + i), (rect.x + rect.width - 1, rect.y + i))

def drawByu(screen, text, xStart, yStart, mmState, colBlack, colWhite):
    for ii, item_text in enumerate(text):
        current_col_black, current_col_white = (colWhite, colBlack) if mmState == ii else (colBlack, colWhite)
        
        font = getfont(42)
        text_surface = font.render(item_text, True, current_col_white)
        text_rect = text_surface.get_rect(topleft=(xStart, yStart + (ii * 50)))
        text_rect.width += 100

        if mmState == ii:
            draw_linear_gradient_rect(screen, text_rect, current_col_black, current_col_white, horizontal=True)
        else:
            pygame.draw.rect(screen, current_col_black, text_rect)
            
        screen.blit(text_surface, text_rect)
    return len(text)

def main():
    colBlack = (20, 0, 20)
    colWhite = (255, 255, 215)
    
    screen, clock = initPygame(colBlack)

    BLINK_EVENT = pygame.USEREVENT + 0
    pygame.time.set_timer(BLINK_EVENT, 500)

    mmState = 0
    mmStage = 0
    buts = 0
    running = True
    blink_surfaces = None
    current_head_display_index = 0 # New variable to track head display

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            # Handle general events and main menu navigation
            running, mmState, mmStage, blink_surfaces = eventHandle(
                event, colBlack, colWhite, mmState, mmStage, buts, blink_surfaces, BLINK_EVENT, screen
            )
            
            # Handle specific stage transitions and logic using the imported function
            new_mmStage, new_mmState, new_current_head_display_index = handle_stage_transitions(
                event, mmState, mmStage, screen, colBlack, current_head_display_index
            )
            # Update our main loop variables with the results
            mmStage = new_mmStage
            mmState = new_mmState
            current_head_display_index = new_current_head_display_index
            
            if not running:
                break

        if not running:
            break

        # Drawing logic based on mmStage
        if mmStage == 0:
            pass # Blinker is drawn in eventHandle for stage 0
        elif mmStage == 1:
            buts = drawByu(screen, ['Blest blame','blustomize mleckh', 'bloptions', 'blehdits'], 20, 20, mmState, colBlack, colWhite)
        elif mmStage == 2:
            draw_stage2_content(screen, colWhite, current_head_display_index)
            # You might want to clear the screen once per frame in stage 2
            # screen.fill(colBlack) # Uncomment if you want screen to be black behind the text
        
        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()