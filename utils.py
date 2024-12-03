from enum import Enum
import pygame

class SettingsManager(Enum):
    GRID_SIZE = 10
    CELL_SIZE = 40
    COLOR_SELECTOR_COLOR = (128, 64, 0)
    BACKGROUND_COLOR = (0, 0, 0)
    MENU_BACKGROUND_COLOR = (50, 50, 50)
    TEXT_COLOR = (255, 255, 255)
    NUMBER_COLOR = (0, 255, 0)
    BUTTON_COLOR = (0, 169, 153)
    BUTTON_HOVER_COLOR = (0, 218, 255)
    GRID_BACKGROUND_COLOR = (0, 155, 155)
    TITLE_BAR_COLOR = (100, 100, 100)
    SIZE_BARRA_SUPERIOR = 50
    DEFAULT_COLOR = (255, 255, 255)
    SELECCION_MODO_COLOR = (255, 255, 255, 192)

class Colores(Enum):
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
    
class BotonSeleccionNivel:
    def __init__(self, x, y, action=None, win=False):
        self.x = x
        self.y = y

        # Carga de imagenes
        self.imagen_boton_undone = pygame.transform.scale(pygame.image.load('resources/button/undone.png'), (50, 50))
        self.imagen_boton_done = pygame.transform.scale(pygame.image.load('resources/button/done.png'), (50, 50))
        self.imagen_boton_done_active = pygame.transform.scale(pygame.image.load('resources/button/done_active.png'), (50, 50))
        self.imagen_boton_undone_active = pygame.transform.scale(pygame.image.load('resources/button/undone_active.png'), (50, 50))

        self.imagen_actual = self.imagen_boton_undone
        self.rect = self.imagen_boton_undone.get_rect(topleft=(x, y))
        self.action = action
        self.selected = False
        self.win = win

        # Animación del botón cuando se gana por primera vez
        self.animacion_index = 0
        self.animacion_tiempo = 0
        self.animacion_win_completada = False
        self.frames_boton_win = []
        self.frame_index_boton_win = 0
        for i in range(1,18):
            img = pygame.image.load("resources/button/win_button/win_"+str(i)+".png")
            img = pygame.transform.scale(img, (50, 50))
            self.frames_boton_win.append(img)    

    def draw(self, screen):
        if self.win and not self.animacion_win_completada:
            self.win_animation()
            self.imagen_actual = self.frames_boton_win[self.animacion_index]
        elif self.win:
            self.imagen_actual = self.imagen_boton_done_active if self.selected else self.imagen_boton_done
        else:
            self.imagen_actual = self.imagen_boton_undone_active if self.selected else self.imagen_boton_undone
        screen.blit(self.imagen_actual, self.rect.topleft)

    def set_selected(self, selected):
        self.selected = selected
        if self.win:
            self.imagen_actual = self.imagen_boton_done_active if self.selected else self.imagen_boton_done
        else:
            self.imagen_actual = self.imagen_boton_undone_active if self.selected else self.imagen_boton_undone

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()
        elif event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.set_selected(True)
            else:
                self.set_selected(False)
    
    def check_hover(self, pos):
        return self.rect.collidepoint(pos)
    
    def set_win_true(self):
        self.win = True

    def win_animation(self):
        self.animacion_tiempo += 1
        if self.animacion_tiempo >= 5:
            self.animacion_tiempo = 0
            self.animacion_index += 1
            if self.animacion_index >= len(self.frames_boton_win):
                self.animacion_index = len(self.frames_boton_win) - 1
                self.animacion_win_completada = True
