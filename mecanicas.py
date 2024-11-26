import pygame, math, json
from utils import SettingsManager, Colores, Boton

class Celda:
    def __init__(self):
        self.color = Colores.DEFAULT.value

    def click(self, color):
        if(color == self.color):
            self.color = Colores.DEFAULT.value
        else:    
            self.color = color

    def get_color(self):
        return self.color

class Tablero:
    def __init__(self, matriz_objetivo):
        self.matriz_objetivo = matriz_objetivo
        self.size_matriz = len(matriz_objetivo[0])
        self.cell_size = SettingsManager.CELL_SIZE.value
        self.tablero = [[Celda() for _ in range(self.size_matriz)] for _ in range(self.size_matriz)]
        self.font = pygame.font.SysFont(None, 24)

        # Variables para manejar el click
        self.celda_anterior = 0 
        self.color_arrastre = 0
        self.color_seleccionado = Colores.BLACK.value
        
    def verificar(self):
        for row in range(len(self.tablero)):
            for col in range(len(self.tablero[row])):
                color = self.tablero[row][col].get_color()
                if color == Colores.DEFAULT.value and self.matriz_objetivo[row][col] != 0:
                    return False
                if color == Colores.BLACK.value and self.matriz_objetivo[row][col] != 1:
                    return False
                if color == Colores.RED.value and self.matriz_objetivo[row][col] != 2:
                    return False
                if color == Colores.GREEN.value and self.matriz_objetivo[row][col] != 3:
                    return False
                if color == Colores.BLUE.value and self.matriz_objetivo[row][col] != 4:
                    return False
        self.completado = True
        return True 
                  
    def draw(self, surface, edge_size, altura_barra_superior):
        # Dibujar la cuadricula
        for row, rowOfCells in enumerate(self.tablero):
            for col, cell in enumerate(rowOfCells):
                color = cell.get_color()
                pygame.draw.rect(surface, color, (
                    (col + edge_size) * self.cell_size + 1,
                    (row + edge_size) * self.cell_size + altura_barra_superior + 1, self.cell_size - 2, self.cell_size - 2))
    
    def handle_click(self, pos, size_borde, presionando=False):
        size_tablero = len(self.tablero)
        cell_size = SettingsManager.CELL_SIZE.value

        row = (pos[1] - (size_borde * cell_size) - SettingsManager.SIZE_BARRA_SUPERIOR.value ) // cell_size
        col = (pos[0] - size_borde * cell_size) // cell_size
        if 0 <= row < size_tablero and 0 <= col < size_tablero:
            if self.celda_anterior != self.tablero[row][col] and presionando:
                if self.tablero[row][col].get_color() != self.color_arrastre: 
                    self.tablero[row][col].click(self.color_seleccionado)                             
            elif not presionando:
                self.tablero[row][col].click(self.color_seleccionado)
                self.color_seleccionado = self.tablero[row][col].get_color()
                self.color_arrastre = self.tablero[row][col].get_color()

            self.celda_anterior = self.tablero[row][col]
        
        for index, color in enumerate(Colores):
            cx = (size_borde+0.5+index)*cell_size
            cy = (size_tablero+size_borde+0.5)*cell_size + SettingsManager.SIZE_BARRA_SUPERIOR.value
            if math.sqrt(pow(cx-pos[0], 2) + pow(cy-pos[1], 2)) <= 10:
                self.color_seleccionado = color.value                
   
    def get_size_matriz(self):
        return self.size_matriz

    def get_tablero(self):
        return self.tablero

class Nivel:
    def __init__(self, matriz_objetivo, id):
        self.altura_barra_superior = SettingsManager.SIZE_BARRA_SUPERIOR.value
        self.matriz_objetivo = matriz_objetivo
        self.id = id
        self.size_borde = self.__calcular_maxima_secuencia__(matriz_objetivo)
        self.secuencias_fila = self.__calcular_secuencias_fila__(matriz_objetivo)
        self.secuencias_columna = self.__calcular_secuencias_columna__(matriz_objetivo)
        self.completado = False
        self.tablero = Tablero(matriz_objetivo)
        
    def __calcular_secuencias__(self, linea):
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
    
    def __calcular_maxima_secuencia__(self, matriz_objetivo):
        maxima_secuencia = 0
        for fila in matriz_objetivo:
            secuencia = self.__calcular_secuencias__(fila)
            maxima_secuencia = max(maxima_secuencia, secuencia)
        for columna in range(len(matriz_objetivo[0])):
            secuencia = self.__calcular_secuencias__([matriz_objetivo[fila][columna] for fila in range(len(matriz_objetivo))])
            maxima_secuencia = max(maxima_secuencia, secuencia)
        return maxima_secuencia
    
    def __calcular_secuencias_fila__(self,matriz_objetivo):
        secuencias = []
        for fila in matriz_objetivo:
            fila_secuencias = self.__get_secuencias__(fila)
            secuencias.append(fila_secuencias)
        return secuencias
    
    def __calcular_secuencias_columna__(self,matriz_objetivo):
        secuencias = []
        for columna in range(len(matriz_objetivo[0])):
            columna_secuencias = self.__get_secuencias__([matriz_objetivo[fila][columna] for fila in range(len(matriz_objetivo))])
            secuencias.append(columna_secuencias)
        return secuencias
    
    def __get_secuencias__(self, linea):
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
        size_matriz = self.tablero.get_size_matriz()
        # Pintar la barra superior
        pygame.draw.rect(surface, SettingsManager.TITLE_BAR_COLOR.value, (0, 0, (size_matriz + self.size_borde) * SettingsManager.CELL_SIZE.value, self.altura_barra_superior))
        font = pygame.font.SysFont("Trebuchet MS", 20)        
        # Dibujar el marco superior
        pygame.draw.rect(surface, SettingsManager.GRID_BACKGROUND_COLOR.value, (0, self.altura_barra_superior, (self.size_borde + size_matriz) * SettingsManager.CELL_SIZE.value, self.size_borde * SettingsManager.CELL_SIZE.value))
        for col in range(size_matriz):
            col_seq = self.secuencias_columna[col]
            for i, num in enumerate(col_seq):
                texto = font.render(str(num[1]), True, SettingsManager.TEXT_COLOR.value)
                if num[0] == 1:
                    texto = font.render(str(num[1]), True, Colores.BLACK.value)
                elif num[0] == 2:
                    texto = font.render(str(num[1]), True, Colores.RED.value)
                elif num[0] == 3:
                    texto = font.render(str(num[1]), True, Colores.GREEN.value)
                elif num[0] == 4:
                    texto = font.render(str(num[1]), True, Colores.BLUE.value)

                text_rect = texto.get_rect(center=((col + self.size_borde) * SettingsManager.CELL_SIZE.value + SettingsManager.CELL_SIZE.value // 2,
                                                   (self.size_borde - len(col_seq) + i) * SettingsManager.CELL_SIZE.value + SettingsManager.CELL_SIZE.value // 2 + self.altura_barra_superior))
                surface.blit(texto, text_rect)

        # Dibujar el marco izquierdo
        pygame.draw.rect(surface, SettingsManager.GRID_BACKGROUND_COLOR.value, (0, self.altura_barra_superior, self.size_borde*SettingsManager.CELL_SIZE.value, (self.size_borde + size_matriz)*SettingsManager.CELL_SIZE.value))
        for row in range(size_matriz):
            row_seq = self.secuencias_fila[row]
            for i, num in enumerate(row_seq):
                texto = font.render(str(num[1]), True, SettingsManager.TEXT_COLOR.value)
                if num[0] == 1:
                    texto = font.render(str(num[1]), True, Colores.BLACK.value)
                elif num[0] == 2:
                    texto = font.render(str(num[1]), True, Colores.RED.value)
                elif num[0] == 3:
                    texto = font.render(str(num[1]), True, Colores.GREEN.value)
                elif num[0] == 4:
                    texto = font.render(str(num[1]), True, Colores.BLUE.value)
                
                text_rect = texto.get_rect(center=((self.size_borde - len(row_seq) + i) * SettingsManager.CELL_SIZE.value + SettingsManager.CELL_SIZE.value // 2,
                                                   (row + self.size_borde) * SettingsManager.CELL_SIZE.value + SettingsManager.CELL_SIZE.value // 2 + self.altura_barra_superior))
                surface.blit(texto, text_rect)

        # Dibujar la esquina superior izquierda (previsualizacion)
        pygame.draw.rect(surface, Colores.DEFAULT.value, (0, self.altura_barra_superior, self.size_borde*SettingsManager.CELL_SIZE.value, self.size_borde*SettingsManager.CELL_SIZE.value))
        mini_cell_size = (SettingsManager.CELL_SIZE.value * self.size_borde) // size_matriz
        for i, fila in enumerate(self.tablero.get_tablero()):
            for j, celda in enumerate(fila):
                color = celda.get_color()
                rect = pygame.Rect(j * mini_cell_size, i * mini_cell_size + self.altura_barra_superior, mini_cell_size, mini_cell_size)
                pygame.draw.rect(surface, color, rect)

        # Dibujar selector de colores
        pygame.draw.rect(surface, SettingsManager.COLOR_SELECTOR_COLOR.value, (0, (size_matriz+self.size_borde)*SettingsManager.CELL_SIZE.value + self.altura_barra_superior,  (size_matriz+self.size_borde)*SettingsManager.CELL_SIZE.value, self.size_borde*SettingsManager.CELL_SIZE.value))
        for index, color in enumerate(Colores):
            pygame.draw.circle(surface, color.value, ((self.size_borde+0.5+index)*SettingsManager.CELL_SIZE.value , (size_matriz+self.size_borde+0.5)*SettingsManager.CELL_SIZE.value + self.altura_barra_superior), 10)

        self.tablero.draw(surface, self.size_borde, self.altura_barra_superior) 
                            
    def verificar(self):
        return self.tablero.verificar()
        
    def get_size_borde(self):
        return self.size_borde
            
    def handle_click(self, pos, presionando=False):
        self.tablero.handle_click(pos, self.size_borde, presionando)
    
    def get_id(self):
        return self.id
    
    def get_size_matriz(self):
        return len(self.matriz_objetivo[0])
    
    def isCompleted(self):
        return self.completado
    
    
class Partida:
    def __init__(self, menu, nivel):
        self.nivel = nivel
        size_tablero = nivel.get_size_matriz()
        
        #Referencia a menu 
        self.menu = menu
        
        #Pygame
        pygame.init()
        self.ancho_ventana = (self.nivel.get_size_borde() + size_tablero) * SettingsManager.CELL_SIZE.value
        self.altura_ventana = ((self.nivel.get_size_borde() + size_tablero + 1) * SettingsManager.CELL_SIZE.value) + SettingsManager.SIZE_BARRA_SUPERIOR.value
        self.window = pygame.display.set_mode((self.ancho_ventana, self.altura_ventana))
        self.clock = pygame.time.Clock()
        self.running = False

        #Botones
        self.fuente = pygame.font.SysFont(None, 35)  # Fuente para el mensaje
        self.fuente_boton = pygame.font.SysFont(None, self.altura_ventana // 100)
        self.boton_salir = Boton("Salir", (self.ancho_ventana // 4, SettingsManager.SIZE_BARRA_SUPERIOR.value/2), ( self.ancho_ventana // 2, SettingsManager.SIZE_BARRA_SUPERIOR.value/2), self.fuente_boton, self.salir)
        self.botones = [self.boton_salir]

        #Estadisticas
        self.tiempo_inicio = None
        self.estadisticas = Estadisticas()
        self.estadisticas.cargarEstadisticas()

    def mostrar_mensaje(self, mensaje):
        texto = self.fuente.render(mensaje, True, SettingsManager.BACKGROUND_COLOR.value)
        rect = texto.get_rect(center=(self.ancho_ventana // 2, self.altura_ventana // 2))

        # Dibujar un rectángulo blanco detrás del texto
        padding = 20  # Espacio adicional alrededor del texto
        background_rect = pygame.Rect(
            rect.left - padding,
            rect.top - padding,
            rect.width + 2 * padding,
            rect.height + 2 * padding
        )
        pygame.draw.rect(self.window, Colores.DEFAULT.value, background_rect)

        self.window.blit(texto, rect)
        pygame.display.flip()
        pygame.time.wait(2000)  # Espera 2 segundos para que el mensaje sea visible

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False 
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.nivel.handle_click(event.pos)

                # Redibujar el tablero después del clic
                self.window.fill(SettingsManager.BACKGROUND_COLOR.value)
                self.draw()
                pygame.display.flip()                               
               
                # Verificar si el nivel está completado después de procesar el clic
                if self.nivel.verificar():
                    self.mostrar_mensaje("¡Nivel completado!")
                    self.estadisticas.actualizar(self.get_tiempo_partida(), 1, 0, self.nivel.id)
                    self.salir()
            
            for button in self.botones:
                button.handle_event(event)
            
        if pygame.mouse.get_pressed()[0]:
            self.nivel.handle_click(pygame.mouse.get_pos(),True)

            # Redibujar el tablero después del clic
            self.window.fill(SettingsManager.BACKGROUND_COLOR.value)
            self.draw()
            pygame.display.flip()                               
               
            # Verificar si el nivel está completado después de procesar el clic
            if self.nivel.verificar():
                self.mostrar_mensaje("¡Nivel completado!")
                self.estadisticas.actualizar(self.get_tiempo_partida(), 1, 0, self.nivel.id)
                self.salir()

    def draw(self):
        self.nivel.draw(self.window)
        for button in self.botones:
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
        self.__verificarArchivo__()

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

    def __verificarArchivo__(self):
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
