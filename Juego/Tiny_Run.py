# --- Tiny_Run.py ---
import pygame
import os # ¡NUEVO! Necesario para construir rutas de imágenes

# Importamos desde los nombres de archivo PLURALES que tú tienes
try:
    from personajes import Jugador
    from escenarios import Escenario
    from musica import GestorMusica
    print("Archivos importados correctamente.")
except ImportError as e:
    print(f"¡¡ERROR DE IMPORTACIÓN!! Revisa tus nombres de archivo. Error: {e}")
    pygame.quit()
    exit()

# --- 1. Inicialización y Configuración ---
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Constantes
ANCHO_VENTANA = 800
ALTO_VENTANA = 600
FPS = 60

# Ventana
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Tiny Run BTS")
reloj = pygame.time.Clock()

# --- Definición de Estados del Juego ---
ESTADO_MENU = "menu_principal"
ESTADO_SELECCION_PERSONAJE = "seleccion_personaje"
ESTADO_SELECCION_NIVEL = "seleccion_nivel"
ESTADO_JUGANDO = "jugando"
ESTADO_GAME_OVER = "game_over"

estado_actual = ESTADO_MENU

# --- Variables de Juego ---
jugador = None
escenario = None
personaje_elegido = ""
nivel_elegido = ""

# Fuentes
fuente_titulo = pygame.font.SysFont('Arial', 60)
fuente_menu = pygame.font.SysFont('Arial', 40)
fuente_botones = pygame.font.SysFont('Arial', 30)

# Colores
COLOR_TEXTO = (255, 255, 255)
COLOR_FONDO_MENU = (30, 30, 30)
COLOR_BOTON_NORMAL = (0, 100, 0)
COLOR_BOTON_HOVER = (0, 150, 0) # Color cuando el mouse está encima

# --- Botones (Rects para clics) ---
# Menú Principal
boton_jugar_rect = pygame.Rect(300, 250, 200, 50)

# ¡NUEVO! Carga de Imágenes de Personajes
imagenes_personajes = {}
RUTA_PERSONAJES_IMG = 'personajes_img' # ¡Asegúrate que esta carpeta exista!
TAMAÑO_PERSONAJE_MENU = (100, 150) # Tamaño para mostrar en el menú

try:
    # Cargar V
    ruta_v = os.path.join(RUTA_PERSONAJES_IMG, 'V.png')
    img_v_original = pygame.image.load(ruta_v).convert_alpha() # .convert_alpha() para transparencia
    imagenes_personajes['V'] = pygame.transform.scale(img_v_original, TAMAÑO_PERSONAJE_MENU)
    
    # Cargar J-Hope (o cualquier otro)
    ruta_jhope = os.path.join(RUTA_PERSONAJES_IMG, 'J-Hope.png')
    img_jhope_original = pygame.image.load(ruta_jhope).convert_alpha()
    imagenes_personajes['J-Hope'] = pygame.transform.scale(img_jhope_original, TAMAÑO_PERSONAJE_MENU)
    
    print("Imágenes de personajes cargadas correctamente.")
except FileNotFoundError as e:
    print(f"¡ERROR! No se encontró una imagen de personaje. Asegúrate que estén en '{RUTA_PERSONAJES_IMG}/' y los nombres coincidan (V.png, J-Hope.png, etc.). Error: {e}")
    # Si las imágenes no cargan, usaremos un rectángulo simple como fallback
    imagenes_personajes['V'] = pygame.Surface(TAMAÑO_PERSONAJE_MENU)
    imagenes_personajes['V'].fill((128, 0, 128))
    imagenes_personajes['J-Hope'] = pygame.Surface(TAMAÑO_PERSONAJE_MENU)
    imagenes_personajes['J-Hope'].fill((0, 150, 0))
except Exception as e:
    print(f"Error al cargar imágenes de personajes: {e}")


# Posiciones para las imágenes de personajes en el menú de selección
pos_img_v = (ANCHO_VENTANA / 2 - TAMAÑO_PERSONAJE_MENU[0] - 50, 250)
pos_img_jhope = (ANCHO_VENTANA / 2 + 50, 250)

# Rects de los botones (ahora envuelven las imágenes + texto opcional)
# Usamos el tamaño de la imagen para los rectángulos
boton_v_rect = pygame.Rect(pos_img_v[0], pos_img_v[1], TAMAÑO_PERSONAJE_MENU[0], TAMAÑO_PERSONAJE_MENU[1] + 30) # +30 para el texto
boton_jhope_rect = pygame.Rect(pos_img_jhope[0], pos_img_jhope[1], TAMAÑO_PERSONAJE_MENU[0], TAMAÑO_PERSONAJE_MENU[1] + 30)


# ¡NUEVO! Selección Nivel (igual que antes)
boton_idol_rect = pygame.Rect(300, 200, 200, 50)
boton_dna_rect = pygame.Rect(300, 300, 200, 50)
boton_nomore_rect = pygame.Rect(300, 400, 200, 50)


# --- 2. Eventos Personalizados ---
EVENTO_GENERAR_OBSTACULO = pygame.USEREVENT + 1
EVENTO_FIN_MUSICA = pygame.USEREVENT + 2

# --- 3. Objetos ---
gestor_musica = GestorMusica(music_end_event=EVENTO_FIN_MUSICA)
gestor_musica.cargar_y_reproducir()


# --- Función para iniciar el juego ---
def iniciar_juego():
    """Crea los objetos del juego y cambia el estado a "JUGANDO"."""
    global jugador, escenario, estado_actual, personaje_elegido, nivel_elegido
    
    # 1. Crea al jugador basado en la selección
    jugador = Jugador(100, ALTO_VENTANA - 50 - 60, personaje_elegido)
    
    # 2. Crea el escenario basado en la selección de nivel
    escenario = Escenario(ANCHO_VENTANA, ALTO_VENTANA, nivel_elegido)
    
    # 3. Re-asignamos y activamos el timer de obstáculos
    escenario.GENERAR_OBSTACULO = EVENTO_GENERAR_OBSTACULO
    pygame.time.set_timer(escenario.GENERAR_OBSTACULO, 1500)
    
    estado_actual = ESTADO_JUGANDO


# --- 4. Bucle Principal ---
en_ejecucion = True
while en_ejecucion:
    
    # --- 5. Manejo de Eventos ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            en_ejecucion = False
            
        if evento.type == gestor_musica.MUSIC_END_EVENT:
            gestor_musica.reproducir_siguiente_cancion()

        # --- A. Eventos Menú Principal ---
        if estado_actual == ESTADO_MENU:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar_rect.collidepoint(evento.pos):
                    estado_actual = ESTADO_SELECCION_PERSONAJE 

        # --- B. Eventos Selección Personaje ---
        elif estado_actual == ESTADO_SELECCION_PERSONAJE:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_v_rect.collidepoint(evento.pos):
                    personaje_elegido = "V"
                    print("Personaje elegido: V")
                    estado_actual = ESTADO_SELECCION_NIVEL
                
                if boton_jhope_rect.collidepoint(evento.pos):
                    personaje_elegido = "J-Hope"
                    print("Personaje elegido: J-Hope")
                    estado_actual = ESTADO_SELECCION_NIVEL

        # --- C. Eventos Selección Nivel ---
        elif estado_actual == ESTADO_SELECCION_NIVEL:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_idol_rect.collidepoint(evento.pos):
                    nivel_elegido = "IDOL.jpg"
                    print("Nivel elegido: IDOL")
                    iniciar_juego()
                
                if boton_dna_rect.collidepoint(evento.pos):
                    nivel_elegido = "DNA.jpg"
                    print("Nivel elegido: DNA")
                    iniciar_juego()

                if boton_nomore_rect.collidepoint(evento.pos):
                    nivel_elegido = "No more dream.jpg"
                    print("Nivel elegido: No more dream")
                    iniciar_juego()

        # --- D. Eventos Jugando ---
        elif estado_actual == ESTADO_JUGANDO:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_w or evento.key == pygame.K_SPACE:
                    jugador.saltar()
            
            if evento.type == escenario.GENERAR_OBSTACULO:
                escenario.generar_obstaculo()

    
    # --- 6. Actualización de Lógica ---
    if estado_actual == ESTADO_JUGANDO:
        jugador.update(escenario.suelo_rect)
        escenario.update()
        
        if escenario.check_colision(jugador.rect):
            print("¡Juego terminado!")
            estado_actual = ESTADO_MENU # Vuelve al menú principal

    
    # --- 7. Dibujar en Pantalla ---
    
    if estado_actual == ESTADO_MENU:
        ventana.fill(COLOR_FONDO_MENU)
        texto_titulo = fuente_titulo.render("Tiny Run BTS", True, COLOR_TEXTO)
        ventana.blit(texto_titulo, (ANCHO_VENTANA/2 - texto_titulo.get_width()/2, 100))
        
        pygame.draw.rect(ventana, COLOR_BOTON_NORMAL, boton_jugar_rect)
        texto_jugar = fuente_menu.render("Jugar", True, COLOR_TEXTO)
        ventana.blit(texto_jugar, (boton_jugar_rect.x + 50, boton_jugar_rect.y + 5))

    elif estado_actual == ESTADO_SELECCION_PERSONAJE:
        ventana.fill(COLOR_FONDO_MENU)
        
        texto_sel = fuente_menu.render("Elige tu Personaje", True, COLOR_TEXTO)
        ventana.blit(texto_sel, (ANCHO_VENTANA/2 - texto_sel.get_width()/2, 100))

        # --- ¡MODIFICADO! Dibujar las IMÁGENES de los personajes ---
        # Dibuja la imagen de V
        ventana.blit(imagenes_personajes['V'], pos_img_v)
        # Dibuja el nombre de V debajo
        texto_v_nombre = fuente_botones.render("V", True, COLOR_TEXTO)
        ventana.blit(texto_v_nombre, (pos_img_v[0] + TAMAÑO_PERSONAJE_MENU[0]/2 - texto_v_nombre.get_width()/2, pos_img_v[1] + TAMAÑO_PERSONAJE_MENU[1] + 5))

        # Dibuja la imagen de J-Hope
        ventana.blit(imagenes_personajes['J-Hope'], pos_img_jhope)
        # Dibuja el nombre de J-Hope debajo
        texto_jh_nombre = fuente_botones.render("J-Hope", True, COLOR_TEXTO)
        ventana.blit(texto_jh_nombre, (pos_img_jhope[0] + TAMAÑO_PERSONAJE_MENU[0]/2 - texto_jh_nombre.get_width()/2, pos_img_jhope[1] + TAMAÑO_PERSONAJE_MENU[1] + 5))

        # Opcional: para visualización, puedes dibujar el rect del botón (como un marco)
        pygame.draw.rect(ventana, (200, 200, 0), boton_v_rect, 2) # Dibuja un borde de 2px
        pygame.draw.rect(ventana, (200, 200, 0), boton_jhope_rect, 2)


    elif estado_actual == ESTADO_SELECCION_NIVEL:
        ventana.fill(COLOR_FONDO_MENU)

        texto_sel = fuente_menu.render("Elige el Nivel (MV)", True, COLOR_TEXTO)
        ventana.blit(texto_sel, (ANCHO_VENTANA/2 - texto_sel.get_width()/2, 100))

        # Botón IDOL
        pygame.draw.rect(ventana, (255, 180, 0), boton_idol_rect)
        texto_idol = fuente_botones.render("IDOL", True, (0,0,0))
        ventana.blit(texto_idol, (boton_idol_rect.x + 70, boton_idol_rect.y + 10))

        # Botón DNA
        pygame.draw.rect(ventana, (50, 200, 255), boton_dna_rect)
        texto_dna = fuente_botones.render("DNA", True, (0,0,0))
        ventana.blit(texto_dna, (boton_dna_rect.x + 75, boton_dna_rect.y + 10))
        
        # Botón No More Dream
        pygame.draw.rect(ventana, (200, 200, 200), boton_nomore_rect)
        texto_nomore = fuente_botones.render("No More Dream", True, (0,0,0))
        ventana.blit(texto_nomore, (boton_nomore_rect.x + 20, boton_nomore_rect.y + 10))


    elif estado_actual == ESTADO_JUGANDO:
        escenario.dibujar(ventana)
        jugador.dibujar(ventana)
    
    
    pygame.display.flip()
    reloj.tick(FPS)

# --- 8. Fin ---
pygame.quit()