import pygame, math, json, random 
from utils import SettingsManager, Colores, Boton
import os, time

class Celda:
    """
    Representa una celda unica con su color.

    Attributes:
        color (Color): El color de la cerda.
    """
    def __init__(self):
        """
        Inicializa una clase celda con el color default.
        """
        self.color = Colores.DEFAULT.value

    def click(self, color):
        """
        Cambia el color de la celda segun el color seleccionado

        Args:
            color (Color): El nuevo color de la celda (si es su color actual se le pone el default).
        """
        if(color == self.color):
            self.color = Colores.DEFAULT.value
        else:    
            self.color = color

    def get_color(self):
        return self.color

class Tablero:
    """
    Representa un tablero de celdas.
    
    Attributes:
        matriz_objetivo (List[List[int]]): La matriz objetivo que se debe alcanzar.
        size_matriz (int): El tamaño de la matriz objetivo.
        size_celda (int): El tamaño de las celdas.
        tablero (List[List[Celda]]): La matriz de celdas.
    """
    def __init__(self, matriz_objetivo):
        """
        Inicializa un tablero con la matriz objetivo.
        
        Args:
            matriz_objetivo (List[List[int]]): La matriz objetivo que se debe alcanzar.
        """
        self.matriz_objetivo = matriz_objetivo
        self.size_matriz = len(matriz_objetivo[0])
        self.size_celda = SettingsManager.CELL_SIZE.value
        self.tablero = [[Celda() for _ in range(self.size_matriz)] for _ in range(self.size_matriz)]
        self.contadorMalas = 0
        self.contadorBuenas = 0
        self.font = pygame.font.SysFont(None, 24)

        # Variables para manejar el click
        self.celda_anterior = None
        self.color_arrastre = None
        self.color_seleccionado = Colores.BLACK.value
        self.color_anterior = self.color_seleccionado
        
    def verificar(self):
        """
        Verifica si el tablero actual es igual a la matriz objetivo.
        
        Returns:
            bool: True si el tablero es igual a la matriz objetivo, False en caso contrario.
        """
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
        return True 
                  
    def draw(self, surface, size_borde, altura_barra_superior):
        """
        Dibuja el tablero en la superficie dada.
        
        Args:
            surface (surface): La superficie en la que se dibujara el tablero.
            size_borde (int): El tamaño del borde del tablero.
            altura_barra_superior (int): La altura de la barra superior.
        """
        # Dibujar la cuadricula
        for row, rowOfCells in enumerate(self.tablero):
            for col, cell in enumerate(rowOfCells):
                color = cell.get_color()
                pygame.draw.rect(surface, color, (
                    (col + size_borde) * self.size_celda + 1,
                    (row + size_borde) * self.size_celda + altura_barra_superior + 1, self.size_celda - 2, self.size_celda - 2))
    
    def handle_click(self, pos, size_borde, presionando=False):
        """
        Maneja el click en el tablero.
        
        Args:
            pos (Tuple[int, int]): La posicion del click.
            size_borde (int): El tamaño del borde del tablero.
            presionando (bool): True si el click se esta presionando, False en caso contrario.
        """
        size_tablero = len(self.tablero)
        cell_size = SettingsManager.CELL_SIZE.value

        row = (pos[1] - (size_borde * cell_size) - SettingsManager.SIZE_BARRA_SUPERIOR.value ) // cell_size
        col = (pos[0] - size_borde * cell_size) // cell_size
        if 0 <= row < size_tablero and 0 <= col < size_tablero:
            if self.celda_anterior != self.tablero[row][col] and presionando:
                if self.tablero[row][col].get_color() != self.color_arrastre: 
                    self.tablero[row][col].click(self.color_seleccionado)                             
            elif not presionando:
                self.color_seleccionado = self.color_anterior  # Restaurar el color anterior
                if self.color_seleccionado == Colores.DEFAULT.value:
                    self.tablero[row][col].click(self.color_seleccionado)                    
                else:
                     self.tablero[row][col].click(self.color_seleccionado)
                     self.color_anterior = self.color_seleccionado  # Recordar el color actual
                     self.color_seleccionado = self.tablero[row][col].get_color()
                     self.color_arrastre = self.tablero[row][col].get_color()

            self.celda_anterior = self.tablero[row][col]
        
        for index, color in enumerate(Colores):
            cx = (size_borde+0.5+index)*cell_size
            cy = (size_tablero+size_borde+0.5)*cell_size + SettingsManager.SIZE_BARRA_SUPERIOR.value
            if math.sqrt(pow(cx-pos[0], 2) + pow(cy-pos[1], 2)) <= 10:
                self.color_seleccionado = color.value   
                self.color_anterior = self.color_seleccionado  

    def comparar(self):
        """
        Compara el tablero actual con la matriz objetivo.
        
        Returns:
            bool: True si todas las casillas marcadas en el tablero actual coinciden con las casillas marcadas en la matriz objetivo, False en caso contrario.
        """
        contadorActualBuenas = 0
        contadorActualMalas = 0
        for row in range(len(self.tablero)):
            for col in range(len(self.tablero[row])):
                color = self.tablero[row][col].get_color()
                objetivo = self.matriz_objetivo[row][col]
                if color != Colores.DEFAULT.value:
                    if (color == Colores.BLACK.value and objetivo != 1) or \
                    (color == Colores.RED.value and objetivo != 2) or \
                    (color == Colores.GREEN.value and objetivo != 3) or \
                    (color == Colores.BLUE.value and objetivo != 4):
                        contadorActualMalas += 1

        if contadorActualMalas <= self.contadorMalas:
            self.contadorMalas = contadorActualMalas
            return True
        else:
            self.contadorMalas = contadorActualMalas
            return False            
   
    def get_size_matriz(self):
        return self.size_matriz

    def get_tablero(self):
        return self.tablero

class Nivel:
    """
    Representa un nivel del juego.
    
    Attributes:
        altura_barra_superior (int): La altura de la barra superior.
        matriz_objetivo (List[List[int]]): La matriz objetivo que se debe alcanzar.
        id (int): El identificador del nivel.
        size_borde (int): El tamaño del borde del tablero.
        secuencias_fila (List[List[Tuple[int, int]]]): Las secuencias de la matriz objetivo por fila.
        secuencias_columna (List[List[Tuple[int, int]]]): Las secuencias de la matriz objetivo por columna.
        completado (bool): True si el nivel esta completado, False en caso contrario.
        tablero (Tablero): El tablero del nivel.
        vidas (int): La cantidad de vidas del nivel.
    """
    def __init__(self, matriz_objetivo, id, contrarreloj=0):
        """
        Inicializa un nivel con la matriz objetivo y el identificador.
        
        Args:
            matriz_objetivo (List[List[int]]): La matriz objetivo que se debe alcanzar.
            id (int): El identificador del nivel.
            vidas (int): La cantidad de vidas del nivel.
        """
        self.altura_barra_superior = SettingsManager.SIZE_BARRA_SUPERIOR.value
        self.matriz_objetivo = matriz_objetivo
        self.id = id
        self.size_borde = self.__calcular_maxima_secuencia__(matriz_objetivo)
        self.secuencias_fila = self.__calcular_secuencias_fila__(matriz_objetivo)
        self.secuencias_columna = self.__calcular_secuencias_columna__(matriz_objetivo)
        self.completado = False
        self.tablero = Tablero(matriz_objetivo)
        self.tipo_nivel = ""
        self.tiempo_contrarreloj = contrarreloj
        
    def __calcular_secuencias__(self, linea):
        """
        Calcula las secuencias de una linea.

        Args:
            linea (List(Celda)): La linea de la matriz objetivo
        Returns:
            int: El numero de secuencias en la linea.
        """
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
        """
        Calcula la maxima secuencia de la matriz objetivo.
        
        Args:
            matriz_objetivo (List[List[int]]): La matriz objetivo.
        Returns:
            int: La maxima secuencia de la matriz objetivo.
        """
        maxima_secuencia = 0
        for fila in matriz_objetivo:
            secuencia = self.__calcular_secuencias__(fila)
            maxima_secuencia = max(maxima_secuencia, secuencia)
        for columna in range(len(matriz_objetivo[0])):
            secuencia = self.__calcular_secuencias__([matriz_objetivo[fila][columna] for fila in range(len(matriz_objetivo))])
            maxima_secuencia = max(maxima_secuencia, secuencia)
        return maxima_secuencia
    
    def __calcular_secuencias_fila__(self,matriz_objetivo):
        """
        Calcula las secuencias de la matriz objetivo por fila.
        
        Args:
            matriz_objetivo (List[List[int]]): La matriz objetivo.
        Returns:
            List[List[Tuple[int, int]]]: Las secuencias de la matriz objetivo por fila.
        """
        secuencias = []
        for fila in matriz_objetivo:
            fila_secuencias = self.__get_secuencias__(fila)
            secuencias.append(fila_secuencias)
        return secuencias
    
    def __calcular_secuencias_columna__(self,matriz_objetivo):
        """
        Calcula las secuencias de la matriz objetivo por columna.
        
        Args:
            matriz_objetivo (List[List[int]]): La matriz objetivo.
        Returns:
            List[List[Tuple[int, int]]]: Las secuencias de la matriz objetivo por columna.
        """
        secuencias = []
        for columna in range(len(matriz_objetivo[0])):
            columna_secuencias = self.__get_secuencias__([matriz_objetivo[fila][columna] for fila in range(len(matriz_objetivo))])
            secuencias.append(columna_secuencias)
        return secuencias
    
    def __get_secuencias__(self, linea):
        """
        Obtiene las secuencias de una linea.
        
        Args:
            linea (List[int]): La linea de la matriz objetivo.
        Returns:
            List[Tuple[int, int]]: Las secuencias de la linea.
        """
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
        """
        Dibuja el nivel en la superficie dada.

        Args:
            surface (Surface): La superficie en la que se dibujara el nivel.
        """
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
        """
        Verifica si el nivel esta completado.
        
        Returns:
            bool: True si el nivel esta completado, False en caso contrario.
        """
        completado = self.tablero.verificar()
        if completado:
            self.completado = True
        return completado
        
    def get_size_borde(self):
        return self.size_borde
            
    def handle_click(self, pos, presionando=False):
        """
        Maneja el click en el nivel.

        Args:
            pos (Tuple[int, int]): La posicion del click.
            presionando (bool, optional): True si el click se esta presionando, False en caso contrario. Defaults to False.
        """
        self.tablero.handle_click(pos, self.size_borde, presionando)
    
    def get_tipo(self):
        return self.tipo_nivel
    
    def get_id(self):
        return self.id
    
    def get_size_matriz(self):
        return len(self.matriz_objetivo[0])
    
    def isCompleted(self):
        """
        Verifica si el nivel fue completado en algun momento.
                
        Returns:
            bool: True si el nivel esta completado, False en caso contrario.
        """
        return self.completado
    
    def get_tablero(self):
        return self.tablero

    def set_tablero(self, tablero):
        self.tablero = tablero
    
    def get_matriz(self):
        return self.matriz_objetivo
    
class NivelConVidas(Nivel):
    def __init__(self, matriz_objetivo, id, vidas):
        super().__init__(matriz_objetivo, id)
        self.vidas = vidas
        self.frames_corazon = []
        self.frames_index = 0
        self.frame_counter = 0
        self.frame_interval = 60  # Ajusta este valor para cambiar la velocidad de la animación
        for i in range(1, 19):
            img = pygame.image.load("resources/corazon/corazon" + str(i) + ".png")
            img = pygame.transform.scale(img, (40, 40))
            self.frames_corazon.append(img)
        
    def draw(self, surface):
        super().draw(surface)
        size_matriz = self.tablero.get_size_matriz()

        for i in range(self.vidas):
            surface.blit(self.frames_corazon[self.frames_index], ((self.size_borde+5.3+i*1.1)*SettingsManager.CELL_SIZE.value,(size_matriz + self.size_borde - 0.08)*SettingsManager.CELL_SIZE.value + self.altura_barra_superior))

        # Actualizar el índice de los frames
        self.frame_counter += 1
        if self.frame_counter >= self.frame_interval:
            self.frames_index = (self.frames_index + 1) % len(self.frames_corazon)
            self.frame_counter = 0      

    def handle_click(self, pos, presionando=False):
        super().handle_click(pos, presionando)
        if not self.tablero.comparar():
            self.vidas -= 1 

class NivelClasico(NivelConVidas):
    def __init__(self, matriz_objetivo, id, vidas):
        super().__init__(matriz_objetivo, id, vidas)
        self.tipo_nivel = "clasico"

class NivelHardcore(NivelConVidas):
    def __init__(self, matriz_objetivo, id):
        super().__init__(matriz_objetivo, id, 1)
        self.tipo_nivel = "hardcore"

class NivelContrarreloj(Nivel):
    def __init__(self, matriz_objetivo, id, tiempo = 15):
        super().__init__(matriz_objetivo, id)
        self.tiempo_maximo = tiempo
        self.tiempo_inicio = time.time()
        self.tiempo_restante = tiempo
        self.tipo_nivel = "contrarreloj"
    
    def actualizar_timer(self):
        tiempo_actual = time.time()
        tiempo_transcurrido = tiempo_actual - self.tiempo_inicio
        if tiempo_transcurrido >= self.tiempo_maximo:
            return True
        else:
            self.tiempo_restante = self.tiempo_maximo - tiempo_transcurrido
            return False
    
    def get_tiempo_restante(self):
        return self.tiempo_restante
    
    def set_tiempo_inicio(self, tiempo):
        self.tiempo_inicio = tiempo

    def reiniciar_tiempo(self):
        self.tiempo_inicio = time.time()
        self.tiempo_restante = self.tiempo_maximo
    
    def draw(self, surface):
        super().draw(surface)

        font = pygame.font.SysFont("Trebuchet MS", 20)
        tiempo_restante_limitado = "{:.2f}".format(self.tiempo_restante)
        text = font.render(tiempo_restante_limitado, True, (255, 255, 255))  # Texto en color blanco
        text_rect = text.get_rect(center=((self.size_borde+8)*SettingsManager.CELL_SIZE.value,(self.tablero.get_size_matriz() + self.size_borde + 0.5)*SettingsManager.CELL_SIZE.value + self.altura_barra_superior))  # Centrar el texto en la superficie

        # Dibujar el texto en la superficie
        surface.blit(text, text_rect)

class Partida:
    """
    Representa una partida del juego.
    
    Attributes:
        nivel (Nivel): El nivel de la partida.
        menu (Menu): El menu de la partida.
        tiempo_inicio (int): El tiempo de inicio de la partida.
        estadisticas (Estadisticas): Las estadisticas de la partida.
    """
    def __init__(self, menu, nivel):
        """
        Inicializa una partida con el nivel y el menu.
        
        Args:
            menu (Menu): El menu de la partida.
            nivel (Nivel): El nivel de la partida.
        """
        self.nivel = nivel
        size_tablero = nivel.get_size_matriz()
        self.tipo_nivel = self.nivel.get_tipo()
        
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
        self.fuente_victoria = pygame.font.SysFont(None, int(self.ancho_ventana * 0.13))
        self.fuente = pygame.font.SysFont(None, int(self.ancho_ventana * 0.20)) # Fuente para el mensaje
        self.fuente_boton = pygame.font.SysFont(None, self.altura_ventana // 20)
        self.boton_salir = Boton("Salir", (self.ancho_ventana // 9, SettingsManager.SIZE_BARRA_SUPERIOR.value / 4), ( 3 * self.ancho_ventana // 9, SettingsManager.SIZE_BARRA_SUPERIOR.value/2), self.fuente_boton, self.salir)
        self.boton_reiniciar = Boton("Reiniciar", ( 5* self.ancho_ventana // 9, SettingsManager.SIZE_BARRA_SUPERIOR.value / 4), (3 * self.ancho_ventana // 9, SettingsManager.SIZE_BARRA_SUPERIOR.value / 2), self.fuente_boton, self.reiniciar_nivel)
        self.botones = [self.boton_salir, self.boton_reiniciar]

        #Estadisticas
        self.tiempo_inicio = None
        self.estadisticas = Estadisticas()
        self.estadisticas.cargarEstadisticas()

        #Cargar progreso
        self.tablero = self.nivel.get_tablero()
        self.cargar_progreso(nivel.id)   

        
    def mostrar_animacion_victoria(self, mensaje):
        alpha = 0
        texto = self.fuente_victoria.render(mensaje, True, SettingsManager.VICTORIA_COLOR.value)
        rect = texto.get_rect(center=(self.ancho_ventana // 2, self.altura_ventana // 2))

        # Dibujar un rectángulo blanco detrás del texto
        padding = 20  # Espacio adicional alrededor del texto
        rect_fondo = pygame.Rect(rect.left - padding, rect.top - padding, rect.width + 2 * padding, rect.height + 2 * padding)
        

        # Crear una superficie transparente para el texto
        text_surface = pygame.Surface((rect.width + 2 * padding, rect.height + 2 * padding), pygame.SRCALPHA)
        text_surface.fill((255, 255, 255, 0))  # Fondo transparente

        # Crear fuegos artificiales
        fireworks = [Firework(random.randint(0, self.ancho_ventana), random.randint(0, self.altura_ventana)) for _ in range(55)]

        # Animar la aparición del texto y los fuegos artificiales
        for alpha in range(0, 256, 5):
            self.window.fill(SettingsManager.BACKGROUND_COLOR.value)  # Limpiar la pantalla
            self.draw()

            # Dibujar fuegos artificiales
            for firework in fireworks:
                firework.update()
                firework.draw(self.window)
            
            pygame.display.flip()
            pygame.time.delay(30)
        
        for alpha in range(0, 256, 5):
            pygame.draw.rect(self.window, SettingsManager.DEFAULT_COLOR.value, rect_fondo)

            text_surface.blit(texto, (padding, padding))
            text_surface.set_alpha(alpha)
            self.window.blit(text_surface, rect_fondo.topleft)

            pygame.display.flip()
            pygame.time.delay(30)

        pygame.time.wait(2000)  # Espera 2 segundos para que el mensaje sea visible


    def mostrar_animacion_derrota(self, mensaje):
            alpha = 0
            texto = self.fuente.render(mensaje, True, SettingsManager.COLOR_SELECTOR_COLOR.value)
            rect = texto.get_rect(center=(self.ancho_ventana // 2, self.altura_ventana // 2))

            # Dibujar un rectángulo blanco detrás del texto
            padding = 20  # Espacio adicional alrededor del texto
            rect_fondo = pygame.Rect(rect.left - padding, rect.top - padding, rect.width + 2 * padding, rect.height + 2 * padding)
           

            # Crear una superficie transparente para el texto
            text_surface = pygame.Surface((rect.width + 2 * padding, rect.height + 2 * padding), pygame.SRCALPHA)
            text_surface.fill((255, 255, 255, 0))  # Fondo transparente

            self.draw()
            # Crear caras enojadas
            caquita = Caquita(self.window, self.ancho_ventana, self.altura_ventana)
            caquita.mostrar_animacion()  

            # Animar la aparición del texto
            for alpha in range(0, 256, 5):
                pygame.draw.rect(self.window, SettingsManager.DEFAULT_COLOR.value, rect_fondo)
                # Renderizar el texto con la opacidad actual
                text_surface.fill((255, 255, 255, 0))  # Limpiar la superficie
                text_surface.blit(texto, (padding, padding))
                text_surface.set_alpha(alpha)

               

                # Blit la superficie del texto en la ventana principal
                self.window.blit(text_surface, (rect.left - padding, rect.top - padding))
                pygame.display.flip()
                pygame.time.wait(30)  # Espera un poco para crear el efecto de animación

            pygame.time.wait(2000)  # Espera 2 segundos para que el mensaje sea visible


    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False 
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.nivel.handle_click(event.pos)
                if self.tipo_nivel == "clasico" or self.tipo_nivel == "hardcore":
                    self.comprobar_vidas()

                for button in self.botones:
                    button.handle_event(event)    
                
                # Redibujar el tablero después del clic
                self.window.fill(SettingsManager.BACKGROUND_COLOR.value)
                self.draw()
                pygame.display.flip()
                                             
        if pygame.mouse.get_pressed()[0]:
            self.nivel.handle_click(pygame.mouse.get_pos(), True)
            if self.tipo_nivel == "clasico" or self.tipo_nivel == "hardcore":
                self.comprobar_vidas()
                
            # Redibujar el tablero después del clic
            self.window.fill(SettingsManager.BACKGROUND_COLOR.value)
            self.draw()
            pygame.display.flip() 


            # Verificar si el nivel está completado después de procesar el clic
            if self.nivel.verificar():
                self.mostrar_animacion_victoria("¡Nivel completado!")
                self.estadisticas.actualizar(self.get_tiempo_partida(), 1, 0, self.nivel.id)
                self.reiniciar_nivel()
                self.salir()

    def comprobar_vidas(self):
        if self.nivel.vidas == 0:
            self.mostrar_animacion_derrota("¡Has perdido!")
            self.estadisticas.actualizar(self.get_tiempo_partida(), 0, 0, self.nivel.id)
            self.reiniciar_nivel()
            self.salir()   

    def draw(self):
        self.nivel.draw(self.window)
        for button in self.botones:
            button.draw(self.window)

        
  

    def salir(self):
        self.guardar_progreso(self.nivel.id) # guarda el progreso cuando sale den nivel
        self.running = False
        self.menu.volver_al_menu()

    def guardar_progreso(self, nivel_id):
        size = self.tablero.get_size_matriz()
        progreso = [[0 for _ in range(size)] for _ in range(size)]
        tablero = self.tablero.get_tablero()
        for row in range(size):
            for col in range(size):                
                color = tablero[row][col].get_color()
                if color == Colores.DEFAULT.value:
                    color = 0
                if color == Colores.BLACK.value: 
                    color = 1                   
                if color == Colores.RED.value:
                    color = 2                     
                if color == Colores.GREEN.value:
                    color = 3  
                if color == Colores.BLUE.value:
                    color = 4 

                progreso[row][col] = color

        # Asegurarse de que el directorio exista
        os.makedirs('levels/partidas', exist_ok=True)

        # Crear el archivo si no existe
        if not os.path.exists('levels/partidas/partidasencurso.json'):
            with open('levels/partidas/partidasencurso.json', 'w') as file:
                json.dump([], file)     
            
        try:
            with open('levels\partidas\partidasencurso.json', 'r') as file:
                partidas = json.load(file)
        except FileNotFoundError:
            partidas = []

        nivel_actualizado = False
        for partida in partidas:
            if partida['id'] == nivel_id:
                partida['progreso'] = progreso
                if self.tipo_nivel == "clasico" or self.tipo_nivel == "hardcore":
                    partida['vidas'] = self.nivel.vidas
                elif self.tipo_nivel == "contrarreloj":
                    partida['tiempo'] = self.nivel.get_tiempo_restante()
                partida['tipo'] = self.tipo_nivel
                nivel_actualizado = True
                break

        if not nivel_actualizado:
            if self.tipo_nivel == "clasico" or self.tipo_nivel == "hardcore":
                partidas.append({'id': nivel_id, 'progreso': progreso, 'vidas': self.nivel.vidas, 'tipo': self.tipo_nivel})
            elif self.tipo_nivel == "contrarreloj":
                partidas.append({'id': nivel_id, 'progreso': progreso, 'tiempo': self.nivel.get_tiempo_restante(), 'tipo': self.tipo_nivel})

        with open('levels\partidas\partidasencurso.json', 'w') as file:
            json.dump(partidas, file, indent=1)


    def cargar_progreso(self, nivel_id):
        try:
            with open('levels/partidas/partidasencurso.json', 'r') as file:
                partidas = json.load(file)
            for partida in partidas:
                if partida['id'] == nivel_id:
                    progreso = partida['progreso']
                    if partida['tipo'] == 'clasico' or partida['tipo'] == 'hardcore':
                        self.nivel.vidas = partida['vidas']
                    elif partida['tipo'] == 'contrarreloj':
                        self.nivel.set_tiempo_inicio(self.nivel.tiempo_inicio - self.nivel.tiempo_maximo + partida['tiempo'])
                        self.nivel.tiempo_restante = partida['tiempo']
                    for row in range(self.tablero.get_size_matriz()):
                        for col in range(self.tablero.get_size_matriz()):
                            color = progreso[row][col]
                            if color == 1:
                                self.tablero.get_tablero()[row][col].click(Colores.BLACK.value)
                            elif color == 2:
                                self.tablero.get_tablero()[row][col].click(Colores.RED.value)
                            elif color == 3:
                                self.tablero.get_tablero()[row][col].click(Colores.GREEN.value)
                            elif color == 4:
                                self.tablero.get_tablero()[row][col].click(Colores.BLUE.value)
                            else:
                                self.tablero.get_tablero()[row][col].click(Colores.DEFAULT.value)
                    break
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def reiniciar_nivel(self):
        self.nivel.set_tablero(Tablero(self.nivel.get_matriz()))
        self.tablero = self.nivel.get_tablero()  # Reiniciar el tablero con la matriz objetivo original
        self.window.fill(SettingsManager.BACKGROUND_COLOR.value)  # Limpiar la ventana
        
        if self.tipo_nivel == "clasico":
            self.nivel.vidas = 3 # Reiniciar las vidas
        elif self.tipo_nivel == "hardcore":
            self.nivel.vidas = 1
        elif self.tipo_nivel == "contrarreloj":
            self.nivel.reiniciar_tiempo()
        
        self.draw()  # Redibujar el tablero
        pygame.display.flip()  # Actualizar la pantalla

    def run(self):
        self.tiempo_inicio = pygame.time.get_ticks()
        self.running = True
        while self.running:
            if self.tipo_nivel == "contrarreloj":
                finalizado = self.nivel.actualizar_timer()
                if finalizado:
                    self.mostrar_animacion_derrota("¡Has perdido!")
                    self.estadisticas.actualizar(self.get_tiempo_partida(), 0, 0, self.nivel.id)
                    self.reiniciar_nivel()
                    self.salir()   

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
    """
    Representa las estadisticas de un jugador.
    
    Attributes:
        id (int): El identificador del jugador.
        segundos_jugados (int): Los segundos jugados por el jugador.
        cant_niveles_superados (int): La cantidad de niveles superados por el jugador.
        puntuacion_total (int): La puntuacion total del jugador.
        niveles_completados (List[str]): Los niveles completados por el jugador.
    """
    def __init__(self, id=1):
        """
        Inicializa las estadisticas con el identificador del jugador.
        
        Args:
            id (int, optional): El identificador del jugador. Defaults to 1.
        """
        self.id = id
        self.segundos_jugados = 0
        self.cant_niveles_superados = 0
        self.puntuacion_total = 0
        self.niveles_completados = []
        self.__verificarArchivo__()

    def actualizar(self, segundos, niveles, puntuacion, nivel_completado=None):
        """
        Actualiza las estadisticas del jugador.
        
        Args:
            segundos (int): Los segundos jugados.
            niveles (int): La cantidad de niveles superados.
            puntuacion (int): La puntuacion obtenida.
            nivel_completado (str, optional): El nivel completado. Defaults to None.
        """
        self.segundos_jugados += segundos
        self.cant_niveles_superados += niveles
        self.puntuacion_total += puntuacion
        if nivel_completado:
            if nivel_completado.endswith(".txt"):
                nivel_completado = nivel_completado[:-4]
            if nivel_completado not in self.niveles_completados:
                self.niveles_completados.append(nivel_completado)
    
        self.__guardarEstadisticas__()

    def __verificarArchivo__(self):
        """
        Verifica si el archivo de estadisticas existe, si no lo crea.
        """
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
        """
        Carga las estadisticas del jugador.
        """
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
                self.cant_niveles_superados = user["niveles_superados"]
                self.puntuacion_total = user["puntuacion_total"]
                self.niveles_completados = user["niveles_completados"]
                break
        
    def __guardarEstadisticas__(self):
        """
        Guarda las estadisticas del jugador.
        """
        try:
            with open("data/estadisticas.json", "r") as file:
                estadisticas = json.load(file)
        except:
            print("Error al cargar el archivo de estadísticas.")
            return
        
        for user in estadisticas:
           if user["id"] == self.id:
                user["segundos_jugados"] = self.segundos_jugados
                user["niveles_superados"] = self.cant_niveles_superados
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
        return self.cant_niveles_superados
    
    def getPuntuacionTotal(self):
        return self.puntuacion_total
    
    def getNivelesCompletados(self):
        return self.niveles_completados

class CrearNivel:
    """
    Representa la creación de un nivel.
    
    Attributes:
        menu (Menu): El menu principal.
        nivel (Nivel): El nivel a crear.
    """
    def __init__(self, menu_principal, nivel):
        """
        Inicializa la creación de un nivel con el menu principal y el nivel.
        
        Args:
            menu_principal (Menu): El menu principal.
            nivel (Nivel): El nivel a crear.
        """
        self.menu = menu_principal
        self.nivel = nivel
        self.altura_ventana = 600
        self.ancho_ventana = 500
        self.window = pygame.display.set_mode((self.ancho_ventana, self.altura_ventana))
        pygame.display.set_caption("Crear Nivel")
        self.clock = pygame.time.Clock()
        self.running = False
        self.fuente = pygame.font.SysFont("Trebuchet MS", 20)
        self.boton_guardar = Boton("Guardar Nivel", (self.ancho_ventana // 2 - 100, self.altura_ventana - 60), (240, 50), self.fuente, self.guardar_nivel)
        self.colores = [Colores.DEFAULT, Colores.BLACK, Colores.RED, Colores.GREEN, Colores.BLUE]
        self.rect_colores = [pygame.Rect(50 + i * 60, self.altura_ventana - 100, 50, 50) for i in range(len(Colores)) ]
        self.color_seleccionado = Colores.DEFAULT

    def handle_events(self):
        """
        Maneja los eventos de la creación del nivel.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Verificar si se selecciona un color
                    for i, rect in enumerate(self.rect_colores):
                        if rect.collidepoint(event.pos):
                            self.color_seleccionado = self.colores[i]

                    # Interacción con el tablero
                    self.nivel.handle_click(event.pos, self.color_seleccionado)

                # Verificar interacción con el botón
                self.boton_guardar.handle_event(event)
    
    def dibujar(self):
        """
        Dibuja la creación del nivel.
        """
        # Fondo
        self.window.fill(SettingsManager.BACKGROUND_COLOR.value)

        # Dibujar el tablero
        self.nivel.draw(self.window)

        # Dibujar el botón
        self.boton_guardar.draw(self.window)

        # Dibujar las opciones de colores
        for i, rect in enumerate(self.rect_colores):
            pygame.draw.rect(self.window, self.colores[i].value, rect)
            if self.colores[i] == self.color_seleccionado:
                pygame.draw.rect(self.window, (255, 255, 255), rect, 2)

        # Actualizar la pantalla
        pygame.display.flip()

    def run(self):
        """
        Ejecuta la creación del nivel.
        """
        self.running = True
        while self.running:
            self.clock.tick(60)
            self.handle_events()

            self.window.fill(SettingsManager.BACKGROUND_COLOR.value)
            self.nivel.draw(self.window)
            self.boton_guardar.draw(self.window)
            pygame.display.flip()
        pygame.quit()

    def guardar_nivel(self):
        """
        Guarda el nivel creado.
        """
        tablero = self.nivel.tablero.get_tablero()
        matriz = []
        for fila in tablero:
            nueva_fila = []
            for celda in fila:
                if celda.get_color() == Colores.DEFAULT.value:
                    nueva_fila.append(0)
                elif celda.get_color() == Colores.BLACK.value:
                    nueva_fila.append(1)
                elif celda.get_color() == Colores.RED.value:
                    nueva_fila.append(2)
                elif celda.get_color() == Colores.GREEN.value:
                    nueva_fila.append(3)
                elif celda.get_color() == Colores.BLUE.value:
                    nueva_fila.append(4)
            matriz.append(nueva_fila)

        # Asegurarse de que el directorio exista
        os.makedirs('levels/creados', exist_ok=True)

        # Crear el archivo si no existe
        if not os.path.exists('levels/creados/levels.json'):
            with open('levels/creados/levels.json', 'w') as file:
                json.dump([], file)     
        
        with open('./levels/creados/levels.json') as file:
            try:
                data = list(json.load(file))
            except:
                data = []
            nivel = {
                "nombre": self.nivel.id,
                "matriz": matriz,
                "contrarreloj": 60
            }
            
            data.append(nivel)
            try:
                with open('./levels/creados/levels.json', 'w') as file:
                    json.dump(data, file)
            except:
                print("Error al guardar el nivel.")
        self.running = False
        self.menu.volver_al_menu()

class Firework:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.particles = []
        self.create_particles()

    def create_particles(self):
        for _ in range(100):
            size = random.randint(2, 5)
            color = random.choice([pygame.Color('purple'), pygame.Color('pink'), pygame.Color('blue'), pygame.Color('cyan')])
            speed_x = random.uniform(-2, 2)
            speed_y = random.uniform(-2, 2)
            self.particles.append([self.x, self.y, size, color, speed_x, speed_y])

    def update(self):
        for particle in self.particles:
            particle[0] += particle[4]
            particle[1] += particle[5]
            particle[5] += 0.1  # Gravity effect

    def draw(self, surface):
        for particle in self.particles:
            pygame.draw.circle(surface, particle[3], (int(particle[0]), int(particle[1])), particle[2])

class Caquita:
    def __init__(self, surface, ancho_ventana, altura_ventana):
        self.surface = surface
        self.ancho_ventana = ancho_ventana
        self.altura_ventana = altura_ventana
        self.caras = []
        self.imagen_caquita = pygame.image.load("resources/caquita/caquita.png")
        self.imagen_caquita = pygame.transform.scale(self.imagen_caquita, (60, 60))  # Ajusta el tamaño según sea necesario
        self.crear_caras()

    def crear_caras(self):
        filas = 5
        columnas = 6
        for  i in range(filas): 
            x = i * self.ancho_ventana // filas
            for j in range(columnas): 
                y = j * self.altura_ventana // columnas
                self.caras.append((x, y))

    def dibujar_caquita(self, x, y):
        self.surface.blit(self.imagen_caquita, (x, y))
    def mostrar_animacion(self):
        for _ in range(60):  # Duración de la animación
            for x, y in self.caras:
                self.dibujar_caquita(x, y)
            pygame.display.flip()
            pygame.time.wait(30)  # Espera un poco para crear el efecto de animación
