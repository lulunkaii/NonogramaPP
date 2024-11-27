import pygame, json
from mecanicas import Partida, Nivel, Estadisticas, CrearNivel
from utils import SettingsManager, Boton, BotonSeleccionNivel
import ambiente as amb

# Carga de sonidos
pygame.mixer.init()
sonido_seleccion = pygame.mixer.Sound("resources/sounds/seleccion.wav")
sonido_presion = pygame.mixer.Sound("resources/sounds/presion.wav")

class Menu:
    def __init__(self):
        self.running = False
        self.partida_en_curso = None
        self.menu_seleccion_nivel = MenuSeleccionNivel(self)  # Instancia del menú de selección de niveles
        self.menu_crear_nivel = MenuCrearNivel(self)  # Instancia del menú de creación de niveles
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

        self.boton_jugar = Boton("Seleccionar Nivel", (150, 235), (200, 50), self.font, self.ir_a_seleccion_nivel)
        self.boton_crear_nivel = Boton("Crear Nivel", (150, 295), (200, 50), self.font, self.crear_nivel)
        self.boton_estadisticas = Boton("Ver Estadísticas", (150, 355), (200, 50), self.font, self.ver_estadisticas)
        self.boton_opciones = Boton("Opciones", (150, 415), (200, 50), self.font, self.opciones)
        self.boton_salir = Boton("Salir", (150, 475), (200, 50), self.font, self.salir)

        self.botones = [self.boton_jugar, self.boton_crear_nivel, self.boton_estadisticas, self.boton_opciones,self.boton_salir]
        
    def ir_a_seleccion_nivel(self):
        self.cerrar_menu()
        self.menu_seleccion_nivel.iniciar_menu()

    def iniciar_partida(self, nivel):
        partida = Partida(self, nivel)
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
        estadisticas = Estadisticas()
        estadisticas.cargarEstadisticas()
        menu_estadisticas = MenuEstadisticas(self, estadisticas)
        menu_estadisticas.iniciar_menu_estadisticas()

    def opciones(self):
        pass

    def salir(self):
        self.cerrar_menu()

    def volver_al_menu(self):
        self.iniciar_menu()

    def crear_nivel(self):
        self.cerrar_menu()
        self.menu_crear_nivel.iniciar_menu()

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

class MenuSeleccionNivel(Menu):
    def __init__(self, menu_principal):
        self.menu_principal = menu_principal
        self.running = False
        self.window = None
        self.clock = None
        self.niveles = []
        self.botones_niveles = []
        self.boton_seleccionado = 0
        

        self.ambientes = {
            amb.AmbienteEnum.INVIERNO: amb.Ambiente(amb.AmbienteEnum.INVIERNO, "resources/environments/images/snowG.png", "resources/environments/music/invierno.ogg", range(1,10))
        }

        self.ambiente_actual = self.ambientes[amb.AmbienteEnum.INVIERNO]
        self.pos_botones_ambiente_actual = self.ambiente_actual.get_pos_botones()
        self.fondo_imagen = self.ambiente_actual.get_fondo()
        self.ambiente_actual.cargar_musica()

    def iniciar_pygame(self):
        pygame.init()
        self.window = pygame.display.set_mode((600, 600))
        self.clock = pygame.time.Clock()

        # obtener lista de archivos de la carpeta
        archivo_niveles = 'levels/snow/levels.json'
        
        with open(archivo_niveles, 'r') as file:
            data = json.load(file)
        
        for nivel in data:
            self.niveles.append(Nivel(nivel["matriz"], nivel["nombre"]))

        # Crear botones para los niveles
        
        for i, nivel in enumerate(self.niveles):
            x, y = self.pos_botones_ambiente_actual[i]  # Obtener posición del nivel
            boton = BotonSeleccionNivel(x, y, lambda n=nivel: self.iniciar_partida(n), nivel.isCompleted())
            self.botones_niveles.append(boton)

        #self.boton_volver = Boton("Volver", (10, 380), (200, 50), self.font, self.volver_al_menu_principal)
    
    def dibujar_menu(self):
        fondo = pygame.transform.scale(self.ambiente_actual.get_fondo(), (600, 600))
        self.window.blit(fondo, (0, 0))
        
        for boton in self.botones_niveles:
            boton.draw(self.window)
        #self.boton_volver.draw(self.window)

        pygame.display.flip()

    def iniciar_menu(self):
        self.iniciar_pygame()
        self.running = True

        while self.running:
            self.clock.tick(144)
            self.dibujar_menu()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                elif event.type == pygame.MOUSEMOTION:
                    for i, boton in enumerate(self.botones_niveles):
                        if boton.check_hover(event.pos):
                            self.botones_niveles[self.boton_seleccionado].set_selected(False)
                            self.boton_seleccionado = i
                            self.botones_niveles[self.boton_seleccionado].set_selected(True)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.volver_al_menu_principal()
                    elif event.key == pygame.K_RIGHT:
                        self.botones_niveles[self.boton_seleccionado].set_selected(False)
                        self.boton_seleccionado = (self.boton_seleccionado + 1) % len(self.botones_niveles)
                        self.botones_niveles[self.boton_seleccionado].set_selected(True)
                        sonido_seleccion.play()
                    elif event.key == pygame.K_LEFT:
                        self.botones_niveles[self.boton_seleccionado].set_selected(False)
                        self.boton_seleccionado = (self.boton_seleccionado - 1) % len(self.botones_niveles)
                        self.botones_niveles[self.boton_seleccionado].set_selected(True)
                        sonido_seleccion.play()
                    elif event.key == pygame.K_RETURN:
                        self.botones_niveles[self.boton_seleccionado].action()
                        sonido_presion.play()
                for boton in self.botones_niveles:
                    boton.handle_event(event)
            
            self.clock.tick(10)
        pygame.quit()

    def iniciar_partida(self, nivel):
        self.cerrar_menu()
        self.menu_principal.iniciar_partida(nivel)

    def volver_al_menu_principal(self):
        self.cerrar_menu()
        self.menu_principal.iniciar_menu()
    
    def cerrar_menu(self):
        self.running = False
        self.niveles = []
        self.botones_niveles = []

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

    def pedir_nombre_nivel(self):
        input_box = pygame.Rect(60, 300, 400, 50)  
        color_inactivo = (100, 100, 100)
        color_activo = (0, 120, 215)
        color_caja = color_inactivo
        activo = False
        texto = ""
        font = pygame.font.Font(None, 32)

        pedir_nombre = True
        while pedir_nombre:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    # Activar/desactivar caja de entrada
                    if input_box.collidepoint(evento.pos):
                        activo = not activo
                    else:
                        activo = False
                    color_caja = color_activo if activo else color_inactivo
                elif evento.type == pygame.KEYDOWN and activo:
                    if evento.key == pygame.K_RETURN:
                        # Retornar texto ingresado al presionar Enter
                        return texto
                    elif evento.key == pygame.K_BACKSPACE:
                        # Borrar último carácter
                        texto = texto[:-1]
                    else:
                        # Añadir carácter
                        texto += evento.unicode

            # Dibujar la ventana
            self.window.blit(self.menu_principal.fondo_imagen, (0, 0))

            # Dibujar instrucciones
            instrucciones = font.render("Ingresa el nombre del nivel y presiona Enter:", True, (255, 255, 255))
            self.window.blit(instrucciones, (25 , 250))

            # Dibujar la caja de entrada
            pygame.draw.rect(self.window, color_caja, input_box, 2)

            # Dibujar texto en la caja
            texto_renderizado = font.render(texto, True, (255, 255, 255))
            self.window.blit(texto_renderizado, (input_box.x + 5, input_box.y + 10))

            # Actualizar la pantalla
            pygame.display.flip()
            
    def crear_nuevo_nivel(self):
        nombre_nivel = self.pedir_nombre_nivel()
        nivel_vacio = Nivel([[0] * SettingsManager.GRID_SIZE.value for _ in range(SettingsManager.GRID_SIZE.value)], nombre_nivel)
        self.partida_en_curso = CrearNivel(self, nivel_vacio)
        self.partida_en_curso.run()

    def jugar_nivel_creado(self):
        self.running = False
        self.menu_principal.jugar_nivel_creado()

    def volver_al_menu_principal(self):
        self.running = False
        self.menu_principal.iniciar_menu()

class MenuEstadisticas:
    def __init__(self, menu_principal, estadisticas):
        self.menu_principal = menu_principal
        self.estadisticas = estadisticas
        self.running = False
        self.window = None
        self.font = None
        self.boton_volver = None

    def iniciar_pygame(self):
        pygame.init()
        self.window = pygame.display.set_mode((500, 600))
        self.font = pygame.font.SysFont("Trebuchet MS", 20)
        self.boton_volver = Boton("Volver al Menú", (150, 500), (200, 50), self.font, self.volver_al_menu)

    def dibujar_estadisticas(self):
        self.window.fill((0, 0, 0))  # Fondo negro

        texto_titulo = self.font.render("Estadísticas", True, (255, 255, 255))
        self.window.blit(texto_titulo, (150, 50))

        lista_niveles_completados = []

        for nivel in self.estadisticas.getNivelesCompletados():
            if nivel.startswith("level"):
                try:
                    numero_nivel = int(nivel[5:])
                    lista_niveles_completados.append(numero_nivel)
                except:
                    lista_niveles_completados.append(nivel)
            else:
                lista_niveles_completados.append(nivel)
        
        # Mostrar estadísticas
        stats = [
            f"Segundos Jugados: {self.estadisticas.getSegundosJugados()}",
            f"Niveles Superados: {self.estadisticas.getNivelesSuperados()}",
            f"Puntuación Total: {self.estadisticas.getPuntuacionTotal()}",
            f"Niveles Completados: {lista_niveles_completados}",
        ]

        for i, stat in enumerate(stats):
            texto = self.font.render(stat, True, (255, 255, 255))
            self.window.blit(texto, (50, 150 + i * 40))  # Espaciado entre líneas

        # Dibujar botón
        self.boton_volver.draw(self.window)

        pygame.display.flip()

    def iniciar_menu_estadisticas(self):
        self.iniciar_pygame()
        self.running = True

        while self.running:
            self.dibujar_estadisticas()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.boton_volver.action()
                self.boton_volver.handle_event(event)

            pygame.time.Clock().tick(30)

        pygame.quit()

    def volver_al_menu(self):
        self.running = False
        self.menu_principal.iniciar_menu()

if __name__ == "__main__":
    menu = Menu()
    menu.iniciar_menu()