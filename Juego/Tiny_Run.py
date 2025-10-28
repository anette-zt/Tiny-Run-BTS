# --- Tiny_Run.py ---

# ... (importaciones y configuración inicial) ...
import pygame
pygame.init()

ANCHO_VENTANA = 800
ALTO_VENTANA = 600

# Ventana, reloj y FPS mínimos necesarios por el resto del código
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
reloj = pygame.time.Clock()
FPS = 60

# Estado del bucle principal
en_ejecucion = True

# Estados del juego
ESTADO_MENU = 0
ESTADO_JUGANDO = 1
ESTADO_PAUSADO = 2
ESTADO_GAMEOVER = 3

# Estado actual por defecto (asegura que la variable existe antes del bucle principal)
estado_actual = ESTADO_MENU

# Definición del mapa nivel 1 (ejemplo básico)
mapa_nivel_1 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "X                       X",
    "X                       X",
    "X         P            X",
    "XXXXXXXXXXXXXXXXXXXXXXXXX"
]

# ¡NUEVO! Variable para la cámara
camera_x = 0

# --- Función iniciar_juego() Modificada ---
def iniciar_juego():
    global jugador, escenario, estado_actual, personaje_elegido, nivel_elegido, camera_x
    
    jugador = jugador(100, ALTO_VENTANA - 150, personaje_elegido)
    
    # ¡NUEVO! Eliges el mapa basado en la selección
    mapa_elegido = []
    if nivel_elegido == "IDOL.jpg":
        mapa_elegido = mapa_nivel_1 # (La variable que definimos arriba)
    # else:
    #     mapa_elegido = mapa_nivel_2
        
    escenario = escenario(nivel_elegido, mapa_elegido)
    
    # ¡YA NO HAY TIMER DE OBSTÁCULOS!
    # pygame.time.set_timer(escenario.GENERAR_OBSTACULO, 0) # Lo desactivamos
    
    camera_x = 0 # Reseteamos la cámara
    estado_actual = ESTADO_JUGANDO

# --- Bucle Principal ---
while en_ejecucion:
    # --- 5. Manejo de Eventos ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            en_ejecucion = False

        # Manejo de eventos sólo cuando estamos jugando
        elif estado_actual == ESTADO_JUGANDO:
            # ¡YA NO HAY EVENTO DE GENERAR OBSTÁCULOS!
            # Presionar tecla para saltar
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_w or evento.key == pygame.K_SPACE:
                    jugador.saltar()

    # ¡NUEVO! Manejo de teclas presionadas (fuera del bucle de eventos)
    # Esto permite que el jugador se mueva si dejas la tecla presionada
    if estado_actual == ESTADO_JUGANDO:
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_d]:
            jugador.mover(1)  # Mover derecha
        if teclas[pygame.K_a]:
            jugador.mover(-1)  # Mover izquierda

        # --- 6. Actualización de Lógica (ESTADO_JUGANDO) ---
        # 1. Actualiza al jugador (gravedad)
        jugador.update()

        # 2. El escenario revisa las colisiones
        escenario.update_colisiones_jugador(jugador)

        # 3. ¡ACTUALIZAR LA CÁMARA!
        # Hacemos que la cámara siga al jugador
        # El '200' es un 'margen' para que el jugador no esté pegado al borde
        camera_x = jugador.rect.x - 200

        # Opcional: Evitar que la cámara se vaya "hacia atrás" al inicio
        if camera_x < 0:
            camera_x = 0

        # --- 7. Dibujar en Pantalla (ESTADO_JUGANDO) ---
        # 1. Dibuja el escenario (pasándole la cámara)
        escenario.dibujar(ventana, camera_x)

        # 2. Dibuja al jugador (restando la cámara)
        # El jugador ahora SÍ se mueve en X, así que debemos restarle
        # la posición de la cámara para que se dibuje en el lugar correcto
        # de la pantalla.
        rect_jugador_en_pantalla = jugador.rect.copy()
        rect_jugador_en_pantalla.x -= camera_x

        # (Aquí dibujarías la IMAGEN del jugador)
        pygame.draw.rect(ventana, jugador.color, rect_jugador_en_pantalla)

    # Puedes agregar otros estados (MENÚ, PAUSADO, GAMEOVER) aquí con elif estado_actual == ...

    pygame.display.flip()
    reloj.tick(FPS)

# --- 8. Fin ---
pygame.quit()