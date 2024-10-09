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
    NUMBER_COLOR = (0, 255, 0)
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
    def __init__(self, grid_size, cell_size, nivel):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.nivel = nivel
        self.desplazamiento = ((self.nivel.get_height() + 1) // 2)
        self.board = [[Celda() for _ in range(grid_size)] for _ in range(grid_size)]
        self.font = pygame.font.SysFont(None, 24)

    def draw(self, surface):
        # Dibujar la cuadricula
        for row, rowOfCells in enumerate(self.board):
            for col, cell in enumerate(rowOfCells):
                color = cell.get_color()
                pygame.draw.rect(surface, color, (
                    (col + self.desplazamiento) * self.cell_size + 1,
                    (row + self.desplazamiento) * self.cell_size + 1, self.cell_size - 2, self.cell_size - 2))
        # Dibujar el marco superior
        pygame.draw.rect(surface, (0, 0, 255),
                         (0, 0, (self.grid_size + self.desplazamiento) * self.cell_size,
                          self.cell_size * self.desplazamiento))
        # Dibujar el marco izquierdo
        pygame.draw.rect(surface, (0, 0, 255),
                         (0, 0, self.cell_size * self.desplazamiento,
                          (self.grid_size + self.desplazamiento) * self.cell_size))

        # Dibujar cuadrado diagonal izquierdo
        pygame.draw.rect(surface, (0, 0, 180),
                         (0, 0, self.desplazamiento * self.cell_size, self.desplazamiento * self.cell_size))

        # Dibujar números en el marco superior (primera fila)
        for col in range(self.grid_size):
            numero = col + 1  # Números secuenciales de izquierda a derecha
            texto = self.font.render(str(numero), True, SettingsManager.TEXT_COLOR.value)
            text_rect = texto.get_rect(center=((col + self.desplazamiento) * self.cell_size + self.cell_size // 2,
                                               self.cell_size // 2))  # Centrar en el marco superior
            surface.blit(texto, text_rect)

        # Dibujar números en el marco izquierdo (primera columna)
        for row in range(self.grid_size):
            numero = row + 1  # Números secuenciales de arriba hacia abajo
            texto = self.font.render(str(numero), True, SettingsManager.TEXT_COLOR.value)
            text_rect = texto.get_rect(center=(self.cell_size // 2,
                                               (
                                                           row + self.desplazamiento) * self.cell_size + self.cell_size // 2))  # Centrar en el marco izquierdo
            surface.blit(texto, text_rect)

    def handle_click(self, pos):
        row = (pos[1] - self.desplazamiento * self.cell_size) // self.cell_size
        col = (pos[0] - self.desplazamiento * self.cell_size) // self.cell_size
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            self.board[row][col].click()


class Partida:
    def __init__(self, nivel, menu, cell_size=SettingsManager.CELL_SIZE.value):
        pygame.init()
        self.grid_size = len(nivel.get_grid())
        self.window_size = ((nivel.get_height() + 1) // 2 + self.grid_size) * cell_size  # asdkajskdkasjdkasjdkaklsdj
        self.window = pygame.display.set_mode((self.window_size, self.window_size))
        self.clock = pygame.time.Clock()
        self.board = Tablero(self.grid_size, cell_size, nivel)
        self.nivel = nivel
        self.menu = menu  # Referencia al menú
        self.running = True
        self.font = pygame.font.SysFont(None, 48)  # Fuente para el mensaje

    def mostrar_mensaje(self, mensaje):
        texto = self.font.render(mensaje, True, SettingsManager.BACKGROUND_COLOR.value)
        rect = texto.get_rect(center=(self.window_size // 2, self.window_size // 2))

        # Dibujar un rectángulo blanco detrás del texto
        padding = 20  # Espacio adicional alrededor del texto
        background_rect = pygame.Rect(
            rect.left - padding,
            rect.top - padding,
            rect.width + 2 * padding,
            rect.height + 2 * padding
        )
        pygame.draw.rect(self.window, SettingsManager.DEFAULT_COLOR.value, background_rect)

        self.window.blit(texto, rect)
        pygame.display.flip()
        pygame.time.wait(2000)  # Espera 2 segundos para que el mensaje sea visible

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.board.handle_click(event.pos)
                if self.nivel.verificar(self.board):
                    self.mostrar_mensaje("¡Nivel completado!")
                    self.running = False
                    self.menu.volver_al_menu()  # Llamar al método del menú para volver al menú

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
        self.running = False  # No se activa hasta iniciar el menú
        self.window = None
        self.clock = None
        self.font = None
        self.boton_jugar = None
        self.boton_cargar = None
        self.boton_estadisticas = None
        self.boton_salir = None
        self.partida_en_curso = None

    def iniciar_pygame(self):
        pygame.init()
        self.window = pygame.display.set_mode((500, 500))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)

        # Inicializa los botones después de crear la ventana
        self.boton_jugar = Boton("Iniciar Partida", (150, 200), (200, 50), self.font, self.iniciar_partida)
        self.boton_cargar = Boton("Cargar Partida", (150, 260), (200, 50), self.font, self.cargar_partida)
        self.boton_estadisticas = Boton("Ver Estadísticas", (150, 320), (200, 50), self.font, self.ver_estadisticas)
        self.boton_salir = Boton("Salir", (150, 380), (200, 50), self.font, self.salir)

    def iniciar_partida(self):
        nivel = Nivel(Nivel.nivel1)
        partida = Partida(nivel, self)  # Pasar la referencia del menú
        self.partida_en_curso = partida
        partida.run()

    def dibujar_menu(self):
        self.window.fill(SettingsManager.MENU_BACKGROUND_COLOR.value)

        titulo = self.font.render("Nonograma", True, SettingsManager.TEXT_COLOR.value)
        self.window.blit(titulo, (150, 100))

        self.boton_jugar.draw(self.window)
        self.boton_cargar.draw(self.window)
        self.boton_estadisticas.draw(self.window)
        self.boton_salir.draw(self.window)

        pygame.display.flip()

    def iniciar_menu(self):
        self.iniciar_pygame()  # Inicia pygame antes de comenzar el bucle
        self.running = True

        while self.running:
            self.clock.tick(60)
            self.dibujar_menu()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.boton_jugar.handle_event(event)
                self.boton_cargar.handle_event(event)
                self.boton_estadisticas.handle_event(event)
                self.boton_salir.handle_event(event)
        pygame.quit()

    def ver_estadisticas(self):
        pass

    def cargar_partida(self):
        pass

    def salir(self):
        self.running = False

    def volver_al_menu(self):
        self.iniciar_menu()


class Boton:
    def __init__(self, text, pos, size, font, action):
        self.rect = pygame.Rect(pos, size)
        self.color = SettingsManager.BUTTON_COLOR.value
        self.hover_color = SettingsManager.BUTTON_HOVER_COLOR.value
        self.text = text
        self.font = font
        self.action = action

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color

        pygame.draw.rect(surface, color, self.rect)
        text_surface = self.font.render(self.text, True, SettingsManager.TEXT_COLOR.value)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.action()


class Estadisticas:
    def __init__(self):
        self.horas_jugadas = 0
        self.niveles_superados = 0
        self.puntuacion_total = 0

    def actualizar(self, horas, niveles, puntuacion):
        self.horas_jugadas += horas
        self.niveles_superados += niveles
        self.puntuacion_total += puntuacion


class Nivel:
    nivel1 = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    def __init__(self, grid):
        self.grid = grid

    def get_grid(self):
        return self.grid

    def get_width(self):
        return len(self.nivel1[0])

    def get_height(self):
        return len(self.nivel1)

    def verificar(self, tablero):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col] == 1 and not tablero.board[row][col].clicked:
                    return False
                if self.grid[row][col] == 0 and tablero.board[row][col].clicked:
                    return False
        return True


class Gamemode:
    def __init__(self):
        pass


if __name__ == "__main__":
    menu = Menu()
    menu.iniciar_menu()