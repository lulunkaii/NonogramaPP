from enum import Enum
import pygame

class SettingsManager(Enum):
    GRID_SIZE = 10
    CELL_SIZE = 40
    DEFAULT_COLOR = (255, 255, 255)
    CLICKED_COLOR = (0, 0, 0)
    COLOR_SELECTOR_COLOR = (128, 64, 0)
    BACKGROUND_COLOR = (0, 0, 0)
    MENU_BACKGROUND_COLOR = (50, 50, 50)
    TEXT_COLOR = (255, 255, 255)
    NUMBER_COLOR = (0, 255, 0)
    BUTTON_COLOR = (0, 169, 153)
    BUTTON_HOVER_COLOR = (0, 218, 255)
    GRID_BACKGROUND_COLOR = (0, 155, 155)
    TITLE_BAR_COLOR = (100, 100, 100)

class colorCelda(Enum):
        DEFAULT = (255, 255, 255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        BLUE = (0, 0, 255)

class Boton:
    def __init__(self, text, pos, size, font, action):
        self.rect = pygame.Rect(pos, size)
        self.color = SettingsManager.BUTTON_COLOR.value
        self.hover_color = SettingsManager.BUTTON_HOVER_COLOR.value
        self.text = text
        self.font = font
        self.action = action

    def draw(self, surface, offset=0, seleccionado=False):
        rect = self.rect.move(0, offset)
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if rect.collidepoint(mouse_pos) else self.color

        pygame.draw.rect(surface, color, rect, border_radius=10)
        if seleccionado:
            pygame.draw.rect(surface, SettingsManager.BUTTON_HOVER_COLOR.value, self.rect, 3, border_radius=10)
        text_surface = self.font.render(self.text, True, SettingsManager.TEXT_COLOR.value)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event, offset=0):
        rect = self.rect.move(0, offset)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if rect.collidepoint(event.pos):
                self.action()
                