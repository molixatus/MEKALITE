# game.py

import pygame
from pygame import mixer
from itertools import cycle
from game_stages import handle_stage_transitions, draw_stage2_content

class Game:
    def __init__(self):
        # Initialize constants and game state
        self.colBlack = (20, 0, 20)
        self.colWhite = (255, 255, 215)
        
        pygame.init()
        self.WIDTH, self.HEIGHT = 1280, 720
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("CMD MECHA")
        self.screen.fill(self.colBlack)
        
        programIcon = pygame.image.load('mol.png')
        pygame.display.set_icon(programIcon)
        self.clock = pygame.time.Clock()
        
        self.mixer_init()
        self.mixer_music_load_and_play()
        
        self.BLINK_EVENT = pygame.USEREVENT + 0
        pygame.time.set_timer(self.BLINK_EVENT, 500)
        
        self.mmState = 0
        self.mmStage = 0
        self.buts = 0
        self.running = True
        self.blink_surfaces = None
        self.current_head_display_index = 0

    def mixer_init(self):
        mixer.init()

    def mixer_music_load_and_play(self):
        mixer.music.load("T4.mp3")
        mixer.music.set_volume(0.1)
        mixer.music.play()

    def clicksound(self):
        click = pygame.mixer.Sound("click.wav")
        click.play()

    def getfont(self, size):
        return pygame.font.Font('DTM-Mono.otf', size)

    def blinker(self):
        font = self.getfont(42)
        onText = font.render('>>>', False, pygame.Color(self.colWhite))
        offText = font.render('>>>', False, pygame.Color(self.colBlack))
        return cycle([onText, offText])

    def draw_linear_gradient_rect(self, surface, rect, color1, color2, horizontal=True):
        for i in range(rect.width if horizontal else rect.height):
            interp_factor = i / (rect.width if horizontal else rect.height)
            r = int(color1[0] + (color2[0] - color1[0]) * interp_factor)
            g = int(color1[1] + (color2[1] - color1[1]) * interp_factor)
            b = int(color1[2] + (color2[2] - color1[2]) * interp_factor)
            
            if horizontal:
                pygame.draw.line(surface, (r, g, b), (rect.x + i, rect.y), (rect.x + i, rect.y + rect.height - 1))
            else:
                pygame.draw.line(surface, (r, g, b), (rect.x, rect.y + i), (rect.x + rect.width - 1, rect.y + i))

    def drawByu(self, text, xStart, yStart):
        for ii, item_text in enumerate(text):
            current_col_black, current_col_white = (self.colWhite, self.colBlack) if self.mmState == ii else (self.colBlack, self.colWhite)
            
            font = self.getfont(42)
            text_surface = font.render(item_text, True, current_col_white)
            text_rect = text_surface.get_rect(topleft=(xStart, yStart + (ii * 50)))
            text_rect.width += 100

            if self.mmState == ii:
                self.draw_linear_gradient_rect(self.screen, text_rect, current_col_black, current_col_white, horizontal=True)
            else:
                pygame.draw.rect(self.screen, current_col_black, text_rect)
                
            self.screen.blit(text_surface, text_rect)
        self.buts = len(text)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            # Handle stage transitions via the imported function
            self.mmStage, self.mmState, self.current_head_display_index = handle_stage_transitions(
                event, self.mmState, self.mmStage, self.screen, self.colBlack, self.current_head_display_index
            )
            
            # Stage 0 blinker logic
            if event.type == self.BLINK_EVENT and self.mmStage == 0:
                if self.blink_surfaces is None:
                    self.blink_surfaces = self.blinker()
                blink_surface = next(self.blink_surfaces)
                blink_rect = blink_surface.get_rect(topleft=(10, 10))
                self.screen.blit(blink_surface, blink_rect)
            
            # Stage 0 to Stage 1 transition
            elif event.type == pygame.KEYDOWN and self.mmStage == 0:
                self.clicksound()
                self.mmStage = 1
                self.screen.fill(self.colBlack)

            # Main menu navigation (Stage 1)
            elif event.type == pygame.KEYDOWN and self.mmStage == 1:
                self.clicksound()
                if event.key == pygame.K_w and self.mmState > 0:
                    self.mmState -= 1
                elif event.key == pygame.K_s and self.mmState < self.buts - 1:
                    self.mmState += 1
                elif event.key == pygame.K_ESCAPE:
                    self.running = False

            # mech builder
            elif event.type == pygame.KEYDOWN and self.mmStage == 2:
                self.clicksound()

    
    def run(self):
        while self.running:
            self.clock.tick(60)

            self.process_events()

            if self.mmStage == 1:
                self.drawByu(['Blest blame', 'blustomize mleckh', 'bloptions', 'blehdits'], 20, 20)
            elif self.mmStage == 2:
                draw_stage2_content(self.screen, self.colWhite, self.current_head_display_index)
            
            pygame.display.update()
        
        pygame.quit()

# This is the main entry point for the game
if __name__ == '__main__':
    game = Game()
    game.run()