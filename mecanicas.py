import pygame
from utils import SettingsManager

class Celda:
    def __init__(self):
        self.clicked = False

    def click(self):
        self.clicked = not self.clicked

    def get_color(self):
        return SettingsManager.CLICKED_COLOR.value if self.clicked else SettingsManager.DEFAULT_COLOR.value
    

    def get_clicked(self):
        return self.clicked
    

class Tablero:
    def __init__(self, grid_size, cell_size, grid):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.edge_size = self.calcular_maxima_secuencia(grid)
        self.board = [[Celda() for _ in range(grid_size)] for _ in range(grid_size)]
        self.font = pygame.font.SysFont(None, 24)
        self.secuencias_fila = self.calcular_secuencias_fila(grid)
        self.secuencias_columna = self.calcular_secuencias_columna(grid)
        self.celda_anterior = 0 
        self.color_arrastre = 0
         

    def calcular_secuencias(self, linea):
        secuencias = 0
        enSecuencia = False
        for valor in linea:
            if valor != 0 and not enSecuencia:
                secuencias += 1
                enSecuencia = True
            elif valor == 0:
                enSecuencia = False
        return secuencias
    
    def calcular_maxima_secuencia(self, grid):
        maxima_secuencia = 0
        for fila in grid:
            secuencia = self.calcular_secuencias(fila)
            maxima_secuencia = max(maxima_secuencia, secuencia)
        for columna in range(len(grid[0])):
            secuencia = self.calcular_secuencias([grid[fila][columna] for fila in range(len(grid))])
            maxima_secuencia = max(maxima_secuencia, secuencia)
        return maxima_secuencia
    
    def calcular_secuencias_fila(self,grid):
        secuencias = []
        for fila in grid:
            fila_secuencias = self.get_secuencias(fila)
            secuencias.append(fila_secuencias)
        return secuencias
    
    def calcular_secuencias_columna(self,grid):
        secuencias = []
        for columna in range(len(grid[0])):
            columna_secuencias = self.get_secuencias([grid[fila][columna] for fila in range(len(grid))])
            secuencias.append(columna_secuencias)
        return secuencias
    
    def get_secuencias(self, linea):
        secuencias = []
        count = 0
        for valor in linea:
            if valor != 0:
                count += 1
            elif count != 0:
                secuencias.append(count)
                count = 0
        if count != 0:
            secuencias.append(count)
        return secuencias
    
    def draw(self, surface):
        # Dibujar la cuadricula
        for row, rowOfCells in enumerate(self.board):
            for col, cell in enumerate(rowOfCells):
                color = cell.get_color()
                pygame.draw.rect(surface, color, (
                    (col + self.edge_size) * self.cell_size + 1,
                    (row + self.edge_size) * self.cell_size + 1, self.cell_size - 2, self.cell_size - 2))
        # Dibujar el marco superior
        pygame.draw.rect(surface, SettingsManager.GRID_BACKGROUND_COLOR.value, (0, 0, (self.edge_size + self.grid_size)*self.cell_size, self.edge_size*self.cell_size))
        for col in range(self.grid_size):
            col_seq = self.secuencias_columna[col]
            for i, num in enumerate(col_seq):
                texto = self.font.render(str(num), True, SettingsManager.TEXT_COLOR.value)
                text_rect = texto.get_rect(center=((col + self.edge_size) * self.cell_size + self.cell_size // 2,
                                                   (self.edge_size - len(col_seq) + i) * self.cell_size + self.cell_size // 2))
                surface.blit(texto, text_rect)

        # Dibujar el marco izquierdo
        pygame.draw.rect(surface, SettingsManager.GRID_BACKGROUND_COLOR.value, (0, 0, self.edge_size*self.cell_size, (self.edge_size + self.grid_size)*self.cell_size))
        for row in range(self.grid_size):
            row_seq = self.secuencias_fila[row]
            for i, num in enumerate(reversed(row_seq)):
                texto = self.font.render(str(num), True, SettingsManager.TEXT_COLOR.value)
                text_rect = texto.get_rect(center=((self.edge_size - len(row_seq) + i) * self.cell_size + self.cell_size // 2,
                                                   (row + self.edge_size) * self.cell_size + self.cell_size // 2))
                surface.blit(texto, text_rect)

        # Dibujar la esquina superior izquierda (previsualizacion)
        pygame.draw.rect(surface, SettingsManager.DEFAULT_COLOR.value, (0, 0, self.edge_size*self.cell_size, self.edge_size*self.cell_size))
        mini_cell_size = (self.cell_size * self.edge_size) // self.grid_size
        for i, fila in enumerate(self.board):
            for j, celda in enumerate(fila):
                color = celda.get_color()
                rect = pygame.Rect(j * mini_cell_size, i * mini_cell_size, mini_cell_size, mini_cell_size)
                pygame.draw.rect(surface, color, rect)
                
    def handle_click(self, pos,presionando=False):
    
        row = (pos[1] - self.edge_size * self.cell_size) // self.cell_size
        col = (pos[0] - self.edge_size * self.cell_size) // self.cell_size
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:            
            if self.celda_anterior != self.board[row][col] and presionando:
                if self.board[row][col].get_color() != self.color_arrastre: 
                    self.board[row][col].click()                              
            elif not presionando:
                self.board[row][col].click()
                self.color_arrastre = self.board[row][col].get_color()

            self.celda_anterior = self.board[row][col]
    
    def get_edge_size(self):
        return self.edge_size

    def get_grid_size(self):
        return self.grid_size

    def get_board(self):
        return self.board

class Partida:
    def __init__(self, nivel, menu, cell_size=SettingsManager.CELL_SIZE.value):
        pygame.init()
        self.grid_size = len(nivel.get_grid())
        self.window_size = (nivel.get_board().get_edge_size() + self.grid_size) * cell_size
        self.window = pygame.display.set_mode((self.window_size, self.window_size))
        self.clock = pygame.time.Clock()
        self.nivel = nivel
        self.board = nivel.get_board()
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

                # Redibujar el tablero después del clic
                self.window.fill(SettingsManager.BACKGROUND_COLOR.value)
                self.board.draw(self.window)
                pygame.display.flip()                               
               
                # Verificar si el nivel está completado después de procesar el clic
                if self.nivel.verificar(self.board):
                    self.mostrar_mensaje("¡Nivel completado!")
                    self.running = False
                    self.menu.volver_al_menu()  # Llamar al método del menú para volver al menú '''

        if pygame.mouse.get_pressed()[0]:
            self.board.handle_click(pygame.mouse.get_pos(),True) #

                
                                    
            ''' elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.board.iniciar_arrastre(event.pos)
            elif event.type == pygame.MOUSEMOTION:
            # Continuar arrastrando si el botón izquierdo está presionado
             if pygame.mouse.get_pressed()[0]:  # Verifica si el botón izquierdo está presionado
                self.board.continuar_arrastre(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP and event.button ==1:
                self.board.finalizar_arrastre() '''
                
            '''self.board.handle_click(event.pos)
            
                # Redibujar el tablero después del clic
                self.window.fill(SettingsManager.BACKGROUND_COLOR.value)
                self.board.draw(self.window)
                pygame.display.flip()
                # Verificar si el nivel está completado después de procesar el clic
                if self.nivel.verificar(self.board):
                    self.mostrar_mensaje("¡Nivel completado!")
                    self.running = False
                    self.menu.volver_al_menu()  # Llamar al método del menú para volver al menú '''


    def run(self):
        while self.running:
            self.clock.tick(1000)
            self.handle_events()         

            self.window.fill(SettingsManager.BACKGROUND_COLOR.value)
            self.board.draw(self.window)
            pygame.display.flip()
        pygame.quit()

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
    def __init__(self, grid):
        self.grid = grid
        self.tablero = Tablero(len(grid), SettingsManager.CELL_SIZE.value, self.grid)

    def get_grid(self):
        return self.grid

    def verificar(self, tablero):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col] == 1 and not tablero.get_board()[row][col].get_clicked():
                    return False
                if self.grid[row][col] == 0 and tablero.get_board()[row][col].get_clicked():
                    return False
        return True

    def get_grid(self):
        return self.grid

    def get_board(self):
        return self.tablero

class Gamemode:
    def __init__(self):
        pass