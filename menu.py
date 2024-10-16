import pygame
import os
from mecanicas import Partida, Nivel
from utils import SettingsManager

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

if __name__ == "__main__":
    menu = Menu()
    menu.iniciar_menu()