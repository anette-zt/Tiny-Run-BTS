import pygame
import sys
# --- NUEVO ---
# No lo usaremos por ahora, pero si quieres aleatoriedad real,
# lo necesitaremos. Por ahora, una lista fija es mejor.
# import random 

# Inicialización
pygame.init()
pygame.mixer.init()

ANCHO, ALTO = 1200, 700 
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Neon Platformer")

# Colores
NEON_RED = (255, 50, 50)
NEON_BLUE = (50, 200, 255)
NEON_GREEN = (0, 255, 128)
NEON_PURPLE = (200, 0, 255)
FONDO = (0, 0, 0)

clock = pygame.time.Clock()
fuente = pygame.font.SysFont("consolas", 22)
fuente_titulo = pygame.font.SysFont("consolas", 40)

# --- CARGA DE ASSETS ---
try:
    # Cargar personajes
    img_v_original = pygame.image.load("V.png").convert_alpha()
    img_p_original = pygame.image.load("V.png").convert_alpha() # Asume V.png si falta la otra

    # Escalar personajes
    NUEVO_ANCHO_PJ, NUEVO_ALTO_PJ = 60, 90
    personaje_verde_img = pygame.transform.scale(img_v_original, (NUEVO_ANCHO_PJ, NUEVO_ALTO_PJ))
    personaje_purpura_img = pygame.transform.scale(img_p_original, (NUEVO_ANCHO_PJ, NUEVO_ALTO_PJ))
    
    # --- NUEVO: Cargar imagen del lightstick ---
    # Asumo que el archivo se llama 'lightstick.png' y lo escalo a 30x30
    img_lightstick_original = pygame.image.load("LightStick BTS.png").convert_alpha()
    lightstick_img = pygame.transform.scale(img_lightstick_original, (30, 30))

    # Cargar fondo y música
    fondo_juego_img = pygame.image.load("Black Swan.jpg").convert()
    fondo_juego_img = pygame.transform.scale(fondo_juego_img, (ANCHO, ALTO))

    pygame.mixer.music.load("Black Swan.ogg")
    pygame.mixer.music.play(-1)

except FileNotFoundError as e:
    print(f"Error al cargar archivo: {e}")
    pygame.time.wait(3000)
    sys.exit()

# Plataformas
plataformas = [
    pygame.Rect(0, ALTO - 40, ANCHO, 40),
    pygame.Rect(200, ALTO - 120, 120, 10),
    pygame.Rect(400, ALTO - 200, 120, 10),
    pygame.Rect(650, ALTO - 160, 150, 10),
    pygame.Rect(900, ALTO - 250, 150, 10),
    pygame.Rect(-3, 10, 3, ALTO),
    pygame.Rect(ANCHO, 10, 3, ALTO),
]

def dibujar_neon(rect, color, ancho=2):
    for i in range(5, 0, -1):
        pygame.draw.rect(pantalla, color, rect.inflate(i, i), ancho)

# --- MENÚ ---
def mostrar_menu():
    opcion_verde_rect = personaje_verde_img.get_rect(center=(ANCHO // 2 - 100, ALTO // 2))
    opcion_purpura_rect = personaje_purpura_img.get_rect(center=(ANCHO // 2 + 100, ALTO // 2))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if opcion_verde_rect.collidepoint(event.pos):
                    return 'verde'
                if opcion_purpura_rect.collidepoint(event.pos):
                    return 'purpura'

        pantalla.fill(FONDO)
        texto_titulo = fuente_titulo.render("Elige tu Personaje (Clic para jugar)", True, NEON_BLUE)
        pantalla.blit(texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, 150))

        pantalla.blit(personaje_verde_img, opcion_verde_rect)
        pantalla.blit(personaje_purpura_img, opcion_purpura_rect)
        
        dibujar_neon(opcion_verde_rect, NEON_GREEN)
        dibujar_neon(opcion_purpura_rect, NEON_PURPLE)

        pygame.display.flip()
        clock.tick(30)

# --- JUEGO ---
def juego_principal(personaje_elegido_id):
    if personaje_elegido_id == 'verde':
        imagen_actual = personaje_verde_img
    else:
        imagen_actual = personaje_purpura_img

    jugador_rect = imagen_actual.get_rect(topleft=(100, ALTO - 150))
    vel_y = 0
    en_suelo = False
    vel_x = 0

    enemigos = [
        pygame.Rect(500, ALTO - 70, 30, 30),
        pygame.Rect(700, ALTO - 190, 30, 30)
    ]
    dir_enemigo = [1, -1]
    puntos = 0

    # --- NUEVO: Lista de lightsticks ---
    # Cada lightstick es un Rect. Modifica estas coordenadas como quieras.
    # Las defino aquí para que se reinicien cada vez que mueres.
    lightsticks = [
        pygame.Rect(250, ALTO - 150, 30, 30), # Sobre la plataforma 1
        pygame.Rect(450, ALTO - 230, 30, 30), # Sobre la plataforma 2
        pygame.Rect(700, ALTO - 190, 30, 30), # Sobre la plataforma 3
        pygame.Rect(950, ALTO - 280, 30, 30), # Sobre la plataforma 4
        pygame.Rect(100, ALTO - 70, 30, 30),  # En el suelo
        pygame.Rect(1200, ALTO - 70, 30, 30)  # En el suelo
    ]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        teclas = pygame.key.get_pressed()
        vel_x = 0
        if teclas[pygame.K_LEFT]: vel_x = -5
        if teclas[pygame.K_RIGHT]: vel_x = 5
        if teclas[pygame.K_SPACE] and en_suelo:
            vel_y = -15
            en_suelo = False

        vel_y += 1
        if vel_y > 10: vel_y = 10

        # Lógica de movimiento y colisión
        jugador_rect.x += vel_x
        for p in plataformas:
            if jugador_rect.colliderect(p):
                if vel_x > 0: jugador_rect.right = p.left
                if vel_x < 0: jugador_rect.left = p.right

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
        
        # Colisión con enemigos
        for i, e in enumerate(enemigos):
            e.x += dir_enemigo[i] * 3
            if e.left < 0 or e.right > ANCHO: dir_enemigo[i] *= -1
            if jugador_rect.colliderect(e):
                print(f"Game Over! Puntos: {puntos // 10}")
                return

        # --- NUEVO: Colisión con lightsticks ---
        # Creamos una lista temporal para guardar los que se recolectan
        recolectados = []
        for ls_rect in lightsticks:
            if jugador_rect.colliderect(ls_rect):
                # Vale 10 puntos de display (100 puntos internos)
                puntos += 100 
                recolectados.append(ls_rect)

        # Eliminamos los recolectados de la lista principal
        # (Esta es la forma segura de eliminar de una lista mientras se itera)
        lightsticks = [ls for ls in lightsticks if ls not in recolectados]


        # --- Dibujado ---
        pantalla.blit(fondo_juego_img, (0, 0))
        for p in plataformas: dibujar_neon(p, NEON_BLUE)

        # --- NUEVO: Dibujar los lightsticks ---
        for ls_rect in lightsticks:
            pantalla.blit(lightstick_img, ls_rect)

        # Dibujar jugador
        pantalla.blit(imagen_actual, jugador_rect) 
        
        # Dibujar enemigos
        for e in enemigos: dibujar_neon(e, NEON_RED)

        # Puntos (--- MODIFICADO ---)
        puntos += 1 # Puntos por tiempo
        texto = fuente.render(f"Puntos: {puntos // 10}", True, NEON_PURPLE)
        pantalla.blit(texto, (10, 10))

        pygame.display.flip()
        clock.tick(60)

# --- BUCLE PRINCIPAL ---
while True:
    personaje = mostrar_menu()
    juego_principal(personaje)