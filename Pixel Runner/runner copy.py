import pygame
from sys import exit
from random import randint, choice
from pygame.sprite import Group

# Definieren der Bildschirmzustände
class ScreenStates:
    MAIN_MENU = "main_menu"
    GAME = "game"
    GAME_OVER = "game_over"

class ScreenManager:
    def __init__(self):
        self.screens = {}

    def add_screen(self, state, screen):
        self.screens[state] = screen

    def set_current_screen(self, state):
        if state in self.screens:
            self.current_screen = self.screens[state]
        else:
            print("Error: Screen state not found.")

class MainMenu(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font("font/Pixeltype.ttf", 50)
        self.title_text_surface = self.font.render("Pixel Runner", False, "Blue")
        self.title_text_rectangle = self.title_text_surface.get_rect(center=(400, 50))
        self.space_text_surface = self.font.render("Click left mouse button to start...", False, (64, 64, 64))
        self.space_text_rectangle = self.space_text_surface.get_rect(midbottom=(400, 300))

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.title_text_surface, self.title_text_rectangle)
        screen.blit(self.space_text_surface, self.space_text_rectangle)

class Level(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Hier können Level-bezogene Initialisierungen durchgeführt werden
        self.font = pygame.font.Font("font/Pixeltype.ttf", 50)
        self.score = 0

    def update(self):
        # Hier können Level-bezogene Aktualisierungen durchgeführt werden
        self.score += 1  # Beispielhafte Aktualisierung der Punktzahl

    def draw(self, screen):
        # Hier können Level-bezogene Elemente gezeichnet werden
        score_surface = self.font.render(f"Score: {self.score}", False, (255, 255, 255))
        score_rectangle = score_surface.get_rect(center=(400, 50))
        screen.blit(score_surface, score_rectangle)

class GameOver(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font("font/Pixeltype.ttf", 50)
        self.dead_text_surface = self.font.render("Game Over", False, (255, 0, 0))
        self.dead_text_rectangle = self.dead_text_surface.get_rect(center=(400, 175))
        self.space_text_surface = self.font.render("Click left mouse button to restart...", False, (64, 64, 64))
        self.space_text_rectangle = self.space_text_surface.get_rect(midtop=(400, 250))

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.dead_text_surface, self.dead_text_rectangle)
        screen.blit(self.space_text_surface, self.space_text_rectangle)

# Initialisieren von Pygame
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()

# Initialisieren des Bildschirmmanagers
screen_manager = ScreenManager()
main_menu = MainMenu()
level = Level()
game_over = GameOver()
screen_manager.add_screen(ScreenStates.MAIN_MENU, main_menu)
screen_manager.add_screen(ScreenStates.GAME, level)
screen_manager.add_screen(ScreenStates.GAME_OVER, game_over)
screen_manager.set_current_screen(ScreenStates.MAIN_MENU)

# Hauptschleife
game_active = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not game_active:
                screen_manager.set_current_screen(ScreenStates.GAME)
                game_active = True
            elif not game_active and screen_manager.current_screen == ScreenStates.GAME_OVER:
                screen_manager.set_current_screen(ScreenStates.GAME)
                game_active = True

    # Aktualisieren des aktuellen Bildschirms
    screen_manager.current_screen.update()

    # Zeichnen des aktuellen Bildschirms
    screen.fill((0, 0, 0))  # Beispielhafte Hintergrundfarbe
    screen_manager.current_screen.draw(screen)

    pygame.display.update()
    clock.tick(60)
