import pygame
from menu import Menu
from utils import SettingsManager

# Evaluar si es conveniente fusionar este boton con el genérico
# Ventajas de la fusión: Reutilización de código
# Desventajas de la fusión: Aumento de complejidad, funcionalidades específicas

class BotonSeleccionNivel:
    def __init__(self, x, y, action=None, win=False):
        self.x = x
        self.y = y

        # Carga de imagenes
        self.imagen_boton_undone = pygame.transform.scale(pygame.image.load('resources/button/undone.png'), (100, 100))
        self.imagen_boton_done = pygame.transform.scale(pygame.image.load('resources/button/done.png'), (100, 100))
        self.imagen_boton_done_active = pygame.transform.scale(pygame.image.load('resources/button/done_active.png'), (100, 100))
        self.imagen_boton_undone_active = pygame.transform.scale(pygame.image.load('resources/button/undone_active.png'), (100, 100))

        self.imagen_actual = self.imagen_boton_undone
        self.rect = self.imagen_boton_undone.get_rect(topleft=(x, y))
        self.action = action
        self.selected = False
        self.win = win

        # Animación del botón cuando se gana por primera vez
        self.animacion_index = 0
        self.animacion_tiempo = 0
        self.animacion_win_completada = False
        self.frames_boton_win = []
        self.frame_index_boton_win = 0
        for i in range(1,18):
            img = pygame.image.load("resources/button/win_button/win_"+str(i)+".png")
            img = pygame.transform.scale(img, (100, 100))
            self.frames_boton_win.append(img)    

    def draw(self, screen):
        if self.win and not self.animacion_win_completada:
            self.win_animation()
            self.imagen_actual = self.frames_boton_win[self.animacion_index]
        elif self.win:
            self.imagen_actual = self.imagen_boton_done_active if self.selected else self.imagen_boton_done
        else:
            self.imagen_actual = self.imagen_boton_undone_active if self.selected else self.imagen_boton_undone
        screen.blit(self.imagen_actual, self.rect.topleft)

    def set_selected(self, selected):
        self.selected = selected

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            if self.action:
                self.action()
            return True
        return False
    
    def check_hover(self, pos):
        return self.rect.collidepoint(pos)
    
    def set_win_true(self):
        self.win = True

    def win_animation(self):
        self.animacion_tiempo += 1
        if self.animacion_tiempo >= 5:
            self.animacion_tiempo = 0
            self.animacion_index += 1
            if self.animacion_index >= len(self.frames_boton_win):
                self.animacion_index = len(self.frames_boton_win) - 1
                self.animacion_win_completada = True


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    botones = [
        BotonSeleccionNivel(100, 100),
        BotonSeleccionNivel(100, 200),
        BotonSeleccionNivel(100, 300)
    ]

    selected_index = 0
    botones[selected_index].set_selected(True)
    nivel_completado= True
    if nivel_completado:
        botones[0].set_win_true()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    botones[selected_index].set_selected(False)
                    selected_index = (selected_index + 1) % len(botones)
                    botones[selected_index].set_selected(True)
                elif event.key == pygame.K_UP:
                    botones[selected_index].set_selected(False)
                    selected_index = (selected_index - 1) % len(botones)
                    botones[selected_index].set_selected(True)
            elif event.type == pygame.MOUSEMOTION:
                for i, boton in enumerate(botones):
                    if boton.check_hover(event.pos):
                        botones[selected_index].set_selected(False)
                        selected_index = i
                        botones[selected_index].set_selected(True)
                        break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    for i, boton in enumerate(botones):
                        if boton.check_click(event.pos):
                            # Aquí puedes agregar la acción para entrar al nivel
                            print(f"Botón {i} clickeado")
                            break

        screen.fill((0, 0, 0))
        for boton in botones:
            boton.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()