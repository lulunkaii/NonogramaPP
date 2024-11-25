import pygame, math, json, os
from utils import SettingsManager, colorCelda, Boton

class Celda:
    def __init__(self):
        self.color = colorCelda.DEFAULT

    def click(self, color):
        if(color == self.color):
            self.color = colorCelda.DEFAULT
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
        self.celda_anterior = 0 
        self.color_arrastre = 0
        self.color_seleccionado = colorCelda.BLACK

    def verificar(self):
        return self.matriz_objetivo == self.tablero 
                
    def draw(self, surface, edge_size, altura_barra_superior):
        # Dibujar la cuadricula
        for row, rowOfCells in enumerate(self.tablero):
            for col, cell in enumerate(rowOfCells):
                color = cell.get_color().value
                pygame.draw.rect(surface, color, (
                    (col + edge_size) * self.cell_size + 1,
                    (row + edge_size) * self.cell_size + altura_barra_superior + 1, self.cell_size - 2, self.cell_size - 2))
        
    def get_size_matriz(self):
        return self.size_matriz

    def get_tablero(self):
        return self.tablero

    def load_tablero(self, tablero):
        self.tablero = tablero

class Nivel:
    def __init__(self, matriz_objetivo, id):
        self.altura_barra_superior = SettingsManager.SIZE_BARRA_SUPERIOR.value
        self.matriz_objetivo = matriz_objetivo
        self.id = id
        self.edge_size = self.__calcular_maxima_secuencia__(matriz_objetivo)
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
        
        # Pintar la barra superior
        pygame.draw.rect(surface, SettingsManager.TITLE_BAR_COLOR.value, (0, 0, (self.grid_size+self.edge_size)*self.cell_size, self.altura_barra_superior))
        
        # Dibujar el marco superior
        pygame.draw.rect(surface, SettingsManager.GRID_BACKGROUND_COLOR.value, (0, self.altura_barra_superior, (self.edge_size + self.grid_size)*self.cell_size, self.edge_size*self.cell_size))
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
                                                   (self.edge_size - len(col_seq) + i) * self.cell_size + self.cell_size // 2 + self.altura_barra_superior))
                surface.blit(texto, text_rect)

        # Dibujar el marco izquierdo
        pygame.draw.rect(surface, SettingsManager.GRID_BACKGROUND_COLOR.value, (0, self.altura_barra_superior, self.edge_size*self.cell_size, (self.edge_size + self.grid_size)*self.cell_size))
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
                                                   (row + self.edge_size) * self.cell_size + self.cell_size // 2 + self.altura_barra_superior))
                surface.blit(texto, text_rect)

        # Dibujar la esquina superior izquierda (previsualizacion)
        pygame.draw.rect(surface, SettingsManager.DEFAULT_COLOR.value, (0, self.altura_barra_superior, self.edge_size*self.cell_size, self.edge_size*self.cell_size))
        mini_cell_size = (self.cell_size * self.edge_size) // self.grid_size
        for i, fila in enumerate(self.tablero):
            for j, celda in enumerate(fila):
                color = celda.get_color().value
                rect = pygame.Rect(j * mini_cell_size, i * mini_cell_size + self.altura_barra_superior, mini_cell_size, mini_cell_size)
                pygame.draw.rect(surface, color, rect)

        # Dibujar selector de colores
        pygame.draw.rect(surface, SettingsManager.COLOR_SELECTOR_COLOR.value, (0, (self.grid_size+self.edge_size)*self.cell_size + self.altura_barra_superior,  (self.grid_size+self.edge_size)*self.cell_size, self.edge_size*self.cell_size))
        for index, color in enumerate(self.colores):
            pygame.draw.circle(surface, color.value, ((self.edge_size+0.5+index)*self.cell_size , (self.grid_size+self.edge_size+0.5)*self.cell_size + self.altura_barra_superior), 10)

        self.tablero.draw(surface, self.edge_size, self.altura_barra_superior)
        
    def handle_click(self, pos, presionando=False):
        size_tablero = self.tablero.get_size_matriz()
        cell_size = SettingsManager.CELL_SIZE.value
        
        row = (pos[1] - (self.edge_size * cell_size) - self.altura_barra_superior ) // cell_size
        col = (pos[0] - self.edge_size * cell_size) // cell_size
        if 0 <= row < size_tablero and 0 <= col < size_tablero:
            if self.celda_anterior != self.tablero[row][col] and presionando:
                if self.tablero[row][col].get_color().value != self.color_arrastre: 
                    self.tablero[row][col].click(self.color_seleccionado)                             
            elif not presionando:
                self.tablero[row][col].click(self.color_seleccionado)
                self.color_seleccionado = self.tablero[row][col].get_color()
                self.color_arrastre = self.tablero[row][col].get_color().value

            self.celda_anterior = self.tablero[row][col]
        
        for index, color in enumerate(colorCelda):
            cx = (self.edge_size+0.5+index)*cell_size
            cy = (size_tablero+self.edge_size+0.5)*cell_size + self.altura_barra_superior
            if math.sqrt(pow(cx-pos[0], 2) + pow(cy-pos[1], 2)) <= 10:
                self.color_seleccionado = color
    
    def verificar(self):
        return self.tablero.verificar()
    
    def get_matriz_objetivo(self):
        return self.matriz_objetivo
        
    def isCompleted(self):
        return self.completado
    
class Partida:
    def __init__(self, nivel, menu, cell_size=SettingsManager.CELL_SIZE.value, url = None):
        pygame.init()
        if url:
            self.url = url + ".json"
        else:
            self.url = None
        self.altura_barra_superior = 50
        self.nivel = nivel
        self.grid_size = len(nivel.get_grid())
        self.tablero = Tablero(self.grid_size, SettingsManager.CELL_SIZE.value, nivel.get_grid(), nivel.get_colors(), self.altura_barra_superior)
        self.window_width = (self.tablero.get_edge_size() + self.grid_size) * cell_size
        self.window_height = ((self.tablero.get_edge_size() + self.grid_size + 1) * cell_size) + self.altura_barra_superior
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.clock = pygame.time.Clock()
        self.menu = menu  # Referencia al menú
        self.running = False
        self.font = pygame.font.SysFont(None, 35)  # Fuente para el mensaje
        self.button_font = pygame.font.SysFont(None, self.window_height // 100)
        self.save_button = Boton("Guardar y salir", (5 * (self.window_width // 9), self.altura_barra_superior/5), (3* (self.window_width // 9), 3 * self.altura_barra_superior/5), self.button_font, self.guardar)
        self.exit_button = Boton("Salir", (self.window_width // 9, self.altura_barra_superior/5), (3 * (self.window_width // 9), 3 * self.altura_barra_superior/5), self.button_font, self.salir)
        self.buttons = [self.save_button, self.exit_button]
        self.tiempo_inicio = None
        self.estadisticas = Estadisticas()
        self.estadisticas.cargarEstadisticas()

    def mostrar_mensaje(self, mensaje):
        texto = self.font.render(mensaje, True, SettingsManager.BACKGROUND_COLOR.value)
        rect = texto.get_rect(center=(self.window_width // 2, self.window_height // 2))

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
                self.tablero.handle_click(event.pos)

                # Redibujar el tablero después del clic
                self.window.fill(SettingsManager.BACKGROUND_COLOR.value)
                self.draw()
                pygame.display.flip()                               
               
                # Verificar si el nivel está completado después de procesar el clic
                if self.nivel.verificar(self.tablero):
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
            
            for button in self.buttons:
                button.handle_event(event)
            

        if pygame.mouse.get_pressed()[0]:
            self.tablero.handle_click(pygame.mouse.get_pos(),True)

            # Redibujar el tablero después del clic
            self.window.fill(SettingsManager.BACKGROUND_COLOR.value)
            self.draw()
            pygame.display.flip()                               
               
            # Verificar si el nivel está completado después de procesar el clic
            if self.nivel.verificar(self.tablero):
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
        tablero_data = [[cell.get_color().value for cell in row] for row in self.tablero.get_tablero()]
        grid_data = self.nivel.get_grid()

        data = {
            'tablero': tablero_data,
            'grid': grid_data
        }

        with open(filename, 'w') as file:
            json.dump(data, file)

        self.mostrar_mensaje("Partida guardada exitosamente.")
        self.salir()


    def cargar(self, tablero):
        self.tablero.load_tablero(tablero)

    def draw(self):
        self.tablero.draw(self.window)
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

class Gamemode:
    def __init__(self):
        pass

if __name__ == "__main__":
    estadisticas = Estadisticas()
    estadisticas.verificarArchivo()