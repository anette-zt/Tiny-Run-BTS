import pygame
import random

# --- 1. Inicialización y Configuración de la Ventana ---
pygame.init()

# Definimos el tamaño de la ventana
ANCHO_VENTANA = 800
ALTO_VENTANA = 600
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Tiny Run BTS")

# Definimos colores (en formato RGB)
COLOR_FONDO = (135, 206, 235) # Un azul cielo
COLOR_SUELO = (0, 100, 0)      # Verde oscuro
COLOR_V = (128, 0, 128)      # Morado (¡Borahae!)
COLOR_OBSTACULO = (255, 0, 0)  # Rojo

# Control para los FPS (Frames Per Second)
reloj = pygame.time.Clock()

# --- 2. Variables del Jugador (TinyTAN V) ---
# Usaremos un rectángulo simple por ahora
v_ancho = 40
v_alto = 60
# Posición inicial (x, y)
v_x = 100
v_y = ALTO_VENTANA - v_alto - 50 # 50 es la altura del suelo

# Variables para la física del salto
v_velocidad_y = 0
gravedad = 1
fuerza_salto = -20 # Negativo es hacia arriba
esta_en_el_suelo = True

# Creamos el rectángulo para el suelo
suelo = pygame.Rect(0, ALTO_VENTANA - 50, ANCHO_VENTANA, 50)

# --- 3. Variables del Juego (Obstáculos) ---
obstaculos = [] # Una lista para guardar todos los obstáculos en pantalla
velocidad_juego = 8

# Creamos un "evento" personalizado para generar obstáculos
GENERAR_OBSTACULO = pygame.USEREVENT + 1
# Le decimos a Pygame que "active" este evento cada 1.5 segundos (1500 milisegundos)
pygame.time.set_timer(GENERAR_OBSTACULO, 1500)

# --- 4. El Bucle Principal del Juego ---
jugando = True
while jugando:
    
    # --- 5. Manejo de Eventos (Inputs del jugador) ---
    for evento in pygame.event.get():
        # Evento: Si el jugador cierra la ventana
        if evento.type == pygame.QUIT:
            jugando = False
            
        # Evento: Si el jugador presiona una tecla
        if evento.type == pygame.KEYDOWN:
            # Si presiona 'W' O 'Espacio' Y está en el suelo
            if (evento.key == pygame.K_w or evento.key == pygame.K_SPACE) and esta_en_el_suelo:
                v_velocidad_y = fuerza_salto # Aplica la fuerza de salto
                esta_en_el_suelo = False # Ya no está en el suelo
                
        # Evento: Si es nuestro evento personalizado de generar obstáculo
        if evento.type == GENERAR_OBSTACULO:
            # Crea un nuevo obstáculo fuera de la pantalla (a la derecha)
            nuevo_obstaculo = pygame.Rect(ANCHO_VENTANA, ALTO_VENTANA - 50 - 30, 30, 30)
            obstaculos.append(nuevo_obstaculo)

    # --- 6. Actualización de la Lógica del Juego ---
    
    # Aplicar gravedad
    if not esta_en_el_suelo:
        v_velocidad_y += gravedad
        v_y += v_velocidad_y

    # Creamos el Rect del jugador en su posición actual
    v_rect = pygame.Rect(v_x, v_y, v_ancho, v_alto)

    # Colisión con el suelo
    if v_rect.colliderect(suelo):
        v_y = suelo.top - v_alto # Pone a V justo encima del suelo
        v_velocidad_y = 0
        esta_en_el_suelo = True

    # Mover los obstáculos
    for obstaculo in obstaculos:
        obstaculo.x -= velocidad_juego
        # Chequear colisión con el jugador
        if v_rect.colliderect(obstaculo):
            print("¡Juego terminado!")
            jugando = False
            
    # Limpiar obstáculos que ya salieron de la pantalla
    obstaculos = [obs for obs in obstaculos if obs.x > -50]


    # --- 7. Dibujar todo en la pantalla ---
    
    # 1. Dibuja el fondo
    ventana.fill(COLOR_FONDO)
    
    # 2. Dibuja el suelo
    pygame.draw.rect(ventana, COLOR_SUELO, suelo)
    
    # 3. Dibuja al jugador (nuestro rectángulo morado)
    pygame.draw.rect(ventana, COLOR_V, v_rect)
    
    # 4. Dibuja todos los obstáculos
    for obstaculo in obstaculos:
        pygame.draw.rect(ventana, COLOR_OBSTACULO, obstaculo)
    
    # Actualiza la pantalla para mostrar lo que dibujamos
    pygame.display.flip()
    
    # Controla que el juego corra a 60 FPS
    reloj.tick(60)

# --- 8. Fin del Juego ---
pygame.quit()