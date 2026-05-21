# event_handler.py

import pygame
from game_stages import handle_stage_transitions
# You'll need to pass the clicksound function to this module since it's used here
# and defined in main.py, or move it here. For simplicity, we will pass it as an argument.

def handle_events(events, state):
    """
    Processes all events in the event queue and updates the game state.
    :param events: A list of pygame events.
    :param state: A dictionary or object containing all relevant game state variables.
    :return: An updated state dictionary.
    """
    running = state['running']
    mmStage = state['mmStage']
    mmState = state['mmState']
    buts = state['buts']
    blink_surfaces = state['blink_surfaces']
    screen = state['screen']
    colBlack = state['colBlack']
    colWhite = state['colWhite']
    BLINK_EVENT = state['BLINK_EVENT']
    current_head_display_index = state['current_head_display_index']
    
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        
        # Handle stage transitions first, as this logic is higher-level
        mmStage, mmState, current_head_display_index = handle_stage_transitions(
            event, mmState, mmStage, screen, colBlack, current_head_display_index
        )
        
        # Then handle other events based on the current stage
        if event.type == BLINK_EVENT and mmStage == 0:
            if blink_surfaces is None:
                # We need a way to get the blinker function from the main file.
                # For now, let's assume it's passed as part of the state or imported.
                # Let's add it to the state dictionary passed from main.
                pass  # This part needs to be handled by the main loop still
        
        elif event.type == pygame.KEYDOWN:
            # We'll need the clicksound function here. Let's pass it in the state.
            # state['clicksound']()
            if mmStage == 0:
                mmStage = 1
                screen.fill(colBlack)
            elif mmStage == 1:
                # Main menu navigation
                if event.key == pygame.K_w and mmState > 0:
                    mmState -= 1
                elif event.key == pygame.K_s and mmState < buts - 1:
                    mmState += 1
                elif event.key == pygame.K_ESCAPE:
                    running = False
    
    # Pack the state back up and return it
    state['running'] = running
    state['mmStage'] = mmStage
    state['mmState'] = mmState
    state['blink_surfaces'] = blink_surfaces
    state['current_head_display_index'] = current_head_display_index
    
    return state