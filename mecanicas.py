import pygame, math, json, os, random
from utils import SettingsManager, colorCelda, Boton

class Celda:
    def __init__(self):
        self.clicked = colorCelda.DEFAULT

    #Pide color del enum colorCelda
    def click(self, color):
        if(color == self.clicked):
            self.clicked = colorCelda.DEFAULT
        else:    
            self.clicked = color

    def get_color(self):
        return self.clicked

class Tablero:
    def __init__(self, grid_size, cell_size, grid, colores, bar_height):
        self.bar_height = bar_height
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.edge_size = self.calcular_maxima_secuencia(grid)
        self.board = [[Celda() for _ in range(grid_size)] for _ in range(grid_size)]
        self.font = pygame.font.SysFont(None, 24)
        self.secuencias_fila = self.calcular_secuencias_fila(grid)
        self.secuencias_columna = self.calcular_secuencias_columna(grid)
        self.celda_anterior = 0 
        self.color_arrastre = 0
        self.colores = colores
        self.color_seleccionado = colorCelda.BLACK

    def calcular_secuencias(self, linea):
        secuencias = 0
        valor_anterior = -1
        enSecuencia = False
        for valor in linea:
            if valor != 0 and (not enSecuencia or valor_anterior!=valor):
                secuencias += 1
                enSecuencia = True
            elif valor == 0:
                enSecuencia = False
            valor_anterior=valor
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
        valor_anterior = 0
        for valor in linea:
            if valor != 0 and (valor == valor_anterior or valor_anterior==0):
                count += 1
            elif count != 0:
                secuencias.append((valor_anterior,count))
                count = 0
                if valor != 0:
                    count+=1
            valor_anterior=valor

        if count != 0:
            secuencias.append((valor_anterior,count))
        return secuencias
    
    def draw(self, surface):
        # Pintar la bar
        pygame.draw.rect(surface, SettingsManager.TITLE_BAR_COLOR.value, (0, 0, (self.grid_size+self.edge_size)*self.cell_size, self.bar_height))

        # Dibujar la cuadricula
        for row, rowOfCells in enumerate(self.board):
            for col, cell in enumerate(rowOfCells):
                color = cell.get_color().value
                pygame.draw.rect(surface, color, (
                    (col + self.edge_size) * self.cell_size + 1,
                    (row + self.edge_size) * self.cell_size + self.bar_height + 1, self.cell_size - 2, self.cell_size - 2))
        # Dibujar el marco superior
        pygame.draw.rect(surface, SettingsManager.GRID_BACKGROUND_COLOR.value, (0, self.bar_height, (self.edge_size + self.grid_size)*self.cell_size, self.edge_size*self.cell_size))
        for col in range(self.grid_size):
            col_seq = self.secuencias_columna[col]
            for i, num in enumerate(col_seq):
                texto = self.font.render(str(num[1]), True, SettingsManager.TEXT_COLOR.value)
                if num[0] == 1:
                    texto = self.font.render(str(num[1]), True, colorCelda.BLACK.value)
                elif num[0] == 2:
                    texto = self.font.render(str(num[1]), True, colorCelda.RED.value)
                elif num[0] == 3:
                    texto = self.font.render(str(num[1]), True, colorCelda.GREEN.value)
                elif num[0] == 4:
                    texto = self.font.render(str(num[1]), True, colorCelda.BLUE.value)

                text_rect = texto.get_rect(center=((col + self.edge_size) * self.cell_size + self.cell_size // 2,
                                                   (self.edge_size - len(col_seq) + i) * self.cell_size + self.cell_size // 2 + self.bar_height))
                surface.blit(texto, text_rect)

        # Dibujar el marco izquierdo
        pygame.draw.rect(surface, SettingsManager.GRID_BACKGROUND_COLOR.value, (0, self.bar_height, self.edge_size*self.cell_size, (self.edge_size + self.grid_size)*self.cell_size))
        for row in range(self.grid_size):
            row_seq = self.secuencias_fila[row]
            for i, num in enumerate(row_seq):
                texto = self.font.render(str(num[1]), True, SettingsManager.TEXT_COLOR.value)
                if num[0] == 1:
                    texto = self.font.render(str(num[1]), True, colorCelda.BLACK.value)
                elif num[0] == 2:
                    texto = self.font.render(str(num[1]), True, colorCelda.RED.value)
                elif num[0] == 3:
                    texto = self.font.render(str(num[1]), True, colorCelda.GREEN.value)
                elif num[0] == 4:
                    texto = self.font.render(str(num[1]), True, colorCelda.BLUE.value)
                
                text_rect = texto.get_rect(center=((self.edge_size - len(row_seq) + i) * self.cell_size + self.cell_size // 2,
                                                   (row + self.edge_size) * self.cell_size + self.cell_size // 2 + self.bar_height))
                surface.blit(texto, text_rect)

        # Dibujar la esquina superior izquierda (previsualizacion)
        pygame.draw.rect(surface, SettingsManager.DEFAULT_COLOR.value, (0, self.bar_height, self.edge_size*self.cell_size, self.edge_size*self.cell_size))
        mini_cell_size = (self.cell_size * self.edge_size) // self.grid_size
        for i, fila in enumerate(self.board):
            for j, celda in enumerate(fila):
                color = celda.get_color().value
                rect = pygame.Rect(j * mini_cell_size, i * mini_cell_size + self.bar_height, mini_cell_size, mini_cell_size)
                pygame.draw.rect(surface, color, rect)

        # Dibujar selector de colores
        pygame.draw.rect(surface, SettingsManager.COLOR_SELECTOR_COLOR.value, (0, (self.grid_size+self.edge_size)*self.cell_size + self.bar_height,  (self.grid_size+self.edge_size)*self.cell_size, self.edge_size*self.cell_size))
        for index, color in enumerate(self.colores):
            pygame.draw.circle(surface, color.value, ((self.edge_size+0.5+index)*self.cell_size , (self.grid_size+self.edge_size+0.5)*self.cell_size + self.bar_height), 10)

    def handle_click(self, pos, presionando=False):
        row = (pos[1] - (self.edge_size * self.cell_size) - self.bar_height ) // self.cell_size
        col = (pos[0] - self.edge_size * self.cell_size) // self.cell_size
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            if self.celda_anterior != self.board[row][col] and presionando:
                if self.board[row][col].get_color().value != self.color_arrastre: 
                    self.board[row][col].click(self.color_seleccionado)                             
            elif not presionando:
                self.board[row][col].click(self.color_seleccionado)
                self.color_seleccionado = self.board[row][col].get_color()
                self.color_arrastre = self.board[row][col].get_color().value

            self.celda_anterior = self.board[row][col]
        
        for index, color in enumerate(self.colores):
            cx = (self.edge_size+0.5+index)*self.cell_size
            cy = (self.grid_size+self.edge_size+0.5)*self.cell_size + self.bar_height
            if math.sqrt(pow(cx-pos[0], 2) + pow(cy-pos[1], 2)) <= 10:
                self.color_seleccionado = color

    def get_edge_size(self):
        return self.edge_size

    def get_grid_size(self):
        return self.grid_size

    def get_board(self):
        return self.board

    def load_board(self, board):
        self.board = board

class Partida:
    def __init__(self, nivel, menu, cell_size=SettingsManager.CELL_SIZE.value, url = None):
        pygame.init()
        if url:
            self.url = url + ".json"
        else:
            self.url = None
        self.bar_height = 50
        self.nivel = nivel
        self.grid_size = len(nivel.get_grid())
        self.board = Tablero(self.grid_size, SettingsManager.CELL_SIZE.value, nivel.get_grid(), nivel.get_colors(), self.bar_height)
        self.window_width = (self.board.get_edge_size() + self.grid_size) * cell_size
        self.window_height = ((self.board.get_edge_size() + self.grid_size + 1) * cell_size) + self.bar_height
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.clock = pygame.time.Clock()
        self.menu = menu  # Referencia al menú
        self.running = False
        self.font = None
        self.button_font = pygame.font.SysFont(None, self.window_height // 20)
        self.save_button = Boton("Guardar y salir", (5 * (self.window_width // 9), self.bar_height/5), (3* (self.window_width // 9), 3 * self.bar_height/5), self.button_font, self.guardar)
        self.exit_button = Boton("Salir", (self.window_width // 9, self.bar_height/5), (3 * (self.window_width // 9), 3 * self.bar_height/5), self.button_font, self.salir)
        self.buttons = [self.save_button, self.exit_button]
        self.tiempo_inicio = None
        self.estadisticas = Estadisticas()
        self.estadisticas.cargarEstadisticas()

    def mostrar_mensaje(self, mensaje):
       #Calcular la dimension del mensaje con respecto al tamaño de la
        font_size = min(self.window_width, self.window_height) // 10  # Adjust this divisor as needed
        self.font = pygame.font.SysFont(None,font_size)

        texto = self.font.render(mensaje, True, SettingsManager.BACKGROUND_COLOR.value)
        rect = texto.get_rect(center=(self.window_width // 2, self.window_height // 2))

        # Dibujar un rectángulo blanco detrás del texto
        padding = font_size // 2  # Adjust padding based on font size
        background_rect = pygame.Rect(
            rect.left - padding,
            rect.top - padding,
            rect.width + 2 * padding,
            rect.height + 2 * padding
        )

        # Crear una superficie transparente para el texto
        text_surface = pygame.Surface((rect.width + 2 * padding, rect.height + 2 * padding), pygame.SRCALPHA)
        text_surface.fill((255, 255, 255, 0))  # Fondo transparente

        # Crear confetti
        confetti_particles = [Confetti(random.randint(0, self.window_width), random.randint(0, self.window_height)) for _ in range(100)]

        # Animar la aparición del texto y el confetti
        for alpha in range(0, 256, 5):
            self.window.fill(SettingsManager.BACKGROUND_COLOR.value)
            self.draw()

            # Dibujar el rectángulo de fondo
            pygame.draw.rect(self.window, SettingsManager.DEFAULT_COLOR.value, background_rect)

            # Renderizar el texto con la opacidad actual
            text_surface.fill((255, 255, 255, 0))  # Limpiar la superficie
            text_surface.blit(texto, (padding, padding))
            text_surface.set_alpha(alpha)

            # Dibujar confetti
            for confetti in confetti_particles:
                confetti.update()
                confetti.draw(self.window)

            # Blit la superficie del texto en la ventana principal
            self.window.blit(text_surface, (rect.left - padding, rect.top - padding))
            pygame.display.flip()
            pygame.time.wait(30)  # Espera un poco para crear el efecto de animación

        pygame.time.wait(2000)  # Espera 2 segundos para que el mensaje sea visible

    def pedir_mensaje(self, question):
        font = pygame.font.SysFont(None, 30)
        input_box = pygame.Rect((self.window_width - 140)/2, (self.window_height - 32)/2 + 50, 140, 32)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        text = ''
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Si el usuario hace clic en el cuadro de entrada
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            done = True
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            pygame.draw.rect(self.window, (0,0,0), ((self.window_width - 140)//2 - 40, (self.window_height - 32)//2 + 10, 320, 112))
            # Renderizar el texto de la pregunta
            question_surface = font.render(question, True, pygame.Color('white'))
            self.window.blit(question_surface, (input_box.x - 30, input_box.y - 30))
            # Renderizar el texto del usuario
            txt_surface = font.render(text, True, color)
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            self.window.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(self.window, color, input_box, 2)

            pygame.display.flip()

        return text


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False 
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.board.handle_click(event.pos)

                # Redibujar el tablero después del clic
                self.window.fill(SettingsManager.BACKGROUND_COLOR.value)
                self.draw()
                pygame.display.flip()

            for button in self.buttons:
                button.handle_event(event)    
         
        if pygame.mouse.get_pressed()[0]:
                self.board.handle_click(pygame.mouse.get_pos(),True)                                                    
              
                # Verificar si el nivel está completado después de procesar el clic
                if self.nivel.verificar(self.board):
                    self.mostrar_mensaje("¡Nivel completado!")
                    self.estadisticas.actualizar(self.get_tiempo_partida(), 1, 0, self.nivel.id)
                    if self.url:
                        url = os.path.join("./saved_levels", self.url)
                        try:
                            os.remove(url)
                        except FileNotFoundError:
                            print(f"Archivo {url} no existe.")
                        except Exception as e:
                            print(f"Ocurrio un error al tratar de eliminar el archivo {url}: {e} ")
                    self.salir()

    def guardar(self):
        filename = "saved_levels/"
        filename += self.pedir_mensaje("Ingrese nombre de guardado:")
        filename += ".json"
        #guardar nivel
        board_data = [[cell.get_color().value for cell in row] for row in self.board.get_board()]
        grid_data = self.nivel.get_grid()

        data = {
            'board': board_data,
            'grid': grid_data
        }

        with open(filename, 'w') as file:
            json.dump(data, file)

        self.mostrar_mensaje("Partida guardada exitosamente.")
        self.salir()


    def cargar(self, board):
        self.board.load_board(board)

    def draw(self):
        self.board.draw(self.window)
        for button in self.buttons:
            button.draw(self.window)

    def salir(self):
        self.running = False
        self.menu.volver_al_menu()

    def run(self):
        self.tiempo_inicio = pygame.time.get_ticks()
        self.running = True
        while self.running:
            self.clock.tick(1000)
            self.handle_events()         
            self.window.fill(SettingsManager.BACKGROUND_COLOR.value)
            self.draw()

            pygame.display.flip()

        pygame.quit()
    
    def get_tiempo_partida(self):
        if self.tiempo_inicio is not None:
            elapsed_time_ms = pygame.time.get_ticks() - self.tiempo_inicio
            return elapsed_time_ms // 1000  # Convertir a segundos
        return 0

class Estadisticas:
    def __init__(self, id=1):
        self.id = id
        self.segundos_jugados = 0
        self.niveles_superados = 0
        self.puntuacion_total = 0
        self.niveles_completados = []
        self.verificarArchivo()

    def actualizar(self, minutos, niveles, puntuacion, nivel_completado=None):
        self.segundos_jugados += minutos
        self.niveles_superados += niveles
        self.puntuacion_total += puntuacion
        if nivel_completado:
            if nivel_completado.endswith(".txt"):
                nivel_completado = nivel_completado[:-4]
            if nivel_completado not in self.niveles_completados:
                self.niveles_completados.append(nivel_completado)
    
        self.__guardarEstadisticas__()

    def verificarArchivo(self):
        try:
            open("data/estadisticas.json", "r")
        except FileNotFoundError: 
            with open("data/estadisticas.json", "w") as file:
                nuevas_estadisticas = [
                    {
                        "id": 1,
                        "nombre": "Usuario 1",
                        "segundos_jugados": 0,
                        "niveles_superados": 0,
                        "puntuacion_total": 0,
                        "niveles_completados": []
                    }
                ]
                json.dump(nuevas_estadisticas, file, indent=4)
        
    def cargarEstadisticas(self):
        estadisticas = {}

        try:
            with open("data/estadisticas.json", "r") as file:
                estadisticas = json.load(file)
        except FileNotFoundError:
            print("No se encontró el archivo de estadísticas.")
            return
        except json.JSONDecodeError:
            print("Error al cargar el archivo de estadísticas.")
            return

        for user in estadisticas:
            if user["id"] == self.id:
                self.segundos_jugados = user["segundos_jugados"]
                self.niveles_superados = user["niveles_superados"]
                self.puntuacion_total = user["puntuacion_total"]
                self.niveles_completados = user["niveles_completados"]
                break
        
    def __guardarEstadisticas__(self):
        try:
            with open("data/estadisticas.json", "r") as file:
                estadisticas = json.load(file)
        except:
            print("Error al cargar el archivo de estadísticas.")
            return
        
        for user in estadisticas:
           if user["id"] == self.id:
                user["segundos_jugados"] = self.segundos_jugados
                user["niveles_superados"] = self.niveles_superados
                user["puntuacion_total"] = self.puntuacion_total
                user["niveles_completados"] = self.niveles_completados
                break
        try:   
            with open("data/estadisticas.json", "w") as file:
                json.dump(estadisticas, file, indent=4)
        except:
            print("Error al guardar las estadísticas.")
            return
        
    def getSegundosJugados(self):
        return self.segundos_jugados
    
    def getNivelesSuperados(self):
        return self.niveles_superados
    
    def getPuntuacionTotal(self):
        return self.puntuacion_total
    
    def getNivelesCompletados(self):
        return self.niveles_completados
    
        
class Nivel:
    def __init__(self, grid, id):
        self.grid = grid
        self.id = id
        self.colores = [colorCelda.DEFAULT, colorCelda.BLACK, colorCelda.BLUE, colorCelda.GREEN, colorCelda.RED]
        self.completado = False

    def verificar(self, tablero):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col] == 0 and tablero.get_board()[row][col].get_color().value != colorCelda.DEFAULT.value:
                    return False
                if self.grid[row][col] == 1 and tablero.get_board()[row][col].get_color().value != colorCelda.BLACK.value:
                    return False
                if self.grid[row][col] == 2 and tablero.get_board()[row][col].get_color().value != colorCelda.RED.value:
                    return False
                if self.grid[row][col] == 3 and tablero.get_board()[row][col].get_color().value != colorCelda.GREEN.value:
                    return False
                if self.grid[row][col] == 4 and tablero.get_board()[row][col].get_color().value != colorCelda.BLUE.value:
                    return False
        self.completado = True
        return True

    def get_grid(self):
        return self.grid
    
    def get_colors(self):
        return self.colores
    
    def isCompleted(self):
        return self.completado

class Gamemode:
    def __init__(self):
        pass

class Confetti:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(2, 5)
        self.color = random.choice([
            (255, 0, 0), (0, 255, 0), (0, 0, 255),
            (255, 255, 0), (255, 0, 255), (0, 255, 255)
        ])
        self.speed_y = random.uniform(1, 3)
        self.speed_x = random.uniform(-1, 1)

    def update(self):
        self.y += self.speed_y
        self.x += self.speed_x

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)


if __name__ == "__main__":
    estadisticas = Estadisticas()
    estadisticas.verificarArchivo()