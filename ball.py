import pygame
import math
import time
import sys

# Dimensiones de la ventana
WIDTH, HEIGHT = 800, 600

# Colores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0,0,0)

posi = []

# Inicialización de Pygame
pygame.init()

def colision_circulos(jugador):
    
    y1 = jugador['ball_y']
    x1 = jugador['ball_x']
    r1 = jugador['ball_radius']
    r2 = r1
    x2 = jugador['target_x']
    y2 = jugador['target_y']
   
    distancia = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    if distancia < r1 + r2:
          return True
    else:
        return False
    
# Configuración de la ventana
def configurar_ventana(width, height):
    return pygame.display.set_mode((width, height))

# Función para reiniciar el juego para un jugador
def reiniciar_juego(jugador):
    jugador['ball_x'] = 50 if jugador['numero'] == 1 else WIDTH - 50
    jugador['ball_y'] = HEIGHT - 50
    jugador['angle_degrees'] = 45
    jugador['angle_radians'] = math.radians(jugador['angle_degrees'])
    jugador['initial_speed'] = 30
    jugador['gravity'] = 0.5
    jugador['pressed_enter'] = False
    jugador['show_line'] = True
    jugador['ball_stopped'] = False

# Dibuja la pantalla del juego
def dibujar_pantalla(screen, jugador, posi = []):
    screen.fill(WHITE)

    if jugador['show_line']:
        line_length = 20
        line_end_x = jugador['ball_x'] + line_length * math.cos(jugador['angle_radians'])
        line_end_y = jugador['ball_y'] - line_length * math.sin(jugador['angle_radians'])
        pygame.draw.line(screen, RED, (jugador['ball_x'], jugador['ball_y']), (line_end_x, line_end_y), 2)
    
        # Mostrar velocidad inicial cerca de la pelota
        font = pygame.font.Font(None, 20)
        speed_text = font.render(f"Velocidad: {int(jugador['initial_speed'])}", True, BLACK)
        speed_text_rect = speed_text.get_rect(center=(jugador['ball_x'], jugador['ball_y'] + 20))
        screen.blit(speed_text, speed_text_rect)
    else:
        for ball in posi:
            pygame.draw.circle(screen, BLUE, (int(ball[0]), int(ball[1])), 2)

    pygame.draw.circle(screen, BLUE, (int(jugador['ball_x']), int(jugador['ball_y'])), jugador['ball_radius'])
    pygame.draw.circle(screen, RED, (int(jugador['target_x']), int(jugador['target_y'])), jugador['ball_radius'])


    font = pygame.font.Font(None, 36)
    text = font.render(f"Jugador {jugador['numero']}", True, BLUE)
    text_rect = text.get_rect(center=(WIDTH // 2, 50))
    screen.blit(text, text_rect)

    pygame.display.flip()

# Función principal del juego
def jugar_juego():
    # Configuración de jugadores
    jugador1 = {
        'numero': 1,
        'ball_radius': 10,
        'ball_x': 50,
        'ball_y': HEIGHT - 50,
        'angle_degrees': 45,
        'angle_radians': math.radians(45),
        'initial_speed': 30,
        'gravity': 0.5,
        'pressed_enter': False,
        'show_line': True,
        'ball_stopped': False,
        'current': True,
        'target_x': WIDTH - 50,
        'target_y': HEIGHT - 50
    }

    jugador2 = {
        'numero': 2,
        'ball_radius': 10,
        'ball_x': WIDTH - 50,
        'ball_y': HEIGHT - 50,
        'angle_degrees': 135,
        'angle_radians': math.radians(45),
        'initial_speed': 30,
        'gravity': 0.5,
        'pressed_enter': False,
        'show_line': True,
        'ball_stopped': False,
        'current': False,
        'target_x':  50,
        'target_y': HEIGHT - 50
    }

    jugadores = [jugador1, jugador2]
    screen = configurar_ventana(WIDTH, HEIGHT)
    pygame.display.set_caption("Movimiento Parabólico")

    reiniciar_juego(jugador1)
    reiniciar_juego(jugador2)

    # Tiempo para mostrar la línea de inicio (en segundos)
    start_line_duration = 3.0  # Cambia este valor según tus preferencias

    # Marca el tiempo de inicio
    start_time = time.time()
    posi = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Solo el jugador actual procesa eventos de teclado
        jugador_actual = jugadores[0] if jugadores[0]['current'] else jugadores[1]
        keys = pygame.key.get_pressed()
        if not jugador_actual['ball_stopped']:
            if keys[pygame.K_RETURN] and not jugador_actual['pressed_enter']:
                # Si se presiona Enter y el movimiento no ha comenzado
                posi = []
                jugador_actual['pressed_enter'] = True
                jugador_actual['angle_radians'] = math.radians(jugador_actual['angle_degrees'])
                jugador_actual['initial_speed_x'] = jugador_actual['initial_speed'] * math.cos(jugador_actual['angle_radians'])
                jugador_actual['initial_speed_y'] = -jugador_actual['initial_speed'] * math.sin(jugador_actual['angle_radians'])
            elif keys[pygame.K_DOWN]:
                # Reduce el ángulo de disparo
                jugador_actual['angle_degrees'] -= 2
                jugador_actual['angle_radians'] = math.radians(jugador_actual['angle_degrees'])
            elif keys[pygame.K_UP]:
                # Aumenta el ángulo de disparo
                jugador_actual['angle_degrees'] += 2
                jugador_actual['angle_radians'] = math.radians(jugador_actual['angle_degrees'])
            elif keys[pygame.K_LEFT]:
                jugador_actual['initial_speed'] += 1
            elif keys[pygame.K_RIGHT]:
                jugador_actual['initial_speed'] -= 1


        if jugador_actual['pressed_enter'] and not jugador_actual['ball_stopped']:
            # Actualiza la posición de la pelota en función del tiempo si se ha presionado Enter
            jugador_actual['show_line'] = False
            jugador_actual['ball_x'] += jugador_actual['initial_speed_x']
            jugador_actual['ball_y'] += jugador_actual['initial_speed_y']
            try:
                if jugador_actual['pressed_enter']:
                    posi.append((jugador_actual['ball_x'],jugador_actual['ball_y']))
            except:
                pass

            # Aplica gravedad
            jugador_actual['initial_speed_y'] += jugador_actual['gravity']

            # Verifica si la pelota ha colisionado con el suelo
            if colision_circulos(jugador_actual):
                font = pygame.font.Font(None, 36)
                text = font.render(f"Jugador {jugador_actual['numero']} Gana el juego", True, BLUE)
                text_rect = text.get_rect(center=(WIDTH // 2, 50))
                screen.blit(text, text_rect)
                time.sleep(2)
                sys.exit()

                pygame.display.flip()
            if jugador_actual['ball_y'] >= HEIGHT - jugador_actual['ball_radius']:
                print(f"La pelota del jugador {jugador_actual['numero']} ha alcanzado el suelo.")
                time.sleep(0.5)  # Espera 2 segundos antes de reiniciar el juego
                reiniciar_juego(jugador_actual)
                # Cambiar al otro jugador
                if jugador_actual['numero'] == 1:
                    jugadores[0]['current'] = False
                    jugadores[1]['current'] = True
                if jugador_actual['numero'] == 2:
                    jugadores[1]['current'] = False
                    jugadores[0]['current'] = True

                

        # Dibuja la pantalla solo para el jugador actual
        dibujar_pantalla(screen, jugador_actual, posi)

        # Agrega un pequeño retraso para ralentizar la visualización
        time.sleep(0.02)  # Ajusta el valor según la velocidad deseada

if __name__ == "__main__":
    jugar_juego()

