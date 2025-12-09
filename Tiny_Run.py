# Nombre del Proyecto: Tiny Run BTS 
# Asignatura: Graficacion
# Estudiante: Ariam Anette Zurita Torres
# Fecha: Noviembre de 2025
# Descripcion: Juego de plataformas en Python utilizando Pygame.
# Implementa fisicas basicas, colisiones, recoleccion de objetos y persistencia de datos  mediante SQLite.
 
import pygame # _Importamos la libreria para videojuegos
import sys # Importamos la libreria del sistema
import sqlite3 # Importamos la libreria de base de datos

pygame.init() # Modulos de pygame
pygame.mixer.init() # Modulo de sonido

ANCHO, ALTO = 1200, 700 # Dimensiones de la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO)) # Ventana de visualizacion
pygame.display.set_caption("Tiny Run BTS ") # Titulo de la ventana

# Definimos los colores
FONDO = (0, 0, 0) # Color negro de fondo
VERDE_NORMAL = (0, 200, 0) # Color verde para plataformas
ROJO_NORMAL = (255, 0, 0) # Color rojo para enemigos
NEGRO = (0, 0, 0) # Color negro para textos

clock = pygame.time.Clock() # Configuramos el reloj para controlar los fps
fuente = pygame.font.SysFont("consolas", 22) # Definimos la fuente para texto normal
fuente_titulo = pygame.font.SysFont("consolas", 40) # Definimos la fuente para titulos grandes

def inicializar_db():
    try:
        conexion = sqlite3.connect("tiny_run.db") # Conectamos a la base de datos
        cursor = conexion.cursor() # Creamos el cursor
        # Creamos la tabla 
        cursor.execute('''
            CREATE TABLE puntuaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                puntos INTEGER
            )
        ''')
        conexion.commit() # Guardamos los cambios
        conexion.close() # Cerramos la conexion
        print("Base de datos cargada correctamente.")
    except Exception as e:
        print(f"Error en base de datos: {e}") # Se muestra un error si falla

def guardar_puntaje(puntos):
    try:
        conexion = sqlite3.connect("tiny_run.db") # Conectamos a la base de datos
        cursor = conexion.cursor() # Creamos el cursor
        cursor.execute("INSERT INTO puntuaciones (puntos) VALUES (?)", (puntos,)) # Insertamos el puntaje
        conexion.commit() # Guardamos los cambios
        conexion.close() # Cerramos la conexion
        print(f"Puntaje guardado: {puntos}")
    except Exception as e:
        print(f"Error al guardar puntaje: {e}") # Mostramos error si falla

def obtener_record():
    try:
        conexion = sqlite3.connect("tiny_run.db") # Conectamos a la base de datos
        cursor = conexion.cursor() # Creamos el cursor
        cursor.execute("SELECT MAX(puntos) FROM puntuaciones") # Puntaje maximo
        record = cursor.fetchone()[0] # Obtenemos el resultado
        conexion.close() # Cerramos la conexion
        return record if record is not None else 0 # Devolvemos el record o 0 si no hay
    except Exception as e:
        return 0 # En caso de error devolvemos 0

inicializar_db() # Llamamos a la funcion de inicio de base de datos

# Carga de recursos
try:
    img_v_original = pygame.image.load("V.png").convert_alpha() # Cargamos la imagen de V

    NUEVO_ANCHO_PJ, NUEVO_ALTO_PJ = 60, 90 # Definimos el nuevo tamano del personaje
    personaje_verde_img = pygame.transform.scale(img_v_original, (NUEVO_ANCHO_PJ, NUEVO_ALTO_PJ)) # Escalamos la imagen
    
    img_lightstick_original = pygame.image.load("LightStick BTS.png").convert_alpha() # Cargamos la imagen del objeto
    lightstick_img = pygame.transform.scale(img_lightstick_original, (30, 30)) # Escalamos el objeto

    fondo_juego_img = pygame.image.load("DNA.jpg").convert() # Cargamos la imagen de fondo
    fondo_juego_img = pygame.transform.scale(fondo_juego_img, (ANCHO, ALTO)) # Ajustamos el fondo a la ventana

    pygame.mixer.music.load("DNA.ogg") # Cargamos la musica de fondo
    pygame.mixer.music.play(-1) # Reproducimos la musica en bucle

except FileNotFoundError as e:
    print(f"Error al cargar archivo: {e}") # Mostramos error si falta archivo
    pygame.time.wait(3000) # Esperamos 3 segundos
    sys.exit() # Salimos del programa

plataformas = [
    pygame.Rect(0, ALTO - 40, ANCHO, 40), # Suelo principal
    pygame.Rect(-3, 10, 3, ALTO), # Pared invisible izquierda
    pygame.Rect(ANCHO, 10, 3, ALTO), # Pared invisible derecha
    pygame.Rect(200, ALTO - 120, 120, 10), # Plataforma flotante 1
    pygame.Rect(400, ALTO - 200, 120, 10), # Plataforma flotante 2
    pygame.Rect(650, ALTO - 160, 150, 10), # Plataforma flotante 3
    pygame.Rect(900, ALTO - 250, 150, 10), # Plataforma flotante 4
    pygame.Rect(100, ALTO - 320, 100, 10), # Plataforma flotante 5
    pygame.Rect(300, ALTO - 400, 150, 10), # Plataforma flotante 6
    pygame.Rect(550, ALTO - 300, 120, 10), # Plataforma flotante 7
    pygame.Rect(600, ALTO - 450, 100, 10), # Plataforma flotante 8
]

def juego_principal():
    
    imagen_actual = personaje_verde_img # Asignamos la imagen al jugador
    jugador_rect = imagen_actual.get_rect(topleft=(100, ALTO - 150)) # Obtenemos el rectangulo del jugador
    vel_y = 0 # Inicializamos velocidad vertical
    en_suelo = False # Inicializamos estado de suelo
    vel_x = 0 # Inicializamos velocidad horizontal

    enemigos = [
        pygame.Rect(500, ALTO - 70, 30, 30), # Enemigo 1
        pygame.Rect(700, ALTO - 190, 30, 30), # Enemigo 2
        pygame.Rect(420, ALTO - 230, 30, 30), # Enemigo 3
        pygame.Rect(320, ALTO - 430, 30, 30) # Enemigo 4
    ]
    
    dir_enemigo = [1, -1, 1, -1] # Direccion inicial de enemigos
    
    puntos = 0 # Inicializamos los puntos
    
    record_actual = obtener_record() # Obtenemos el record actual

    lightsticks = [
        pygame.Rect(250, ALTO - 150, 30, 30), # Objeto 1
        pygame.Rect(450, ALTO - 230, 30, 30), # Objeto 2
        pygame.Rect(700, ALTO - 190, 30, 30), # Objeto 3
        pygame.Rect(950, ALTO - 280, 30, 30), # Objeto 4
        pygame.Rect(100, ALTO - 70, 30, 30), # Objeto 5
        pygame.Rect(1100, ALTO - 70, 30, 30), # Objeto 6
        pygame.Rect(130, ALTO - 350, 30, 30), # Objeto 7
        pygame.Rect(350, ALTO - 430, 30, 30), # Objeto 8
        pygame.Rect(580, ALTO - 330, 30, 30), # Objeto 9
        pygame.Rect(830, ALTO - 480, 30, 30), # Objeto 10
    ]

    while True: # Bucle principal del nivel
        for event in pygame.event.get(): # Revisamos eventos
            if event.type == pygame.QUIT: # Si cerramos ventana
                pygame.quit() # Cerramos pygame
                sys.exit() # Salimos del sistema

        teclas = pygame.key.get_pressed() # Obtenemos teclas presionadas
        vel_x = 0 # Reiniciamos velocidad horizontal
        if teclas[pygame.K_LEFT]: vel_x = -5 # Movemos a izquierda
        if teclas[pygame.K_RIGHT]: vel_x = 5 # Movemos a derecha
        if teclas[pygame.K_SPACE] and en_suelo: # Si saltamos y estamos en suelo
            vel_y = -15 # Aplicamos fuerza de salto
            en_suelo = False # Ya no estamos en suelo

        vel_y += 1 # Aplicamos gravedad
        if vel_y > 10: vel_y = 10 # Limitamos velocidad de caida

        jugador_rect.x += vel_x # Actualizamos posicion en x
        for p in plataformas: # Revisamos colision horizontal
            if jugador_rect.colliderect(p): # Si hay colision
                if vel_x > 0: jugador_rect.right = p.left 
                if vel_x < 0: jugador_rect.left = p.right 

        jugador_rect.y += vel_y # Actualizamos posicion y
        en_suelo = False # Asumimos aire por defecto
        for p in plataformas: # Revisamos colision vertical
            if jugador_rect.colliderect(p): # Si hay colision
                if vel_y > 0: # Si caemos
                    jugador_rect.bottom = p.top # Nos paramos encima
                    en_suelo = True # Estamos en suelo
                    vel_y = 0 # Detenemos caida
                elif vel_y < 0: # Si saltamos hacia arriba
                    jugador_rect.top = p.bottom 
                    vel_y = 0 
        
        for i, e in enumerate(enemigos): # Logica de enemigos
            e.x += dir_enemigo[i] * 3 # Movemos enemigo
            if e.left < 0 or e.right > ANCHO: dir_enemigo[i] *= -1 # Rebotamos en bordes
            if jugador_rect.colliderect(e): # Si tocamos enemigo
                print(f"Game Over! Puntos: {puntos}") # Imprimimos puntos
                
                guardar_puntaje(puntos) # Guardamos puntaje
                
                texto_go = fuente_titulo.render("GAME OVER", True, ROJO_NORMAL) # Texto game over
                pantalla.blit(texto_go, (ANCHO//2 - 100, ALTO//2)) # Texto
                pygame.display.flip() 
                pygame.time.wait(2000) 
                return # Reiniciamos juego

        recolectados = [] # 
        for ls_rect in lightsticks:
            if jugador_rect.colliderect(ls_rect): 
                puntos += 10 # Sumamos puntos
                recolectados.append(ls_rect) # Marcamos para borrar

        lightsticks = [ls for ls in lightsticks if ls not in recolectados] # Lista de objetos

        pantalla.blit(fondo_juego_img, (0, 0)) # Fondo
        
        for p in plataformas: # Plataformas
            pygame.draw.rect(pantalla, VERDE_NORMAL, p) # Rectangulo verde

        for ls_rect in lightsticks: # Dibujamos objetos
            pantalla.blit(lightstick_img, ls_rect) # Imagen del objeto

        pantalla.blit(imagen_actual, jugador_rect) # Jugador
        
        for e in enemigos: # Dibujamos enemigos
            pygame.draw.rect(pantalla, ROJO_NORMAL, e) # Rectangulo rojo

        texto_puntos = fuente.render(f"Puntos: {puntos}", True, NEGRO) # Renderizamos puntos
        pantalla.blit(texto_puntos, (10, 10)) # Mostramos puntos
        
        display_record = max(puntos, record_actual) # Calculamos record visible
        texto_record = fuente.render(f"Record: {display_record}", True, NEGRO) # Renderizamos record
        pantalla.blit(texto_record, (10, 40)) # Mostramos record

        pygame.display.flip() # Pantalla completa
        clock.tick(60) # Controlamos fps

while True: # Bucle infinito
    juego_principal() 