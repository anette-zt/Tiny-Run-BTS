# Nombre del Proyecto: Tiny Run BTS 
# Asignatura: Graficacion
# Estudiante: Ariam Anette Zurita Torres
# Fecha: Noviembre - Diciembre 2025
# Descripcion: Juego completo con Menú, Game Over y Pantalla de Victoria.

import pygame
import sys
import sqlite3

# --- 1. INICIALIZACIÓN ---
pygame.init()
pygame.mixer.init()

ANCHO, ALTO = 1200, 700
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Tiny Run BTS - Ariam Anette Zurita Torres")

# Colores
FONDO = (0, 0, 0)
VERDE_PLATAFORMA = (0, 200, 0)
ROJO_ENEMIGO = (255, 0, 0)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
MORADO_BTS = (150, 50, 200) # Color especial para la victoria

clock = pygame.time.Clock()
# Fuentes
fuente_peque = pygame.font.SysFont("consolas", 22)
fuente_titulo = pygame.font.SysFont("consolas", 40)
fuente_gigante = pygame.font.SysFont("consolas", 60)

# --- 2. BASE DE DATOS ---
def inicializar_db():
    try:
        conexion = sqlite3.connect("tiny_run.db")
        cursor = conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS puntuaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                puntos INTEGER
            )
        ''')
        conexion.commit()
        conexion.close()
        print("Base de datos cargada correctamente.")
    except Exception as e:
        print(f"Error en base de datos: {e}")

def guardar_puntaje(puntos):
    try:
        conexion = sqlite3.connect("tiny_run.db")
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO puntuaciones (puntos) VALUES (?)", (puntos,))
        conexion.commit()
        conexion.close()
        print(f"Puntaje guardado: {puntos}")
    except Exception as e:
        print(f"Error al guardar puntaje: {e}")

def obtener_record():
    try:
        conexion = sqlite3.connect("tiny_run.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT MAX(puntos) FROM puntuaciones")
        record = cursor.fetchone()[0]
        conexion.close()
        return record if record is not None else 0
    except Exception as e:
        return 0

# Iniciamos la BD al arrancar
inicializar_db()

# --- 3. CARGA DE IMÁGENES Y SONIDO ---
# Variables globales para los assets
img_v_original = None
personaje_verde_img = None
fondo_juego_img = None
lightstick_img = None

try:
    # Intenta cargar las imágenes reales
    img_v_original = pygame.image.load("V.png").convert_alpha()
    NUEVO_ANCHO_PJ, NUEVO_ALTO_PJ = 60, 90
    personaje_verde_img = pygame.transform.scale(img_v_original, (NUEVO_ANCHO_PJ, NUEVO_ALTO_PJ))
    
    img_lightstick_original = pygame.image.load("LightStick BTS.png").convert_alpha()
    lightstick_img = pygame.transform.scale(img_lightstick_original, (30, 30))

    fondo_juego_img = pygame.image.load("Black Swan.jpg").convert()
    fondo_juego_img = pygame.transform.scale(fondo_juego_img, (ANCHO, ALTO))

    # Música
    pygame.mixer.music.load("Black Swan.ogg")
    pygame.mixer.music.play(-1) # Play infinito

except Exception as e:
    print(f"AVISO: No se encontraron algunas imágenes o música ({e}).")
    print("Usando modo de respaldo con cuadrados de colores.")
    
    # Si fallan las imágenes, creamos cuadrados de colores para que el juego no falle
    personaje_verde_img = pygame.Surface((60, 90))
    personaje_verde_img.fill((0, 255, 0)) # Verde brillante
    
    fondo_juego_img = pygame.Surface((ANCHO, ALTO))
    fondo_juego_img.fill((30, 30, 50)) # Azul oscuro
    
    lightstick_img = pygame.Surface((30, 30))
    lightstick_img.fill((255, 255, 0)) # Amarillo

# --- 4. FUNCIÓN DEL MENÚ ---
def mostrar_menu():
    """Muestra la pantalla de bienvenida"""
    ejecutando_menu = True
    
    # Botón JUGAR
    boton_rect = pygame.Rect(ANCHO//2 - 100, ALTO - 150, 200, 60)
    
    while ejecutando_menu:
        # Dibujar fondo (usamos el del juego pero un poco oscurecido)
        pantalla.blit(fondo_juego_img, (0,0))
        overlay = pygame.Surface((ANCHO, ALTO))
        overlay.set_alpha(150) # Transparencia
        overlay.fill(NEGRO)
        pantalla.blit(overlay, (0,0))

        # Eventos del menú
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_rect.collidepoint(event.pos):
                    ejecutando_menu = False # Salir del menú -> Ir al juego

        # Textos del menú
        titulo = fuente_gigante.render("Tiny Run BTS", True, MORADO_BTS)
        autora = fuente_peque.render("Desarrollado por: Ariam Anette Zurita Torres", True, BLANCO)
        
        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 100))
        pantalla.blit(autora, (ANCHO//2 - autora.get_width()//2, 170))

        # Lista de instrucciones
        instrucciones = [
            "--- CÓMO JUGAR ---",
            "flecha IZQ / DER : Moverse",
            "ESPACIO : Saltar",
            "Recoge todos los Lightsticks para GANAR",
            "¡Evita a los enemigos rojos!"
        ]
        
        y_pos = 250
        for linea in instrucciones:
            txt = fuente_peque.render(linea, True, BLANCO)
            pantalla.blit(txt, (ANCHO//2 - txt.get_width()//2, y_pos))
            y_pos += 40

        # Dibujar el botón
        mouse_pos = pygame.mouse.get_pos()
        color_btn = VERDE_PLATAFORMA if boton_rect.collidepoint(mouse_pos) else (0, 100, 0)
        
        pygame.draw.rect(pantalla, color_btn, boton_rect, border_radius=15)
        pygame.draw.rect(pantalla, BLANCO, boton_rect, 2, border_radius=15) # Borde blanco
        
        txt_btn = fuente_titulo.render("JUGAR", True, BLANCO)
        pantalla.blit(txt_btn, (boton_rect.centerx - txt_btn.get_width()//2, boton_rect.centery - txt_btn.get_height()//2))

        pygame.display.flip()
        clock.tick(60)

# --- 5. FUNCIÓN DEL JUEGO PRINCIPAL ---
def juego_principal():
    
    # Reiniciar variables del jugador
    jugador_rect = personaje_verde_img.get_rect(topleft=(100, ALTO - 150))
    vel_y = 0
    en_suelo = False
    puntos = 0
    record_actual = obtener_record()

    # Definir Plataformas
    plataformas = [
        pygame.Rect(0, ALTO - 40, ANCHO, 40),
        pygame.Rect(-3, 10, 3, ALTO),
        pygame.Rect(ANCHO, 10, 3, ALTO),
        pygame.Rect(200, ALTO - 120, 120, 10),
        pygame.Rect(400, ALTO - 200, 120, 10),
        pygame.Rect(650, ALTO - 160, 150, 10),
        pygame.Rect(900, ALTO - 250, 150, 10),
        pygame.Rect(100, ALTO - 320, 100, 10),
        pygame.Rect(300, ALTO - 400, 150, 10),
        pygame.Rect(550, ALTO - 300, 120, 10),
        pygame.Rect(600, ALTO - 450, 100, 10),
    ]

    # Definir Enemigos
    enemigos = [
        pygame.Rect(500, ALTO - 70, 30, 30),
        pygame.Rect(700, ALTO - 190, 30, 30),
        pygame.Rect(420, ALTO - 230, 30, 30),
        pygame.Rect(320, ALTO - 430, 30, 30),
        pygame.Rect(850, ALTO - 280, 30, 30),
        pygame.Rect(1100, ALTO - 70, 30, 30),
    ]
    dir_enemigo = [1, -1, 1, -1] # Dirección de cada enemigo

    # Definir Objetos (Lightstick s)
    lightsticks = [
        pygame.Rect(250, ALTO - 150, 30, 30),
        pygame.Rect(450, ALTO - 230, 30, 30),
        pygame.Rect(700, ALTO - 190, 30, 30),
        pygame.Rect(950, ALTO - 280, 30, 30),
        pygame.Rect(100, ALTO - 70, 30, 30),
        pygame.Rect(1100, ALTO - 70, 30, 30),
        pygame.Rect(130, ALTO - 350, 30, 30),
        pygame.Rect(350, ALTO - 430, 30, 30),
        pygame.Rect(580, ALTO - 330, 30, 30),
        pygame.Rect(830, ALTO - 480, 30, 30),
        pygame.Rect(600, ALTO - 470, 30, 30),
        pygame.Rect(920, ALTO - 600, 30, 30),
        pygame.Rect(1150, ALTO - 500, 30, 30),
        pygame.Rect(400, ALTO - 600, 30, 30),
        pygame.Rect(750, ALTO - 400, 30, 30),
    ]

    jugando = True
    while jugando:
        # A. EVENTOS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # B. MOVIMIENTO JUGADOR
        teclas = pygame.key.get_pressed()
        vel_x = 0
        if teclas[pygame.K_LEFT]: vel_x = -5
        if teclas[pygame.K_RIGHT]: vel_x = 5
        if teclas[pygame.K_SPACE] and en_suelo:
            vel_y = -15
            en_suelo = False

        # Gravedad
        vel_y += 1
        if vel_y > 10: vel_y = 10

        # Movimiento Horizontal y Colisiones
        jugador_rect.x += vel_x
        for p in plataformas:
            if jugador_rect.colliderect(p):
                if vel_x > 0: jugador_rect.right = p.left 
                if vel_x < 0: jugador_rect.left = p.right 

        # Movimiento Vertical y Colisiones
        jugador_rect.y += vel_y
        en_suelo = False
        for p in plataformas:
            if jugador_rect.colliderect(p):
                if vel_y > 0:
                    jugador_rect.bottom = p.top
                    en_suelo = True
                    vel_y = 0
                elif vel_y < 0:
                    jugador_rect.top = p.bottom 
                    vel_y = 0 
        
        # C. LÓGICA DE ENEMIGOS (GAME OVER)
        for i in range(len(enemigos)):
            if i % 2 == 0:
                dir_enemigo.append(1)  # Los pares van a la derecha
        else:
            dir_enemigo.append(-1)     # Los impares van a la izquierda
            
            # Colision Jugador con Enemigo
            if jugador_rect.colliderect(enemigos[i]):
                print(f"Game Over. Puntos: {puntos}")
                guardar_puntaje(puntos)
                
                # Pantalla Roja de Game Over
                texto_go = fuente_titulo.render("GAME OVER", True, ROJO_ENEMIGO)
                texto_pts = fuente_peque.render(f"Puntos obtenidos: {puntos}", True, BLANCO)
                pantalla.blit(texto_go, (ANCHO//2 - 100, ALTO//2 - 20))
                pantalla.blit(texto_pts, (ANCHO//2 - 120, ALTO//2 + 30))
                
                pygame.display.flip()
                pygame.time.wait(3000) # Esperar 3 seg
                return # Volver al Menú

        # D. RECOLECCIÓN (LIGHTSTICKS)
        recolectados = []
        for ls_rect in lightsticks:
            if jugador_rect.colliderect(ls_rect): 
                puntos += 10
                recolectados.append(ls_rect)

        # Actualizar lista eliminando los recolectados
        lightsticks = [ls for ls in lightsticks if ls not in recolectados]

        # --- E. CONDICIÓN DE VICTORIA ---
        if len(lightsticks) == 0:
            # Si no quedan lightsticks, ¡GANASTE!
            guardar_puntaje(puntos)
            
            pantalla.fill(MORADO_BTS) # Fondo morado
            
            txt_ganaste = fuente_gigante.render("¡FELICIDADES ARMY!", True, BLANCO)
            txt_sub = fuente_titulo.render("Nivel Completado", True, BLANCO)
            txt_puntos = fuente_peque.render(f"Puntaje Final: {puntos}", True, BLANCO)
            
            pantalla.blit(txt_ganaste, (ANCHO//2 - txt_ganaste.get_width()//2, ALTO//2 - 80))
            pantalla.blit(txt_sub, (ANCHO//2 - txt_sub.get_width()//2, ALTO//2))
            pantalla.blit(txt_puntos, (ANCHO//2 - txt_puntos.get_width()//2, ALTO//2 + 50))
            
            pygame.display.flip()
            pygame.time.wait(5000) # Celebrar por 5 segundos
            return # Volver al Menú

        # F. DIBUJAR TODO
        pantalla.blit(fondo_juego_img, (0, 0)) # Fondo
        
        for p in plataformas:
            pygame.draw.rect(pantalla, VERDE_PLATAFORMA, p)

        for ls_rect in lightsticks:
            pantalla.blit(lightstick_img, ls_rect)

        pantalla.blit(personaje_verde_img, jugador_rect) # Personaje
        
        for e in enemigos:
            pygame.draw.rect(pantalla, ROJO_ENEMIGO, e)

        # Interfaz (HUD)
        texto_puntos = fuente_peque.render(f"Puntos: {puntos}", True, NEGRO)
        pantalla.blit(texto_puntos, (10, 10))
        
        # Mostrar solo si hay record
        display_record = max(puntos, record_actual)
        texto_record = fuente_peque.render(f"Récord: {display_record}", True, NEGRO)
        pantalla.blit(texto_record, (10, 40))

        # Cuántos faltan
        texto_restantes = fuente_peque.render(f"Faltan: {len(lightsticks)}", True, NEGRO)
        pantalla.blit(texto_restantes, (ANCHO - 150, 10))

        pygame.display.flip()
        clock.tick(60)

# --- 6. BUCLE PRINCIPAL (EL CEREBRO) ---
# Este bucle controla que primero salga el menú, y luego el juego, infinitamente.
while True:
    mostrar_menu()
    juego_principal()