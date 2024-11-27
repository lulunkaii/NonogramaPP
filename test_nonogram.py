import pytest, pygame
from mecanicas import Estadisticas
from menu import Boton

# Verifica el funcionamiento del boton
def test_boton_click():
    result = []

    def accion():
        result.append(1)

    boton = Boton("Test", (0, 0), (100, 50), None, accion)

    boton.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (10, 10), "button": 1}))
    assert len(result) == 1  # Verifica que la acción se haya ejecutado

# Verifica el funcionamiento de iniciar la partida
def test_actualizar_estadisticas():
    estadisticas = Estadisticas()
    estadisticas.actualizar(1, 2, 3)

    assert estadisticas.segundos_jugados == 1
    assert estadisticas.cant_niveles_superados == 2
    assert estadisticas.puntuacion_total == 3
    
if __name__ == '__main__':
    pytest.main()