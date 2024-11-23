import pygame
from menu import Menu
from utils import BotonSeleccionNivel
import ambiente as amb
import os
from mecanicas import Nivel

# Evaluar si es conveniente fusionar este boton con el genérico
# Ventajas de la fusión: Reutilización de código
# Desventajas de la fusión: Aumento de complejidad, funcionalidades específicas

pygame.mixer.init()
sonido_seleccion = pygame.mixer.Sound("resources/sounds/seleccion.wav")
sonido_presion = pygame.mixer.Sound("resources/sounds/presion.wav")


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
        carpeta_niveles = './levels/snow'
        archivos_niveles = [f for f in os.listdir(carpeta_niveles) if os.path.isfile(os.path.join(carpeta_niveles, f))]

        # Crear niveles
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
                        
                self.niveles.append(Nivel(matriz, "test"))

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
