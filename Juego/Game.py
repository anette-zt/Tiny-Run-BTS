# --- tiny_run.py ---
import pygame

# Importamos las clases de nuestros otros archivos
from personajes import Jugador
from escenarios import Escenario
from musica import GestorMusica

# --- 1. Inicialización y Configuración ---
pygame.init() # Inicializa Pygame
pygame.mixer.init() # Inicializa el módulo de sonido

# Constantes de la ventana
ANCHO_VENTANA = 800
ALTO_VENTANA = 600
FPS = 60 # Frames Per Second

# Creamos la ventana
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Tiny Run BTS")
reloj = pygame.time.Clock()

# --- 2. Definición de Eventos Personalizados ---
# Estos deben definirse aquí, en el archivo principal
EVENTO_GENERAR_OBSTACULO = pygame.USEREVENT + 1
EVENTO_FIN_MUSICA = pygame.USEREVENT + 2

# --- 3. Creación de Objetos (Instancias) ---

# Creamos al jugador
# Lo ponemos a 100px del borde izq, y 60px arriba del suelo (que está a 50px del fondo)
jugador = Jugador(100, ALTO_VENTANA - 50 - 60)

# Creamos el escenario
# Le pasamos los eventos que definimos
escenario = Escenario(ANCHO_VENTANA, ALTO_VENTANA)
escenario.GENERAR_OBSTACULO = EVENTO_GENERAR_OBSTACULO # Re-asignamos el evento
pygame.time.set_timer(escenario.GENERAR_OBSTACULO, 1500) # Activamos el timer

# Creamos el gestor de música
gestor_musica = GestorMusica(music_end_event=EVENTO_FIN_MUSICA)
gestor_musica.cargar_y_reproducir()


# --- 4. El Bucle Principal del Juego ---
jugando = True
while jugando:
    
    # --- 5. Manejo de Eventos (Inputs) ---
    for evento in pygame.event.get():
        # Evento: Salir del juego
        if evento.type == pygame.QUIT:
            jugando = False
            
        # Evento: Presionar una tecla
        if evento.type == pygame.KEYDOWN:
            # Si presiona 'W' O 'Espacio'
            if evento.key == pygame.K_w or evento.key == pygame.K_SPACE:
                jugador.saltar() # Llama al método de la clase Jugador
                
        # Evento: Generar un obstáculo
        if evento.type == escenario.GENERAR_OBSTACULO:
            escenario.generar_obstaculo() # Llama al método de la clase Escenario
            
        # Evento: La canción terminó
        if evento.type == gestor_musica.MUSIC_END_EVENT:
            gestor_musica.reproducir_siguiente_cancion()

    # --- 6. Actualización de la Lógica (Update) ---
    # (Lo que pasa en cada frame sin importar los inputs)
    
    # Actualiza la física del jugador (gravedad, colisión con suelo)
    jugador.update(escenario.suelo_rect)
    
    # Mueve los obstáculos
    escenario.update()
    
    # Comprobar si perdimos
    if escenario.check_colision(jugador.rect):
        print("¡Juego terminado!")
        jugando = False

    # --- 7. Dibujar en Pantalla (Render) ---
    
    # 1. Dibuja el escenario (fondo, suelo, obstáculos)
    escenario.dibujar(ventana)
    
    # 2. Dibuja al jugador
    jugador.dibujar(ventana)
    
    # Actualiza la pantalla completa
    pygame.display.flip()
    
    # Controla la velocidad del juego
    reloj.tick(FPS)

# --- 8. Fin del Juego ---
pygame.quit()