import pygame
from enum import Enum

class SettingsManager(Enum):
    GRID_SIZE = 10
    CELL_SIZE = 30
    DEFAULT_COLOR = (255, 255, 255)
    CLICKED_COLOR = (0, 0, 0)
    BACKGROUND_COLOR = (0, 0, 0)
    MENU_BACKGROUND_COLOR = (50, 50, 50)
    TEXT_COLOR = (255, 255, 255)
    BUTTON_COLOR = (100, 100, 200)
    BUTTON_HOVER_COLOR = (150, 150, 255)

class Celda:
    def __init__(self):
        self.clicked = False

    def click(self):
        self.clicked = not self.clicked

    def get_color(self):
        return SettingsManager.CLICKED_COLOR.value if self.clicked else SettingsManager.DEFAULT_COLOR.value


class Tablero:
    def __init__(self, grid_size, cell_size):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.board = [[Celda() for _ in range(grid_size)] for _ in range(grid_size)]

    def draw(self, surface):
        for row, rowOfCells in enumerate(self.board):
            for col, cell in enumerate(rowOfCells):
                color = cell.get_color()
                pygame.draw.rect(surface, color, (
                col * self.cell_size + 1, row * self.cell_size + 1, self.cell_size - 2, self.cell_size - 2))

    def handle_click(self, pos):
        row = pos[1] // self.cell_size
        col = pos[0] // self.cell_size
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            self.board[row][col].click()


class Partida:
    def __init__(self, grid_size=SettingsManager.GRID_SIZE.value, cell_size=SettingsManager.CELL_SIZE.value):
        pygame.init()
        self.window_size = grid_size * cell_size
        self.window = pygame.display.set_mode((self.window_size, self.window_size))
        self.clock = pygame.time.Clock()
        self.board = Tablero(grid_size, cell_size)
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.board.handle_click(event.pos)

    def run(self):
        while self.running:
            self.clock.tick(120)
            self.handle_events()
            self.window.fill(SettingsManager.BACKGROUND_COLOR.value)
            self.board.draw(self.window)
            pygame.display.flip()
        pygame.quit()

class Menu:
    def __init__(self):
        pass
    
class Boton:
    def __init__(self):
        pass
    def handle_event(self):
        pass
    
class Estadisticas:
    def __init__(self):
        pass
    def actualizar(self):
        pass

class Nivel:
    def __init__(self):
        pass
    
class Gamemode:
    def __init__(self):
        pass