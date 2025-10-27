# --- tiny_run.py ---
import pygame

# Importamos las clases de nuestros otros archivos
from personajes      import Jugador
from escenarios import Escenario
from musica import GestorMusica

# --- 1. Inicialización y Configuración ---
pygame.init()
pygame.font.init() # ¡¡NUEVO!! Inicializamos el módulo de fuentes
pygame.mixer.init()

# Constantes de la ventana
ANCHO_VENTANA = 800
ALTO_VENTANA = 600
FPS = 60

# Creamos la ventana
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Tiny Run BTS")
reloj = pygame.time.Clock()

# --- ¡¡NUEVO!! Definición de Estados del Juego ---
ESTADO_MENU = "menu_principal"
ESTADO_JUGANDO = "jugando"
ESTADO_GAME_OVER = "game_over"

# Empezamos en el menú principal
estado_actual = ESTADO_MENU

# --- ¡¡NUEVO!! Variables para el Menú ---
# Usaremos 'None' para crear las variables, pero las iniciaremos
# solo cuando el jugador presione "Jugar".
jugador = None
escenario = None

# Fuentes para el texto
fuente_titulo = pygame.font.SysFont('Arial', 60)
fuente_menu = pygame.font.SysFont('Arial', 40)

# Colores
COLOR_TEXTO = (255, 255, 255)
COLOR_FONDO_MENU = (30, 30, 30)

# Botones (como rectángulos invisibles para detectar clics)
boton_jugar_rect = pygame.Rect(300, 250, 200, 50)


# --- 2. Definición de Eventos Personalizados ---
EVENTO_GENERAR_OBSTACULO = pygame.USEREVENT + 1
EVENTO_FIN_MUSICA = pygame.USEREVENT + 2

# --- 3. Creación de Objetos (Instancias) ---
# ¡¡IMPORTANTE!! No creamos al jugador ni al escenario aquí
# Lo haremos cuando el jugador presione "Jugar"

# Gestor de música (puede empezar a sonar en el menú)
gestor_musica = GestorMusica(music_end_event=EVENTO_FIN_MUSICA)
gestor_musica.cargar_y_reproducir()


# --- ¡¡NUEVO!! Función para iniciar el juego ---
def iniciar_juego():
    """Crea los objetos del juego y cambia el estado a "JUGANDO"."""
    global jugador, escenario, estado_actual
    
    # ¡¡Aquí es donde creamos al jugador y escenario!!
    jugador = Jugador(100, ALTO_VENTANA - 50 - 60)
    escenario = Escenario(ANCHO_VENTANA, ALTO_VENTANA)
    
    # Re-asignamos y activamos el timer de obstáculos
    escenario.GENERAR_OBSTACULO = EVENTO_GENERAR_OBSTACULO
    pygame.time.set_timer(escenario.GENERAR_OBSTACULO, 1500)
    
    # Cambiamos el estado
    estado_actual = ESTADO_JUGANDO


# --- 4. El Bucle Principal del Juego ---
en_ejecucion = True # Cambiamos 'jugando' por 'en_ejecucion'
while en_ejecucion:
    
    # --- 5. Manejo de Eventos (Inputs) ---
    for evento in pygame.event.get():
        # Evento: Salir del juego (funciona en todos los estados)
        if evento.type == pygame.QUIT:
            en_ejecucion = False
            
        # Evento: La canción terminó (funciona en todos los estados)
        if evento.type == gestor_musica.MUSIC_END_EVENT:
            gestor_musica.reproducir_siguiente_cancion()

        # --- A. Eventos del ESTADO_MENU ---
        if estado_actual == ESTADO_MENU:
            # Si el jugador hace clic
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Comprobamos si el clic fue DENTRO del rectángulo del botón
                if boton_jugar_rect.collidepoint(evento.pos):
                    iniciar_juego() # ¡Empezamos el juego!

        # --- B. Eventos del ESTADO_JUGANDO ---
        elif estado_actual == ESTADO_JUGANDO:
            # Presionar tecla para saltar
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_w or evento.key == pygame.K_SPACE:
                    jugador.saltar()
            
            # Generar un obstáculo
            if evento.type == escenario.GENERAR_OBSTACULO:
                escenario.generar_obstaculo()

    
    # --- 6. Actualización de la Lógica (Update) ---
    
    if estado_actual == ESTADO_JUGANDO:
        # Actualiza la física del jugador
        jugador.update(escenario.suelo_rect)
        
        # Mueve los obstáculos
        escenario.update()
        
        # Comprobar si perdimos
        if escenario.check_colision(jugador.rect):
            print("¡Juego terminado!")
            # (Aquí podríamos cambiar a ESTADO_GAME_OVER)
            en_ejecucion = False # Por ahora, solo salimos del juego

    
    # --- 7. Dibujar en Pantalla (Render) ---
    
    if estado_actual == ESTADO_MENU:
        ventana.fill(COLOR_FONDO_MENU)
        
        # Dibujar título
        texto_titulo = fuente_titulo.render("Tiny Run BTS", True, COLOR_TEXTO)
        ventana.blit(texto_titulo, (ANCHO_VENTANA/2 - texto_titulo.get_width()/2, 100))
        
        # Dibujar botón
        pygame.draw.rect(ventana, (0, 100, 0), boton_jugar_rect) # Dibuja el fondo del botón
        texto_jugar = fuente_menu.render("Jugar", True, COLOR_TEXTO)
        ventana.blit(texto_jugar, (boton_jugar_rect.x + 50, boton_jugar_rect.y + 5))

    elif estado_actual == ESTADO_JUGANDO:
        # Dibuja el escenario (fondo, suelo, obstáculos)
        escenario.dibujar(ventana)
        
        # Dibuja al jugador
        jugador.dibujar(ventana)
    
    
    # Actualiza la pantalla completa
    pygame.display.flip()
    
    # Controla la velocidad del juego
    reloj.tick(FPS)

# --- 8. Fin del Juego ---
pygame.quit()