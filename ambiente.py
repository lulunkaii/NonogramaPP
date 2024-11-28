import pygame
from enum import Enum

class AmbienteEnum(Enum):
    """
    Representa los posibles ambientes del juego.
    
    Attributes:
        INVIERNO: Ambiente de invierno.
        MONTAÑA: Ambiente de montaña.
        PRADO: Ambiente de prado.
    """
    pos_botones = []
    INVIERNO = "invierno"
    MONTAÑA = "montaña"
    PRADO = "prado"

class Ambiente:
    """
    Representa un ambiente del juego.
    
    Attributes:
        tipo (AmbienteEnum): Tipo de ambiente.
        fondo (Surface): Imagen de fondo.
        musica (str): Direccion archivo de música.
        niveles (List(Nivel)): Niveles del ambiente.
    """
    def __init__(self, tipo: AmbienteEnum, fondo, musica, niveles):
        """
        Crea un ambiente.
        Args:
            tipo (AmbienteEnum): Tipo de ambiente.
            fondo (Surface): Imagen de fondo.
            musica (str): Archivo de música.
            niveles (List(Nivel)): Niveles del ambiente.
        """
        self.tipo = tipo
        self.fondo = pygame.image.load(fondo)
        self.musica = musica
        self.niveles = niveles
        self.pos_botones = []

    def get_pos_botones(self):
        if self.tipo == AmbienteEnum.INVIERNO:
            return [
                (15, 470),
                (67, 525),
                (162, 502),
                (245, 540),
                (341, 510),
                (420, 540),
                (283, 455),
                (387, 464),
                (495, 483),
                (470, 510),
                (453, 330)
            ]

    def cargar_musica(self, volumen=0.1):  
        """
        Carga y reproduce la música del ambiente.

        Args:
            volumen (float, optional): Volumen para la musica. Defaults to 0.1.
        """
        try:
            pygame.mixer.music.load(self.musica)
            pygame.mixer.music.set_volume(volumen)  
            pygame.mixer.music.play(-1)  
        except pygame.error as e:
            print(f"Error al cargar la música: {e}")

    def get_fondo(self):
        return self.fondo

    def get_niveles(self):
        return self.niveles
    
    def get_tipo(self):
        return self.tipo
    