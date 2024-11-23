import pygame, os, json
from mecanicas import Partida, Nivel, Celda
from utils import SettingsManager, colorCelda, Boton
import menu_seleccion

# Carga de sonidos
pygame.mixer.init()
sonido_seleccion = pygame.mixer.Sound("resources/sounds/seleccion.wav")
sonido_presion = pygame.mixer.Sound("resources/sounds/presion.wav")

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
        self.boton_crear_nivel = None
        self.partida_en_curso = None
        self.menu_seleccion_nivel = menu_seleccion.MenuSeleccionNivel(self)  # Instancia del menú de selección de niveles
        self.menu_crear_nivel = MenuCrearNivel(self)  # Instancia del menú de creación de niveles
        self.menu_cargar_partida = MenuCargarNivel(self)
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
        self.window = pygame.display.set_mode((500, 600))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Trebuchet MS", 20)

        self.boton_jugar = Boton("Seleccionar Nivel", (150, 175), (200, 50), self.font, self.ir_a_seleccion_nivel)
        self.boton_cargar = Boton("Cargar Partida", (150, 235), (200, 50), self.font, self.cargar_partida)
        self.boton_crear_nivel = Boton("Crear Nivel", (150, 295), (200, 50), self.font, self.crear_nivel)
        self.boton_estadisticas = Boton("Ver Estadísticas", (150, 355), (200, 50), self.font, self.ver_estadisticas)
        self.boton_opciones = Boton("Opciones", (150, 415), (200, 50), self.font, self.opciones)
        self.boton_salir = Boton("Salir", (150, 475), (200, 50), self.font, self.salir)

        self.botones = [self.boton_jugar, self.boton_cargar, self.boton_crear_nivel, self.boton_estadisticas, self.boton_opciones, self.boton_salir]
    
    def ir_a_seleccion_nivel(self):
        self.cerrar_menu()
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
        self.clock.tick(144)
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
        self.cerrar_menu()
        pass

    def cargar_partida(self):
        self.cerrar_menu()
        self.menu_cargar_partida.run_menu()

    def opciones(self):
        pass

    def salir(self):
        self.cerrar_menu()

    def volver_al_menu(self):
        self.iniciar_menu()

    def crear_nivel(self):
        self.cerrar_menu()
        self.menu_crear_nivel.iniciar_menu()

    def crear_nuevo_nivel(self):
        nivel_vacio = Nivel([[0] * SettingsManager.GRID_SIZE.value for _ in range(SettingsManager.GRID_SIZE.value)])
        self.partida_en_curso = CrearNivel(nivel_vacio, self)
        self.partida_en_curso.run()

    def jugar_nivel_creado(self):
        # Implementar la lógica para jugar un nivel creado
        self.cerrar_menu() # Para que no se creen botones superpuestos

    def cerrar_menu(self):
        self.running = False
        self.botones = []
        self.boton_jugar = None
        self.boton_cargar = None
        self.boton_estadisticas = None
        self.boton_opciones = None
        self.boton_salir = None
        self.boton_crear_nivel = None

class MenuCargarNivel():
    def __init__(self, menu_principal):
        self.menu = menu_principal
        self.running = False
        self.window = pygame.display.set_mode((600, 600))
        self.clock = pygame.time.Clock()
        self.levels = []
        self.boards = []
        self.levels_buttons = []
        self.boton_volver = None
        self.scroll_offset = 0
        self.scroll_speed = 20
        self.font = None

    def iniciar_menu(self):
        pygame.init()
        self.clock.tick(144)
        self.font = pygame.font.SysFont("Trebuchet MS", 20)

        # Obtener niveles 
        carpeta_niveles = "./saved_levels"
        archivos_niveles = [f for f in os.listdir(carpeta_niveles) if os.path.isfile(os.path.join(carpeta_niveles, f))]

        # Crear botones para niveles guardados
        for archivo in archivos_niveles:
            with open(os.path.join(carpeta_niveles, archivo), 'r') as file:
                data = json.load(file)

                board_data = data['board']
                grid_data = data['grid']
                
                board = []
                for i, row in enumerate(board_data):
                    board.append([])
                    for celda in row:
                        if celda == [255, 255, 255]:
                            celda = Celda()
                            celda.click(colorCelda.DEFAULT)
                            board[i].append(celda)
                        elif celda == [0, 0, 0]:
                            celda = Celda()
                            celda.click(colorCelda.BLACK)
                            board[i].append(celda)
                        elif celda == [255, 0 , 0]:
                            celda = Celda()
                            celda.click(colorCelda.RED)
                            board[i].append(celda)
                        elif celda == [0, 255, 0]:
                            celda = Celda()
                            celda.click(colorCelda.GREEN)
                            board[i].append(celda)
                        elif celda == [0, 0, 255]:
                            celda = Celda()
                            celda.click(colorCelda.BLUE)
                            board[i].append(celda)

                nombre = archivo.replace(".json", "")
                self.levels.append([nombre, Nivel(grid_data, "test"), board])

        for i, level in enumerate(self.levels):
            boton = Boton(level[0], (250, 100 + i * 60), (200, 50), self.font, lambda n=level: self.iniciar_partida(n))
            self.levels_buttons.append(boton)

        self.boton_volver = Boton("Volver", (10, 380), (200, 50), self.font, self.volver_al_menu)

    def run_menu(self):
        self.iniciar_menu()
        self.running = True
        while self.running:
            self.dibujar_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:  # Scroll up
                        self.scroll_offset = min(self.scroll_offset + self.scroll_speed, 0)
                    elif event.button == 5:  # Scroll down
                        self.scroll_offset = max(self.scroll_offset - self.scroll_speed, len(self.levels_buttons)*-110 + 930)
                        if(self.scroll_offset>0):
                            self.scroll_offset = 0

                for boton in self.levels_buttons:
                    boton.handle_event(event, self.scroll_offset)
                self.boton_volver.handle_event(event)
                
    def dibujar_menu(self):
        fondo = pygame.transform.scale(self.menu.fondo_imagen, (600, 600))
        self.window.blit(fondo, (0, 0))
        titulo = self.font.render("Seleccionar", True, SettingsManager.TEXT_COLOR.value)
        titulo2 = self.font.render("Nivel", True, SettingsManager.TEXT_COLOR.value)
        self.window.blit(titulo, (50, 100))
        self.window.blit(titulo2, (50, 130))
        
        for boton in self.levels_buttons:
            boton.draw(self.window, self.scroll_offset)
        self.boton_volver.draw(self.window)

        pygame.display.flip()

    def iniciar_partida(self, game):
        partida = Partida(game[1], self.menu, url=game[0])
        partida.cargar(game[2])
        self.cerrar_menu()
        partida.run()

    def volver_al_menu(self):
        self.cerrar_menu()
        self.menu.iniciar_menu()

    def cerrar_menu(self):
        self.running = False
        self.levels = []
        self.boards = []
        self.levels_buttons = []

class CrearNivel(Partida):
    def __init__(self, nivel, menu_principal):
        super().__init__(nivel, menu_principal)
        self.window_height = 500  # Aumentar la altura de la ventana
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.boton_guardar = Boton("Guardar Nivel", (self.window_width // 2 - 100, self.window_height - 60), (240, 50), self.font, self.guardar_nivel)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.board.handle_click(event.pos)
                self.window.fill(SettingsManager.BACKGROUND_COLOR.value)
                self.board.draw(self.window)
                self.boton_guardar.draw(self.window)
                pygame.display.flip()
            self.boton_guardar.handle_event(event)

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.handle_events()

            self.window.fill(SettingsManager.BACKGROUND_COLOR.value)
            self.board.draw(self.window)
            self.boton_guardar.draw(self.window)
            pygame.display.flip()
        pygame.quit()

    def guardar_nivel(self):
        nombre_nivel = input("Ingrese el nombre del nuevo nivel: ")
        matriz = [[1 if celda.get_color() != colorCelda.DEFAULT else 0 for celda in fila] for fila in self.board.get_board()]
        with open(f'./levels/{nombre_nivel}.txt', 'w') as file:
            for fila in matriz:
                file.write(''.join(map(str, fila)) + '\n')
        print(f'Nivel guardado como {nombre_nivel}.txt')
        self.running = False
        self.menu.volver_al_menu()

class MenuCrearNivel(Menu):
    def __init__(self, menu_principal):
        self.menu_principal = menu_principal
        self.boton_crear_nuevo_nivel = None
        self.boton_jugar_nivel_creado = None
        # Lista de botones para seleccionado
        self.botones = []
        self.boton_seleccionado = 0

    def iniciar_pygame(self):
        super().iniciar_pygame()
        self.boton_crear_nuevo_nivel = Boton("Crear Nuevo Nivel", (150, 200), (200, 50), self.font, self.crear_nuevo_nivel)
        self.boton_jugar_nivel_creado = Boton("Jugar Nivel Creado", (150, 260), (200, 50), self.font, self.jugar_nivel_creado)
        self.botones = [self.boton_crear_nuevo_nivel, self.boton_jugar_nivel_creado]

    def dibujar_menu(self):
        self.window.blit(self.menu_principal.fondo_imagen, (0, 0))
        for i, boton in enumerate(self.botones):
            boton.draw(self.window, seleccionado=i == self.boton_seleccionado)  
        pygame.display.flip()
        

    def iniciar_menu(self):
        super().iniciar_menu()

    def crear_nuevo_nivel(self):
        self.running = False
        self.menu_principal.crear_nuevo_nivel()

    def jugar_nivel_creado(self):
        self.running = False
        self.menu_principal.jugar_nivel_creado()

    def volver_al_menu_principal(self):
        self.running = False
        self.menu_principal.iniciar_menu()

if __name__ == "__main__":
    menu = Menu()
    menu.iniciar_menu()