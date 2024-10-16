import pygame
from enum import Enum

# Carga de sonidos
pygame.mixer.init()
sonido_seleccion = pygame.mixer.Sound("resources/sounds/seleccion.wav")
sonido_presion = pygame.mixer.Sound("resources/sounds/presion.wav")

class SettingsManager(Enum):
    GRID_SIZE = 10
    CELL_SIZE = 30
    DEFAULT_COLOR = (255, 255, 255)
    CLICKED_COLOR = (0, 0, 0)
    BACKGROUND_COLOR = (0, 0, 0)
    MENU_BACKGROUND_COLOR = (50, 50, 50)
    TEXT_COLOR = (255, 255, 255)
    NUMBER_COLOR = (0, 255, 0)
    BUTTON_COLOR = (0, 169, 153)
    BUTTON_HOVER_COLOR = (0, 218, 255)
    GRID_BACKGROUND_COLOR = (0,155,155)


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
        for col in range(self.grid_size):
            col_seq = self.secuencias_columna[col]
            for i, num in enumerate(reversed(col_seq)):
                texto = self.font.render(str(num), True, SettingsManager.TEXT_COLOR.value)
                text_rect = texto.get_rect(center=((col + self.edge_size) * self.cell_size + self.cell_size // 2,
                                                   (i + 1) * self.cell_size // 2))
                surface.blit(texto, text_rect)

        # Dibujar el marco izquierdo
        for row in range(self.grid_size):
            row_seq = self.secuencias_fila[row]
            for i, num in enumerate(reversed(row_seq)):
                texto = self.font.render(str(num), True, SettingsManager.TEXT_COLOR.value)
                text_rect = texto.get_rect(center=((self.edge_size - len(row_seq) + i) * self.cell_size + self.cell_size // 2,
                                                   (row + self.edge_size) * self.cell_size + self.cell_size // 2))
                surface.blit(texto, text_rect)

    def handle_click(self, pos):
        row = (pos[1] - self.edge_size * self.cell_size) // self.cell_size
        col = (pos[0] - self.edge_size * self.cell_size) // self.cell_size
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            self.board[row][col].click()

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
        self.running = False
        self.window = None
        self.clock = None
        self.font = None
        self.boton_jugar = None
        self.boton_cargar = None
        self.boton_estadisticas = None
        self.boton_opciones = None
        self.boton_salir = None
        self.partida_en_curso = None
        self.menu_seleccion_nivel = MenuSeleccionNivel(self)  # Instancia del menú de selección de niveles
        self.estado = "menu_principal"
        # Lista de botones para seleccionado
        self.botones = []
        self.boton_seleccionado = 0
        # Carga y reescala de la imagen de título y fondo
        self.fondo_imagen = pygame.image.load("resources/lotus_pond.png")
        self.fondo_imagen = pygame.transform.scale(self.fondo_imagen, (500, 716))
        self.frames_titulo = []
        self.frame_index_titulo = 0
        for i in range(1,24):
            img = pygame.image.load("resources/title/title_"+str(i)+".png")
            img = pygame.transform.scale(img, (200, 137))
            self.frames_titulo.append(img)    

    def iniciar_pygame(self):
        pygame.init()
        self.window = pygame.display.set_mode((500, 500))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Trebuchet MS", 20)

        self.boton_jugar = Boton("Seleccionar Nivel", (150, 175), (200, 50), self.font, self.ir_a_seleccion_nivel)
        self.boton_cargar = Boton("Cargar Partida", (150, 235), (200, 50), self.font, self.cargar_partida)
        self.boton_estadisticas = Boton("Ver Estadísticas", (150, 295), (200, 50), self.font, self.ver_estadisticas)
        self.boton_opciones = Boton("Opciones", (150, 355), (200, 50), self.font, self.opciones)
        self.boton_salir = Boton("Salir", (150, 415), (200, 50), self.font, self.salir)

        self.botones = [self.boton_jugar, self.boton_cargar, self.boton_estadisticas, self.boton_opciones, self.boton_salir]
    
    def ir_a_seleccion_nivel(self):
        self.running = False
        self.menu_seleccion_nivel.iniciar_menu()

    def iniciar_partida(self, nivel):
        partida = Partida(nivel, self)
        self.partida_en_curso = partida
        partida.run()

    def dibujar_menu(self):
        self.window.blit(self.fondo_imagen, (0, 0))

        if self.estado == "menu_principal":
            self.window.blit(self.frames_titulo[self.frame_index_titulo], (150, 50))
            self.frame_index_titulo = (self.frame_index_titulo + 1) % len(self.frames_titulo)
            for i, boton in enumerate(self.botones):
                boton.draw(self.window, seleccionado=i == self.boton_seleccionado)        
        elif self.estado == "estadisticas":
            texto = self.font.render("Estadísticas", True, (255, 255, 255))
            self.window.blit(texto, (150, 100))
        elif self.estado == "cargar_partida":
            texto = self.font.render("Cargar Partida", True, (255, 255, 255))
            self.window.blit(texto, (150, 100))
        elif self.estado == "opciones":
            texto = self.font.render("Opciones", True, (255, 255, 255))
            self.window.blit(texto, (150, 100))

        pygame.display.flip()

    def iniciar_menu(self):
        self.iniciar_pygame()
        self.running = True

        while self.running:
            self.dibujar_menu()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_DOWN:
                        self.boton_seleccionado = (self.boton_seleccionado + 1) % len(self.botones)
                        sonido_seleccion.play()
                    elif event.key == pygame.K_UP:
                        self.boton_seleccionado = (self.boton_seleccionado - 1) % len(self.botones)
                        sonido_seleccion.play()
                    elif event.key == pygame.K_RETURN:
                        self.botones[self.boton_seleccionado].action()
                        sonido_presion.play()
                for boton in self.botones:
                    boton.handle_event(event)
            
            self.clock.tick(10)
                
        pygame.quit()

    def ver_estadisticas(self):
        pass

    def cargar_partida(self):
        pass

    def opciones(self):
        pass

    def salir(self):
        self.running = False

    def volver_al_menu(self):
        self.iniciar_menu()

class MenuSeleccionNivel:
    def __init__(self, menu_principal):
        self.menu_principal = menu_principal
        self.running = False
        self.window = None
        self.clock = None
        self.font = None
        self.botones_niveles = []
        self.scroll_offset = 0  # Offset de desplazamiento
        self.scroll_speed = 20  # Velocidad de desplazamiento

    def iniciar_pygame(self):
        pygame.init()
        self.window = pygame.display.set_mode((600, 600))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Trebuchet MS", 20)

        # obtener lista de archivos de la carpeta
        carpeta_niveles = './levels'
        archivos_niveles = [f for f in os.listdir(carpeta_niveles) if os.path.isfile(os.path.join(carpeta_niveles, f))]

        # Crear niveles
        niveles = []
        for archivo in archivos_niveles:
            with open(os.path.join(carpeta_niveles, archivo), 'r') as file:
                linea = 'a'
                matriz = []
                while(linea != ''):
                    fila = []
                    linea = file.readline()
                    for char in linea:
                        if(char.isdigit()):
                            fila.append(int(char))

                    if(len(fila) != 0):
                        matriz.append(fila)
                        
                niveles.append(Nivel(matriz))

        # Crear botones para los niveles
        niveles = [Nivel(Nivel.nivel1), Nivel(Nivel.nivel2), Nivel(Nivel.nivel3), Nivel(Nivel.nivel4), Nivel(Nivel.nivel5), Nivel(Nivel.nivel6), Nivel(Nivel.nivel7), Nivel(Nivel.nivel8), Nivel(Nivel.nivel9)]  # Aquí puedes añadir más niveles
        for i, nivel in enumerate(niveles):
            boton = Boton(f"Nivel {i+1}", (250, 200 + i * 60), (200, 50), self.font, lambda n=nivel: self.iniciar_partida(n))
            self.botones_niveles.append(boton)

        self.boton_volver = Boton("Volver", (10, 380), (200, 50), self.font, self.volver_al_menu_principal)

    def dibujar_menu(self):
        self.window.fill(SettingsManager.MENU_BACKGROUND_COLOR.value)

        titulo = self.font.render("Seleccionar", True, SettingsManager.TEXT_COLOR.value)
        titulo2 = self.font.render("Nivel", True, SettingsManager.TEXT_COLOR.value)
        self.window.blit(titulo, (20, 100))
        self.window.blit(titulo2, (20, 130))

        for boton in self.botones_niveles:
            boton.draw(self.window, self.scroll_offset)
        self.boton_volver.draw(self.window)

        pygame.display.flip()

    def iniciar_menu(self):
        self.iniciar_pygame()
        self.running = True

        while self.running:
            self.clock.tick(60)
            self.dibujar_menu()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:  # Scroll up
                        self.scroll_offset = min(self.scroll_offset + self.scroll_speed, 0)
                    elif event.button == 5:  # Scroll down
                        self.scroll_offset -= self.scroll_speed
                for boton in self.botones_niveles:
                    boton.handle_event(event, self.scroll_offset)
                self.boton_volver.handle_event(event)
        pygame.quit()

    def iniciar_partida(self, nivel):
        self.running = False
        self.menu_principal.iniciar_partida(nivel)

    def volver_al_menu_principal(self):
        self.running = False
        self.menu_principal.iniciar_menu()

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
    nivel1 = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    ]
    nivel2 = [
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
    nivel3 = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0]

    ]
    nivel4 = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    nivel5 = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    ]
    nivel6 = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    nivel7 = [
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0]

    ]
    nivel8 = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
        [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    nivel9 = [
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 1],
        [0, 1, 0, 0, 1, 0],
        [0, 0, 1, 1, 0, 0]
    ]

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

if __name__ == "__main__":
    menu = Menu()
    menu.iniciar_menu()import pygame
import os
from enum import Enum

# Carga de sonidos
pygame.mixer.init()
sonido_seleccion = pygame.mixer.Sound("resources/sounds/seleccion.wav")
sonido_presion = pygame.mixer.Sound("resources/sounds/presion.wav")

class SettingsManager(Enum):
    GRID_SIZE = 10
    CELL_SIZE = 40
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
        pygame.draw.rect(surface, SettingsManager.GRID_BACKGROUND_COLOR.value, (0, 0, (self.edge_size + self.grid_size)*self.cell_size, self.   edge_size*self.cell_size))
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

    def handle_click(self, pos):
        row = (pos[1] - self.edge_size * self.cell_size) // self.cell_size
        col = (pos[0] - self.edge_size * self.cell_size) // self.cell_size
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            self.board[row][col].click()

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
        self.running = False
        self.window = None
        self.clock = None
        self.font = None
        self.boton_jugar = None
        self.boton_cargar = None
        self.boton_estadisticas = None
        self.boton_opciones = None
        self.boton_salir = None
        self.partida_en_curso = None
        self.menu_seleccion_nivel = MenuSeleccionNivel(self)  # Instancia del menú de selección de niveles
        self.estado = "menu_principal"
        # Lista de botones para seleccionado
        self.botones = []
        self.boton_seleccionado = 0
        # Carga y reescala de la imagen de título y fondo
        self.fondo_imagen = pygame.image.load("resources/lotus_pond.png")
        self.fondo_imagen = pygame.transform.scale(self.fondo_imagen, (500, 716))
        self.frames_titulo = []
        self.frame_index_titulo = 0
        for i in range(1,24):
            img = pygame.image.load("resources/title/title_"+str(i)+".png")
            img = pygame.transform.scale(img, (200, 137))
            self.frames_titulo.append(img)    

    def iniciar_pygame(self):
        pygame.init()
        self.window = pygame.display.set_mode((500, 500))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Trebuchet MS", 20)

        self.boton_jugar = Boton("Seleccionar Nivel", (150, 175), (200, 50), self.font, self.ir_a_seleccion_nivel)
        self.boton_cargar = Boton("Cargar Partida", (150, 235), (200, 50), self.font, self.cargar_partida)
        self.boton_estadisticas = Boton("Ver Estadísticas", (150, 295), (200, 50), self.font, self.ver_estadisticas)
        self.boton_opciones = Boton("Opciones", (150, 355), (200, 50), self.font, self.opciones)
        self.boton_salir = Boton("Salir", (150, 415), (200, 50), self.font, self.salir)

        self.botones = [self.boton_jugar, self.boton_cargar, self.boton_estadisticas, self.boton_opciones, self.boton_salir]
    
    def ir_a_seleccion_nivel(self):
        self.running = False
        self.menu_seleccion_nivel.iniciar_menu()

    def iniciar_partida(self, nivel):
        partida = Partida(nivel, self)
        self.partida_en_curso = partida
        partida.run()

    def dibujar_menu(self):
        self.window.blit(self.fondo_imagen, (0, 0))

        if self.estado == "menu_principal":
            self.window.blit(self.frames_titulo[self.frame_index_titulo], (150, 50))
            self.frame_index_titulo = (self.frame_index_titulo + 1) % len(self.frames_titulo)
            for i, boton in enumerate(self.botones):
                boton.draw(self.window, seleccionado=i == self.boton_seleccionado)        
        elif self.estado == "estadisticas":
            texto = self.font.render("Estadísticas", True, (255, 255, 255))
            self.window.blit(texto, (150, 100))
        elif self.estado == "cargar_partida":
            texto = self.font.render("Cargar Partida", True, (255, 255, 255))
            self.window.blit(texto, (150, 100))
        elif self.estado == "opciones":
            texto = self.font.render("Opciones", True, (255, 255, 255))
            self.window.blit(texto, (150, 100))

        pygame.display.flip()

    def iniciar_menu(self):
        self.iniciar_pygame()
        self.running = True

        while self.running:
            self.dibujar_menu()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_DOWN:
                        self.boton_seleccionado = (self.boton_seleccionado + 1) % len(self.botones)
                        sonido_seleccion.play()
                    elif event.key == pygame.K_UP:
                        self.boton_seleccionado = (self.boton_seleccionado - 1) % len(self.botones)
                        sonido_seleccion.play()
                    elif event.key == pygame.K_RETURN:
                        self.botones[self.boton_seleccionado].action()
                        sonido_presion.play()
                for boton in self.botones:
                    boton.handle_event(event)
            
            self.clock.tick(10)
                
        pygame.quit()

    def ver_estadisticas(self):
        pass

    def cargar_partida(self):
        pass

    def opciones(self):
        pass

    def salir(self):
        self.running = False

    def volver_al_menu(self):
        self.iniciar_menu()

class MenuSeleccionNivel:
    def __init__(self, menu_principal):
        self.menu_principal = menu_principal
        self.running = False
        self.window = None
        self.clock = None
        self.font = None
        self.botones_niveles = []
        self.scroll_offset = 0  # Offset de desplazamiento
        self.scroll_speed = 20  # Velocidad de desplazamiento

    def iniciar_pygame(self):
        pygame.init()
        self.window = pygame.display.set_mode((600, 600))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Trebuchet MS", 20)

        # obtener lista de archivos de la carpeta
        carpeta_niveles = './levels'
        archivos_niveles = [f for f in os.listdir(carpeta_niveles) if os.path.isfile(os.path.join(carpeta_niveles, f))]

        # Crear niveles
        niveles = []
        for archivo in archivos_niveles:
            with open(os.path.join(carpeta_niveles, archivo), 'r') as file:
                linea = 'a'
                matriz = []
                while(linea != ''):
                    fila = []
                    linea = file.readline()
                    for char in linea:
                        if(char.isdigit()):
                            fila.append(int(char))

                    if(len(fila) != 0):
                        matriz.append(fila)
                        
                niveles.append(Nivel(matriz))

        # Crear botones para los niveles
        for i, nivel in enumerate(niveles):
            boton = Boton(f"Nivel {i+1}", (250, 200 + i * 60), (200, 50), self.font, lambda n=nivel: self.iniciar_partida(n))
            self.botones_niveles.append(boton)

        self.boton_volver = Boton("Volver", (10, 380), (200, 50), self.font, self.volver_al_menu_principal)

    def dibujar_menu(self):
        self.window.fill(SettingsManager.MENU_BACKGROUND_COLOR.value)

        titulo = self.font.render("Seleccionar", True, SettingsManager.TEXT_COLOR.value)
        titulo2 = self.font.render("Nivel", True, SettingsManager.TEXT_COLOR.value)
        self.window.blit(titulo, (20, 100))
        self.window.blit(titulo2, (20, 130))

        for boton in self.botones_niveles:
            boton.draw(self.window, self.scroll_offset)
        self.boton_volver.draw(self.window)

        pygame.display.flip()

    def iniciar_menu(self):
        self.iniciar_pygame()
        self.running = True

        while self.running:
            self.clock.tick(60)
            self.dibujar_menu()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:  # Scroll up
                        self.scroll_offset = min(self.scroll_offset + self.scroll_speed, 0)
                    elif event.button == 5:  # Scroll down
                        self.scroll_offset -= self.scroll_speed
                for boton in self.botones_niveles:
                    boton.handle_event(event, self.scroll_offset)
                self.boton_volver.handle_event(event)
        pygame.quit()

    def iniciar_partida(self, nivel):
        self.running = False
        self.menu_principal.iniciar_partida(nivel)

    def volver_al_menu_principal(self):
        self.running = False
        self.menu_principal.iniciar_menu()

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

if __name__ == "__main__":
    menu = Menu()
    menu.iniciar_menu()