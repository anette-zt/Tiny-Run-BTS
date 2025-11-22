import pygame
import sys
import sqlite3 # Importamos la libreria de base de datos  

# Inicializacion
pygame.init()
pygame.mixer.init()

ANCHO, ALTO = 1200, 700 
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Tiny Run BTS ")

# Colores
FONDO = (0, 0, 0)
VERDE_NORMAL = (0, 200, 0)
ROJO_NORMAL = (255, 0, 0)
BLANCO = (255, 255, 255)
AMARILLO = (255, 255, 0) # color para el record

clock = pygame.time.Clock()
fuente = pygame.font.SysFont("consolas", 22)
fuente_titulo = pygame.font.SysFont("consolas", 40)

# Base de datos 
def inicializar_db():
    try:
        conexion = sqlite3.connect("tiny_run.db")
        cursor = conexion.cursor()
        # Crea la tabla si no existe
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
        # Selecciona el puntaje más alto
        cursor.execute("SELECT MAX(puntos) FROM puntuaciones")
        record = cursor.fetchone()[0]
        conexion.close()
        # Si no hay record (es la primera vez), devuelve 0
        return record if record is not None else 0
    except Exception as e:
        return 0

# Inicializamos la DB al arrancar el juego
inicializar_db()

# Cargar recursos 
try:
    # Cargar personaje
    img_v_original = pygame.image.load("V.png").convert_alpha()

    # Escalar personaje
    NUEVO_ANCHO_PJ, NUEVO_ALTO_PJ = 60, 90
    personaje_verde_img = pygame.transform.scale(img_v_original, (NUEVO_ANCHO_PJ, NUEVO_ALTO_PJ))
    
    # Cargar imagen del lightstick
    img_lightstick_original = pygame.image.load("LightStick BTS.png").convert_alpha()
    lightstick_img = pygame.transform.scale(img_lightstick_original, (30, 30))

    # Cargar fondo y música
    fondo_juego_img = pygame.image.load(" DNA.png").convert()
    fondo_juego_img = pygame.transform.scale(fondo_juego_img, (ANCHO, ALTO))

    pygame.mixer.music.load(" DNA.ogg")
    pygame.mixer.music.play(-1)

except FileNotFoundError as e:
    print(f"Error al cargar archivo: {e}")
    pygame.time.wait(3000)
    sys.exit()

# Plataformas
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

#   JUEGO  
def juego_principal():
    
    imagen_actual = personaje_verde_img
    jugador_rect = imagen_actual.get_rect(topleft=(100, ALTO - 150))
    vel_y = 0
    en_suelo = False
    vel_x = 0

    enemigos = [
        pygame.Rect(500, ALTO - 70, 30, 30),
        pygame.Rect(700, ALTO - 190, 30, 30),
        pygame.Rect(420, ALTO - 230, 30, 30),
        pygame.Rect(320, ALTO - 430, 30, 30)
    ]
    
    dir_enemigo = [1, -1, 1, -1] 
    
    puntos = 0 
    
    # Obtener el record actual de la base de datos  
    record_actual = obtener_record()

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

        # Logica de movimiento y colision X
        jugador_rect.x += vel_x
        for p in plataformas:
            if jugador_rect.colliderect(p):
                if vel_x > 0: jugador_rect.right = p.left
                if vel_x < 0: jugador_rect.left = p.right

        # Logica de movimiento y colision Y
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
        
        # Colision con enemigos
        for i, e in enumerate(enemigos):
            e.x += dir_enemigo[i] * 3
            if e.left < 0 or e.right > ANCHO: dir_enemigo[i] *= -1
            if jugador_rect.colliderect(e):
                print(f"Game Over! Puntos: {puntos}")
                
                # Guardarpuntaje al morir  
                guardar_puntaje(puntos)
                
                # Pequeña pausa antes de reiniciar
                texto_go = fuente_titulo.render("GAME OVER", True, ROJO_NORMAL)
                pantalla.blit(texto_go, (ANCHO//2 - 100, ALTO//2))
                pygame.display.flip()
                pygame.time.wait(2000)
                return 

        # Colision con lightsticks
        recolectados = []
        for ls_rect in lightsticks:
            if jugador_rect.colliderect(ls_rect):
                puntos += 10 
                recolectados.append(ls_rect)

        lightsticks = [ls for ls in lightsticks if ls not in recolectados]

        #   Dibujado 
        pantalla.blit(fondo_juego_img, (0, 0))
        
        for p in plataformas:
            pygame.draw.rect(pantalla, VERDE_NORMAL, p)

        for ls_rect in lightsticks:
            pantalla.blit(lightstick_img, ls_rect)

        pantalla.blit(imagen_actual, jugador_rect) 
        
        for e in enemigos:
            pygame.draw.rect(pantalla, ROJO_NORMAL, e)

        #   Puntos y record pasados  
        texto_puntos = fuente.render(f"Puntos: {puntos}", True, BLANCO)
        pantalla.blit(texto_puntos, (10, 10))
        
        # Si superamos el record en tiempo real, mostramos el puntaje actual como record
        display_record = max(puntos, record_actual)
        texto_record = fuente.render(f"Récord: {display_record}", True, AMARILLO)
        pantalla.blit(texto_record, (10, 40)) 

        pygame.display.flip()
        clock.tick(60)

# bucle principal 
while True:
    juego_principal()