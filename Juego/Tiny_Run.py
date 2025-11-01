import pygame
import sys
import random
import os

# Inicializa Pygame
pygame.init()

# Configuración de ventana
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Tiny Run BTS")

# Fuente
fuente = pygame.font.Font(None, 36)

# Colores
AZUL_CIELO = (135, 206, 235)
MARRON_SUELO = (139, 69, 19)
VERDE_PLATAFORMA = (0, 200, 0)

# Rutas base
RUTA_ESCENARIOS = "escenarios"
RUTA_MUSICA = "musica"
RUTA_PERSONAJES = "Personajes_img"

# Configuración de niveles (ordenados)
niveles = [
    {"nombre": "No more dream", "fondo": "No more dream.jpg", "musica": "No more dream.mp3", "personaje": "Jin.png"},
    {"nombre": "Mic Drop", "fondo": "Mic Drop.jpg", "musica": "Mic Drop.mp3", "personaje": "Suga.png"},
    {"nombre": "Fake Love", "fondo": "Fake Love.jpg", "musica": "Fake Love.mp3", "personaje": "J-hope.png"},
    {"nombre": "IDOL", "fondo": "IDOL.jpg", "musica": "IDOL.mp3", "personaje": "RM.png"},
    {"nombre": "Blood Sweet and Tears", "fondo": "Blood Sweet and Tears.jpg", "musica": "Blood Sweet and Tears.mp3", "personaje": "Jimin.png"},
    {"nombre": "DNA", "fondo": "DNA.jpg", "musica": "DNA.mp3", "personaje": "V.png"},
    {"nombre": "ON", "fondo": "ON.jpg", "musica": "ON.mp3", "personaje": "Jungkook.png"},
    {"nombre": "Black Swan", "fondo": "Black Swan.jpg", "musica": "Black Swan.mp3", "personaje": "V.png"},


]

# Variables globales
puntos = 0
nivel_actual = 0
gravedad = 0.5

# _____________________________
# CLASES
# _____________________________

class Jugador(pygame.sprite.Sprite):
    def __init__(self, personaje_img, x, y):
        super().__init__()
        self.image_derecha = pygame.image.load(os.path.join(RUTA_PERSONAJES, personaje_img)).convert_alpha()
        self.image_izquierda = pygame.transform.flip(self.image_derecha, True, False)
        self.image = self.image_derecha
        self.rect = self.image.get_rect(center=(x, y))
        self.vel_x = 0
        self.vel_y = 0
        self.en_suelo = False

    def mover(self, teclas):
        self.vel_x = 0
        if teclas[pygame.K_LEFT]:
            self.vel_x = -5
            self.image = self.image_izquierda
        if teclas[pygame.K_RIGHT]:
            self.vel_x = 5
            self.image = self.image_derecha
        if teclas[pygame.K_SPACE] and self.en_suelo:
            self.vel_y = -10
            self.en_suelo = False

    def aplicar_gravedad(self):
        self.vel_y += gravedad
        if self.vel_y > 10:
            self.vel_y = 10

    def update(self, plataformas):
        self.rect.x += self.vel_x
        self.aplicar_gravedad()
        self.rect.y += self.vel_y

        # Colisiones con plataformas
        self.en_suelo = False
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma.rect):
                if self.vel_y > 0 and self.rect.bottom > plataforma.rect.top:
                    self.rect.bottom = plataforma.rect.top
                    self.vel_y = 0
                    self.en_suelo = True

        # Limites pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, ancho, alto):
        super().__init__()
        self.image = pygame.Surface((ancho, alto))
        self.image.fill(VERDE_PLATAFORMA)
        self.rect = self.image.get_rect(topleft=(x, y))

class Moneda(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("LightStick BTS.png").convert()
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(center=(x, y))

# _____________________________
# FUNCIONES
# _____________________________

def cargar_fondo(nombre_archivo):
    ruta = os.path.join(RUTA_ESCENARIOS, nombre_archivo)
    fondo = pygame.image.load(ruta).convert()
    return pygame.transform.scale(fondo, (ANCHO, ALTO))

def reproducir_musica(nombre_archivo):
    ruta = os.path.join(RUTA_MUSICA, nombre_archivo)
    pygame.mixer.music.load(ruta)
    pygame.mixer.music.play(-1)  # bucle infinito
    pygame.mixer.music.set_volume(0.3)

def crear_nivel(nivel_info):
    global jugador, grupo_jugador, grupo_plataformas, grupo_monedas, fondo

    # Fondo
    fondo = cargar_fondo(nivel_info["fondo"])
    reproducir_musica(nivel_info["musica"])

    # Jugador
    jugador = Jugador(nivel_info["personaje"], 100, 450)
    grupo_jugador = pygame.sprite.GroupSingle(jugador)

    # Plataformas
    grupo_plataformas = pygame.sprite.Group()
    grupo_plataformas.add(Plataforma(0, 550, ANCHO, 50))
    grupo_plataformas.add(Plataforma(200, 450, 150, 20))
    grupo_plataformas.add(Plataforma(450, 350, 150, 20))
    grupo_plataformas.add(Plataforma(650, 250, 100, 20))

    # Monedas
    grupo_monedas = pygame.sprite.Group()
    for _ in range(5):
        x = random.randint(100, 700)
        y = random.choice([200, 300, 400])
        grupo_monedas.add(Moneda(x, y))

    return grupo_jugador, grupo_plataformas, grupo_monedas, fondo

# _____________________________
# INICIO DEL JUEGO
# _____________________________

grupo_jugador, grupo_plataformas, grupo_monedas, fondo = crear_nivel(niveles[nivel_actual])
clock = pygame.time.Clock()
corriendo = True
puntos = 0

# _____________________________
# BUCLE PRINCIPAL
# _____________________________

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    teclas = pygame.key.get_pressed()
    jugador.mover(teclas)
    jugador.update(grupo_plataformas)

    # Colisiones con monedas
    colisiones = pygame.sprite.spritecollide(jugador, grupo_monedas, dokill=True)
    if colisiones:
        puntos += 10

    # Cambiar de nivel cada 50 puntos
    if puntos >= 50 * (nivel_actual + 1) and nivel_actual < len(niveles) - 1:
        nivel_actual += 1
        grupo_jugador, grupo_plataformas, grupo_monedas, fondo = crear_nivel(niveles[nivel_actual])

    # _____________________________
    # DIBUJAR
    # _____________________________
    pantalla.blit(fondo, (0, 0))
    grupo_plataformas.draw(pantalla)
    grupo_monedas.draw(pantalla)
    grupo_jugador.draw(pantalla)

    # Texto
    texto_puntos = fuente.render(f"Puntos: {puntos}", True, (255, 255, 255))
    texto_nivel = fuente.render(f"Nivel: {niveles[nivel_actual]['nombre']}", True, (255, 255, 255))
    pantalla.blit(texto_puntos, (20, 20))
    pantalla.blit(texto_nivel, (20, 60))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
